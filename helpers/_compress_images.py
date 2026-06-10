#!/usr/bin/env python3
"""Lossy recompression for large web JPEG/PNG assets (forum gallery + activities)."""
from __future__ import annotations

import argparse
import tempfile
from dataclasses import dataclass
from pathlib import Path

from _paths import ROOT

try:
    from PIL import Image, ImageOps
except ImportError as exc:
    raise SystemExit("Install: pip install Pillow") from exc

EXTS = {".jpg", ".jpeg", ".png", ".webp"}
SKIP_DIR_NAMES = {"_thumbs", ".git"}

DEFAULT_TARGETS = [
    ROOT / "images" / "photos-gallery",
    ROOT / "images" / "activities",
]


@dataclass
class Profile:
    name: str
    max_edge: int
    jpeg_quality: int
    min_bytes: int
    min_ratio: float


PROFILES = {
    "gallery": Profile("gallery", max_edge=1920, jpeg_quality=82, min_bytes=180_000, min_ratio=0.04),
    "activities": Profile("activities", max_edge=1600, jpeg_quality=82, min_bytes=120_000, min_ratio=0.04),
}


def profile_for(path: Path) -> Profile:
    parts = {p.lower() for p in path.parts}
    if "activities" in parts:
        return PROFILES["activities"]
    return PROFILES["gallery"]


def iter_images(root: Path) -> list[Path]:
    if not root.is_dir():
        return []
    out: list[Path] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(part in SKIP_DIR_NAMES for part in path.parts):
            continue
        if path.suffix.lower() not in EXTS:
            continue
        if path.name.startswith("_"):
            continue
        out.append(path)
    return out


def resize_if_needed(im: Image.Image, max_edge: int) -> Image.Image:
    w, h = im.size
    longest = max(w, h)
    if longest <= max_edge:
        return im
    scale = max_edge / float(longest)
    new_size = (max(1, int(w * scale)), max(1, int(h * scale)))
    return im.resize(new_size, Image.Resampling.LANCZOS)


def save_jpeg(im: Image.Image, dest: Path, quality: int) -> None:
    if im.mode not in ("RGB", "L"):
        im = im.convert("RGB")
    im.save(
        dest,
        "JPEG",
        quality=quality,
        optimize=True,
        progressive=True,
        subsampling="4:2:0",
    )


def save_png(im: Image.Image, dest: Path) -> None:
    if im.mode == "P":
        im = im.convert("RGBA")
    im.save(dest, "PNG", optimize=True, compress_level=9)


def save_webp(im: Image.Image, dest: Path, quality: int) -> None:
    im.save(dest, "WEBP", quality=quality, method=6)


def compress_file(path: Path, *, dry_run: bool = False) -> tuple[str, int, int]:
    """Return (status, before_bytes, after_bytes)."""
    prof = profile_for(path)
    before = path.stat().st_size
    if before < prof.min_bytes:
        return "skip-small", before, before

    suffix = path.suffix.lower()
    try:
        with ImageOps.exif_transpose(Image.open(path)) as im:
            im = resize_if_needed(im, prof.max_edge)
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix, dir=path.parent) as tmp:
                tmp_path = Path(tmp.name)
            try:
                if suffix in (".jpg", ".jpeg"):
                    save_jpeg(im, tmp_path, prof.jpeg_quality)
                elif suffix == ".png":
                    save_png(im, tmp_path)
                elif suffix == ".webp":
                    save_webp(im, tmp_path, prof.jpeg_quality)
                else:
                    return "skip-ext", before, before

                after = tmp_path.stat().st_size
                if after >= before * (1 - prof.min_ratio):
                    tmp_path.unlink(missing_ok=True)
                    return "skip-gain", before, before

                if dry_run:
                    tmp_path.unlink(missing_ok=True)
                    return "would-compress", before, after

                tmp_path.replace(path)
                return "compressed", before, after
            except Exception:
                tmp_path.unlink(missing_ok=True)
                raise
    except Exception as exc:
        print(f"ERROR {path.relative_to(ROOT)}: {exc}")
        return "error", before, before


def format_mb(num: int) -> str:
    return f"{num / 1_048_576:.2f} MB"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "targets",
        nargs="*",
        type=Path,
        help="Folders to process (default: photos-gallery + activities)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Report savings without writing")
    args = parser.parse_args()

    targets = [Path(t) if t.is_absolute() else ROOT / t for t in args.targets] if args.targets else DEFAULT_TARGETS

    stats = {
        "compressed": 0,
        "skip-small": 0,
        "skip-gain": 0,
        "skip-ext": 0,
        "would-compress": 0,
        "error": 0,
    }
    before_total = after_total = 0

    for target in targets:
        if not target.is_dir():
            print(f"Skip missing folder: {target}")
            continue
        print(f"\n== {target.relative_to(ROOT)} ==")
        files = iter_images(target)
        print(f"Found {len(files)} image(s)")
        for path in files:
            status, before, after = compress_file(path, dry_run=args.dry_run)
            stats[status] = stats.get(status, 0) + 1
            before_total += before
            if status in ("compressed", "would-compress"):
                after_total += after
                saved = before - after
                print(
                    f"  {status:14} {saved / 1024:7.0f} KB saved  "
                    f"{path.relative_to(ROOT)}  ({before/1024:.0f} -> {after/1024:.0f} KB)"
                )
            else:
                after_total += after

    saved = before_total - after_total
    print("\nSummary")
    print(f"  compressed: {stats.get('compressed', 0)}")
    print(f"  would-compress: {stats.get('would-compress', 0)}")
    print(f"  skip-small: {stats.get('skip-small', 0)}")
    print(f"  skip-gain: {stats.get('skip-gain', 0)}")
    print(f"  errors: {stats.get('error', 0)}")
    print(f"  before: {format_mb(before_total)}")
    print(f"  after:  {format_mb(after_total)}")
    print(f"  saved:  {format_mb(saved)} ({(saved / before_total * 100) if before_total else 0:.1f}%)")


if __name__ == "__main__":
    main()
