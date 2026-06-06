#!/usr/bin/env python3
"""Fix EN profile section titles: '{Name} haqqında' → 'About {Name}'."""
from __future__ import annotations

from _az_profile_translator import fix_section_title_about
from _paths import ROOT

EN_ROOT = ROOT / "en" / "prominent_figures"


def main() -> int:
    n = 0
    for group in ("azturk", "world"):
        folder = EN_ROOT / group
        if not folder.is_dir():
            continue
        for path in sorted(folder.glob("*.html")):
            text = path.read_text(encoding="utf-8")
            fixed = fix_section_title_about(text)
            if fixed != text:
                path.write_text(fixed, encoding="utf-8", newline="\n")
                n += 1
    print(f"Fixed section titles in {n} EN profile pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
