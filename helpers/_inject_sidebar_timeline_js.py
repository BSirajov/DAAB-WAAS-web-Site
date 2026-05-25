#!/usr/bin/env python3
"""Replace duplicated inline sidebar timeline scripts with js/daab-sidebar-timeline.js."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

INLINE = re.compile(
    r"<script>\s*\(function \(\) \{\s*"
    r"const links = Array\.from\(document\.querySelectorAll\('\.timeline-list a\[href\^=\"#\"\]'\)\);"
    r".*?"
    r"}\)\(\);\s*</script>",
    re.DOTALL,
)

SCRIPT_TAG = '<script src="../../../js/daab-sidebar-timeline.js?v=1" defer></script>'

PAGES = [
    * (ROOT / "az" / "forum" / "2024").glob("*.html"),
    * (ROOT / "en" / "forum" / "2024").glob("*.html"),
]


def main() -> None:
    for path in sorted(PAGES):
        if path.name == "index.html":
            continue
        text = path.read_text(encoding="utf-8")
        if "daab-sidebar-timeline.js" in text:
            print(f"skip {path.relative_to(ROOT)} (already injected)")
            continue
        new, n = INLINE.subn(SCRIPT_TAG, text, count=1)
        if n:
            path.write_text(new, encoding="utf-8", newline="\n")
            print(f"updated {path.relative_to(ROOT)}")
        else:
            print(f"no inline script {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
