#!/usr/bin/env python3
"""Report manifest vs thumb vs disk counts per gallery category."""
from __future__ import annotations

import json
from pathlib import Path

from _paths import ROOT

GALLERY_ROOT = ROOT / "images" / "photos-gallery"
THUMB_ROOT = GALLERY_ROOT / "_thumbs"
MANIFEST = ROOT / "js" / "photos-gallery-manifest.json"
THUMB_INDEX = ROOT / "js" / "photos-gallery-thumbs.json"
EXTS = {".jpg", ".jpeg", ".png", ".webp"}


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    thumb_index = json.loads(THUMB_INDEX.read_text(encoding="utf-8"))

    for cat in manifest["categories"]:
        folder = cat["folder"]
        src_dir = GALLERY_ROOT / folder
        thumb_dir = THUMB_ROOT / folder
        listed = cat["images"]
        with_thumb = [
            f
            for f in listed
            if (thumb_dir / f"{Path(f).stem}.jpg").is_file()
            and (thumb_dir / f"{Path(f).stem}.jpg").stat().st_size > 0
        ]
        on_disk = sorted(
            f.name
            for f in src_dir.iterdir()
            if f.is_file() and f.suffix.lower() in EXTS and not f.name.startswith("_")
        )
        idx_keys = set(thumb_index.get("folders", {}).get(folder, {}))
        print(
            f"{cat['title']['en']:22}  listed={len(listed):3}  count={cat['count']:3}  "
            f"thumb_files={len(with_thumb):3}  disk={len(on_disk):3}  index={len(idx_keys):3}"
        )
        if cat["count"] != len(with_thumb):
            print(f"  -> count field should be {len(with_thumb)}")


if __name__ == "__main__":
    main()
