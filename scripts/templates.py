"""Expanders for the 34 templates in the EasyUO wiki dump.

`expand(text, title)` repeatedly rewrites ``{{...}}`` calls to wikitext until
none remain. Notes become ``<blockquote>`` with a ``Note:`` lead-in that mdpost
turns into a GitHub ``[!NOTE]`` callout. The ~22 navigation/list templates are
*not* expanded here -- they are chrome on detail pages (dropped) and structure
elsewhere (parsed directly by structure.py).
"""
from __future__ import annotations

import re

from mwlib import find_templates

NOTE_LEAD = "'''Note:'''"  # blockquote lead-in; mdpost rewrites "> **Note:**"

# Navigation / list templates: transcluded by Documentation (structure) and as
# "See Also" blocks on detail pages (chrome). Dropped by the generic expander.
NAV_TEMPLATES = {
    "flow control", "client", "event", "exevent", "menu", "namespace",
    "miscellaneous", "obsolete", "character variables", "status variables",
    "container", "last action", "finditem", "shop", "extended",
    "client variables", "combat", "namespace variables",
    "miscellaneous variables", "result", "tile", "constant",
}

# Pure chrome -> removed outright.
DROP_TEMPLATES = {"command header", "back to top", "footer", "disambig"}

_WIKILINK = re.compile(r"\[\[\s*([^\]|]+?)\s*(?:\|\s*([^\]]*?))?\s*\]\]")


def _strip_synopsis(s: str) -> str:
    s = s.replace("<nowiki>", "").replace("</nowiki>", "")
    s = re.sub(r"<br\s*/?>", "\n", s)
    s = _WIKILINK.sub(lambda m: (m.group(2) or m.group(1)).strip(), s)
    lines = [ln.strip() for ln in s.splitlines()]
    return "\n".join(ln for ln in lines if ln)


def _expand_body(args: list[str]) -> str:
    synopsis = _strip_synopsis(args[0]) if args else ""
    description = args[1].strip() if len(args) > 1 else ""
    out = []
    if synopsis:
        out.append("'''Synopsis'''\n\n<pre>\n" + synopsis + "\n</pre>")
    out.append("'''Description'''\n\n" + description)
    return "\n\n" + "\n\n".join(out) + "\n\n"


def _expand_header(args: list[str]) -> str:
    mode = args[1].strip().lower() if len(args) > 1 else "ro"
    desc = args[2].strip() if len(args) > 2 else ""
    badge = "''Read-only.''" if mode == "ro" else "''Read / write.''"
    return badge + " " + desc


def _expand_note(body: str) -> str:
    body = body.strip().strip("'").strip()
    # a first line that is "*item" / "#item" needs a blank line after the lead-in
    # so pandoc renders it as a real list inside the alert (not glued text).
    sep = "\n\n" if body[:1] in "*#" else " "
    return "\n\n<blockquote>\n\n" + NOTE_LEAD + sep + body + "\n\n</blockquote>\n\n"


_STATUSNOTE = (
    "This variable will not work unless the character status bar is open. "
    "You can use [[Event_Macro#Gump_Control|Event Macro 8 2]] to open it "
    "from your script."
)
_CONTNOTE = (
    "EasyUO currently only holds information in the #cont* on the "
    '"top most" gump. This means that the last gump that was opened or moved '
    "in any way is what EUO is reporting."
)


def _handler(name: str, args: list[str], title: str) -> str:
    n = name.strip().lower()
    if n == "body":
        return _expand_body(args)
    if n == "header":
        return _expand_header(args)
    if n == "note":
        return _expand_note(args[0] if args else "")
    if n == "statusnote":
        return _expand_note(_STATUSNOTE)
    if n == "contnote":
        return _expand_note(_CONTNOTE)
    if n == "1.5only":
        return _expand_note("Only available in EasyUO 1.5+")
    if n == "ro":
        return "_(read-only)_"
    if n == "rw":
        return "_(read/write)_"
    if n in NAV_TEMPLATES or n in DROP_TEMPLATES:
        return ""
    return "{{" + name + "}}"  # unknown -> visible marker for verify_markdown


def expand(text: str, title: str, max_passes: int = 12) -> str:
    for _ in range(max_passes):
        calls = [c for c in find_templates(text)
                 if not c[2].lstrip().startswith("{{{")]
        if not calls:
            return text
        out, pos = [], 0
        for start, end, name, args in calls:
            out.append(text[pos:start])
            out.append(_handler(name, args, title))
            pos = end
        out.append(text[pos:])
        new = "".join(out)
        if new == text:
            return new
        text = new
    return text
