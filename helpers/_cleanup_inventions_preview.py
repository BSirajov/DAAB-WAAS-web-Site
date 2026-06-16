#!/usr/bin/env python3
"""Remove deleted images/inventions/ references from documents/preview/."""
from __future__ import annotations

import json
import re
from pathlib import Path

from _paths import ROOT

PREVIEW = ROOT / "documents" / "preview"
HTML = PREVIEW / "major_scientific_inventions.html"
OVERRIDES = PREVIEW / "inventions-card-overrides.json"
ICON_FIGURE = re.compile(
    r'<figure class="inventions-entry-icon">.*?</figure>',
    re.DOTALL,
)


def main() -> int:
    text = HTML.read_text(encoding="utf-8")
    cleaned, count = ICON_FIGURE.subn("", text)
    HTML.write_text(cleaned, encoding="utf-8", newline="\n")
    print(f"Removed {count} icon figures from {HTML.relative_to(ROOT)}")

    data = json.loads(OVERRIDES.read_text(encoding="utf-8"))
    emptied = 0
    for key in list(data):
        entry = data[key]
        if isinstance(entry, dict) and "icon" in entry:
            del entry["icon"]
        if isinstance(entry, dict) and not entry:
            del data[key]
            emptied += 1
    OVERRIDES.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Removed icon overrides; dropped {emptied} empty entries")

    stale: list[str] = []
    for path in PREVIEW.rglob("*"):
        if path.is_file() and "images/inventions/" in path.read_text(encoding="utf-8", errors="replace"):
            stale.append(str(path.relative_to(ROOT)))
    if stale:
        print("Still references images/inventions/:")
        for item in stale:
            print(f"  - {item}")
        return 1
    print("No stale images/inventions/ references in preview folder.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
