"""Build the document spine from the `Documentation` page + nav templates.

The wiki's `Documentation` page defines the section order; each transcluded
navigation template (`{{Flow Control}}`, `{{Status Variables}}`, ...) defines a
subsection heading, an intro line and an ordered list of member pages with
one-line summaries. `build_spine()` returns that as an ordered tree plus the
rows needed for the per-section summary tables.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from mwlib import iter_pages, normalize_title, split_top_level

# Pages that belong in a section but the nav template forgot to list them.
EXTRA_PAGES = {
    "Flow Control": ["Else", "Sub", "Label"],
}
# Orphan overview page -> prepended as the section's intro page.
SECTION_INTRO_PAGE = {"ExEvent": "Exevent"}

APPENDIX_PAGES = [
    ("Item Database", "Container & Gump Sizes"),
    ("QG True False", "Quick Guide: #True & #False"),
    ("Tutorials:Cheffe1", "Script Execution Speed"),
    ("How stat and skill gains work on RunUO freeshards",
     "Stat & Skill Gains on RunUO Freeshards"),
]

# Pages reachable from Documentation that are NOT emitted as their own entries.
SKIP_AS_ENTRY = {"Documentation", "Main Page", "Current events", "Tutorials",
                 "Finnish Tutorial", "Str"}

_WIKILINK = re.compile(r"\[\[\s*([^\]|]+?)\s*(?:\|\s*([^\]]*?))?\s*\]\]")
_HEADING = re.compile(r"^\s*(=+)\s*(.*?)\s*=+\s*$")


@dataclass
class Row:
    target: str            # normalized page title
    label: str             # display label (e.g. "#charPosX" or "break")
    mode: str              # "", "ro" or "rw"
    summary: str           # one-line description (plain text)


@dataclass
class Subsection:
    title: str
    intro: str = ""
    caveat: str = ""
    rows: list[Row] = field(default_factory=list)
    pages: list[str] = field(default_factory=list)   # ordered entry titles


@dataclass
class Group:
    title: str
    subsections: list[Subsection] = field(default_factory=list)


def _clean(text: str) -> str:
    """Wikilinks -> label, drop apostrophe markup / ro-rw templates, trim."""
    text = _WIKILINK.sub(lambda m: (m.group(2) or m.group(1)).strip(), text)
    text = text.replace("{{ro}}", "").replace("{{rw}}", "")
    text = re.sub(r"'{2,5}", "", text)
    return re.sub(r"\s+", " ", text).strip()


def _first_link(cell: str) -> tuple[str, str] | None:
    m = _WIKILINK.search(cell)
    if not m:
        return None
    target = normalize_title(m.group(1))
    label = (m.group(2) or m.group(1)).strip()
    return target, label


def parse_nav_template(body: str) -> Subsection:
    """Parse a `Template:*` nav/list body into a Subsection."""
    lines = body.splitlines()
    sub = Subsection(title="")
    for ln in lines:
        h = _HEADING.match(ln)
        if h and not sub.title:
            sub.title = h.group(2).strip()
            continue
        s = ln.strip()
        if s.startswith("*") and not sub.intro:
            sub.intro = _clean(s[1:])
            continue
        if s.startswith("'''") and not sub.caveat:
            sub.caveat = _clean(s)
            continue

    # table rows: everything between {| and |}
    if "{|" in body:
        table = body.split("{|", 1)[1].rsplit("|}", 1)[0]
        for chunk in re.split(r"\n\|-", table):
            cells = _split_cells(chunk)
            if not cells:
                continue
            fl = _first_link(cells[0])
            if not fl:
                continue
            target, label = fl
            mode = ""
            desc = ""
            rest = cells[1:]
            if rest and re.fullmatch(r"\{\{(ro|rw)\}\}", rest[0].strip()):
                mode = rest[0].strip()[2:4]
                rest = rest[1:]
            if rest:
                desc = _clean(rest[-1])
            sub.rows.append(Row(target, label, mode, desc))
            sub.pages.append(target)
    return sub


def _split_cells(chunk: str) -> list[str]:
    """Split a wikitable row chunk into cell contents.

    Handles ``| a || b`` and multi-line ``| a\n| b``; strips a leading
    ``style=...|`` / ``width=...|`` attribute segment from each cell.
    """
    cells: list[str] = []
    for line in chunk.splitlines():
        line = line.strip()
        if not line or line in ("|", "|}"):
            continue
        if line.startswith("|+") or line.startswith("!"):
            continue
        if line.startswith("|"):
            line = line[1:]
        for cell in split_top_level(line, "|"):
            # "||" -> empty segments between; skip pure separators
            cell = cell.strip()
            if cell == "":
                continue
            # drop a leading HTML-ish attribute chunk: "style=... " with no [[
            if re.match(r'^(style|width|align|valign|colspan|rowspan)\s*=',
                        cell, re.I) and "[[" not in cell and "{{" not in cell:
                continue
            cells.append(cell)
    return cells


def build_spine(xml_path: str):
    pages = {t: body for ns, t, body in iter_pages(xml_path)}
    tmpl = {t[len("Template:"):]: b for t, b in pages.items()
            if t.startswith("Template:")}

    doc = pages["Documentation"]
    groups: list[Group] = []
    cur_group: Group | None = None

    # Getting Started + Language Reference are plain link lists on the page.
    def links_after(header_re: str) -> list[str]:
        m = re.search(header_re + r"(.*?)(?:\n==[^=]|\Z)", doc, re.S)
        if not m:
            return []
        seen: list[str] = []
        for lm in _WIKILINK.finditer(m.group(1)):
            t = normalize_title(lm.group(1).split("#")[0])
            if t and t not in seen:
                seen.append(t)
        return seen

    gs = Group("Getting Started")
    gs.subsections.append(Subsection(
        title="Getting Started",
        pages=[p for p in links_after(r"==\s*Getting Started\s*==")]))
    groups.append(gs)

    lr = Group("Language Reference")
    lr_pages: list[str] = []
    for t in ("Variables", "Expressions", "Operators", "Control Structures"):
        if t in pages:
            lr_pages.append(t)
    lr.subsections.append(Subsection(title="Language Reference", pages=lr_pages))
    groups.append(lr)

    # Command / System Variable Reference: walk the page top-to-bottom.
    for ln in doc.splitlines():
        h = _HEADING.match(ln)
        if h and len(h.group(1)) == 2:
            name = h.group(2).strip()
            if name in ("Command Reference", "System Variable Reference"):
                cur_group = Group(name)
                groups.append(cur_group)
            else:
                cur_group = None
            continue
        tm = re.match(r"\{\{\s*([^}|]+?)\s*\}\}", ln.strip())
        if tm and cur_group is not None:
            tname = tm.group(1).strip()
            if tname.lower() in ("back to top", "note"):
                continue
            key = _match_template_key(tname, tmpl)
            if key is None:
                continue
            sub = parse_nav_template(tmpl[key])
            if not sub.title:
                sub.title = tname
            _augment(sub, pages)
            cur_group.subsections.append(sub)

    # Appendices
    ap = Group("Appendices")
    apsub = Subsection(title="Appendices")
    for title, label in APPENDIX_PAGES:
        nt = normalize_title(title)
        if nt in pages:
            apsub.pages.append(nt)
            apsub.rows.append(Row(nt, label, "", ""))
    ap.subsections.append(apsub)
    groups.append(ap)

    return groups, pages


def _match_template_key(name: str, tmpl: dict) -> str | None:
    for k in tmpl:
        if normalize_title(k) == normalize_title(name):
            return k
    return None


def _augment(sub: Subsection, pages: dict) -> None:
    """Fold in orphan pages and de-duplicate the page list."""
    intro_page = SECTION_INTRO_PAGE.get(sub.title)
    if intro_page and normalize_title(intro_page) in pages:
        sub.pages.insert(0, normalize_title(intro_page))
    for extra in EXTRA_PAGES.get(sub.title, []):
        nt = normalize_title(extra)
        if nt in pages and nt not in sub.pages:
            sub.pages.append(nt)
            sub.rows.append(Row(nt, extra.lower(), "", ""))
    # de-dupe, keep first occurrence
    seen: set[str] = set()
    uniq: list[str] = []
    for p in sub.pages:
        if p not in seen and p in pages and p not in SKIP_AS_ENTRY:
            seen.add(p)
            uniq.append(p)
    sub.pages = uniq
