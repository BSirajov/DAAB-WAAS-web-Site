#!/usr/bin/env python3
"""Export Forum 2024 Strategic Implementation Framework to Word (uses shared DAAB template)."""
from __future__ import annotations

from pathlib import Path

try:
    from _paths import ROOT
except ImportError:
    ROOT = Path(__file__).resolve().parents[1]

from daab_docx_export import export_markdown_to_docx

MD_SOURCE = ROOT / "documents" / "DAAB-Forum-2024-Strategic-Implementation-Framework.md"
DOCX_OUT = ROOT / "documents" / "docx" / "DAAB-Forum-2024-Strategic-Implementation-Framework.docx"
# Legacy path (repo root documents/) for backward compatibility
DOCX_LEGACY = ROOT / "documents" / "DAAB-Forum-2024-Strategic-Implementation-Framework.docx"


def main() -> None:
    if not MD_SOURCE.exists():
        raise FileNotFoundError(MD_SOURCE)
    export_markdown_to_docx(MD_SOURCE, DOCX_OUT)
    export_markdown_to_docx(MD_SOURCE, DOCX_LEGACY)
    print(f"Wrote {DOCX_OUT.relative_to(ROOT)}")
    print(f"Wrote {DOCX_LEGACY.relative_to(ROOT)} (legacy copy)")


if __name__ == "__main__":
    main()
