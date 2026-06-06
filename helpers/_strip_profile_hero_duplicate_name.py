#!/usr/bin/env python3
"""Remove duplicate pf-hero-latin line when it repeats the h1 name on profile pages."""
from __future__ import annotations

import re

from _paths import ROOT

# Matches hero subtitle immediately after title row closing </div>
DUPLICATE_NAME_RE = re.compile(
    r"(</h1></div>)<div class=\"page-hero-subtitle pf-hero-latin\">[^<]*</div>",
    re.IGNORECASE,
)

PF_ROOTS = (
    ROOT / "az" / "prominent_figures",
    ROOT / "en" / "prominent_figures",
)


def strip_duplicate_name(html: str) -> str:
    return DUPLICATE_NAME_RE.sub(r"\1", html, count=1)


def main() -> int:
    n = 0
    for root in PF_ROOTS:
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*.html")):
            if path.name == "hazirlanir.html":
                continue
            text = path.read_text(encoding="utf-8")
            fixed = strip_duplicate_name(text)
            if fixed != text:
                path.write_text(fixed, encoding="utf-8", newline="\n")
                n += 1
    print(f"Removed duplicate hero name from {n} profile pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
