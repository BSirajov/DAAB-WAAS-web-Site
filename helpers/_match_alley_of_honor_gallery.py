#!/usr/bin/env python3
"""
Match Google Sites Fəxri Xiyaban gallery images to local forum photos by perceptual hash,
then copy originals into images/photos-gallery/AlleyOfHonor/.
"""
from __future__ import annotations

import json
import shutil
import urllib.request
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
OUT_DIR = ROOT / "images" / "photos-gallery" / "AlleyOfHonor"
MANIFEST = OUT_DIR / "_match-manifest.json"
PAGE_CACHE = ROOT / "helpers" / "_cache_alley_gallery_urls.txt"
THUMB_DIR = ROOT / "helpers" / "_cache_alley_gallery_thumbs"
MAX_DIST = 14  # dHash hamming distance (64 bits)


def load_gallery_urls() -> list[str]:
    cache = PAGE_CACHE
    if cache.is_file():
        urls = [ln.strip() for ln in cache.read_text(encoding="utf-8").splitlines() if ln.strip()]
        if urls:
            return urls
    raise FileNotFoundError(f"Missing {cache}")


def open_normalized(path: Path | None = None, data: bytes | None = None) -> Image.Image:
    if data is not None:
        im = Image.open(BytesIO(data))
    else:
        im = Image.open(path)
    return ImageOps.exif_transpose(im).convert("RGB")


def dhash_bits(im: Image.Image, size: int = 8) -> int:
    """Difference hash -> 64-bit int."""
    gray = im.convert("L").resize((size + 1, size), Image.Resampling.LANCZOS)
    pixels = list(gray.getdata())
    bits = 0
    idx = 0
    for row in range(size):
        row_start = row * (size + 1)
        for col in range(size):
            left = pixels[row_start + col]
            right = pixels[row_start + col + 1]
            if left > right:
                bits |= 1 << idx
            idx += 1
    return bits


def hash_image(im: Image.Image) -> int:
    im = im.copy()
    im.thumbnail((512, 512), Image.Resampling.LANCZOS)
    return dhash_bits(im)


def hash_file(path: Path) -> int:
    with open_normalized(path) as im:
        return hash_image(im)


def hash_thumb(index: int, url: str) -> int:
    """Prefer Playwright-cached thumbnails (Google blocks urllib)."""
    cached = THUMB_DIR / f"{index:02d}.jpg"
    if cached.is_file() and cached.stat().st_size > 1000:
        return hash_file(cached)
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            ),
            "Referer": "https://sites.google.com/",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()
    with open_normalized(data=data) as im:
        return hash_image(im)


def hamming(a: int, b: int) -> int:
    return (a ^ b).bit_count()


def build_local_index() -> list[tuple[Path, int]]:
    cache_path = ROOT / "helpers" / "_cache_alley_local_hashes.json"
    exts = {".jpg", ".jpeg", ".png", ".webp"}
    cached: dict[str, int] = {}
    if cache_path.is_file():
        try:
            raw = json.loads(cache_path.read_text(encoding="utf-8"))
            cached = {k: int(v) for k, v in raw.items()}
        except (json.JSONDecodeError, ValueError):
            cached = {}

    items: list[tuple[Path, int]] = []
    updated: dict[str, int] = {}
    for path in sorted(LOCAL_FOTOLAR.iterdir()):
        if path.suffix.lower() not in exts or not path.is_file():
            continue
        key = path.name
        try:
            mtime = path.stat().st_mtime
            cache_key = f"{key}:{mtime}"
            if cache_key in cached:
                h = cached[cache_key]
            else:
                h = hash_file(path)
            items.append((path, h))
            updated[cache_key] = h
        except Exception as exc:
            print("skip local", path.name, exc)
    cache_path.write_text(json.dumps(updated, ensure_ascii=False), encoding="utf-8")
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
    if not LOCAL_FOTOLAR.is_dir():
        raise SystemExit(f"Local folder not found: {LOCAL_FOTOLAR}")

    urls = load_gallery_urls()
    print(f"Gallery URLs: {len(urls)}")
    if not THUMB_DIR.is_dir() or not any(THUMB_DIR.glob("*.jpg")):
        print("No cached thumbnails — run: python helpers/_fetch_alley_gallery_playwright.py")
    print("Indexing local photos…")
    local_index = build_local_index()
    print(f"Local index: {len(local_index)} files")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    # Clear previous outputs except manifest
    for old in OUT_DIR.iterdir():
        if old.name.startswith("_"):
            continue
        old.unlink()

    used: set[Path] = set()
    manifest: list[dict] = []

    for i, url in enumerate(urls, start=1):
        print(f"Match {i}/{len(urls)}…", end=" ", flush=True)
        thumb = THUMB_DIR / f"{i:02d}.jpg"
        if not thumb.is_file() or thumb.stat().st_size < 1000:
            print("SKIP (no thumbnail)")
            manifest.append({"index": i, "url": url, "skipped": True, "reason": "no_thumbnail"})
            continue
        try:
            wh = hash_thumb(i, url)
        except Exception as exc:
            print(f"FAIL hash: {exc}")
            manifest.append({"index": i, "url": url, "error": str(exc)})
            continue

        match_path, dist = best_match(wh, local_index, used)
        if match_path is None or dist > MAX_DIST:
            print(f"NO MATCH (best dist={dist})")
            manifest.append(
                {
                    "index": i,
                    "url": url,
                    "matched": False,
                    "distance": dist,
                }
            )
            continue

        used.add(match_path)
        dest_name = f"alley-of-honor-{i:02d}{match_path.suffix.lower()}"
        dest = OUT_DIR / dest_name
        shutil.copy2(match_path, dest)
        print(f"OK {match_path.name} -> {dest_name} (d={dist})")
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
    print(f"\nDone: {matched}/{len(urls)} matched -> {OUT_DIR}")
    print(f"Manifest: {MANIFEST}")


if __name__ == "__main__":
    main()
