#!/usr/bin/env python3
"""Canonicalise scripts/export_titles.txt in place.

`export_titles.txt` is the authoritative list of page titles to fetch via
Special:Export (`fetch_export.py`) and to reconcile a dump against
(`verify_links.py`). Edit that file directly to add or remove pages, then run
this to normalise casing/whitespace, de-duplicate and sort — so the fetch
reconciliation doesn't trip over a mis-cased title. Idempotent.
"""
from __future__ import annotations

from pathlib import Path

from mwlib import normalize_title, read_title_list

ROOT = Path(__file__).resolve().parent.parent
TITLES = ROOT / "scripts" / "export_titles.txt"


def main() -> None:
    raw = read_title_list(TITLES)
    canon = sorted({normalize_title(t) for t in raw},
                   key=lambda s: (":" in s, s.lower()))
    before = TITLES.read_text(encoding="utf-8")
    after = "\n".join(canon) + "\n"
    TITLES.write_text(after, encoding="utf-8")

    print(f"titles      : {len(canon)}")
    print(f"raw lines   : {len(raw)}  (removed {len(raw) - len(canon)} dupes)")
    print(f"changed     : {'yes' if after != before else 'no'} -> "
          f"{TITLES.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
