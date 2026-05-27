#!/usr/bin/env python3
"""Scan images/photos-gallery and write js/photos-gallery-manifest.json."""
from __future__ import annotations

import json
import re
from pathlib import Path

from _paths import ROOT

GALLERY_ROOT = ROOT / "images" / "photos-gallery"
THUMB_ROOT = GALLERY_ROOT / "_thumbs"
OUT = ROOT / "js" / "photos-gallery-manifest.json"

# Manifest-only ghosts (listed in old builds but no longer on disk)
SKIP_FILENAMES = frozenset(
    {
        "lunch-break-21.jpg",
        "010. Ziyafətdən görüntülər.jpg",
    }
)

CATEGORY_TITLES: dict[str, tuple[str, str]] = {
    "1.AlleyOfHonor": (
        "Alley of Honor and Martyrs' Lane",
        "Fəxri Xiyaban, Şəhidlər Xiyabanı",
    ),
    "2.OpeningDay": ("Opening day", "Açılış günü"),
    "3.BookExibition": ("Book exhibition", "Kitab sərgisi"),
    "4.Discussions": ("Discussions", "Müzakirələr"),
    "5. BetweenSessions": ("Between sessions", "Sessiyalar arası"),
    "6. Portraits": ("Portraits", "Portretlər"),
    "7. Garabagh": ("Karabakh", "Qarabağ"),
    "8. CoffeeBreak": ("Coffee break", "Kofe fasiləsi"),
    "9. LunchBreak": ("Lunch break", "Nahar fasiləsi"),
    "10. Party": ("Evening reception", "Ziyafət"),
}


def folder_sort_key(path: Path) -> int:
    m = re.match(r"^(\d+)", path.name)
    return int(m.group(1)) if m else 999


def natural_sort_key(name: str) -> list:
    return [int(p) if p.isdigit() else p.lower() for p in re.split(r"(\d+)", name)]


def has_thumbnail(folder_name: str, filename: str) -> bool:
    thumb = THUMB_ROOT / folder_name / f"{Path(filename).stem}.jpg"
    return thumb.is_file() and thumb.stat().st_size > 0


def collect_images(folder: Path) -> list[str]:
    """Only files on disk with a generated thumbnail (matches what the gallery can show)."""
    images: list[str] = []
    for f in folder.iterdir():
        if not f.is_file():
            continue
        if f.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
            continue
        if f.name.startswith("_") or f.name in SKIP_FILENAMES:
            continue
        if f.stat().st_size <= 0:
            continue
        if not has_thumbnail(folder.name, f.name):
            continue
        images.append(f.name)
    return sorted(images, key=natural_sort_key)


def title_from_folder(folder: str) -> tuple[str, str]:
    if folder in CATEGORY_TITLES:
        return CATEGORY_TITLES[folder]
    stem = re.sub(r"^\d+\.?\s*", "", folder).replace("_", " ")
    readable = re.sub(r"([a-z])([A-Z])", r"\1 \2", stem).strip()
    return readable or folder, readable or folder


def main() -> None:
    if not GALLERY_ROOT.is_dir():
        raise SystemExit(f"Missing gallery root: {GALLERY_ROOT}")

    categories: list[dict] = []
    order = 0
    for folder in sorted(
        (p for p in GALLERY_ROOT.iterdir() if p.is_dir() and p.name != "_thumbs"),
        key=folder_sort_key,
    ):
        images = collect_images(folder)
        if not images:
            continue
        order += 1
        en_title, az_title = title_from_folder(folder.name)
        categories.append(
            {
                "id": f"gallery-{order:02d}",
                "order": order,
                "folder": folder.name,
                "title": {"en": en_title, "az": az_title},
                "count": len(images),
                "images": images,
            }
        )

    payload = {"version": 2, "generatedFrom": "images/photos-gallery", "categories": categories}
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    total = sum(c["count"] for c in categories)
    print(f"Wrote {len(categories)} categories, {total} images -> {OUT}")


if __name__ == "__main__":
    main()
