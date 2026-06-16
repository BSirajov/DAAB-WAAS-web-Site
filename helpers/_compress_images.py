#!/usr/bin/env python3
"""Lossy recompression for large web JPEG/PNG assets across deploy image folders."""
from __future__ import annotations

import argparse
import json
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
SKIP_REF_DIRS = {"Deployment", ".git", "__pycache__", "documents"}
REF_EXTS = {".html", ".js", ".json", ".py", ".css", ".xml", ".md"}

DEFAULT_TARGETS = [
    ROOT / "images" / "photos-gallery",
    ROOT / "images" / "activities",
    ROOT / "images" / "scientists-photos",
    ROOT / "images" / "board-members-photos",
    ROOT / "images" / "inventions",
    ROOT / "images" / "work_done_2024_2026",
    ROOT / "images" / "videos-gallery",
]


@dataclass
class Profile:
    name: str
    max_edge: int
    jpeg_quality: int
    min_bytes: int
    min_ratio: float


PROFILES = {
    "gallery": Profile("gallery", max_edge=1920, jpeg_quality=78, min_bytes=180_000, min_ratio=0.04),
    "activities": Profile("activities", max_edge=1600, jpeg_quality=82, min_bytes=120_000, min_ratio=0.04),
    "portraits": Profile("portraits", max_edge=960, jpeg_quality=85, min_bytes=80_000, min_ratio=0.04),
}


def profile_for(path: Path) -> Profile:
    parts = {p.lower() for p in path.parts}
    if "activities" in parts:
        return PROFILES["activities"]
    if "board-members-photos" in parts or "scientists-photos" in parts:
        return PROFILES["portraits"]
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


def has_meaningful_alpha(im: Image.Image) -> bool:
    if im.mode not in ("RGBA", "LA", "PA"):
        return False
    if im.mode == "RGBA":
        lo, hi = im.getchannel("A").getextrema()
        return lo < 255
    return True


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


def jpeg_qualities(prof: Profile) -> list[int]:
    primary = prof.jpeg_quality
    out = [primary]
    if primary > 75:
        out.append(primary - 4)
    return out


def write_best_jpeg(im: Image.Image, tmp_path: Path, prof: Profile, before: int) -> int:
    best_after = before
    best_quality = prof.jpeg_quality
    for quality in jpeg_qualities(prof):
        save_jpeg(im, tmp_path, quality)
        after = tmp_path.stat().st_size
        if after < best_after:
            best_after = after
            best_quality = quality
    if best_quality != prof.jpeg_quality:
        save_jpeg(im, tmp_path, best_quality)
    return best_after


