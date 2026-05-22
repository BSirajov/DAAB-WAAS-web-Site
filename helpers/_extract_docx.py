"""Extract paragraph text from the forum book DOCX."""
from __future__ import annotations

from pathlib import Path

from docx import Document

from _paths import ROOT

DOCX_PATH = ROOT / "documents" / "Forum_haqqinda_kitab_ (24.04.2026_4.0).docx"
OUT_PATH = ROOT / "_docx_extract.txt"


def main() -> None:
    doc = Document(str(DOCX_PATH))
    lines: list[str] = []
    for p in doc.paragraphs:
        text = p.text.replace("\r", "").strip()
        if text:
            lines.append(text)
    OUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"paragraphs {len(lines)}")
    print(f"written {OUT_PATH} chars {OUT_PATH.stat().st_size}")


if __name__ == "__main__":
    main()
