#!/usr/bin/env python3
"""Remove inline daab-critical-paint blocks added for first-paint (reverted)."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

CRITICAL = re.compile(
    r'\n<style id="daab-critical-paint">html\{background-color:#f5fbff\}</style>',
    re.IGNORECASE,
)


def main() -> None:
    updated = 0
    for path in sorted(ROOT.rglob("*.html")):
        if "_archive" in path.parts or "Deployment" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        new_text, n = CRITICAL.subn("", text, count=1)
        if n:
            path.write_text(new_text, encoding="utf-8")
            updated += 1
            print(f"updated: {path.relative_to(ROOT)}")
    print(f"Done. {updated} file(s) updated.")


if __name__ == "__main__":
    main()
