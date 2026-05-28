#!/usr/bin/env python3
"""Export DAAB-Website-User-Manual.md to Word and PDF."""
from __future__ import annotations

import sys

from _paths import ROOT
from daab_docx_export import export_markdown_to_docx
from _export_markdown_to_pdf import export_markdown_to_pdf

MD = ROOT / "documents" / "DAAB-Website-User-Manual.md"
DOCX = ROOT / "documents" / "docx" / "DAAB-Website-User-Manual.docx"
PDF = ROOT / "documents" / "pdf" / "DAAB-Website-User-Manual.pdf"


def main() -> int:
    if not MD.is_file():
        print(f"Missing {MD}", file=sys.stderr)
        return 1
    export_markdown_to_docx(MD, DOCX)
    print(f"  Word: {DOCX.relative_to(ROOT)}")
    export_markdown_to_pdf(MD, PDF)
    print(f"  PDF:  {PDF.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
