"""Remove participants panel CSS/JS from Forum 2024 inner pages (hub keeps static panel)."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

CSS_RE = re.compile(
    r'<link href="\.\./\.\./\.\./css/daab-forum-participants-panel\.css\?v=\d+" rel="stylesheet"/>'
)
JS_RE = re.compile(
    r'<script src="\.\./\.\./\.\./js/forum-participants-panel\.js\?v=\d+" defer></script>'
)


def strip_panel_assets(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    new_text = JS_RE.sub("", text)
    new_text = CSS_RE.sub("", new_text)
    if new_text == text:
        return False
    path.write_text(new_text, encoding="utf-8", newline="\n")
    return True


def main() -> None:
    count = 0
    for lang in ("az", "en"):
        for path in sorted((ROOT / lang / "forum" / "2024").glob("*.html")):
            if path.name == "index.html":
                continue
            if strip_panel_assets(path):
                print(f"stripped {path.relative_to(ROOT)}")
                count += 1
    print(f"done: {count} files updated")


if __name__ == "__main__":
    main()
