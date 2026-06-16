#!/usr/bin/env python3
"""Update bare photo filenames and scan for broken PNG paths after compression."""
from __future__ import annotations

import json
import re
from pathlib import Path

from _paths import ROOT

PHOTO_DIRS = (
    "images/scientists-photos",
    "images/board-members-photos",
    "images/activities",
    "images/inventions",
)


def converted_basenames() -> dict[str, str]:
    out: dict[str, str] = {}
    for folder in PHOTO_DIRS:
        base = ROOT / folder
        if not base.is_dir():
            continue
        for jpg in base.rglob("*.jpg"):
            png = jpg.with_suffix(".png")
            if not png.is_file():
                out[png.name] = jpg.name
    return out


def sync_profiles_json(conversions: dict[str, str]) -> int:
    path = ROOT / "i18n" / "scientists-profiles.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    changed = 0
    for card in data.get("profiles", []):
        photo = card.get("photo", "")
        if photo in conversions:
            card["photo"] = conversions[photo]
            changed += 1
    if changed:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return changed


def broken_png_refs() -> list[tuple[str, str]]:
    pattern = re.compile(
        r"images/(?:scientists-photos|board-members-photos|activities|inventions)/[^\s\"']+\.png"
    )
    broken: list[tuple[str, str]] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".html", ".js", ".json", ".py"}:
            continue
        if "Deployment" in path.parts or "documents" in path.parts:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for match in pattern.finditer(text):
            ref = match.group(0)
            if not (ROOT / ref).is_file():
                broken.append((path.relative_to(ROOT).as_posix(), ref))
    return broken


def fix_broken_refs(broken: list[tuple[str, str]], conversions: dict[str, str]) -> int:
    files_changed = 0
    by_file: dict[str, set[str]] = {}
    for file_path, ref in broken:
        by_file.setdefault(file_path, set()).add(ref)

    for file_path, refs in sorted(by_file.items()):
        path = ROOT / file_path
        text = path.read_text(encoding="utf-8")
        new_text = text
        for ref in refs:
            old_name = Path(ref).name
            if old_name not in conversions:
                continue
            new_ref = str(Path(ref).with_name(conversions[old_name])).replace("\\", "/")
            new_text = new_text.replace(ref, new_ref)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8", newline="\n")
            files_changed += 1
    return files_changed


def main() -> None:
    conversions = converted_basenames()
    print(f"Converted basenames: {len(conversions)}")
    profile_updates = sync_profiles_json(conversions)
    print(f"scientists-profiles.json photo fields updated: {profile_updates}")
    broken = broken_png_refs()
    print(f"Broken full-path PNG refs before fix: {len(broken)}")
    fixed = fix_broken_refs(broken, conversions)
    print(f"Files fixed: {fixed}")
    remaining = broken_png_refs()
    print(f"Broken full-path PNG refs after fix: {len(remaining)}")
    for file_path, ref in remaining[:20]:
        print(f"  {file_path} -> {ref}")


if __name__ == "__main__":
    main()
