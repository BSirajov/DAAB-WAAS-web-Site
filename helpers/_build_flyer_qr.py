#!/usr/bin/env python3
"""Generate static QR PNGs for membership and sponsorship flyers."""
from __future__ import annotations

import argparse
from pathlib import Path

from _build_home_qr import DEFAULT_BASE, write_qr_png
from _paths import ROOT

FLYER_TARGETS = {
    "flyer-membership-az.png": "/az/application.html",
    "flyer-membership-en.png": "/en/application.html",
    "flyer-sponsorship-az.png": "/az/sponsorship_partnership.html#contact",
    "flyer-sponsorship-en.png": "/en/sponsorship_partnership.html#contact",
}

OUT_DIR = ROOT / "images" / "qr"


def build(*, base_url: str = DEFAULT_BASE) -> list[str]:
    base = base_url.rstrip("/")
    written: list[str] = []
    for filename, path in FLYER_TARGETS.items():
        url = f"{base}{path}"
        dest = OUT_DIR / filename
        write_qr_png(url, dest)
        written.append(dest.relative_to(ROOT).as_posix())
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default=DEFAULT_BASE)
    args = parser.parse_args()
    for rel in build(base_url=args.base_url):
        print(f"Wrote {rel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
