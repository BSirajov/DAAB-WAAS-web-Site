#!/usr/bin/env python3
"""Point forum HTML scientist avatars at images/scientists-photos/_thumbs/*.jpg."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

# scientists-photos/foo.png -> scientists-photos/_thumbs/foo.jpg
PHOTO_RE = re.compile(
    r"(images/scientists-photos/)(?!_thumbs/)([A-Za-z0-9._-]+)\.(?:png|jpe?g|webp)",
    re.I,
)


def patch_text(text: str) -> tuple[str, int]:
    count = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal count
        count += 1
        return f"{m.group(1)}_thumbs/{m.group(2)}.jpg"

    return PHOTO_RE.sub(repl, text), count


def main() -> int:
    targets = sorted((ROOT / "az" / "forum").rglob("*.html"))
    targets.extend(sorted((ROOT / "en" / "forum").rglob("*.html")))
    changed_files = 0
    total = 0
    for path in targets:
        text = path.read_text(encoding="utf-8")
        new, n = patch_text(text)
        if n:
            path.write_text(new, encoding="utf-8", newline="\n")
            changed_files += 1
            total += n
            print(f"  {path.relative_to(ROOT)}: {n} avatar(s)")
    print(f"Updated {changed_files} file(s), {total} reference(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
