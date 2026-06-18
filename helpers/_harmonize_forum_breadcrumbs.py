"""Normalize forum/2024 static breadcrumbs: I Forum hub label, remove stale static flag."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

FORUM_2024_DIRS = (
    ROOT / "az" / "forum" / "2024",
    ROOT / "en" / "forum" / "2024",
)

STATIC_ATTR = ' data-daab-breadcrumbs-static="1"'
HUB_OLD = '<a href="index.html">Forum 2024</a>'
HUB_NEW = '<a href="index.html">I Forum</a>'


def harmonize_text(text: str) -> tuple[str, list[str]]:
    changes: list[str] = []
    if STATIC_ATTR in text:
        text = text.replace(STATIC_ATTR, "")
        changes.append("remove-static-flag")
    if HUB_OLD in text:
        text = text.replace(HUB_OLD, HUB_NEW)
        changes.append("hub-label")
    # Normalize attribute order on legacy blocks (aria-label first → role first).
    text, n = re.subn(
        r'<div aria-label="([^"]+)" class="breadcrumbs forum-breadcrumbs" role="navigation">',
        r'<div class="breadcrumbs forum-breadcrumbs" role="navigation" aria-label="\1">',
        text,
    )
    if n:
        changes.append("attr-order")
    return text, changes


def main() -> int:
    updated = 0
    for directory in FORUM_2024_DIRS:
        if not directory.is_dir():
            continue
        for path in sorted(directory.glob("*.html")):
            text = path.read_text(encoding="utf-8")
            new_text, changes = harmonize_text(text)
            if new_text != text:
                path.write_text(new_text, encoding="utf-8", newline="\n")
                print(f"{path.relative_to(ROOT)}: {', '.join(changes)}")
                updated += 1
    print(f"Done — {updated} file(s) updated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
