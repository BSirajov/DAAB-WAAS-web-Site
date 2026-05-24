#!/usr/bin/env python3
"""Generate locale-specific QR PNGs for scientist profile deep links."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from _paths import ROOT
    from scientists_profiles_core import PROFILES_JSON, load_profiles, slug_from_photo
except ImportError:
    from helpers._paths import ROOT  # type: ignore
    from helpers.scientists_profiles_core import (  # type: ignore
        PROFILES_JSON,
        load_profiles,
        slug_from_photo,
    )

DEFAULT_BASE = "https://daab-waas.com"
OUT_DIR = ROOT / "images" / "qr"


def profile_url(base: str, lang: str, slug: str) -> str:
    locale = "az" if lang == "az" else "en"
    base = base.rstrip("/")
    return f"{base}/{locale}/scientists/profiles.html#{slug}"


def write_qr_png(url: str, path: Path, *, box_size: int = 8, border: int = 2) -> None:
    try:
        import qrcode
    except ImportError as exc:
        raise SystemExit(
            "Missing dependency: pip install qrcode[pil]\n"
            "Required once to generate PNG files under images/qr/."
        ) from exc

    path.parent.mkdir(parents=True, exist_ok=True)
    img = qrcode.make(
        url,
        box_size=box_size,
        border=border,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
    )
    img.save(path, format="PNG", optimize=True)


def build(*, base_url: str = DEFAULT_BASE, langs: tuple[str, ...] = ("az", "en")) -> list[str]:
    if not PROFILES_JSON.is_file():
        raise SystemExit(f"Missing {PROFILES_JSON.relative_to(ROOT)}")

    profiles = load_profiles()
    written: list[str] = []
    seen: set[str] = set()

    for profile in profiles:
        slug = slug_from_photo(profile.get("photo", ""))
        if not slug:
            continue
        if slug in seen:
            print(f"Warning: duplicate slug {slug!r}", file=sys.stderr)
        seen.add(slug)
        for lang in langs:
            url = profile_url(base_url, lang, slug)
            rel = Path("images") / "qr" / lang / f"{slug}.png"
            out = ROOT / rel
            write_qr_png(url, out)
            written.append(rel.as_posix())

    manifest = {
        "baseUrl": base_url,
        "count": len(profiles),
        "files": len(written),
        "langs": list(langs),
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description="Build scientist profile QR PNGs")
    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE,
        help=f"Site origin for encoded URLs (default: {DEFAULT_BASE})",
    )
    parser.add_argument("--az-only", action="store_true")
    parser.add_argument("--en-only", action="store_true")
    args = parser.parse_args()

    langs: tuple[str, ...]
    if args.az_only and not args.en_only:
        langs = ("az",)
    elif args.en_only and not args.az_only:
        langs = ("en",)
    else:
        langs = ("az", "en")

    written = build(base_url=args.base_url, langs=langs)
    print(f"Wrote {len(written)} QR PNG(s) under images/qr/ (base: {args.base_url})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
