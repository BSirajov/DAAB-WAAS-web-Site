#!/usr/bin/env python3
"""
Convert all Markdown files in documents/ to publication-ready Word files in documents/docx/.
"""
from __future__ import annotations

import sys
from pathlib import Path

try:
    from _paths import ROOT
except ImportError:
    ROOT = Path(__file__).resolve().parents[1]

from daab_docx_export import export_markdown_to_docx

DOCS_DIR = ROOT / "documents"
OUT_DIR = DOCS_DIR / "docx"


def collect_markdown_files() -> list[Path]:
    files = sorted(DOCS_DIR.glob("*.md"), key=lambda p: p.name.lower())
    seen: set[str] = set()
    unique: list[Path] = []
    for path in files:
        key = path.name.lower()
        if key in seen:
            continue
        seen.add(key)
        unique.append(path)
    return unique


def main() -> int:
    md_files = collect_markdown_files()
    if not md_files:
        print("No .md files found in documents/", file=sys.stderr)
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ok = 0
    failed: list[str] = []

    print(f"Exporting {len(md_files)} document(s) to {OUT_DIR.relative_to(ROOT)}/\n")

    for md_path in md_files:
        docx_name = md_path.stem + ".docx"
        docx_path = OUT_DIR / docx_name
        try:
            export_markdown_to_docx(md_path, docx_path)
            rel = docx_path.relative_to(ROOT)
            print(f"  OK  {rel}")
            ok += 1
        except Exception as exc:
            failed.append(f"{md_path.name}: {exc}")
            print(f"  FAIL {md_path.name}: {exc}", file=sys.stderr)

    print(f"\nDone: {ok}/{len(md_files)} written.")
    if failed:
        print("Failures:", file=sys.stderr)
        for msg in failed:
            print(f"  - {msg}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
