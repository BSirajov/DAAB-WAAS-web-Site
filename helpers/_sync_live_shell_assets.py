"""Sync shared shell asset ?v= tags on az/ and en/ HTML to current site baseline."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

# Baseline aligned with az/index.html and en/index.html
REPLACEMENTS: list[tuple[str, str]] = [
    ("daab-common.css?v=18", "daab-common.css?v=21"),
    ("daab-mobile.css?v=3", "daab-mobile.css?v=4"),
    ("daab-lang.css?v=7", "daab-lang.css?v=9"),
    ("daab-lang-position.js?v=3", "daab-lang-position.js?v=4"),
    ("daab-nav.js?v=7", "daab-nav.js?v=8"),
    ("daab-shell.js?v=7", "daab-shell.js?v=9"),
]


def process(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    for old, new in REPLACEMENTS:
        text = text.replace(old, new)
    if text != original:
        path.write_text(text, encoding="utf-8", newline="\n")
        return True
    return False


def main() -> None:
    updated: list[str] = []
    for folder in ("az", "en"):
        base = ROOT / folder
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.html")):
            if process(path):
                updated.append(path.relative_to(ROOT).as_posix())
    print(f"Synced {len(updated)} file(s):")
    for line in updated:
        print(f"  {line}")


if __name__ == "__main__":
    main()
