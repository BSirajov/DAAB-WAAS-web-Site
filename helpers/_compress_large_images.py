#!/usr/bin/env python3
"""Aggressively recompress deploy images larger than a byte threshold."""
from __future__ import annotations

import argparse
import tempfile
from pathlib import Path

from PIL import Image, ImageOps

from _compress_images import has_meaningful_alpha, save_jpeg, save_png, sync_converted_refs
from _paths import ROOT

SKIP_PARTS = {"_thumbs", "Deployment", "documents"}
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp"}
PORTRAIT_DIRS = {"scientists-photos", "board-members-photos", "activities"}


def is_portrait_path(path: Path) -> bool:
    return path.parent.name in PORTRAIT_DIRS


def flatten_to_rgb(im: Image.Image) -> Image.Image:
    if im.mode in ("RGB", "L"):
        return im.convert("RGB")
    if im.mode in ("RGBA", "LA"):
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1])
        return bg
    return im.convert("RGB")


def iter_large_images(min_bytes: int) -> list[Path]:
    out: list[Path] = []
    for path in sorted(ROOT.joinpath("images").rglob("*")):
        if not path.is_file():
            continue
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        if path.suffix.lower() not in IMAGE_EXTS:
            continue
        if path.stat().st_size > min_bytes:
            out.append(path)
    return out


def compress_large(path: Path, *, max_edge: int, quality: int) -> tuple[bool, int, int, Path]:
    before = path.stat().st_size
    suffix = path.suffix.lower()
    with ImageOps.exif_transpose(Image.open(path)) as im:
        w, h = im.size
        longest = max(w, h)
        if longest > max_edge:
            scale = max_edge / float(longest)
            im = im.resize(
                (max(1, int(w * scale)), max(1, int(h * scale))),
                Image.Resampling.LANCZOS,
            )
        final_path = path
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg", dir=path.parent) as tmp:
            tmp_path = Path(tmp.name)
        force_jpeg = suffix == ".png" and is_portrait_path(path)
        if suffix == ".png" and has_meaningful_alpha(im) and not force_jpeg:
            save_png(im, tmp_path.with_suffix(".png"))
            tmp_path = tmp_path.with_suffix(".png")
            final_path = path
        else:
            if suffix == ".png":
                final_path = path.with_suffix(".jpg")
            save_jpeg(flatten_to_rgb(im) if force_jpeg else im, tmp_path, quality)
        after = tmp_path.stat().st_size
        if after >= before:
            tmp_path.unlink(missing_ok=True)
            return False, before, before, path
        if final_path != path:
            tmp_path.replace(final_path)
            path.unlink(missing_ok=True)
        else:
            tmp_path.replace(path)
        return True, before, after, final_path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--min-kb", type=int, default=400, help="Only files larger than this")
    parser.add_argument("--max-edge", type=int, default=1600)
    parser.add_argument("--quality", type=int, default=72)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    min_bytes = args.min_kb * 1024
    files = iter_large_images(min_bytes)
    conversions: list[tuple[str, str]] = []
    saved = 0
    done = 0

    for path in files:
        if args.dry_run:
            print(f"would process {path.relative_to(ROOT)} ({path.stat().st_size // 1024} KB)")
            continue
        try:
            ok, before, after, final = compress_large(
                path, max_edge=args.max_edge, quality=args.quality
            )
        except OSError as exc:
            print(f"ERROR {path.relative_to(ROOT)}: {exc}")
            continue
        if not ok:
            continue
        done += 1
        saved += before - after
        if final != path:
            conversions.append(
                (path.relative_to(ROOT).as_posix(), final.relative_to(ROOT).as_posix())
            )
        print(
            f"  {path.relative_to(ROOT)}: {before // 1024} KB -> {after // 1024} KB"
        )

    if conversions:
        changed = sync_converted_refs(list(dict.fromkeys(conversions)))
        print(f"Reference sync: {changed} file(s) updated")

    remaining = len(iter_large_images(min_bytes))
    print(f"Compressed {done} file(s); saved {saved / 1024 / 1024:.2f} MB; still >{args.min_kb}KB: {remaining}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
