"""Per-page wikitext preprocessing, applied before pandoc.

Pipeline: malformed-page patches -> template expansion -> strip wiki chrome ->
fix tables -> inline "Related Commands" -> normalize heading depth.
"""
from __future__ import annotations

import re

import templates

# --- malformed-page fixes (asserted: the `old` string must be present) --------

_SIMPLE_PATCHES: dict[str, list[tuple[str, str]]] = {
    # Two identical table-open lines in a row -> pandoc parse error.
    "CmpPix": [
        ('{| border="1" cellpadding="2"\n{| border="1" cellpadding="2"\n',
         '{| border="1" cellpadding="2"\n'),
    ],
}


def _patch_operators(text: str) -> str:
    # cells whose value contains a literal "||" / a leading "-" break pandoc's
    # table parser.
    text = text.replace("|10||<nowiki>||</nowiki>||left-associative",
                        "|10|| the OR operator ||left-associative")
    text = text.replace("|4||- (unary) !||right-associative",
                        "|4|| unary minus, and NOT ||right-associative")
    # Logical Operators table: the "Or" row's example is a literal "||".
    text = text.replace(
        "|%a <nowiki>||</nowiki> %b||Or||",
        "|<code>%a &#124;&#124; %b</code>||Or||")
    # &#10; is a newline the author put between two statements in a cramped cell.
    text = text.replace("&#10;", " ")
    # the precedence table ends with a nested table in a colspan cell -> pandoc
    # emits raw HTML. Flatten: close the table, footnote becomes a paragraph.
    pat = re.compile(
        r"\n\|-\n\|\s*colspan=\"3\"[^\n]*\n\{\|\n\|(?P<note>.*?)\n\|-\n\|\}\n\|-\n\|\}",
        re.S,
    )
    m = pat.search(text)
    if not m:
        return text
    raw = re.sub(r"<sup>.*?</sup>\s*", "", m.group("note"))
    note = re.sub(r"\s+", " ", raw.split("<pre>")[0]).strip()
    pm = re.search(r"<pre>.*?</pre>", raw, re.S)
    pre = "\n\n" + pm.group(0) if pm else ""
    return text[: m.start()] + "\n|}\n\n" + note + pre + text[m.end():]


def _patch_item_database(text: str) -> str:
    """The whole page is one big rowspan/colspan wikitable that pandoc can't
    render. Parse it and emit a clean HTML <table> (GitHub renders those)."""
    body = text.split("{|", 1)[1].rsplit("|}", 1)[0]
    rows: list[list[tuple[str, str, str]]] = []      # (tag-less content, rs, cs)
    cur: list[tuple[str, str, str]] = []
    for raw in body.split("\n"):
        ln = raw.rstrip()
        if ln.startswith("|-"):
            if cur:
                rows.append(cur)
                cur = []
            continue
        if not ln.startswith("|") or ln.startswith("|+"):
            continue
        seg = ln[1:]
        attrs, content = (seg.split("|", 1) if "|" in seg else ("", seg))
        rs = (re.search(r'rowspan="?(\d+)"?', attrs, re.I) or [None, ""])[1]
        cs = (re.search(r'colspan="?(\d+)"?', attrs, re.I) or [None, ""])[1]
        cur.append((content.strip(), rs, cs))
    if cur:
        rows.append(cur)
    if not rows:
        return text

    out = ["<table>"]
    for i, row in enumerate(rows):
        tag = "th" if i == 0 else "td"
        cells = []
        for content, rs, cs in row:
            a = (f' rowspan="{rs}"' if rs else "") + (f' colspan="{cs}"' if cs else "")
            cells.append(f"<{tag}{a}>{content or '&nbsp;'}</{tag}>")
        out.append("<tr>" + "".join(cells) + "</tr>")
    out.append("</table>")
    return "\n".join(out)


def _patch_sendheader(text: str) -> str:
    # the author left two sub-sections' example code un-wrapped (bare lines + <br>)
    def wrap(m: re.Match) -> str:
        body = re.sub(r"\s*<br\s*/?>\s*", "\n", m.group(2)).strip()
        return m.group(1) + "<pre>\n" + body + "\n</pre>\n\n"

    return re.sub(
        r"(^==[ \t]*(?:Send cookie|HTTP POST)[ \t]*==[ \t]*\n\n?)(.*?)(?=^=|\Z)",
        wrap, text, flags=re.M | re.S,
    )


def _patch_ignoreitem(text: str) -> str:
    # runs of single-space-indented preformatted lines (with '' markup inside)
    # -> a real <pre> block.
    lines = text.split("\n")
    out: list[str] = []
    buf: list[str] = []

    def flush() -> None:
        if buf:
            code = "\n".join(re.sub(r"'{2,5}", "", ln[1:]) for ln in buf)
            out.extend(["<pre>", code, "</pre>"])
            buf.clear()

    for ln in lines:
        if ln.startswith(" ") and not ln.startswith("  ") and ln.strip():
            buf.append(ln)
        else:
            flush()
            out.append(ln)
    flush()
    return "\n".join(out)


