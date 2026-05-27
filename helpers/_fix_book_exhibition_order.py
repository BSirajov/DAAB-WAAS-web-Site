#!/usr/bin/env python3
"""Drop page banner (index 1); renumber gallery photos 02–19 → 01–18."""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

from _paths import ROOT

OUT_DIR = ROOT / "images" / "photos-gallery" / "BookExibition"
MANIFEST = OUT_DIR / "_match-manifest.json"
URL_CACHE = ROOT / "helpers" / "_cache_book_exhibition_gallery_urls.txt"
THUMB_DIR = ROOT / "helpers" / "_cache_book_exhibition_gallery_thumbs"
MD = ROOT / "helpers" / "_cache_book_exhibition_page.md"


def gallery_urls() -> list[str]:
    text = MD.read_text(encoding="utf-8")
    urls = re.findall(
        r"^!\[\]\((https://lh3\.googleusercontent\.com/sitesv/[^)]+)\)",
        text,
        re.MULTILINE,
    )
    return [re.sub(r"=w\d+", "=w1280", u) for u in urls if "=w16383" not in u]


def main() -> None:
    urls = gallery_urls()
    URL_CACHE.write_text("\n".join(urls) + "\n", encoding="utf-8")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    by_index = {e["index"]: e for e in manifest if e.get("index")}

    tmp = OUT_DIR / "_renumber_tmp"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir()

    new_manifest: list[dict] = []
    for new_i in range(1, len(urls) + 1):
        old_i = new_i + 1
        old_dest = OUT_DIR / f"book-exhibition-{old_i:02d}.jpg"
        new_dest = tmp / f"book-exhibition-{new_i:02d}.jpg"
        if old_dest.is_file():
            shutil.copy2(old_dest, new_dest)
        old_entry = by_index.get(old_i, {})
        new_manifest.append(
            {
                "index": new_i,
                "url": urls[new_i - 1],
                "matched": old_dest.is_file(),
                "source": old_entry.get("source"),
                "dest": f"book-exhibition-{new_i:02d}.jpg",
                "distance": old_entry.get("distance"),
                "source_bytes": old_entry.get("source_bytes"),
                "renumbered_from": old_i,
                "note": "banner removed from index 1",
            }
        )

    for old in OUT_DIR.glob("book-exhibition-*.jpg"):
        old.unlink()
    for f in sorted(tmp.glob("*.jpg")):
        shutil.move(str(f), str(OUT_DIR / f.name))
    tmp.rmdir()

    if THUMB_DIR.is_dir():
        tmp_t = THUMB_DIR / "_renumber_tmp"
        if tmp_t.exists():
            shutil.rmtree(tmp_t)
        tmp_t.mkdir()
        (THUMB_DIR / "01.jpg").unlink(missing_ok=True)
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

    MANIFEST.write_text(
        json.dumps(new_manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    matched = sum(1 for e in new_manifest if e.get("matched"))
    print(f"Gallery photos: {matched}/{len(urls)} -> {OUT_DIR}")


if __name__ == "__main__":
    main()
