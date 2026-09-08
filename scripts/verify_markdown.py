#!/usr/bin/env python3
"""Integrity checks for the generated EasyUO-Documentation.md.

    python3 scripts/verify_markdown.py [EasyUO-Documentation.md] [Wiki-<stamp>.xml]

Checks: every ``](#anchor)`` link resolves to the FIRST element with that id on
github.com (explicit ``<a id>`` and GitHub's auto heading anchors both count);
every spine page appears once; no stray wiki markup; excluded pages absent.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from linkmap import build_anchor_map
from mwlib import normalize_title
from structure import build_spine

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MD = ROOT / "EasyUO-Documentation.md"
DEFAULT_XML = ROOT / "Wiki-20260908T054528Z.xml"

EXCLUDED = ["Suomenkielinen"]  # Finnish Tutorial body marker
STRAY = [
    (r"\{\{[A-Za-z][a-z ]", "unexpanded template call"),
    (r'class="wikilink"', "leftover pandoc wikilink"),
    (r"⟦", "leftover note sentinel"),
    (r"__NOTE__", "leftover note marker"),
    (r"^=+[^\n=]+=+\s*$", "unconverted wiki heading"),
    (r"</?blockquote>", "leftover blockquote tag"),
    (r"\{\{\{", "leftover template parameter"),
    (r"<nowiki", "leftover nowiki tag"),
    (r"&#\d+;", "leftover numeric entity"),
]


def _strip_code(md: str) -> str:
    md = re.sub(r"```.*?```", "", md, flags=re.S)
    md = re.sub(r"^(?: {4}|\t).*$", "", md, flags=re.M)
    md = re.sub(r"`[^`\n]*`", "", md)
    return md


def gh_slug(text: str, seen: dict[str, int]) -> str:
    """GitHub / github-slugger heading id (with -1, -2 dedupe)."""
    text = re.sub(r"<[^>]+>", "", text).strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)          # keeps underscores
    base = text.replace(" ", "-")                  # one hyphen per space
    n = seen.get(base, 0)
    seen[base] = n + 1
    return base if n == 0 else f"{base}-{n}"


def main() -> int:
    md_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_MD
    xml_path = sys.argv[2] if len(sys.argv) > 2 else str(DEFAULT_XML)
    md = md_path.read_text(encoding="utf-8")
    ok = True

    groups, _pages = build_spine(xml_path)
    anchor_map = build_anchor_map(groups)

    # ---- ordered id map: what does github.com resolve #foo to first? ----
    first_id: dict[str, str] = {}          # id -> 'explicit' | 'heading'
    seen: dict[str, int] = {}
    for m in re.finditer(r'<a id="([^"]+)"></a>|^(#{1,6})[ \t]+(.*?)[ \t]*$', md, re.M):
        if m.group(1):
            first_id.setdefault(m.group(1), "explicit")
        else:
            first_id.setdefault(gh_slug(m.group(3), seen), "heading")

    # ---- 1. every internal link resolves to a real, correct target ----
    broken, shadowed = [], []
    for m in re.finditer(r"\]\(#([^)]+)\)", md):
        tgt = m.group(1)
        kind = first_id.get(tgt)
        if kind is None:
            broken.append(tgt)
        elif kind == "heading" and tgt in anchor_map.values():
            shadowed.append(tgt)
    if broken:
        ok = False
        print(f"BROKEN internal links ({len(set(broken))}):")
        for b in sorted(set(broken)):
            print("  #" + b)
    if shadowed:
        ok = False
        print(f"SHADOWED links (a heading auto-anchor wins over the entry) "
              f"({len(set(shadowed))}):")
        for s in sorted(set(shadowed)):
            print("  #" + s)

    # ---- 2. explicit anchor vs earlier heading-slug collision ----
    collisions = [aid for aid, kind in first_id.items()
                  if kind == "heading" and f'<a id="{aid}"></a>' in md]
    if collisions:
        ok = False
        print(f"ANCHOR/HEADING collisions ({len(collisions)}):", sorted(collisions))

    # ---- 3. spine coverage ----
    spine = [p for g in groups for s in g.subsections for p in s.pages]
    for title in spine:
        aid = anchor_map[normalize_title(title)]
        c = md.count(f'<a id="{aid}"></a>')
        if c != 1:
            ok = False
            print(f"{'MISSING' if c == 0 else 'DUPLICATE'} entry: {title}  (#{aid})")
    print(f"spine entries: {len(spine)}   entry anchors: "
          f"{len(re.findall(r'<a id=', md))}")

    # ---- 4. stray markup ----
    scan = _strip_code(md)
    for pat, desc in STRAY:
        hits = re.findall(pat, scan, re.M)
        if hits:
            ok = False
            print(f"STRAY {desc}: {len(hits)}x  e.g. {hits[:3]}")
    for m in re.finditer(r"\[\[([A-Za-z#][^\]]*)\]\]", scan):
        ok = False
        print(f"STRAY unconverted wikilink: {m.group(0)!r}")

    # ---- 5. excluded content ----
    for token in EXCLUDED:
        if token in md:
            ok = False
            print(f"EXCLUDED content present: {token!r}")
    for t in ("Main Page", "Current events", "Tutorials", "Finnish Tutorial"):
        if re.search(rf'<a id="[a-z]+-{re.escape(t.lower().replace(" ", "-"))}"', md):
            ok = False
            print(f"EXCLUDED page emitted: {t}")

    print("\nRESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
