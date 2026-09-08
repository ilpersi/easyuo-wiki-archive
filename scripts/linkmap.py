"""Resolve wiki page titles / ``Page#Section`` links to in-document anchors."""
from __future__ import annotations

import re

from mwlib import iter_pages, normalize_title

_SLUG_STRIP = re.compile(r"[^a-z0-9\s-]")
_SLUG_WS = re.compile(r"[\s_]+")


def slug(title: str) -> str:
    s = normalize_title(title).lower()
    s = s.replace("&", " and ")
    s = _SLUG_STRIP.sub("", s)
    s = _SLUG_WS.sub("-", s).strip("-")
    return s


# Per-group entry-anchor prefix. Prefixed so an entry anchor can never collide
# with one of GitHub's auto-generated heading slugs (which are un-prefixed).
GROUP_PREFIX = {
    "Getting Started": "guide-",
    "Language Reference": "ref-",
    "Command Reference": "cmd-",
    "System Variable Reference": "var-",
    "Appendices": "apx-",
}


def build_anchor_map(groups) -> dict[str, str]:
    """normalized page title -> in-document anchor id (with its group prefix)."""
    out: dict[str, str] = {}
    for g in groups:
        prefix = GROUP_PREFIX.get(g.title, "doc-")
        for s in g.subsections:
            for title in s.pages:
                out[normalize_title(title)] = prefix + slug(title)
    return out


# ``Page#Section`` -> (anchor id, heading text to anchor in that page).
# Only the ~15 section targets that wiki links actually point at.
SECTION_ANCHORS: dict[tuple[str, str], tuple[str, str]] = {
    ("Variables", "Basics"): ("variables--basics", "Basics"),
    ("Variables", "Standard_Variables"): ("variables--standard", "Standard Variables"),
    ("Variables", "Namespace_Variables_and_Scope"): ("variables--namespace", "Namespace Variables and Scope"),
    ("Variables", "Persistent_Variables"): ("variables--persistent", "Persistent Variables"),
    ("Variables", "System_Variables"): ("variables--system", "System Variables"),
    ("Variables", "Variable_Scope"): ("variables--scope", "Variable Scope"),
    ("Expressions", "Expressions"): ("expressions--expressions", "Expressions"),
    ("Expressions", "Statements"): ("expressions--statements", "Statements"),
    ("Operators", "Arithmetic_Operators"): ("operators--arithmetic", "Arithmetic Operators"),
    ("Operators", "Comparison_Operators"): ("operators--comparison", "Comparison Operators"),
    ("Operators", "Logical_Operators"): ("operators--logical", "Logical Operators"),
    ("Operators", "Concatenation_Operators"): ("operators--concatenation", "Concatenation Operators"),
    ("Operators", "Precedence_and_associativity"): ("operators--precedence", "Precedence and associativity"),
    ("Operators", "Associativity_for_Dummies"): ("operators--associativity", "Associativity for Dummies"),
    ("Control Structures", "Goto.27s"): ("control-structures--gotos", "Goto's"),
    ("Control Structures", "Subs"): ("control-structures--subs", "Subs"),
}

# ``Documentation#X`` links point at command/variable sections.
DOC_SECTION_ALIASES = {
    "Namespace": "sec-namespace",
    "Namespace local": "cmd-namespace-local",   # the individual command entry
    "Namespace Commands": "sec-namespace",
    "System_Variable_Reference": "sec-system-variable-reference",
    "Command_Reference": "sec-command-reference",
}

# Bare / ambiguous titles -> the page actually meant.
TITLE_ALIASES = {
    "Str": "Str (command)",
    "Exevent DropC": "Exevent Dropc",
    "Exevent dropc": "Exevent Dropc",
}

INTERWIKI_URL = {
    "wikipedia": "http://en.wikipedia.org/wiki/{}",
    "wiki": "http://en.wikipedia.org/wiki/{}",
}


class LinkResolver:
    def __init__(self, xml_path: str, anchor_map: dict[str, str]):
        self.anchors = anchor_map
        self.redirects: dict[str, str] = {}
        for ns, title, body in iter_pages(xml_path):
            if ns == 0 and body.strip().upper().startswith("#REDIRECT"):
                m = re.search(r"\[\[\s*([^\]|#]+)", body)
                if m:
                    self.redirects[normalize_title(title)] = normalize_title(m.group(1))
        self.unresolved: set[str] = set()

    def resolve(self, target: str) -> str | None:
        """Return ``#anchor`` / URL for a ``[[target]]`` (may include #section)."""
        target = target.strip().lstrip(":").strip()
        if not target:
            return None
        page, _, section = target.partition("#")
        page = page.strip()
        section = section.strip()

        if page and ":" in page:
            prefix = page.split(":", 1)[0].lower()
            if prefix in INTERWIKI_URL:
                rest = page.split(":", 1)[1].strip().replace(" ", "_")
                return INTERWIKI_URL[prefix].format(rest)
            if prefix in ("special",):
                return None

        npage = normalize_title(page) if page else ""

        if npage == "Documentation":
            if section:
                key = section.replace(" ", "_")
                if key in DOC_SECTION_ALIASES:
                    return "#" + DOC_SECTION_ALIASES[key]
                if section in DOC_SECTION_ALIASES:
                    return "#" + DOC_SECTION_ALIASES[section]
            return "#easyuo-documentation"

        if section:
            sa = SECTION_ANCHORS.get((npage, section)) or \
                SECTION_ANCHORS.get((npage, section.replace(" ", "_")))
            if sa:
                return "#" + sa[0]
            # unknown section -> fall through to the page anchor

        npage = TITLE_ALIASES.get(npage, npage)
        npage = self.redirects.get(npage, npage)
        npage = TITLE_ALIASES.get(npage, npage)

        if not npage:
            return None
        anchor = self.anchors.get(npage)
        if anchor:
            return "#" + anchor
        self.unresolved.add(npage)
        return None
