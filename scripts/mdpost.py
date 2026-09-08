"""Post-pandoc cleanup of a single page's GFM output."""
from __future__ import annotations

import re

_WIKILINK_A = re.compile(
    r'<a href="(?P<href>[^"]*)"[^>]*\bclass="wikilink"[^>]*>(?P<text>.*?)</a>',
    re.S,
)
_INLINE_HTML = [
    (re.compile(r"</?(?:b|strong)>"), "**"),
    (re.compile(r"</?(?:i|em)>"), "*"),
    (re.compile(r"</?(?:tt|code)>"), "`"),
    (re.compile(r"</?(?:u|span|sup|sub|big|small|font)(?:\s[^>]*)?>"), ""),
    (re.compile(r"<br\s*/?>"), "  \n"),
    (re.compile(r"</?p(?:\s[^>]*)?>"), ""),
]
# `<pre>` only survives pandoc when embedded somewhere it can't be a block
# (e.g. a table cell) -> collapse to an inline code span.
_INLINE_PRE = re.compile(r"<pre>(.*?)</pre>", re.S)


def _inline_pre(m: re.Match) -> str:
    body = re.sub(r"</?code>|`", "", m.group(1))
    body = re.sub(r"\s*&#10;\s*|\s+", " ", body).strip()
    return f"`{body}`" if body else ""
# a pipe table with a header row + separator but no body rows
_HEADER_ONLY_TABLE = re.compile(
    r"^\|.*\|[ \t]*\n\|[ \t:|-]+\|[ \t]*\n(?=\n|\Z|[^|])", re.M
)
_HEADING = re.compile(r"^(#{1,6})[ \t]+(.*?)[ \t]*#*$", re.M)
_EMPTY_THEAD = re.compile(
    r"^(?P<blank>\|(?:[ \t]*\|)+)[ \t]*\n"
    r"(?P<sep>\|(?:[ \t]*:?-+:?[ \t]*\|)+)[ \t]*\n"
    r"(?P<first>\|.*\|)[ \t]*$",
    re.M,
)
_EMPTY_ROW = re.compile(r"^\|(?:[ \t]*\|)+[ \t]*$", re.M)
_NOTE_LEAD = re.compile(r"^(>+)[ \t]*\*\*Note:\*\*[ \t]?", re.M)
_HTML_TABLE = re.compile(r"<table\b[^>]*>(.*?)</table>", re.S | re.I)
_HTML_TR = re.compile(r"<tr\b[^>]*>(.*?)</tr>", re.S | re.I)
_HTML_CELL = re.compile(r"<t[dh]\b[^>]*>(.*?)</t[dh]>", re.S | re.I)


def _convert_wikilinks(md: str, resolve) -> str:
    def repl(m: re.Match) -> str:
        text = m.group("text").strip()
        href = m.group("href").replace("_", " ")
        anchor = resolve(href)
        return f"[{text}]({anchor})" if anchor else text

    return _WIKILINK_A.sub(repl, md)


def _strip_inline_html(md: str) -> str:
    md = _INLINE_PRE.sub(_inline_pre, md)
    for pat, rep in _INLINE_HTML:
        md = pat.sub(rep, md)
    md = re.sub(r"</?(?:div|center)(?:\s[^>]*)?>", "", md)
    md = re.sub(r"^[ \t]*<!--.*?-->[ \t]*$", "", md, flags=re.M | re.S)
    return md


def _compact_html_tables(md: str) -> str:
    """pandoc pads raw HTML tables with blank lines; GitHub needs them tight."""
    def repl(m: re.Match) -> str:
        t = re.sub(r"\s*\n\s*", "", m.group(0))
        t = re.sub(r"(</t[dh]>)(?=<t[dh])", r"\1", t)
        t = (t.replace("<tr>", "\n<tr>").replace("</table>", "\n</table>"))
        return "\n" + t.strip() + "\n"

    return _HTML_TABLE.sub(repl, md)


