#!/usr/bin/env python3
"""Compare embedded page-hero-subtitle text with i18n/page-subtitles.json."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from _paths import ROOT

SUBTITLE_RE = re.compile(r'id="page-hero-subtitle"[^>]*>([^<]+)<')


def audit() -> list[tuple[str, str, str, str, str]]:
    subs = json.loads((ROOT / "i18n/page-subtitles.json").read_text(encoding="utf-8"))["pages"]
    routes = json.loads((ROOT / "i18n/routes.json").read_text(encoding="utf-8"))
    route_ids = {page["id"] for page in routes["pages"]}
    mismatches: list[tuple[str, str, str, str, str]] = []

    for lang in ("az", "en"):
        for page in routes["pages"]:
            pid = page["id"]
            if pid not in subs or lang not in subs[pid]:
                continue
            rel = page[lang]
            path = ROOT / rel
            if not path.is_file():
                continue
            html = path.read_text(encoding="utf-8")
            match = SUBTITLE_RE.search(html)
            if not match:
                continue
            embedded = match.group(1).strip()
            expected = subs[pid][lang].strip()
            if embedded != expected:
                mismatches.append((pid, lang, rel, expected, embedded))

    orphans = sorted(k for k in subs if k not in route_ids)
    if orphans:
        mismatches.append(("__orphan_keys__", "", "", ", ".join(orphans), ""))

    return mismatches


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fail-on-findings",
        action="store_true",
        help="Exit 1 when any mismatches remain",
    )
    args = parser.parse_args()

    mismatches = audit()
    if not mismatches:
        print("Page subtitle audit OK — embedded subtitles match i18n/page-subtitles.json.")
        return 0

    print(f"Page subtitle audit — {len(mismatches)} finding(s):\n")
    for pid, lang, rel, expected, embedded in mismatches:
        if pid == "__orphan_keys__":
            print(f"  Orphan keys in page-subtitles.json: {expected}")
            continue
        print(f"  {pid} ({lang}) -> {rel}")
        print(f"    JSON: {expected}")
        print(f"    HTML: {embedded}")
    return 1 if args.fail_on_findings else 0


if __name__ == "__main__":
    sys.exit(main())
