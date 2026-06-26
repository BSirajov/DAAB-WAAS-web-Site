#!/usr/bin/env python3
"""Rename non-ASCII image files to ASCII slugs and sync refs sitewide."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from _compress_images import sync_converted_refs
from _paths import ROOT

# (subdir under images/, old basename, new basename)
RENAMES: list[tuple[str, str, str]] = [
    (
        "forum",
        "Aimlərimizin_müraciəti_Xankəndi_1.jpg",
        "scientists-address-khankendi-1.jpg",
    ),
    (
        "forum",
        "Aimlərimizin_müraciəti_Xankəndi_2.jpg",
        "scientists-address-khankendi-2.jpg",
    ),
    ("forum", "Prezidentin_müraciəti.jpg", "president-address.jpg"),
    ("forum", "VƏTƏN HİSSLƏRİ.jpg", "homeland-feelings.jpg"),
    ("forum", "CIDIR DÜZÜ.jpg", "jidir-plain.jpg"),
    ("forum", "XƏDİCƏ.jpg", "xedice-story.jpg"),
]

_DAAD_OLD = re.compile(
    r"^DAAD, İstanbul görüşü, 09\.12\.2022 \((\d{3})\)\.jpg$"
)


def _daad_new_name(num: str) -> str:
    return f"daad-istanbul-meeting-2022-12-09-{num}.jpg"


def build_rename_map() -> list[tuple[Path, Path]]:
    pairs: list[tuple[Path, Path]] = []
    for subdir, old_name, new_name in RENAMES:
        old_path = ROOT / "images" / subdir / old_name
        new_path = ROOT / "images" / subdir / new_name
        pairs.append((old_path, new_path))

    activities = ROOT / "images" / "activities"
    if activities.is_dir():
        for path in sorted(activities.iterdir()):
            match = _DAAD_OLD.match(path.name)
            if match:
                pairs.append((path, activities / _daad_new_name(match.group(1))))

    return pairs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Rename files and update refs (default: dry-run)",
    )
    args = parser.parse_args()

    pairs = build_rename_map()
    if not pairs:
        print("No Unicode image renames configured.")
        return 0

    missing = [old for old, _ in pairs if not old.is_file()]
    conflicts = [new for _, new in pairs if new.is_file() and new not in {n for _, n in pairs}]

    print(f"Planned renames: {len(pairs)}")
    for old, new in pairs:
        status = "OK" if old.is_file() else "MISSING"
        print(f"  [{status}] {old.relative_to(ROOT)} -> {new.name}")

    if missing:
        print(f"\n{len(missing)} source file(s) missing — aborting.")
        return 1

    if conflicts:
        print(f"\n{len(conflicts)} target file(s) already exist — aborting.")
        return 1

    if not args.apply:
        print("\nDry run only. Pass --apply to rename and sync refs.")
        return 0

    conversions: list[tuple[str, str]] = []
    for old, new in pairs:
        old.rename(new)
        conversions.append(
            (old.relative_to(ROOT).as_posix(), new.relative_to(ROOT).as_posix())
        )

    changed = sync_converted_refs(conversions)
    print(f"\nRenamed {len(pairs)} file(s); updated {changed} ref file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