def _html_tables_to_pipe(md: str) -> str:
    """Flat ``<table><tr><td>`` (no nesting) -> GFM pipe table."""
    def cell(c: str) -> str:
        return " ".join(c.split()).replace("|", "\\|") or " "

    def repl(m: re.Match) -> str:
        if re.search(r"\b(?:rowspan|colspan)=", m.group(1), re.I):
            return m.group(0)          # keep spanned tables as raw HTML
        rows = []
        for tr in _HTML_TR.finditer(m.group(1)):
            cells = [cell(c.group(1)) for c in _HTML_CELL.finditer(tr.group(1))]
            if cells:
                rows.append(cells)
        if not rows:
            return m.group(0)
        width = max(len(r) for r in rows)
        rows = [r + [" "] * (width - len(r)) for r in rows]
        out = ["| " + " | ".join(rows[0]) + " |",
               "|" + "|".join(["---"] * width) + "|"]
        for r in rows[1:]:
            out.append("| " + " | ".join(r) + " |")
        return "\n\n" + "\n".join(out) + "\n\n"

    if "<table" not in md.lower():
        return md
    return _HTML_TABLE.sub(repl, md)


_CODE_SPAN = re.compile(r"`[^`\n]*`")
_TABLE_ROW = re.compile(r"^\|.*\|[ \t]*$")
_BOLD_CAPTION = re.compile(r"^\*\*[A-Z][^*\n]+\*\*[ \t]*$")
_META_HEADING = {"purpose", "overview", "item", "synopsis", "description",
                 "related", "related commands", "related functions"}


def _escape_pipes_in_table_code(md: str) -> str:
    """`\\|` inside code spans within table rows (GFM needs it even in code)."""
    out = []
    for line in md.split("\n"):
        if line.startswith("|") and "`" in line:
            line = _CODE_SPAN.sub(
                lambda m: m.group(0).replace("|", "\\|"), line)
        out.append(line)
    return "\n".join(out)


def _strip_table_captions(md: str) -> str:
    lines = md.split("\n")
    out: list[str] = []
    for line in lines:
        if _BOLD_CAPTION.match(line):
            prev = next((x for x in reversed(out) if x.strip()), "")
            if prev and _TABLE_ROW.match(prev):
                continue
        out.append(line)
    return "\n".join(out)


def _demote_meta_headings(md: str) -> str:
    def repl(m: re.Match) -> str:
        text = m.group(2).strip()
        low = text.lower().rstrip(":")
        if low in _META_HEADING or low.startswith("author"):
            return f"**{text}**"
        return m.group(0)

    return _HEADING.sub(repl, md)


def _shift_headings(md: str, base_level: int, page_title: str) -> str:
    norm_pt = page_title.strip().lower()
    md = _HEADING.sub(
        lambda m: "" if m.group(2).strip().lower() == norm_pt else m.group(0), md
    )
    levels = [len(m.group(1)) for m in _HEADING.finditer(md)]
    if not levels:
        return md
    shift = base_level - min(levels)

    def repl(m: re.Match) -> str:
        lvl = max(1, min(6, len(m.group(1)) + shift))
        return "#" * lvl + " " + m.group(2).strip()

    return _HEADING.sub(repl, md)


def postprocess(md: str, *, page_title: str, resolve, heading_base: int = 5) -> str:
    md = _convert_wikilinks(md, resolve)
    md = _compact_html_tables(md)
    md = _html_tables_to_pipe(md)
    md = _strip_inline_html(md)
    md = _NOTE_LEAD.sub(lambda m: m.group(1) + " [!NOTE]\n" + m.group(1) + " ", md)
    md = _EMPTY_THEAD.sub(lambda m: m.group("first") + "\n" + m.group("sep"), md)
    md = _EMPTY_ROW.sub("", md)
    md = _HEADER_ONLY_TABLE.sub("", md)
    md = _escape_pipes_in_table_code(md)
    md = _strip_table_captions(md)
    md = _demote_meta_headings(md)
    md = _shift_headings(md, heading_base, page_title)
    md = md.replace("\\#", "#").replace("\\%", "%").replace("\\$", "$")
    # entities that survive from raw-HTML table cells render fine but read badly
    md = (md.replace("&lt;", "<").replace("&gt;", ">")
            .replace("&quot;", '"').replace("&amp;", "&"))
    md = re.sub(r"\s*&#10;\s*", " ", md)   # newline entity in a table cell
    md = re.sub(r"\\?</?nowiki\s*/?\\?>", "", md)   # author's =/| escaping wrappers
    # redact real e-mail addresses left in old "user contributed notes" (keep the
    # handle for attribution, drop the resolvable domain)
    md = re.sub(r"\b([\w.+-]{1,64})@[\w-]+(?:\.[\w-]+)+\b", "\\1@\u2026", md)
    # a trailing line that is just someone's initials (unsigned contributor tag)
    md = re.sub(r"\n{2,}[A-Z]{2,4}[ \t]*$", "", md)
    md = re.sub(r"\n{3,}", "\n\n", md).strip()
    return md
