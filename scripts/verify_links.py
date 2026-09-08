#!/usr/bin/env python3
"""Link-graph checker for an EasyUO MediaWiki export XML.

Reports internal [[links]] and {{template}} calls that do not resolve to a
page present in the dump, plus a few sanity buckets. Exits non-zero if any
unresolved reference is outside the known allowlist, if a requested title is
missing, or if an unexpected (spam) page appears.

Usage:
    python3 scripts/verify_links.py <export.xml> [--requested scripts/export_titles.txt]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from mwlib import (
    INTERWIKI_PREFIXES,
    NONCONTENT_PREFIXES,
    iter_pages,
    normalize_title,
    read_title_list,
)

ROOT = Path(__file__).resolve().parent.parent

# Known dead links: MediaWiki case-folds only the first letter, so these
# mixed/lower-case variants on the "Exevent Dropc" page never resolved even on
# the live wiki. The correct page "Exevent Dropc" is present. Compared after
# normalize_title() on both source and target.
DEAD_LINK_ALLOWLIST = {
    ("Exevent Dropc", "Exevent DropC"),
    ("Exevent Dropc", "Exevent dropc"),
}

# "Finnish Tutorial" is archived verbatim but excluded from the English Markdown
# build; its many broken redlinks (Var charPosX, Finditem, ...) are not our
# problem to fix.
SKIP_SOURCE_PAGES = {"Finnish Tutorial"}

# MediaWiki magic words / parser tokens that look like {{template}} calls.
MAGIC_WORDS = {
    "pagename", "fullpagename", "basepagename", "subpagename", "namespace",
    "fullpagenamee", "pagenamee", "sitename", "servername", "server",
    "scriptpath", "currentyear", "currentmonth", "currentday", "localurl",
    "ns", "int", "plural", "urlencode", "lc", "uc", "lcfirst", "ucfirst",
    "!", "toc", "forcetoc", "notoc",
}

LINK_RE = re.compile(r"\[\[\s*([^\]|\n]+?)\s*(?:\|[^\]]*)?\]\]")
TEMPLATE_RE = re.compile(r"\{\{\s*([^}|{#<\n][^}|{\n]*?)\s*(?:\||\}\})")


def strip_anchor(target: str) -> str:
    return target.split("#", 1)[0].strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("xml")
    ap.add_argument("--requested", default=str(ROOT / "scripts" / "export_titles.txt"))
    args = ap.parse_args()

    pages: list[tuple[int, str, str]] = list(iter_pages(args.xml))

    ns0_titles = {normalize_title(t) for ns, t, _ in pages if ns == 0}
    template_names = {
        normalize_title(t.split(":", 1)[1])
        for ns, t, _ in pages
        if ns == 10 and ":" in t
    }
    all_titles = {normalize_title(t) for _, t, _ in pages}

    unresolved_links: list[tuple[str, str]] = []
    unresolved_templates: list[tuple[str, str]] = []
    interwiki: set[str] = set()

    for ns, title, text in pages:
        if normalize_title(title) in SKIP_SOURCE_PAGES:
            continue
        for m in LINK_RE.finditer(text):
            raw = strip_anchor(m.group(1))
            if not raw or raw.startswith("{{"):
                continue
            raw = raw.lstrip(":").strip()
            if not raw:
                continue  # bare [[#anchor]]
            prefix = raw.split(":", 1)[0].strip().lower() if ":" in raw else ""
            if prefix in INTERWIKI_PREFIXES:
                interwiki.add(raw)
                continue
            if prefix in NONCONTENT_PREFIXES:
                continue
            norm = normalize_title(raw)
            if norm not in ns0_titles:
                unresolved_links.append((normalize_title(title), norm))

        for m in TEMPLATE_RE.finditer(text):
            raw = m.group(1).strip()
            if not raw or raw.startswith("{") or raw.startswith("#"):
                continue
            # {{{param}}} placeholder: the "{{" we matched is really the inner
            # two braces of a triple. Skip when preceded by another "{".
            if m.start() > 0 and text[m.start() - 1] == "{":
                continue
            if raw.isdigit() or raw.lower() in MAGIC_WORDS:
                continue
            if raw.lower().startswith("template:"):
                raw = raw.split(":", 1)[1].strip()
            norm = normalize_title(raw)
            if norm not in template_names:
                unresolved_templates.append((title, raw))

    # Requested vs present.
    missing_requested: list[str] = []
    unexpected_pages: list[str] = []
    req_path = Path(args.requested)
    if req_path.exists():
        requested = {normalize_title(t) for t in read_title_list(req_path)}
        missing_requested = sorted(requested - all_titles)
        unexpected_pages = sorted(all_titles - requested)

    # ---- report ----
    def dump(label: str, items) -> None:
        print(f"\n{label} ({len(items)})")
        for it in items:
            print(f"  {it}")

    uniq_links = sorted(set(unresolved_links))
    uniq_templates = sorted(set(unresolved_templates))

    print(f"=== verify_links: {args.xml} ===")
    print(f"pages: {len(pages)}  ns0: {len(ns0_titles)}  templates: {len(template_names)}")

    unexpected_dead = [p for p in uniq_links if p not in DEAD_LINK_ALLOWLIST]
    allowlisted = [p for p in uniq_links if p in DEAD_LINK_ALLOWLIST]

    dump("UNRESOLVED internal links (not allowlisted)", unexpected_dead)
    dump("unresolved internal links (allowlisted dead links)", allowlisted)
    dump("UNRESOLVED template calls", uniq_templates)
    dump("interwiki / external links (informational)", sorted(interwiki))
    if req_path.exists():
        dump("REQUESTED titles missing from dump", missing_requested)
        dump("pages present but NOT requested (spam guard)", unexpected_pages)
    else:
        print("\n(no --requested list found; skipping requested/unexpected checks)")

    ok = not unexpected_dead and not uniq_templates and not missing_requested and not unexpected_pages
    print("\nRESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
