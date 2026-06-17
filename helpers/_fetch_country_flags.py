#!/usr/bin/env python3
"""Download 4x3 SVG country flags (lipis/flag-icons) for DAAB phone picker."""
from __future__ import annotations

import re
import time
import urllib.error
import urllib.request

from _paths import ROOT

COUNTRY_CODES_JS = ROOT / "js" / "daab-country-codes.js"
OUT_DIR = ROOT / "images" / "flags" / "4x3"
FLAG_URL = "https://raw.githubusercontent.com/lipis/flag-icons/main/flags/4x3/{cc}.svg"


def load_iso_codes() -> list[str]:
    text = COUNTRY_CODES_JS.read_text(encoding="utf-8")
    match = re.search(r"var CODES = \[(.*?)\];", text, re.S)
    if not match:
        raise SystemExit("Could not parse DAAB_COUNTRY_CODES from daab-country-codes.js")
    return [c.strip().strip('"') for c in match.group(1).split(",") if c.strip()]


def fetch_flag(code: str) -> bytes:
    url = FLAG_URL.format(cc=code.lower())
    request = urllib.request.Request(url, headers={"User-Agent": "DAAB-site-build/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    codes = load_iso_codes()
    downloaded = 0
    skipped = 0
    failed: list[str] = []

    for code in codes:
        dest = OUT_DIR / f"{code.lower()}.svg"
        if dest.exists() and dest.stat().st_size > 0:
            skipped += 1
            continue
        try:
            dest.write_bytes(fetch_flag(code))
            downloaded += 1
            time.sleep(0.05)
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
            failed.append(f"{code}: {exc}")

    print(
        f"Flags in {OUT_DIR.relative_to(ROOT)}: "
        f"{downloaded} downloaded, {skipped} skipped, {len(failed)} failed"
    )
    if failed:
        raise SystemExit("Failed codes:\n  " + "\n  ".join(failed))


if __name__ == "__main__":
    main()