_FUNC_PATCHES = {
    "Item Database": _patch_item_database,
    "Operators": _patch_operators,
    "SendHeader": _patch_sendheader,
    "IgnoreItem": _patch_ignoreitem,
}


def apply_malformed_patches(title: str, text: str) -> str:
    for old, new in _SIMPLE_PATCHES.get(title, []):
        assert old in text, f"patch for {title!r} did not match"
        text = text.replace(old, new)
    if title in _FUNC_PATCHES:
        text = _FUNC_PATCHES[title](text)
    return text


# --- table fixes -------------------------------------------------------------

def fix_table_header_rows(text: str) -> str:
    """`!a||!b||!c` on one line -> separate `!` lines (pandoc needs this)."""
    out = []
    for line in text.splitlines():
        s = line.lstrip()
        if s.startswith("!") and "||" in line:
            indent = line[: len(line) - len(s)]
            parts = s.split("||")
            for p in parts:
                p = p.strip()
                if not p.startswith("!"):
                    p = "!" + p
                out.append(indent + p)
        else:
            out.append(line)
    return "\n".join(out)


def lift_headings_out_of_tables(text: str) -> str:
    """A `==== X ====` heading inside a `{|...|}` -> close table, heading, reopen."""
    lines = text.splitlines()
    out: list[str] = []
    in_table = False
    opener = '{| border="1"'
    header_row = ""
    for line in lines:
        st = line.strip()
        if st.startswith("{|"):
            in_table = True
            opener = st
            header_row = ""
            out.append(line)
            continue
        if st == "|}":
            in_table = False
            out.append(line)
            continue
        if in_table and re.match(r"^=+.*=+$", st):
            heading = st.strip("=").strip()
            out.append("|}")
            out.append("")
            out.append("==== " + heading + " ====")
            out.append("")
            out.append(opener)
            if header_row:
                out.append(header_row)
                out.append("|-")
            continue
        if in_table and not header_row and st.startswith("!"):
            header_row = line
        out.append(line)
    return "\n".join(out)


# --- wiki chrome ------------------------------------------------------------

_CATEGORY = re.compile(r"\[\[\s*Category\s*:[^\]]*\]\]\s*", re.I)
_MAGIC = re.compile(r"__(TOC|NOTOC|FORCETOC)__\s*")
_COMMENT = re.compile(r"<!--.*?-->", re.S)
_SEEALSO = re.compile(r"^\s*=+\s*See also\s*=+\s*$", re.I | re.M)
_NAV_TABLE = re.compile(
    r"\n-{3,}\s*\n+\s*\{\|[^{}]*?\[\[\s*Main[ _]Page\s*\]\][^{}]*?(?:\|\}|\Z)",
    re.S,
)
_TRAIL_NAV_OPEN = re.compile(
    r"\n-{3,}\s*\n+\s*\{\|\s*\n\|[^\n]*\[\[\s*Main[ _]Page\s*\]\][^\n]*\Z", re.S
)


def strip_chrome(text: str) -> str:
    text = _COMMENT.sub("", text)
    text = _CATEGORY.sub("", text)
    text = _MAGIC.sub("", text)
    text = _NAV_TABLE.sub("", text)
    text = _TRAIL_NAV_OPEN.sub("", text)
    text = _SEEALSO.sub("", text)
    return text


# --- Related Commands -> inline --------------------------------------------

_WIKILINK = re.compile(r"\[\[\s*([^\]|]+?)\s*(?:\|\s*([^\]]*?))?\s*\]\]")
_RELATED = re.compile(
    r"^[ \t]*=+[ \t]*Related (?:Commands|Functions)[ \t]*=+[ \t]*\n"
    r"\s*(\{\|.*?\n[ \t]*\|\})",
    re.S | re.M | re.I,
)
_RELATED_EMPTY = re.compile(
    r"^[ \t]*=+[ \t]*Related (?:Commands|Functions)[ \t]*=+[ \t]*$", re.M | re.I
)


def inline_related(text: str) -> str:
    def repl(m: re.Match) -> str:
        seen: list[str] = []
        for lm in _WIKILINK.finditer(m.group(1)):
            tgt = lm.group(1).strip()
            lbl = (lm.group(2) or lm.group(1)).strip()
            entry = f"[[{tgt}|{lbl}]]"
            if entry not in seen:
                seen.append(entry)
        if not seen:
            return ""
        return "\n'''Related:''' " + ", ".join(seen) + "\n"

    text = _RELATED.sub(repl, text)
    text = _RELATED_EMPTY.sub("", text)
    return text


# --- orchestration -------------------------------------------------------

def prep_page(title: str, wikitext: str) -> str:
    text = apply_malformed_patches(title, wikitext)
    text = templates.expand(text, title)
    text = strip_chrome(text)
    text = lift_headings_out_of_tables(text)
    text = fix_table_header_rows(text)
    text = inline_related(text)
    # collapse the blank lines left by removed chrome
    text = re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"
    return text
