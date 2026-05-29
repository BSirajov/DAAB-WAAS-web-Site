#!/usr/bin/env python3
"""Report CSS class selectors not found in HTML under given paths.

Usage:
    python helpers/_audit_css_usage.py css/daab-forum-book.css az/forum en/forum
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from _paths import ROOT

CLASS_RE = re.compile(r"\.([a-zA-Z_][\w-]*)")
SKIP_CLASS_NAMES = frozenset({"html", "jpg", "jpeg", "png", "svg", "webp", "gif"})


def extract_css_classes(css_path: Path) -> set[str]:
    text = css_path.read_text(encoding="utf-8", errors="replace")
    classes: set[str] = set()
    for m in CLASS_RE.finditer(text):
        name = m.group(1)
        if name.startswith("daab-"):
            continue
        if name in SKIP_CLASS_NAMES:
            continue
        classes.add(name)
    return classes


def collect_html(paths: list[Path]) -> str:
    chunks: list[str] = []
    for base in paths:
        if base.is_file() and base.suffix == ".html":
            chunks.append(base.read_text(encoding="utf-8", errors="replace"))
            continue
        if base.is_dir():
            for html in base.rglob("*.html"):
                chunks.append(html.read_text(encoding="utf-8", errors="replace"))
    js_dir = ROOT / "js"
    if js_dir.is_dir():
        for js in js_dir.glob("*.js"):
            chunks.append(js.read_text(encoding="utf-8", errors="replace"))
    return "\n".join(chunks)


def class_referenced(cls: str, blob: str) -> bool:
    if re.search(rf'\bclass=["\'][^"\']*\b{re.escape(cls)}\b', blob):
        return True
    if re.search(rf'classList\.(?:add|remove|toggle)\(["\']{re.escape(cls)}["\']', blob):
        return True
    return False


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print(__doc__.strip(), file=sys.stderr)
        return 1

    css_path = ROOT / argv[1]
    html_roots = [ROOT / p for p in argv[2:]]

    if not css_path.is_file():
        print(f"CSS not found: {css_path}", file=sys.stderr)
        return 1

    classes = extract_css_classes(css_path)
    html = collect_html(html_roots)

    unused: list[str] = []
    used: list[str] = []
    for cls in sorted(classes):
        if class_referenced(cls, html):
            used.append(cls)
        else:
            unused.append(cls)

    print(f"CSS: {css_path.relative_to(ROOT)}")
    print(f"HTML roots: {', '.join(str(p.relative_to(ROOT)) for p in html_roots)}")
    print(f"Classes in CSS: {len(classes)}  used in HTML: {len(used)}  unused: {len(unused)}")
    if unused:
        print("\nUnused (not in HTML class attributes):")
        for name in unused[:60]:
            print(f"  - .{name}")
        if len(unused) > 60:
            print(f"  … and {len(unused) - 60} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
