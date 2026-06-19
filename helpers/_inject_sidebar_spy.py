#!/usr/bin/env python3
"""Insert daab-sidebar-spy.js before daab-sidebar-timeline.js on live pages."""
from __future__ import annotations

import re

from _paths import ROOT

TIMELINE_RE = re.compile(
    r'(<script[^>]+daab-sidebar-timeline\.js[^>]*></script>)',
    re.I,
)


def patch_file(path) -> bool:
    text = path.read_text(encoding="utf-8")
    if "daab-sidebar-timeline.js" not in text or "daab-sidebar-spy.js" in text:
        return False
    depth = len(path.relative_to(ROOT).parts) - 1
    rel = "../" * max(depth, 0) + "js/daab-sidebar-spy.js?v=1"
    spy_tag = f'<script defer src="{rel}"></script>'
    text = TIMELINE_RE.sub(spy_tag + r"\n\1", text, count=1)
    text = text.replace("daab-sidebar-timeline.js?v=3", "daab-sidebar-timeline.js?v=4")
    path.write_text(text, encoding="utf-8")
    return True


def main() -> None:
    changed = 0
    for lang in ("az", "en"):
        for path in sorted((ROOT / lang).rglob("*.html")):
            if patch_file(path):
                changed += 1
                print(f"  {path.relative_to(ROOT)}")
    print(f"OK — {changed} file(s)")


if __name__ == "__main__":
    main()
