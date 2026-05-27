#!/usr/bin/env python3
"""Remove page banner; align CoffeeBreak outputs with gallery order."""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

from _paths import ROOT

OUT_DIR = ROOT / "images" / "photos-gallery" / "CoffeeBreak"
MANIFEST = OUT_DIR / "_match-manifest.json"
URL_CACHE = ROOT / "helpers" / "_cache_coffee_break_gallery_urls.txt"
THUMB_DIR = ROOT / "helpers" / "_cache_coffee_break_gallery_thumbs"
MD = ROOT / "helpers" / "_cache_coffee_break_page.md"
BANNER_BYTES = 682043


def gallery_urls() -> list[str]:
    if MD.is_file():
        text = MD.read_text(encoding="utf-8")
        urls = re.findall(
            r"^!\[\]\((https://lh3\.googleusercontent\.com/sitesv/[^)]+)\)",
            text,
            re.MULTILINE,
        )
        urls = [re.sub(r"=w\d+", "=w1280", u) for u in urls if "=w16383" not in u]
        if urls:
            return urls
    lines = [ln.strip() for ln in URL_CACHE.read_text(encoding="utf-8").splitlines() if ln.strip()]
    banner = THUMB_DIR / "01.jpg"
    if banner.is_file() and banner.stat().st_size == BANNER_BYTES and len(lines) > 1:
        return lines[1:]
    return lines


def main() -> None:
    urls = gallery_urls()
    URL_CACHE.write_text("\n".join(urls) + "\n", encoding="utf-8")
    if not MANIFEST.is_file():
        print(f"URLs only: {len(urls)}")
        return

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    by_index = {e["index"]: e for e in manifest if e.get("index")}

    tmp = OUT_DIR / "_renumber_tmp"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir()

    new_manifest: list[dict] = []
    for new_i in range(1, len(urls) + 1):
        old_i = new_i + 1
        old_dest = OUT_DIR / f"coffee-break-{old_i:02d}.jpg"
        new_dest = tmp / f"coffee-break-{new_i:02d}.jpg"
        if old_dest.is_file():
            shutil.copy2(old_dest, new_dest)
        old_entry = by_index.get(old_i, {})
        new_manifest.append(
            {
                "index": new_i,
                "url": urls[new_i - 1],
                "matched": old_dest.is_file(),
                "source": old_entry.get("source"),
                "dest": f"coffee-break-{new_i:02d}.jpg",
                "distance": old_entry.get("distance"),
                "source_bytes": old_entry.get("source_bytes"),
                "renumbered_from": old_i,
            }
        )

    for old in OUT_DIR.glob("coffee-break-*.jpg"):
        old.unlink()
    for f in sorted(tmp.glob("*.jpg")):
        shutil.move(str(f), str(OUT_DIR / f.name))
    tmp.rmdir()

    banner = THUMB_DIR / "01.jpg"
    if banner.is_file() and banner.stat().st_size == BANNER_BYTES:
        banner.unlink()
    tmp_t = THUMB_DIR / "_renumber_tmp"
    if tmp_t.exists():
        shutil.rmtree(tmp_t)
    tmp_t.mkdir()
    for new_i in range(1, len(urls) + 1):
        src = THUMB_DIR / f"{new_i + 1:02d}.jpg"
        if src.is_file():
            shutil.copy2(src, tmp_t / f"{new_i:02d}.jpg")
    for f in THUMB_DIR.glob("*.jpg"):
        if f.parent == THUMB_DIR:
            f.unlink()
    for f in sorted(tmp_t.glob("*.jpg")):
        shutil.move(str(f), str(THUMB_DIR / f.name))
    tmp_t.rmdir()

    MANIFEST.write_text(json.dumps(new_manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    matched = sum(1 for e in new_manifest if e.get("matched"))
    print(f"Gallery photos: {matched}/{len(urls)} -> {OUT_DIR}")


if __name__ == "__main__":
    main()
