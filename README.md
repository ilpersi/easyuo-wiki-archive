# EasyUO Documentation Archive

[![verify](https://github.com/ilpersi/easyuo-wiki-archive/actions/workflows/verify.yml/badge.svg)](https://github.com/ilpersi/easyuo-wiki-archive/actions/workflows/verify.yml)

The [EasyUO](http://www.easyuo.com/) scripting documentation lives in an aging MediaWiki
at <http://wiki.easyuo.com/index.php?title=Documentation>. This repository **preserves that
documentation** and republishes it as a single, readable Markdown file.

- **[`EasyUO-Documentation.md`](EasyUO-Documentation.md)** — the deliverable. All ~255 command,
  system-variable and reference pages in one file, ordered exactly as the wiki's `Documentation`
  page organises them, with a generated table of contents and working in-document cross-links.
- **`Wiki-20260908T054528Z.xml`** — a complete MediaWiki `Special:Export` dump (300 pages) that
  the Markdown is generated from. This is the archival source of truth.
- **`scripts/`** — a reproducible, standard-library pipeline that (1) fetches/refreshes the export
  and (2) converts it to Markdown.

**`EasyUO-Documentation.md` and every `Wiki-*.xml` are generated.** Never hand-edit them — change
the scripts and re-run. Corrections to link targets, typos in the rendered output, etc. all belong
in the conversion scripts, not in the output or the source XML.

## Requirements

| Tool | Version used | Notes |
|---|---|---|
| Python | 3.11+ | standard library only, no `pip install` needed |
| [pandoc](https://pandoc.org/) | 3.x (developed against 3.11) | only needed for the Markdown conversion, not the fetch or the verifiers |
| [`gh`](https://cli.github.com/) | any | optional — only for the GitHub-render preview |

The live wiki is reachable **over plain HTTP only** — its HTTPS certificate is invalid, so
anything that upgrades to or requires `https://` (browsers, many fetch libraries) fails against
it. `fetch_export.py` talks to `http://wiki.easyuo.com` directly.

## Repository layout

```
EasyUO-Documentation.md      generated deliverable
Wiki-20260908T054528Z.xml    generated source-of-truth export (300 pages)
LICENSE                      MIT — covers the code only
LICENSE-DOCS.txt             GFDL 1.2 — covers the archived documentation
.github/workflows/verify.yml CI: runs the two verifiers on push / PR
scripts/
  mwlib.py                   shared helpers: XML iteration, MediaWiki title normalisation,
                             wikitext template/link parsing
  export_titles.txt          authoritative list of page titles to fetch (checked in)
  build_title_list.py        canonicalises export_titles.txt (normalise / de-dupe / sort)
  fetch_export.py            batched Special:Export fetch + reconcile -> Wiki-<stamp>.xml
  verify_links.py            checks every [[link]] / {{template}} in an export resolves
  structure.py               parses Documentation + nav templates -> ordered section tree
  templates.py               expanders for all 34 wiki templates
  wikiprep.py                per-page wikitext preprocessing (template expansion, page patches)
  linkmap.py                 wiki title -> in-document anchor id; link resolution
  mdpost.py                  post-pandoc Markdown cleanup
  convert.py                 orchestrator: export XML -> EasyUO-Documentation.md
  verify_markdown.py         checks the generated Markdown (anchors, coverage, stray markup)
get_download_pages.js        historical browser snippet, superseded by export_titles.txt
```

## Workflow 1 — refresh or expand the wiki export

Run this only when you need newer wiki content or want to add pages the crawl missed.

```sh
# 1. (optional) add or remove page titles
$EDITOR scripts/export_titles.txt

# 2. canonicalise the list (normalise casing/whitespace, de-duplicate, sort) so the
#    fetch reconciliation doesn't trip over a mis-cased title
python3 scripts/build_title_list.py

# 3. fetch every title via Special:Export into a new timestamped XML.
#    --stamp is required (the scripts never read the wall clock, for reproducibility)
python3 scripts/fetch_export.py --stamp "$(date -u +%Y%m%dT%H%M%SZ)"

# 4. verify every internal link and template reference in the new export resolves
python3 scripts/verify_links.py Wiki-<stamp>.xml            # must print RESULT: PASS
```

`scripts/export_titles.txt` is the authoritative list — the naive alternative, running
`get_download_pages.js` on the live `Documentation` page, only captures the ~150 pages linked
directly and misses every per-system-variable page (those are transcluded via templates).

`fetch_export.py` POSTs the title list to `Special:Export` in batches, saves each raw response to
`export/raw/` (git-ignored) for debugging, then splices one deterministic `Wiki-<stamp>.xml`. It
reconciles the titles it received against the titles it requested (MediaWiki silently drops
non-existent titles) and **fails loudly** if any are missing.

After a successful fetch, point the pipeline at the new file — update the default `Wiki-*.xml`
filename in `scripts/convert.py`, `scripts/verify_markdown.py` and
`.github/workflows/verify.yml` — then run Workflow 2.

## Workflow 2 — regenerate the Markdown

The common case: rebuild `EasyUO-Documentation.md` from the current export.

```sh
python3 scripts/convert.py
python3 scripts/verify_markdown.py                         # must print RESULT: PASS
```

Optional arguments:

```sh
python3 scripts/convert.py path/to/Wiki-<stamp>.xml -o path/to/output.md
python3 scripts/verify_markdown.py output.md path/to/Wiki-<stamp>.xml
```

## Previewing the Markdown as GitHub renders it

```sh
gh api -X POST /markdown -f mode=gfm --field text=@EasyUO-Documentation.md > /tmp/preview.html
```

or push `EasyUO-Documentation.md` to a repo / gist and open it on github.com.

---

## How it works

### The wiki's structure

The `Documentation` page barely lists anything itself — it transcludes ~22 **navigation
templates** (`{{Flow Control}}`, `{{Client}}`, `{{Status Variables}}`, …). Each of those
`Template:` pages holds a table of links to the individual command / system-variable pages, with a
one-line summary per entry. So the real table of contents is:
`Documentation` → nav templates → the pages they link. `structure.py` walks exactly that to
produce the ordered section tree and the per-section summary tables.

MediaWiki title rules the pipeline relies on: titles are **first-letter-case-insensitive** and
treat space and underscore as equivalent (`[[break]]`, `[[control_structures]]` →
`Break`, `Control Structures`). All matching goes through `mwlib.normalize_title()`.

### The conversion pipeline (`convert.py`)

Per page: **`wikiprep` → `pandoc -f mediawiki -t gfm` → `mdpost`**, then concatenate in
`Documentation` order behind a generated TOC.

1. **`wikiprep.prep_page`**
   - Applies **per-page patches** (`_SIMPLE_PATCHES` / `_FUNC_PATCHES`) for pages pandoc can't
     parse or that render badly: `CmpPix`, `Operators`, `SendHeader`, `IgnoreItem`, and
     `Item Database` — one giant `rowspan`/`colspan` wikitable, re-emitted as a clean HTML
     `<table>` (GitHub renders those natively; `mdpost` leaves any table with `rowspan`/`colspan`
     as raw HTML). A few other rough pages (`Event Macro`, `Variables`) are handled by general
     passes — lifting headings out of table cells, dropping trailing "Main Page" nav tables.
   - **Expands all 34 templates** (`templates.py`). This is mandatory: **pandoc silently deletes
     every `{{...}}` call**, and the load-bearing prose on command pages (`{{body}}`), variable
     pages (`{{header}}`) and note callouts (`{{note}}`) lives inside template arguments.
   - Strips `[[Category:…]]`, `__TOC__`/`__NOTOC__` and navigational cruft; lifts headings out of
     table cells; inlines the "Related Commands" boxes.
2. **pandoc** `-f mediawiki -t gfm --wrap=none`.
3. **`mdpost.postprocess`** — rewrites pandoc's `<a class="wikilink">` to `[label](#anchor)` via
   `linkmap`; converts `{{note}}` blocks to GitHub `> [!NOTE]` callouts; flattens leftover raw
   HTML tables; strips residual inline HTML; shifts heading levels so a page body starts one level
   below its entry heading.

### Anchor scheme

Every explicit `<a id>` is **prefixed** so it can never collide with one of GitHub's
auto-generated (un-prefixed, from heading text) anchor ids:

| prefix | used for |
|---|---|
| `sec-` | group and section headers |
| `guide-` `ref-` `cmd-` `var-` `apx-` | page entries, one per `Documentation` group (see `linkmap.GROUP_PREFIX`) |
| `ref-<page>--<section>` | the handful of hub-page sub-sections that wiki links point at |

`linkmap.slug()` matches GitHub's `github-slugger` algorithm. `linkmap.build_anchor_map()` is the
single source of truth for both anchor emission (`convert.py`) and link resolution
(`LinkResolver`), and `verify_markdown.py` uses it too. Confirmed behaviour: GitHub keeps
`<a id="x">` (rewriting the id to `user-content-x`) and a `[…](#x)` link still scrolls to it.

### What `verify_markdown.py` checks

Every `](#anchor)` resolves to the *first* element with that id on github.com (explicit `<a id>`
**and** simulated heading auto-anchors both count, so it catches an entry being shadowed by an
earlier heading); every source page appears exactly once; no wiki markup (`{{`, `[[`,
`<blockquote>`, note sentinels, …) leaked through; the excluded pages are absent.

---

## Maintenance notes

- **If you re-fetch the export with new pages, revisit `scripts/templates.py` and
  `scripts/wikiprep.py`.** A new template or a new unparseable page needs handling;
  `verify_markdown.py`'s "no stray `{{`" check will flag an unhandled template.
- Two link edge cases are handled in the conversion, not the XML:
  - `[[Exevent DropC]]` / `[[Exevent dropc]]` on the `Exevent Dropc` page are dead even on the
    live wiki (MediaWiki only case-folds the first letter) → repointed to `Exevent Dropc`.
  - `[[Wikipedia:disambiguation]]` in `Template:Disambig` is a valid interwiki link → rendered as
    an external `en.wikipedia.org` URL.
- The first export (a naive crawl of the `Documentation` page) missed ~150 linked pages — chiefly
  every per-system-variable detail page, three templates, and a few orphans. `export_titles.txt`
  is the corrected, complete list; the current `Wiki-*.xml` was fetched from it.
- Keep the pipeline reproducible: no wall-clock reads, deterministic output ordering, and the
  export/output are always regenerated rather than edited.

### Included vs excluded

- **Included:** every command and system-variable page reachable from `Documentation`, plus the
  orphaned `Else` / `Sub` / `Label` / `Exevent` pages folded into Command Reference, and four
  appendix articles (`Item Database`, `QG True False`, `Tutorials:Cheffe1`, and the RunUO
  stat/skill-gains write-up).
- **Excluded from the Markdown but kept in the XML export:** the wiki `Main Page`, the `Current
  events` maintenance page, the `Tutorials` link index, the `Str` disambiguation stub, and the
  non-English `Finnish Tutorial`.

## License

This repository has **two licenses** because it contains two kinds of thing:

| What | License | Where |
|---|---|---|
| The code — everything in `scripts/`, `get_download_pages.js` | MIT | [`LICENSE`](LICENSE) |
| The archived documentation — `EasyUO-Documentation.md`, `Wiki-*.xml` | GNU Free Documentation License 1.2 | [`LICENSE-DOCS.txt`](LICENSE-DOCS.txt) |

The documentation content is a verbatim archive of the [EasyUO community
wiki](http://wiki.easyuo.com/), which publishes its content under the GFDL 1.2. This repository
redistributes it under the same license; original authorship and full page history remain on the
source wiki. In the generated Markdown, e-mail addresses that appeared in old "user contributed
notes" are redacted (handle kept, domain removed); the `Wiki-*.xml` export is left byte-faithful.

## Continuous integration

[`.github/workflows/verify.yml`](.github/workflows/verify.yml) runs `verify_links.py` and
`verify_markdown.py` on every push and pull request. Regenerating `EasyUO-Documentation.md`
requires a local pandoc and is not done in CI.
