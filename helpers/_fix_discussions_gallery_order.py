#!/usr/bin/env python3
"""Remove page banner from discussions gallery cache; align with markdown URL list."""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

from _paths import ROOT

OUT_DIR = ROOT / "images" / "photos-gallery" / "Discussions"
MANIFEST = OUT_DIR / "_match-manifest.json"
URL_CACHE = ROOT / "helpers" / "_cache_discussions_gallery_urls.txt"
THUMB_DIR = ROOT / "helpers" / "_cache_discussions_gallery_thumbs"
MD = ROOT / "helpers" / "_cache_discussions_page.md"
BANNER_BYTES = 682043


def gallery_urls_from_md() -> list[str]:
    text = MD.read_text(encoding="utf-8")
    urls = re.findall(
        r"^!\[\]\((https://lh3\.googleusercontent\.com/sitesv/[^)]+)\)",
        text,
        re.MULTILINE,
    )
    return [re.sub(r"=w\d+", "=w1280", u) for u in urls if "=w16383" not in u]


def main() -> None:
    urls = gallery_urls_from_md()
    URL_CACHE.write_text("\n".join(urls) + "\n", encoding="utf-8")
    print(f"URL cache: {len(urls)} gallery URLs")

    if not MANIFEST.is_file():
        print("No manifest yet — run matcher after re-fetching thumbs from markdown URLs")
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
        old_dest = OUT_DIR / f"discussions-{old_i:03d}.jpg"
        new_dest = tmp / f"discussions-{new_i:03d}.jpg"
        if old_dest.is_file():
            shutil.copy2(old_dest, new_dest)
        old_entry = by_index.get(old_i, {})
        new_manifest.append(
            {
                "index": new_i,
                "url": urls[new_i - 1],
                "matched": old_dest.is_file(),
                "source": old_entry.get("source"),
                "dest": f"discussions-{new_i:03d}.jpg",
                "distance": old_entry.get("distance"),
                "source_bytes": old_entry.get("source_bytes"),
                "renumbered_from": old_i,
            }
        )

    for old in OUT_DIR.glob("discussions-*.jpg"):
        old.unlink()
    for f in sorted(tmp.glob("*.jpg")):
        shutil.move(str(f), str(OUT_DIR / f.name))
    tmp.rmdir()

    if THUMB_DIR.is_dir():
        banner = THUMB_DIR / "001.jpg"
        if banner.is_file() and banner.stat().st_size == BANNER_BYTES:
            banner.unlink()
        tmp_t = THUMB_DIR / "_renumber_tmp"
        if tmp_t.exists():
            shutil.rmtree(tmp_t)
        tmp_t.mkdir()
        for new_i in range(1, len(urls) + 1):
            src = THUMB_DIR / f"{new_i + 1:03d}.jpg"
            if src.is_file():
                shutil.copy2(src, tmp_t / f"{new_i:03d}.jpg")
        for f in THUMB_DIR.glob("*.jpg"):
            if f.parent == THUMB_DIR:
                f.unlink()
        for f in sorted(tmp_t.glob("*.jpg")):
            shutil.move(str(f), str(THUMB_DIR / f.name))
        tmp_t.rmdir()

    MANIFEST.write_text(
        json.dumps(new_manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    matched = sum(1 for e in new_manifest if e.get("matched"))
    print(f"Renumbered outputs: {matched}/{len(urls)} -> {OUT_DIR}")


if __name__ == "__main__":
    main()
