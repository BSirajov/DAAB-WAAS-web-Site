"""Inject daab-hero-summary.css link after the first </style> in pages with summary boxes."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKER = "daab-hero-summary.css"
LINK_TEMPLATE = '<link href="{href}" rel="stylesheet"/>'
SUMMARY_MARKERS = (
    "hero-panel",
    "hero-summary-panel",
    "activities-summary-panel",
    "panel-card",
    "hero-summary-card",
    "activities-summary-card",
)


def css_href_for(path: Path, text: str) -> str:
    m = re.search(r'data-daab-asset-root="([^"]*)"', text)
    if m:
        root = m.group(1)
        return f"{root}css/{MARKER}?v=1"
    rel = path.relative_to(ROOT).as_posix()
    if rel.startswith(("az/scientists/", "en/scientists/")):
        return f"../../css/{MARKER}?v=1"
    if rel.startswith(("az/", "en/")):
        return f"../css/{MARKER}?v=1"
    return f"css/{MARKER}?v=1"


def inject(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        return False
    if not any(m in text for m in SUMMARY_MARKERS):
        return False
    href = css_href_for(path, text)
    link = LINK_TEMPLATE.format(href=href)
    idx = text.lower().find("</style>")
    if idx == -1:
        # Fallback: after daab-mobile.css
        m = re.search(
            r'(<link[^>]+daab-mobile\.css[^>]*>)',
            text,
            re.I,
        )
        if not m:
            return False
        insert_at = m.end()
        new_text = text[:insert_at] + "\n" + link + text[insert_at:]
    else:
        insert_at = idx + len("</style>")
        new_text = text[:insert_at] + "\n" + link + text[insert_at:]
    path.write_text(new_text, encoding="utf-8", newline="\n")
    return True


def main() -> None:
    updated: list[str] = []
    for path in sorted(ROOT.rglob("*.html")):
        if "node_modules" in path.parts:
            continue
        if inject(path):
            updated.append(path.relative_to(ROOT).as_posix())
    print(f"Updated {len(updated)} file(s):")
    for name in updated:
        print(f"  {name}")


if __name__ == "__main__":
    main()
