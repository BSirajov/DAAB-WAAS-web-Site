#!/usr/bin/env python3
"""Report non-ASCII characters in image paths referenced from deploy HTML."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from _paths import ROOT

REF_RE = re.compile(r'(?:src|href)=["\']([^"\']+)["\']', re.I)
SKIP_PARTS = {"Deployment", "documents", "helpers", "templates", "cv"}


def iter_deploy_html() -> list[Path]:
    out: list[Path] = []
    for rel in ("index.html", "404.html"):
        p = ROOT / rel
        if p.is_file():
            out.append(p)
    for folder in ("az", "en"):
        base = ROOT / folder
        if base.is_dir():
            out.extend(sorted(base.rglob("*.html")))
    return out


def is_non_ascii_image_ref(ref: str) -> bool:
    if not ref.startswith(("../", "../../", "../../../")):
        return False
    if "/images/" not in ref.replace("\\", "/"):
        return False
    return any(ord(ch) > 127 for ch in ref)


def audit() -> dict[str, list[str]]:
    issues: dict[str, list[str]] = {}
    for path in iter_deploy_html():
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8")
        for match in REF_RE.finditer(text):
            ref = match.group(1).split("#")[0].split("?")[0]
            if is_non_ascii_image_ref(ref):
                rel = path.relative_to(ROOT).as_posix()
                issues.setdefault(ref, []).append(rel)
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fail-on-findings",
        action="store_true",
        help="Exit 1 when any non-ASCII image refs remain",
    )
    args = parser.parse_args()

    issues = audit()
    if not issues:
        print("Unicode image path audit OK — no non-ASCII /images/ refs in deploy HTML.")
        return 0

    print(f"Unicode image path audit — {len(issues)} unique ref(s):\n")
    for ref in sorted(issues):
        pages = sorted(set(issues[ref]))
        print(f"  {ref}")
        print(f"    pages ({len(pages)}): {', '.join(pages[:4])}" + (" …" if len(pages) > 4 else ""))
    print("\nRename assets to ASCII slugs and update refs (see _compress_images.sync_converted_refs).")
    return 1 if args.fail_on_findings else 0


if __name__ == "__main__":
    sys.exit(main())
