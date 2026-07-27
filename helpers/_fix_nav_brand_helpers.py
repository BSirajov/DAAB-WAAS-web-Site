#!/usr/bin/env python3
"""Update helper string templates that still use the old nav brand <br> markup."""
from __future__ import annotations

from pathlib import Path

from _paths import ROOT, HELPERS

# Patterns as they appear in source files (including escaped quotes inside py strings).
REPLACEMENTS = [
    (
        'World Association of<br class="mobile-hidden-break">Azerbaijani Scientists',
        '<span class="nav-brand-line">World Association of</span>'
        '<span class="nav-brand-line">Azerbaijani Scientists</span>',
    ),
    (
        r'World Association of<br class=\"mobile-hidden-break\">Azerbaijani Scientists',
        r'<span class=\"nav-brand-line\">World Association of</span>'
        r'<span class=\"nav-brand-line\">Azerbaijani Scientists</span>',
    ),
    (
        'Dünya Azərbaycanlı<br class="mobile-hidden-break">Alimlər Birliyi',
        '<span class="nav-brand-line">Dünya Azərbaycanlı</span>'
        '<span class="nav-brand-line">Alimlər Birliyi</span>',
    ),
    (
        r'Dünya Azərbaycanlı<br class=\"mobile-hidden-break\">Alimlər Birliyi',
        r'<span class=\"nav-brand-line\">Dünya Azərbaycanlı</span>'
        r'<span class=\"nav-brand-line\">Alimlər Birliyi</span>',
    ),
]


def main() -> int:
    updated = 0
    for path in sorted(HELPERS.rglob("*.py")):
        if path.name.startswith("_fix_nav_brand"):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            print(f"  skip (encoding) {path.relative_to(ROOT)}")
            continue
        original = text
        for old, new in REPLACEMENTS:
            text = text.replace(old, new)
        # Split brand title across two f-string/concat lines in some builders.
        text = text.replace(
            '<span class="nav-brand-text">World Association of<br class="mobile-hidden-break">\'\n'
            '        "Azerbaijani Scientists</span>',
            '<span class="nav-brand-text">'
            '<span class="nav-brand-line">World Association of</span>'
            '<span class="nav-brand-line">Azerbaijani Scientists</span></span>',
        )
        if text != original:
            path.write_text(text, encoding="utf-8", newline="\n")
            updated += 1
            print(f"  updated {path.relative_to(ROOT)}")
    print(f"Done — {updated} helper file(s) updated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
