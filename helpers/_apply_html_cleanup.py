"""Apply bulk HTML cleanup fixes (duplicate lang, cache bust alignment)."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT


def fix_file(path: Path) -> list[str]:
    changes: list[str] = []
    text = path.read_text(encoding="utf-8")
    original = text

    if 'lang="az" lang="az"' in text:
        text = text.replace('lang="az" lang="az"', 'lang="az"', 1)
        changes.append("duplicate lang")

    if "daab-mobile.css?v=2" in text:
        text = text.replace("daab-mobile.css?v=2", "daab-mobile.css?v=3")
        changes.append("daab-mobile v=3")

    if "scientists-catalog-data.js?v=1" in text:
        text = text.replace("scientists-catalog-data.js?v=1", "scientists-catalog-data.js?v=2")
        changes.append("catalog-data v=2")

    if "daab-shell.js?v=6" in text:
        text = text.replace("daab-shell.js?v=6", "daab-shell.js?v=7")
        changes.append("daab-shell v=7")

    if "daab-lang-position.js?v=2" in text:
        text = text.replace("daab-lang-position.js?v=2", "daab-lang-position.js?v=3")
        changes.append("daab-lang-position v=3")

    if "daab-lang.css?v=6" in text:
        text = text.replace("daab-lang.css?v=6", "daab-lang.css?v=7")
        changes.append("daab-lang v=7")

    if text != original:
        path.write_text(text, encoding="utf-8", newline="\n")
    return changes


def main() -> int:
    updated = 0
    for pattern in ("az/**/*.html", "en/**/*.html"):
        for path in sorted(ROOT.glob(pattern)):
            changes = fix_file(path)
            if changes:
                updated += 1
                print(f"{path.relative_to(ROOT)}: {', '.join(changes)}")
    print(f"Updated {updated} file(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
