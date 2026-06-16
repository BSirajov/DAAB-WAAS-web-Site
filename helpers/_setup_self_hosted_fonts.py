#!/usr/bin/env python3
"""Download Inter + Playfair Display woff2 files and wire css/daab-fonts.css."""
from __future__ import annotations

import re
import urllib.request
from pathlib import Path

from _paths import ROOT

FONTS_DIR = ROOT / "fonts"
CSS_OUT = ROOT / "css" / "daab-fonts.css"

# Trimmed set: drop Inter 800 if Playfair covers display heavy weights.
FONT_CSS_URL = (
    "https://fonts.googleapis.com/css2?"
    "family=Inter:wght@400;500;600;700;800&"
    "family=Playfair+Display:wght@700;800&display=swap"
)
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

LOCAL_FONT_LINK = '<link href="{root}css/daab-fonts.css?v={version}" rel="stylesheet"/>'

GOOGLE_BLOCK = re.compile(
    r'<link href="https://fonts\.googleapis\.com" rel="preconnect"\s*/>\s*'
    r'<link crossorigin="" href="https://fonts\.gstatic\.com" rel="preconnect"\s*/>\s*'
    r'<link href="https://fonts\.googleapis\.com/css2\?[^"]+" rel="stylesheet"\s*/>',
    re.I,
)
GOOGLE_BLOCK_ALT = re.compile(
    r'<link rel="preconnect" href="https://fonts\.googleapis\.com"\s*/>\s*'
    r'<link rel="preconnect" href="https://fonts\.gstatic\.com"(?:\s+crossorigin(?:="")?)?\s*/>\s*'
    r'(?:<link href="https://fonts\.googleapis\.com/css2\?[^"]+" rel="stylesheet"\s*/>\s*)?',
    re.I,
)


def fetch_google_css() -> str:
    req = urllib.request.Request(FONT_CSS_URL, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read().decode("utf-8")


def download_fonts(css_text: str) -> tuple[str, list[str]]:
    FONTS_DIR.mkdir(parents=True, exist_ok=True)
    faces = re.findall(r"@font-face\s*\{[^}]+\}", css_text, re.I | re.S)
    local_css_parts: list[str] = [
        "/* Self-hosted Inter + Playfair Display — replaces Google Fonts CSS */",
        "",
    ]
    downloaded: list[str] = []

    for face in faces:
        url_m = re.search(r"url\((https://fonts\.gstatic\.com/[^)]+)\)", face)
        if not url_m:
            continue
        url = url_m.group(1)
        filename = url.split("/")[-1].split("?")[0]
        dest = FONTS_DIR / filename
        if not dest.is_file():
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=60) as resp:
                dest.write_bytes(resp.read())
        downloaded.append(filename)
        local_face = re.sub(
            r"url\((https://fonts\.gstatic\.com/[^)]+)\)",
            f'url("../fonts/{filename}")',
            face,
        )
        local_css_parts.append(local_face)
        local_css_parts.append("")

    return "\n".join(local_css_parts), downloaded


def replace_font_links_in_html(text: str, *, css_root: str, version: int) -> str:
    local = LOCAL_FONT_LINK.format(root=css_root, version=version)
    text, n1 = GOOGLE_BLOCK.subn(local + "\n", text)
    text, n2 = GOOGLE_BLOCK_ALT.subn(local + "\n", text)
    if n1 + n2 == 0 and "daab-fonts.css" not in text:
        # gateway pages with different formatting
        text = re.sub(
            r'<link href="https://fonts\.googleapis\.com/css2\?[^"]+" rel="stylesheet"\s*/>',
            local,
            text,
            count=1,
        )
    return text


def patch_deploy_html(version: int = 1) -> int:
    targets = [ROOT / "index.html", ROOT / "404.html"]
    for base in (ROOT / "az", ROOT / "en"):
        targets.extend(sorted(base.rglob("*.html")))
    changed = 0
    for path in targets:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if "fonts.googleapis.com/css2" not in text and "daab-fonts.css" in text:
            continue
        depth = len(path.relative_to(ROOT).parts) - 1
        css_root = "../" * depth if depth else ""
        new_text = replace_font_links_in_html(text, css_root=css_root, version=version)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8", newline="\n")
            changed += 1
    return changed


def main() -> int:
    print("Fetching Google Fonts CSS…")
    css_text = fetch_google_css()
    print("Downloading woff2 files…")
    local_css, files = download_fonts(css_text)
    CSS_OUT.write_text(local_css, encoding="utf-8", newline="\n")
    print(f"Wrote {CSS_OUT.relative_to(ROOT)} ({len(files)} files in fonts/)")
    n = patch_deploy_html(version=1)
    print(f"Updated {n} HTML page(s) to use daab-fonts.css")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