def sync_converted_refs(conversions: list[tuple[str, str]]) -> int:
    if not conversions:
        return 0
    unique = list(dict.fromkeys(conversions))
    files_changed = 0
    basename_map = {Path(old).name: Path(new).name for old, new in unique if Path(old).name != Path(new).name}

    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in REF_EXTS:
            continue
        if any(part in SKIP_REF_DIRS for part in path.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        new_text = text
        for old, new in unique:
            new_text = new_text.replace(old, new)
        if basename_map and path.name == "scientists-profiles.json":
            data = json.loads(new_text)
            touched = False
            for card in data.get("profiles", []):
                photo = card.get("photo", "")
                if photo in basename_map:
                    card["photo"] = basename_map[photo]
                    touched = True
            if touched:
                new_text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
        if new_text != text:
            path.write_text(new_text, encoding="utf-8", newline="\n")
            files_changed += 1
    return files_changed


def compress_file(
    path: Path,
    *,
    dry_run: bool = False,
    conversions: list[tuple[str, str]] | None = None,
) -> tuple[str, int, int, Path | None]:
    """Return (status, before_bytes, after_bytes, final_path)."""
    prof = profile_for(path)
    before = path.stat().st_size
    if before < prof.min_bytes:
        return "skip-small", before, before, path

    suffix = path.suffix.lower()
    try:
        with ImageOps.exif_transpose(Image.open(path)) as im:
            im = resize_if_needed(im, prof.max_edge)
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix, dir=path.parent) as tmp:
                tmp_path = Path(tmp.name)
            try:
                final_path = path
                if suffix in (".jpg", ".jpeg"):
                    after = write_best_jpeg(im, tmp_path, prof, before)
                elif suffix == ".png":
                    if has_meaningful_alpha(im):
                        save_png(im, tmp_path)
                        after = tmp_path.stat().st_size
                    else:
                        jpg_path = path.with_suffix(".jpg")
                        with tempfile.NamedTemporaryFile(
                            delete=False, suffix=".jpg", dir=path.parent
                        ) as jpg_tmp:
                            jpg_tmp_path = Path(jpg_tmp.name)
                        try:
                            after = write_best_jpeg(im, jpg_tmp_path, prof, before)
                            tmp_path.unlink(missing_ok=True)
                            tmp_path = jpg_tmp_path
                            final_path = jpg_path
                        except Exception:
                            jpg_tmp_path.unlink(missing_ok=True)
                            raise
                elif suffix == ".webp":
                    save_webp(im, tmp_path, prof.jpeg_quality)
                    after = tmp_path.stat().st_size
                else:
                    return "skip-ext", before, before, path

                if after >= before * (1 - prof.min_ratio):
                    tmp_path.unlink(missing_ok=True)
                    return "skip-gain", before, before, path

                if dry_run:
                    tmp_path.unlink(missing_ok=True)
                    if final_path != path and conversions is not None:
                        old_rel = path.relative_to(ROOT).as_posix()
                        new_rel = final_path.relative_to(ROOT).as_posix()
                        conversions.append((old_rel, new_rel))
                    return "would-compress", before, after, final_path

                if final_path != path:
                    tmp_path.replace(final_path)
                    path.unlink(missing_ok=True)
                    if conversions is not None:
                        old_rel = path.relative_to(ROOT).as_posix()
                        new_rel = final_path.relative_to(ROOT).as_posix()
                        conversions.append((old_rel, new_rel))
                    return "converted-png", before, after, final_path

                tmp_path.replace(path)
                return "compressed", before, after, path
            except Exception:
                tmp_path.unlink(missing_ok=True)
                raise
    except Exception as exc:
        print(f"ERROR {path.relative_to(ROOT)}: {exc}")
        return "error", before, before, path


def format_mb(num: int) -> str:
    return f"{num / 1_048_576:.2f} MB"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "targets",
        nargs="*",
        type=Path,
        help="Folders to process (default: all deploy image folders)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Report savings without writing")
    parser.add_argument(
        "--no-sync-refs",
        action="store_true",
        help="Do not rewrite .png paths after PNG→JPEG conversion",
    )
    args = parser.parse_args()

    targets = [Path(t) if t.is_absolute() else ROOT / t for t in args.targets] if args.targets else DEFAULT_TARGETS

    stats: dict[str, int] = {}
    before_total = after_total = 0
    conversions: list[tuple[str, str]] = []

    for target in targets:
        if not target.is_dir():
            print(f"Skip missing folder: {target}")
            continue
        print(f"\n== {target.relative_to(ROOT)} ==")
        files = iter_images(target)
        print(f"Found {len(files)} image(s)")
        for path in files:
            status, before, after, _final = compress_file(
                path,
                dry_run=args.dry_run,
                conversions=conversions if not args.no_sync_refs else None,
            )
            stats[status] = stats.get(status, 0) + 1
            before_total += before
            if status in ("compressed", "would-compress", "converted-png"):
                after_total += after
                saved = before - after
                print(
                    f"  {status:14} {saved / 1024:7.0f} KB saved  "
                    f"{path.relative_to(ROOT)}  ({before/1024:.0f} -> {after/1024:.0f} KB)"
                )
            else:
                after_total += after

    if conversions and not args.dry_run and not args.no_sync_refs:
        unique = list(dict.fromkeys(conversions))
        changed = sync_converted_refs(unique)
        print(f"\nReference sync: {len(unique)} path(s), {changed} file(s) updated")

    saved = before_total - after_total
    print("\nSummary")
    for key in (
        "compressed",
        "converted-png",
        "would-compress",
        "skip-small",
        "skip-gain",
        "error",
    ):
        if stats.get(key):
            print(f"  {key}: {stats[key]}")
    print(f"  before: {format_mb(before_total)}")
    print(f"  after:  {format_mb(after_total)}")
    print(f"  saved:  {format_mb(saved)} ({(saved / before_total * 100) if before_total else 0:.1f}%)")


if __name__ == "__main__":
    main()
