#!/usr/bin/env python3
"""Remove decorative arrow glyphs from buttons and button-styled controls site-wide."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

HTML_ROOTS = (
    ROOT,
    ROOT / "az",
    ROOT / "en",
    ROOT / "sources",
)

SKIP_PARTS = {"deployment", "Deployment", "helpers", "documents", "cv", ".git", "__pycache__"}

CARD_ARROW_RE = re.compile(
    r"\s*<span\s+class=\"card-arrow\">\s*[↗→←↓↑↺]\s*</span>\s*",
    re.IGNORECASE,
)

BTN_TEXT_REPLACEMENTS = (
    (">İrəli →<", ">İrəli<"),
    (">Next →<", ">Next<"),
    (">← Geri<", ">Geri<"),
    (">← Back<", ">Back<"),
    (r"keçin →</a>", "keçin</a>"),
    (r"page →</a>", "page</a>"),
)


def should_skip(path: Path) -> bool:
    return any(part in SKIP_PARTS for part in path.parts)


def iter_html() -> list[Path]:
    out: list[Path] = []
    for base in HTML_ROOTS:
        if not base.is_dir():
            continue
        for path in base.rglob("*.html"):
            if path.is_file() and not should_skip(path):
                out.append(path)
    return sorted(set(out))


def patch_html(text: str, path: Path) -> str:
    text = CARD_ARROW_RE.sub("\n", text)
    for old, new in BTN_TEXT_REPLACEMENTS:
        text = text.replace(old, new)
    if path.name == "list.html" and "scientists" in path.as_posix():
        if path.parts[-3] == "az":
            text = text.replace("btn(page-1,'←',", "btn(page-1,'Əvvəl',")
            text = text.replace("btn(page+1,'→',", "btn(page+1,'Sonra',")
        else:
            text = text.replace("btn(page-1,'←',", "btn(page-1,'Prev',")
            text = text.replace("btn(page+1,'→',", "btn(page+1,'Next',")
    return text


def patch_js(path: Path, text: str) -> str:
    if path.name != "scientists-list-preview.js":
        return text
    return text.replace("Tam profil ↗", "Tam profil").replace(
        "View full profile ↗", "View full profile"
    )


def main() -> None:
    updated: list[str] = []

    for path in iter_html():
        original = path.read_text(encoding="utf-8")
        text = patch_html(original, path)
        if text != original:
            path.write_text(text, encoding="utf-8", newline="\n")
            updated.append(str(path.relative_to(ROOT)))

    for rel in ("js/scientists-list-preview.js",):
        path = ROOT / rel
        if not path.is_file():
            continue
        original = path.read_text(encoding="utf-8")
        text = patch_js(path, original)
        if text != original:
            path.write_text(text, encoding="utf-8", newline="\n")
            updated.append(rel)

    print(f"Updated {len(updated)} file(s):")
    for line in updated:
        print(f"  - {line}")


if __name__ == "__main__":
    main()
