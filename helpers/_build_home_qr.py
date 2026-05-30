#!/usr/bin/env python3
"""Generate locale-specific QR PNGs for the DAAB home page."""
from __future__ import annotations

import argparse
from pathlib import Path

from _paths import ROOT

DEFAULT_BASE = "https://daab-waas.com"
OUT_AZ = ROOT / "images" / "qr" / "home-az.png"
OUT_EN = ROOT / "images" / "qr" / "home-en.png"


def home_url(base: str, lang: str) -> str:
    locale = "az" if lang == "az" else "en"
    return f"{base.rstrip('/')}/{locale}/"


def write_qr_png(url: str, path: Path, *, box_size: int = 6, border: int = 2) -> None:
    try:
        import qrcode
    except ImportError as exc:
        raise SystemExit(
            "Missing dependency: pip install qrcode[pil]\n"
            "Required once to generate PNG files under images/qr/."
        ) from exc

    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    img = qrcode.make(
        url,
        box_size=box_size,
        border=border,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
    )
    img.save(path, format="PNG", optimize=True)


def build(*, base_url: str = DEFAULT_BASE) -> tuple[str, str]:
    az_url = home_url(base_url, "az")
    en_url = home_url(base_url, "en")
    write_qr_png(az_url, OUT_AZ)
    write_qr_png(en_url, OUT_EN)
    return (
        OUT_AZ.relative_to(ROOT).as_posix(),
        OUT_EN.relative_to(ROOT).as_posix(),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Build home page QR PNGs")
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE,
        help=f"Site origin for encoded URLs (default: {DEFAULT_BASE})",
    )
    args = parser.parse_args()
    az_rel, en_rel = build(base_url=args.base_url)
    print(f"Wrote {az_rel} -> {home_url(args.base_url, 'az')}")
    print(f"Wrote {en_rel} -> {home_url(args.base_url, 'en')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
