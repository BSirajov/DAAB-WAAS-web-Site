#!/usr/bin/env python3
"""Replace Google Fonts URLs with self-hosted daab-fonts.css in deploy HTML, helpers, and templates."""
from __future__ import annotations

import re
from pathlib import Path

from _page_shell_assets import font_stylesheet_link, modernize_shell_source, replace_google_fonts
from _paths import ROOT

PATTERNS = (
    re.compile(
        r'<link href="https://fonts\.googleapis\.com/css2\?[^"]+" rel="stylesheet"\s*/?>',
        re.I,
    ),
    re.compile(
        r'<link href="https://fonts\.googleapis\.com" rel="preconnect"\s*/>\s*'
        r'<link crossorigin="" href="https://fonts\.gstatic\.com" rel="preconnect"\s*/>\s*'
        r'<link href="https://fonts\.googleapis\.com/css2\?[^"]+" rel="stylesheet"\s*/?>',
        re.I,
    ),
)


def normalize_html(text: str, *, css_root: str = "../") -> tuple[str, int]:
    local = font_stylesheet_link(css_root=css_root)
    count = 0

    def repl(_: re.Match[str]) -> str:
        nonlocal count
        count += 1
        return local

    new_text = text
    for pattern in PATTERNS:
        new_text, n = pattern.subn(repl, new_text)
        count += n
    new_text, n_extra = replace_google_fonts(new_text)
    count += n_extra
    return new_text, count


def collect_targets() -> list[Path]:
    targets: list[Path] = [ROOT / "index.html", ROOT / "404.html"]
    for base in (ROOT / "az", ROOT / "en"):
        if base.is_dir():
            targets.extend(sorted(base.rglob("*.html")))
    targets.extend(sorted((ROOT / "templates").glob("*.html")))
    targets.extend(sorted((ROOT / "helpers").glob("*.py")))
    return targets


def should_skip(path: Path, text: str) -> bool:
    if path.suffix == ".html":
        return "fonts.googleapis.com/css2" not in text and "daab-fonts.css" in text
    if path.suffix == ".py":
        if path.name in ("_normalize_google_fonts.py", "_setup_self_hosted_fonts.py"):
            return True
        return "fonts.googleapis.com" not in text and "daab-logo.svg" not in text
    return True


def process_file(path: Path) -> int:
    text = path.read_text(encoding="utf-8", errors="replace")
    if should_skip(path, text):
        return 0

    if path.suffix == ".html":
        depth = len(path.relative_to(ROOT).parts) - 1
        css_root = "../" * depth if depth else ""
        new_text, n = normalize_html(text, css_root=css_root)
        new_text = new_text.replace("daab-logo.svg", "daab-logo.png")
    else:
        new_text, n = modernize_shell_source(text)

    if new_text != text:
        path.write_text(new_text, encoding="utf-8", newline="\n")
    return n


def main() -> int:
    total = 0
    files = 0
    for path in collect_targets():
        if not path.is_file():
            continue
        n = process_file(path)
        if n:
            total += n
            files += 1
            print(f"  {path.relative_to(ROOT)} ({n})")

    print(f"\nNormalized shell assets in {files} file(s), {total} replacement(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
