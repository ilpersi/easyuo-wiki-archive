#!/usr/bin/env python3
"""Convert the EasyUO MediaWiki dump into one Markdown file.

    python3 scripts/convert.py [Wiki-<stamp>.xml] [-o EasyUO-Documentation.md]

Pipeline per page: wikiprep (expand templates, patch, clean) -> pandoc
(mediawiki -> gfm) -> mdpost (resolve links, notes, headings). Pages are
emitted in the order the wiki's `Documentation` page defines, wrapped with a
generated table of contents.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

from linkmap import SECTION_ANCHORS, LinkResolver, build_anchor_map, slug
from mdpost import postprocess
from mwlib import normalize_title
from structure import build_spine
from wikiprep import prep_page

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_XML = ROOT / "Wiki-20260908T054528Z.xml"
DEFAULT_OUT = ROOT / "EasyUO-Documentation.md"

PREAMBLE = """\
# EasyUO Documentation

A single-file rendering of the EasyUO scripting documentation, converted from the
[EasyUO wiki](http://wiki.easyuo.com/index.php?title=Documentation). Section
order follows the wiki's `Documentation` page. The non-English *Finnish Tutorial*
is preserved in the source export but omitted here.

This document is a verbatim archive of community wiki content and is licensed,
like the wiki, under the [GNU Free Documentation License, Version 1.2](http://www.gnu.org/licenses/old-licenses/fdl-1.2.html).
Original authorship and page history are on the [source wiki](http://wiki.easyuo.com/).
"""


def run_pandoc(wikitext: str, title: str) -> str:
    r = subprocess.run(
        ["pandoc", "-f", "mediawiki", "-t", "gfm", "--wrap=none"],
        input=wikitext, capture_output=True, text=True,
    )
    if r.returncode != 0:
        raise RuntimeError(f"pandoc failed on {title!r}: {r.stderr.strip()}")
    return r.stdout


def inject_section_anchors(md: str, page_title: str) -> str:
    for (pg, _sec), (anchor, heading) in SECTION_ANCHORS.items():
        if pg != page_title:
            continue
        pat = re.compile(
            r"^(#{1,6}[ \t]+" + re.escape(heading) + r")[ \t]*$", re.M | re.I
        )
        md = pat.sub(lambda m: f'<a id="{anchor}"></a>\n\n' + m.group(1), md, count=1)
    return md


def render_page(title: str, wikitext: str, resolver: LinkResolver,
                heading_base: int) -> str:
    pre = prep_page(title, wikitext)
    gfm = run_pandoc(pre, title)
    md = postprocess(gfm, page_title=title, resolve=resolver.resolve,
                     heading_base=heading_base)
    md = inject_section_anchors(md, title)
    md = md.strip()
    if len(md) < 15:
        raise RuntimeError(f"{title!r} rendered empty ({md!r})")
    return md


def summary_table(sub, resolver: LinkResolver) -> str:
    rows = [r for r in sub.rows if r.summary]
    if len(rows) < 2:
        return ""
    kind = "Variable" if any(r.mode for r in rows) else "Command"
    out = [f"| {kind} | Summary |", "|---|---|"]
    for r in rows:
        anchor = resolver.resolve(r.target) or ""
        name = f"[{r.label}]({anchor})" if anchor else r.label
        badge = {"ro": " _(ro)_", "rw": " _(rw)_"}.get(r.mode, "")
        out.append(f"| {name}{badge} | {r.summary} |")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("xml", nargs="?", default=str(DEFAULT_XML))
    ap.add_argument("-o", "--out", default=str(DEFAULT_OUT))
    args = ap.parse_args()

    groups, pages = build_spine(args.xml)

    anchor_map = build_anchor_map(groups)
    resolver = LinkResolver(args.xml, anchor_map)

    # --- render every page up front (so TOC + link check see them all) ---
    rendered: dict[str, str] = {}
    for g in groups:
        for s in g.subsections:
            entry_level = 3 if s.title == g.title else 4
            for title in s.pages:
                rendered[title] = render_page(
                    title, pages[title], resolver, entry_level + 1
                )

    # --- assemble ---
    parts: list[str] = [PREAMBLE.rstrip(), ""]

    # table of contents
    toc: list[str] = []
    for g in groups:
        toc.append(f"- [{g.title}](#sec-{slug(g.title)})")
        for s in g.subsections:
            if s.title != g.title:
                toc.append(f"  - [{s.title}](#sec-{slug(s.title)})")
    parts.append("## Contents\n\n" + "\n".join(toc))

    for g in groups:
        parts.append(f'<a id="sec-{slug(g.title)}"></a>\n\n## {g.title}')
        for s in g.subsections:
            if s.title != g.title:
                parts.append(f'<a id="sec-{slug(s.title)}"></a>\n\n### {s.title}')
            if s.intro:
                parts.append(s.intro)
            if s.caveat:
                parts.append(f"**{s.caveat}**")
            tbl = summary_table(s, resolver)
            if tbl:
                parts.append(tbl)
            entry_level = 3 if s.title == g.title else 4
            for title in s.pages:
                disp = display_title(title)
                anchor = anchor_map[normalize_title(title)]
                parts.append(
                    f'<a id="{anchor}"></a>\n\n{"#" * entry_level} {disp}'
                )
                parts.append(rendered[title])

    out_text = "\n\n".join(p for p in parts if p is not None).strip() + "\n"
    out_text = re.sub(r"\n{3,}", "\n\n", out_text)
    Path(args.out).write_text(out_text, encoding="utf-8", newline="\n")

    n_entries = sum(len(s.pages) for g in groups for s in g.subsections)
    print(f"pages rendered : {n_entries}")
    print(f"output         : {args.out} ({len(out_text):,} bytes)")
    if resolver.unresolved:
        print(f"unresolved links ({len(resolver.unresolved)}):",
              ", ".join(sorted(resolver.unresolved)))
    return 0


def display_title(title: str) -> str:
    # keep the wiki's mixed-case command names ("event PathFind"), tidy the rest
    return title


if __name__ == "__main__":
    sys.exit(main())
