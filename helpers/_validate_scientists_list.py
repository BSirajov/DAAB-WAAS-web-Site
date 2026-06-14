#!/usr/bin/env python3
"""Validate scientists list pages use external catalog JS (no inline DATA drift)."""
from __future__ import annotations

import re
import sys

from _paths import ROOT

INLINE_DATA_RE = re.compile(r"\bconst\s+DATA\s*=")


def check_list(lang: str) -> list[str]:
    path = ROOT / lang / "scientists" / "list.html"
    if not path.is_file():
        return [f"missing {path.relative_to(ROOT)}"]
    text = path.read_text(encoding="utf-8")
    issues: list[str] = []
    expected_js = (
        "scientists-catalog-data.js"
        if lang == "az"
        else "scientists-catalog-data-en.js"
    )
    if expected_js not in text:
        issues.append(f"{path.relative_to(ROOT)}: missing script {expected_js}")
    if INLINE_DATA_RE.search(text):
        issues.append(f"{path.relative_to(ROOT)}: inline const DATA — use {expected_js} only")
    return issues


def main() -> int:
    issues: list[str] = []
    for lang in ("az", "en"):
        issues.extend(check_list(lang))
    if issues:
        print("Scientists list validation FAILED:")
        for item in issues:
            print(f"  - {item}")
        return 1
    print("Scientists list validation OK (external catalog JS, no inline DATA)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
