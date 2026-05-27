#!/usr/bin/env python3
"""Match Kofe Fasiləsi gallery to local forum photos; copy to CoffeeBreak/."""
from __future__ import annotations

import json
import shutil
from io import BytesIO
from pathlib import Path

from _paths import ROOT

try:
    from PIL import Image, ImageOps
except ImportError:
    raise SystemExit("Install: pip install Pillow")

LOCAL_FOTOLAR = Path(
    r"C:\Users\BSira\Documents\Azərbaycanlı Alimlərin Istanbul görüşü, 8-10 Dekabr 2022"
    r"\1-ci Bakı forumu, 8-12 Sentyabr 2024\Forumdan foto və videolar\Fotolar"
)
OUT_DIR = ROOT / "images" / "photos-gallery" / "CoffeeBreak"
MANIFEST = OUT_DIR / "_match-manifest.json"
PAGE_CACHE = ROOT / "helpers" / "_cache_coffee_break_gallery_urls.txt"
THUMB_DIR = ROOT / "helpers" / "_cache_coffee_break_gallery_thumbs"
LOCAL_HASH_CACHE = ROOT / "helpers" / "_cache_alley_local_hashes.json"
DEST_PREFIX = "coffee-break"
MAX_DIST = 14
RETRY_MAX_DIST = 19


def load_gallery_urls() -> list[str]:
    if not PAGE_CACHE.is_file():
        raise FileNotFoundError("Run _fetch_coffee_break_gallery_playwright.py first")
    return [ln.strip() for ln in PAGE_CACHE.read_text(encoding="utf-8").splitlines() if ln.strip()]


def open_normalized(path: Path) -> Image.Image:
    return ImageOps.exif_transpose(Image.open(path)).convert("RGB")


def dhash_bits(im: Image.Image, size: int = 8) -> int:
    gray = im.convert("L").resize((size + 1, size), Image.Resampling.LANCZOS)
    pixels = list(gray.getdata())
    bits = 0
    idx = 0
    for row in range(size):
        row_start = row * (size + 1)
        for col in range(size):
            if pixels[row_start + col] > pixels[row_start + col + 1]:
                bits |= 1 << idx
            idx += 1
    return bits


def hash_file(path: Path) -> int:
    im = Image.open(path)
    im = ImageOps.exif_transpose(im).convert("RGB")
    im.thumbnail((512, 512), Image.Resampling.LANCZOS)
    return dhash_bits(im)


def hamming(a: int, b: int) -> int:
    return (a ^ b).bit_count()


def build_local_index() -> list[tuple[Path, int]]:
    exts = {".jpg", ".jpeg", ".png", ".webp"}
    cached: dict[str, int] = {}
    if LOCAL_HASH_CACHE.is_file():
        try:
            raw = json.loads(LOCAL_HASH_CACHE.read_text(encoding="utf-8"))
            cached = {k: int(v) for k, v in raw.items()}
        except (json.JSONDecodeError, ValueError):
            cached = {}
    items: list[tuple[Path, int]] = []
    updated: dict[str, int] = {}
    for path in sorted(LOCAL_FOTOLAR.iterdir()):
        if path.suffix.lower() not in exts or not path.is_file():
            continue
        try:
            cache_key = f"{path.name}:{path.stat().st_mtime}"
            h = cached.get(cache_key) or hash_file(path)
            items.append((path, h))
            updated[cache_key] = h
        except Exception as exc:
            print("skip local", path.name, exc)
    LOCAL_HASH_CACHE.write_text(json.dumps(updated, ensure_ascii=False), encoding="utf-8")
    return items


def best_match(
    web_hash: int,
    local_index: list[tuple[Path, int]],
    used: set[Path],
) -> tuple[Path | None, int]:
    best_path: Path | None = None
    best_dist = 999
    for path, lh in local_index:
        if path in used:
            continue
        dist = hamming(web_hash, lh)
        if dist < best_dist:
            best_dist = dist
            best_path = path
    return best_path, best_dist


def main() -> None:
    urls = load_gallery_urls()
    print(f"Gallery URLs: {len(urls)}")
    local_index = build_local_index()
    print(f"Local index: {len(local_index)} files")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for old in OUT_DIR.iterdir():
        if not old.name.startswith("_"):
            old.unlink()

    used: set[Path] = set()
    manifest: list[dict] = []

    for i, url in enumerate(urls, start=1):
        print(f"Match {i}/{len(urls)}…", end=" ", flush=True)
        thumb = THUMB_DIR / f"{i:02d}.jpg"
        if not thumb.is_file() or thumb.stat().st_size < 1000:
            print("SKIP")
            manifest.append({"index": i, "url": url, "skipped": True})
            continue
        wh = hash_file(thumb)
        match_path, dist = best_match(wh, local_index, used)
        if match_path is None or dist > MAX_DIST:
            if not (match_path and dist <= RETRY_MAX_DIST):
                print(f"NO MATCH (d={dist})")
                manifest.append({"index": i, "url": url, "matched": False, "distance": dist})
                continue
        used.add(match_path)
        dest_name = f"{DEST_PREFIX}-{i:02d}{match_path.suffix.lower()}"
        shutil.copy2(match_path, OUT_DIR / dest_name)
        note = " retry" if dist > MAX_DIST else ""
        print(f"OK {match_path.name} (d={dist}){note}")
        manifest.append(
            {
                "index": i,
                "url": url,
                "matched": True,
                "distance": int(dist),
                "source": match_path.name,
                "dest": dest_name,
                "source_bytes": match_path.stat().st_size,
            }
        )

    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    matched = sum(1 for m in manifest if m.get("matched"))
    print(f"\nDone: {matched}/{len(urls)} -> {OUT_DIR}")


if __name__ == "__main__":
    main()
