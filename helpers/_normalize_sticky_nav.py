"""Normalize sticky-nav CSS versions and legacy scroll-margin overrides on live pages."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

LIVE_DIRS = (ROOT / "az", ROOT / "en")

SCROLL_MARGIN_LEGACY = re.compile(
    r"scroll-margin-top:\s*(?:110|230|70)px\s*;?",
    re.IGNORECASE,
)
SCROLL_MARGIN_REPL = (
    "scroll-margin-top: calc(var(--daab-nav-height, 86px) + 1.25rem);"
)

VERSION_REPLACEMENTS = (
    ("daab-common.css?v=21", "daab-common.css?v=22"),
    ("daab-mobile.css?v=4", "daab-mobile.css?v=5"),
)


def patch_html(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    for old, new in VERSION_REPLACEMENTS:
        text = text.replace(old, new)
    text = SCROLL_MARGIN_LEGACY.sub(SCROLL_MARGIN_REPL, text)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed: list[str] = []
    for base in LIVE_DIRS:
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.html")):
            if patch_html(path):
                changed.append(str(path.relative_to(ROOT)))
    gateway = ROOT / "index.html"
    if gateway.is_file() and patch_html(gateway):
        changed.append("index.html")
    print(f"Patched {len(changed)} file(s)")
    for rel in changed:
        print(f"  {rel}")


if __name__ == "__main__":
    main()
