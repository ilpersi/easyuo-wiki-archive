"""Shared helpers for working with the EasyUO MediaWiki Special:Export dumps.

Standard library only. Used by build_title_list.py, fetch_export.py and
verify_links.py.
"""
from __future__ import annotations

import html
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Iterator

MW_NS = "http://www.mediawiki.org/xml/export-0.10/"
_NS = {"mw": MW_NS}

# Interwiki prefixes registered on wiki.easyuo.com (from api.php action=query
# meta=siteinfo siprop=interwikimap). Links using these are external, not
# broken internal links.
INTERWIKI_PREFIXES = {"wikipedia", "wiki", "metawikipedia", "mw", "google"}

# Pseudo-namespaces / prefixes that are not article content.
NONCONTENT_PREFIXES = {
    "category", "file", "image", "media", "special", "help",
    "user", "user talk", "talk", "template talk",
}

# Registered namespaces on this wiki (siteinfo/namespaces). Used so that a
# leading "Foo:" is only stripped when Foo really is a namespace -- e.g.
# "Tutorials:Cheffe1" must stay a full ns0 title.
REGISTERED_NAMESPACES = {
    "media", "special", "talk", "user", "user talk", "wiki", "wiki talk",
    "file", "file talk", "mediawiki", "mediawiki talk", "template",
    "template talk", "help", "help talk", "category", "category talk",
}


def normalize_title(title: str) -> str:
    """Apply MediaWiki's title canonicalisation (case = first-letter).

    - underscores <-> spaces, collapse runs of whitespace, strip ends
    - uppercase the first character only
    - leave any "prefix:" intact unless prefix is a registered namespace
    """
    t = title.replace("_", " ").strip()
    t = re.sub(r"\s+", " ", t)
    if not t:
        return t
    if ":" in t:
        prefix, rest = t.split(":", 1)
        if prefix.strip().lower() in REGISTERED_NAMESPACES:
            rest = rest.strip()
            ns = prefix.strip()
            ns = ns[:1].upper() + ns[1:]
            rest = rest[:1].upper() + rest[1:] if rest else rest
            return f"{ns}:{rest}"
    return t[:1].upper() + t[1:]


def decode_text(text: str | None) -> str:
    """HTML-entity decode a <text> body into raw wikitext."""
    if not text:
        return ""
    return html.unescape(text)


def iter_pages(xml_path: str | Path) -> Iterator[tuple[int, str, str]]:
    """Yield (ns, title, decoded_wikitext) for every <page> in an export XML."""
    for _, elem in ET.iterparse(str(xml_path)):
        if elem.tag == f"{{{MW_NS}}}page":
            title = elem.findtext("mw:title", default="", namespaces=_NS)
            ns_txt = elem.findtext("mw:ns", default="0", namespaces=_NS)
            try:
                ns = int(ns_txt)
            except ValueError:
                ns = 0
            text_el = elem.find("mw:revision/mw:text", _NS)
            text = decode_text(text_el.text if text_el is not None else "")
            yield ns, title, text
            elem.clear()


def split_top_level(body: str, sep: str = "|") -> list[str]:
    """Split on `sep` at brace/bracket depth 0, ignoring <nowiki> regions.

    Depth is tracked for ``{{ }}``, ``{{{ }}}`` and ``[[ ]]`` so that a pipe
    inside a nested template call, a parameter default or a wikilink label is
    not treated as an argument separator.
    """
    parts: list[str] = []
    buf: list[str] = []
    i, n = 0, len(body)
    depth = 0
    while i < n:
        two = body[i : i + 2]
        if body.startswith("<nowiki>", i):
            end = body.find("</nowiki>", i)
            end = n if end == -1 else end + len("</nowiki>")
            buf.append(body[i:end])
            i = end
            continue
        if two == "{{" or two == "[[":
            depth += 1
            buf.append(two)
            i += 2
            continue
        if two == "}}" or two == "]]":
            depth = max(0, depth - 1)
            buf.append(two)
            i += 2
            continue
        if depth == 0 and body[i] == sep:
            parts.append("".join(buf))
            buf = []
            i += 1
            continue
        buf.append(body[i])
        i += 1
    parts.append("".join(buf))
    return parts


def find_templates(text: str) -> list[tuple[int, int, str, list[str]]]:
    """Return (start, end, name, args) for each outermost ``{{...}}`` call.

    ``{{{param}}}`` parameter references are skipped. Nested calls are left
    inside the returned arg strings for the caller to expand recursively.
    """
    out: list[tuple[int, int, str, list[str]]] = []
    i, n = 0, len(text)
    while i < n:
        if text.startswith("{{{", i):
            i += 3
            continue
        if text.startswith("{{", i):
            depth = 0
            j = i
            while j < n:
                if text.startswith("<nowiki>", j):
                    end = text.find("</nowiki>", j)
                    j = n if end == -1 else end + len("</nowiki>")
                    continue
                if text.startswith("{{", j):
                    depth += 1
                    j += 2
                    continue
                if text.startswith("}}", j):
                    depth -= 1
                    j += 2
                    if depth == 0:
                        break
                    continue
                j += 1
            if depth != 0:
                break  # unbalanced; give up scanning
            inner = text[i + 2 : j - 2]
            segs = split_top_level(inner)
            name = segs[0].strip()
            args = [s.strip() for s in segs[1:]]
            out.append((i, j, name, args))
            i = j
            continue
        i += 1
    return out


def read_title_list(path: str | Path) -> list[str]:
    """Read a newline-separated title list, skipping blanks and # comments."""
    out: list[str] = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        out.append(line)
    return out
