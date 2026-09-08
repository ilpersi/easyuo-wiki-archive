#!/usr/bin/env python3
"""Fetch a full MediaWiki Special:Export dump for wiki.easyuo.com.

Reads scripts/export_titles.txt, POSTs it to Special:Export in batches over
plain HTTP (the site's HTTPS cert is broken), reconciles what came back
against what was requested, then splices one deterministic
Wiki-<UTCSTAMP>.xml that becomes the source of truth. Never modifies an
existing Wiki-*.xml.

Usage:
    python3 scripts/fetch_export.py [--batch-size 40] [--stamp 20260908T120000Z]
"""
from __future__ import annotations

import argparse
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from mwlib import normalize_title, read_title_list

ROOT = Path(__file__).resolve().parent.parent
TITLE_LIST = ROOT / "scripts" / "export_titles.txt"
RAW_DIR = ROOT / "export" / "raw"

EXPORT_URL = "http://wiki.easyuo.com/index.php?title=Special:Export&action=submit"
USER_AGENT = "EasyUO-Docs-Archiver/1.0 (one-off documentation-preservation export)"

SITEINFO_RE = re.compile(r"[ \t]*<siteinfo>.*?</siteinfo>\n", re.S)
PAGE_RE = re.compile(r"[ \t]*<page>\n.*?[ \t]*</page>\n", re.S)
TITLE_IN_PAGE_RE = re.compile(r"<title>(.*?)</title>")
NS_IN_PAGE_RE = re.compile(r"<ns>(\d+)</ns>")


def chunked(seq, n):
    for i in range(0, len(seq), n):
        yield seq[i : i + n]


def post_export(titles: list[str], attempt_delays=(2, 4, 8)) -> str:
    data = urllib.parse.urlencode(
        {"pages": "\n".join(titles), "curonly": "1"}
    ).encode("utf-8")
    last_err: Exception | None = None
    for attempt, delay in enumerate([0, *attempt_delays]):
        if delay:
            time.sleep(delay)
        try:
            req = urllib.request.Request(
                EXPORT_URL, data=data, headers={"User-Agent": USER_AGENT}
            )
            with urllib.request.urlopen(req, timeout=120) as resp:
                if resp.status != 200:
                    raise RuntimeError(f"HTTP {resp.status}")
                body = resp.read().decode("utf-8")
            if "<mediawiki " not in body or not body.rstrip().endswith("</mediawiki>"):
                raise RuntimeError("response not a complete <mediawiki> document")
            return body
        except (urllib.error.URLError, RuntimeError, TimeoutError) as e:  # noqa: PERF203
            last_err = e
            print(f"    attempt {attempt + 1} failed: {e}", file=sys.stderr)
    raise RuntimeError(f"batch failed after retries: {last_err}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch-size", type=int, default=40)
    ap.add_argument(
        "--stamp",
        help="UTC timestamp for the output filename, e.g. 20260908T120000Z. "
        "Required because scripts cannot read the clock in this environment.",
    )
    args = ap.parse_args()

    if not args.stamp:
        ap.error("--stamp is required (e.g. --stamp 20260908T120000Z)")

    titles = read_title_list(TITLE_LIST)
    requested_norm = {normalize_title(t) for t in titles}
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    siteinfo: str | None = None
    pages: dict[str, str] = {}  # normalized title -> verbatim <page> block
    returned_norm: set[str] = set()

    batches = list(chunked(titles, args.batch_size))
    for i, batch in enumerate(batches, 1):
        print(f"[{i}/{len(batches)}] requesting {len(batch)} titles ...")
        body = post_export(batch)
        (RAW_DIR / f"batch_{i:02d}.xml").write_text(body, encoding="utf-8")

        if siteinfo is None:
            m = SITEINFO_RE.search(body)
            if not m:
                raise RuntimeError("no <siteinfo> in first batch response")
            siteinfo = m.group(0)

        for pm in PAGE_RE.finditer(body):
            block = pm.group(0)
            tm = TITLE_IN_PAGE_RE.search(block)
            if not tm:
                continue
            nt = normalize_title(tm.group(1))
            returned_norm.add(nt)
            pages.setdefault(nt, block)

        if i < len(batches):
            time.sleep(2)

    missing = sorted(requested_norm - returned_norm)
    extra = sorted(returned_norm - requested_norm)

    def ns_of(block: str) -> int:
        m = NS_IN_PAGE_RE.search(block)
        return int(m.group(1)) if m else 0

    ordered = sorted(pages.items(), key=lambda kv: (ns_of(kv[1]), kv[0].lower()))

    header = (
        '<mediawiki xmlns="http://www.mediawiki.org/xml/export-0.10/" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        'xsi:schemaLocation="http://www.mediawiki.org/xml/export-0.10/ '
        'http://www.mediawiki.org/xml/export-0.10.xsd" version="0.10" '
        'xml:lang="en">\n'
    )
    out_path = ROOT / f"Wiki-{args.stamp}.xml"
    with out_path.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(header)
        fh.write(siteinfo or "")
        for _, block in ordered:
            fh.write(block)
        fh.write("</mediawiki>\n")

    print("\n=== fetch summary ===")
    print(f"batches           : {len(batches)}")
    print(f"titles requested  : {len(requested_norm)}")
    print(f"pages fetched      : {len(pages)}")
    print(f"missing (dropped)  : {len(missing)}")
    for t in missing:
        print(f"    MISSING {t}")
    print(f"unexpected extra   : {len(extra)}")
    for t in extra:
        print(f"    EXTRA {t}")
    size = out_path.stat().st_size
    print(f"output             : {out_path.name} ({size:,} bytes)")

    return 1 if (missing or extra) else 0


if __name__ == "__main__":
    sys.exit(main())
