#!/usr/bin/env python3
"""Remove daab-locale-hint (Rəsmi sayt AZ/EN bar) from all HTML files."""
from __future__ import annotations

import re
import sys
from pathlib import Path

from _paths import ROOT

LOCALE_HINT_RE = re.compile(
    r'<div id="daab-locale-hint"[^>]*>.*?</div>\s*',
    re.DOTALL | re.IGNORECASE,
)


def main() -> int:
    count = 0
    for path in ROOT.rglob("*.html"):
        if "node_modules" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        updated = LOCALE_HINT_RE.sub("", text)
        if updated != text:
            path.write_text(updated, encoding="utf-8", newline="\n")
            count += 1
            print(path.relative_to(ROOT))
    print(f"Removed locale hint from {count} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
