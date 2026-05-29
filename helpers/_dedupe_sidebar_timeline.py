#!/usr/bin/env python3
"""Remove duplicate sidebar timeline inline scripts; use daab-sidebar-timeline.js."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

INLINE_RE = re.compile(
    r"<script>\s*\(function\s*\(\)\s*\{"
    r"[\s\S]*?"
    r"const links = Array\.from\(document\.querySelectorAll\('\.timeline-list a\[href\^=\"#\"\]'\)\);"
    r"[\s\S]*?"
    r"onScroll\(\);\s*"
    r"\}\)\(\);\s*</script>\s*",
    re.MULTILINE,
)

SCRIPT_TAG = '<script src="{root}js/daab-sidebar-timeline.js?v=2" defer></script>'

# Pages with bespoke sidebar logic — do not inject shared timeline script.
SKIP_PAGE_IDS = frozenset({"charter", "forum-photos-gallery"})


def js_root(path: Path) -> str:
    rel = path.relative_to(ROOT)
    depth = len(rel.parts) - 1
    return "../" * depth


def has_external_timeline(html: str) -> bool:
    return "daab-sidebar-timeline.js" in html


def has_timeline_list(html: str) -> bool:
    return 'class="timeline-list"' in html or "class='timeline-list'" in html


def page_id(html: str) -> str:
    m = re.search(r'data-daab-page-id="([^"]+)"', html)
    return m.group(1) if m else ""


def process(html: str, path: Path) -> tuple[str, bool]:
    if page_id(html) in SKIP_PAGE_IDS:
        return html, False
    if not has_timeline_list(html):
        return html, False

    original = html
    html = INLINE_RE.sub("", html)

    if not has_external_timeline(html):
        root = js_root(path)
        tag = SCRIPT_TAG.format(root=root)
        if "</body>" in html:
            html = html.replace("</body>", f"{tag}\n</body>", 1)
        else:
            html = html + "\n" + tag + "\n"

    return html, html != original


def main() -> None:
    targets: list[Path] = []
    for base in (ROOT / "az", ROOT / "en"):
        if not base.is_dir():
            continue
        for path in base.rglob("*.html"):
            if path.parent.name == "application":
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            if INLINE_RE.search(text) or (
                has_timeline_list(text) and not has_external_timeline(text)
            ):
                targets.append(path)

    updated: list[str] = []
    for path in sorted(set(targets)):
        text = path.read_text(encoding="utf-8", errors="replace")
        new_text, changed = process(text, path)
        if changed:
            path.write_text(new_text, encoding="utf-8", newline="\n")
            updated.append(str(path.relative_to(ROOT)))

    if updated:
        print(f"Updated {len(updated)} file(s):")
        for line in updated:
            print(f"  - {line}")
    else:
        print("No duplicate sidebar timeline scripts found.")

    leftover = 0
    for path in (ROOT / "az").rglob("*.html"):
        if path.parent.name == "application":
            continue
        t = path.read_text(encoding="utf-8", errors="replace")
        if INLINE_RE.search(t):
            leftover += 1
    for path in (ROOT / "en").rglob("*.html"):
        if path.parent.name == "application":
            continue
        t = path.read_text(encoding="utf-8", errors="replace")
        if INLINE_RE.search(t):
            leftover += 1
    if leftover:
        raise SystemExit(f"Warning: {leftover} page(s) still have inline timeline blocks (charter?)")


if __name__ == "__main__":
    main()
