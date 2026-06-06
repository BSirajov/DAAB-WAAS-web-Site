#!/usr/bin/env python3
"""Remove obsolete Activities segment from Forum 2024 static breadcrumb bars."""
from __future__ import annotations

from _paths import ROOT

import re

# Remove obsolete Activities crumb between Home and Forum 2024 (old submenu layout).
ACTIVITIES_CRUMB_RE = re.compile(
    r'<span aria-hidden="true">›</span><a href="../../activities\.html">(?:Fəaliyyətimiz|Activities)</a>',
    re.IGNORECASE,
)


def main() -> None:
    updated: list[str] = []
    for pattern in ("az/forum/2024/*.html", "en/forum/2024/*.html", "deployment/az/forum/2024/*.html", "deployment/en/forum/2024/*.html"):
        for path in sorted(ROOT.glob(pattern)):
            text = path.read_text(encoding="utf-8")
            new = ACTIVITIES_CRUMB_RE.sub("", text)
            if new != text:
                path.write_text(new, encoding="utf-8")
                updated.append(path.relative_to(ROOT).as_posix())
    if updated:
        print("Updated breadcrumb trails:")
        for rel in updated:
            print(f"  {rel}")
    else:
        print("No forum breadcrumb files needed changes.")


if __name__ == "__main__":
    main()
