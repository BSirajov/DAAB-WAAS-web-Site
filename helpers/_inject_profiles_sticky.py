"""Inject scientists-profiles sticky chrome CSS/JS into az/en profiles.html."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from helpers._paths import AZ_SCIENTISTS_PROFILES, EN_SCIENTISTS_PROFILES

CSS_LINK = '<link href="../../css/scientists-profiles-sticky.css?v=2" rel="stylesheet"/>'
JS_SCRIPT = '<script src="../../js/daab-profiles-sticky.js?v=1" defer></script>'
MARKER = "scientists-profiles-sticky.css"


def inject(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if MARKER in text and "daab-profiles-sticky.js" in text:
        print(f"ok: {path.relative_to(ROOT)}")
        return

    if MARKER not in text:
        anchor = '<link href="../../css/scientists-profile-qr.css?v='
        idx = text.find(anchor)
        if idx == -1:
            raise SystemExit(f"QR css anchor not found in {path}")
        line_end = text.find("\n", idx)
        text = text[: line_end + 1] + CSS_LINK + "\n" + text[line_end + 1 :]

    if "daab-profiles-sticky.js" not in text:
        anchor = '<script src="../../js/daab-breadcrumbs.js'
        idx = text.find(anchor)
        if idx == -1:
            raise SystemExit(f"breadcrumbs script anchor not found in {path}")
        line_end = text.find("\n", idx)
        text = text[: line_end + 1] + JS_SCRIPT + "\n" + text[line_end + 1 :]

    text = re.sub(
        r"scroll-margin-top:\s*calc\(var\(--daab-nav-height[^)]+\)[^;]*;",
        "scroll-margin-top: calc(var(--daab-profiles-chrome-height, var(--daab-sticky-top-stack, var(--daab-nav-height, 86px))) + 1.25rem);",
        text,
    )

    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"updated: {path.relative_to(ROOT)}")


def main() -> None:
    for p in (AZ_SCIENTISTS_PROFILES, EN_SCIENTISTS_PROFILES):
        inject(p)


if __name__ == "__main__":
    main()
