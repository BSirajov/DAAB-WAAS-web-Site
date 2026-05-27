#!/usr/bin/env python3
"""Remove logo URL from gallery cache; renumber outputs 01–70 to match Google Sites order."""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

from _paths import ROOT

URL_CACHE = ROOT / "helpers" / "_cache_alley_gallery_urls.txt"
OUT_DIR = ROOT / "images" / "photos-gallery" / "AlleyOfHonor"
MANIFEST = OUT_DIR / "_match-manifest.json"
THUMB_DIR = ROOT / "helpers" / "_cache_alley_gallery_thumbs"


def gallery_urls_from_page_markdown(md_path: Path) -> list[str]:
    text = md_path.read_text(encoding="utf-8")
    # Only standalone gallery lines (not logo inside a markdown link)
    urls = re.findall(
        r"^!\[\]\((https://lh3\.googleusercontent\.com/sitesv/[^)]+)\)",
        text,
        re.MULTILINE,
    )
    return [re.sub(r"=w\d+", "=w1280", u) for u in urls]


def main() -> None:
    md = ROOT / "helpers" / "_cache_alley_page.md"
    if not md.is_file():
        raise SystemExit(f"Save live page markdown to {md} first")

    urls = gallery_urls_from_page_markdown(md)
    print(f"Gallery URLs (no logo): {len(urls)}")
    URL_CACHE.write_text("\n".join(urls) + "\n", encoding="utf-8")

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.is_file() else []
    by_index = {e["index"]: e for e in manifest if e.get("index")}

    # Drop wrong index 1; shift 2..71 -> 1..70
    tmp = OUT_DIR / "_renumber_tmp"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir()

    new_manifest: list[dict] = []
    for new_i in range(1, len(urls) + 1):
        old_i = new_i + 1  # old list had logo at index 1
        old_dest = OUT_DIR / f"alley-of-honor-{old_i:02d}.jpg"
        new_dest = tmp / f"alley-of-honor-{new_i:02d}.jpg"
        if old_dest.is_file():
            shutil.copy2(old_dest, new_dest)
        old_entry = by_index.get(old_i, {})
        new_manifest.append(
            {
                "index": new_i,
                "url": urls[new_i - 1],
                "matched": old_dest.is_file(),
                "source": old_entry.get("source"),
                "dest": f"alley-of-honor-{new_i:02d}.jpg",
                "distance": old_entry.get("distance"),
                "source_bytes": old_entry.get("source_bytes"),
                "renumbered_from": old_i,
            }
        )

    # Remove old outputs and install renumbered set
    for old in OUT_DIR.glob("alley-of-honor-*.jpg"):
        old.unlink()
    for f in sorted(tmp.glob("*.jpg")):
        shutil.move(str(f), str(OUT_DIR / f.name))
    tmp.rmdir()

    # Renumber thumbnails 02..71 -> 01..70
    if THUMB_DIR.is_dir():
        tmp_t = THUMB_DIR / "_renumber_tmp"
        if tmp_t.exists():
            shutil.rmtree(tmp_t)
        tmp_t.mkdir()
        (THUMB_DIR / "01.jpg").unlink(missing_ok=True)
        for new_i in range(1, len(urls) + 1):
            old_i = new_i + 1
            src = THUMB_DIR / f"{old_i:02d}.jpg"
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
    print(f"Renumbered: {matched}/{len(urls)} -> {OUT_DIR}")


if __name__ == "__main__":
    main()
