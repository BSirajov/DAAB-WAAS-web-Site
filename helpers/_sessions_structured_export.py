#!/usr/bin/env python3
"""Export structured session sections from the Word source (maintenance helper)."""
from __future__ import annotations

import json

from docx import Document

from _build_sessions_preview import (
    DOCX,
    find_heading_index,
    parse_structured_section,
)
from _paths import ROOT


def main() -> None:
    doc = Document(str(DOCX))
    paras = doc.paragraphs
    start_strategi = find_heading_index(
        paras,
        "STRATEJİ PLANLAŞDIRMA İSTİQAMƏTLƏRİ",
        heading_only=True,
    )
    start_elm = find_heading_index(
        paras,
        "ELM SAHƏLƏRİ ÜZRƏ TÖVSİYƏ OLUNAN MÜZAKİRƏ MÖVZULARI",
        heading_only=True,
    )
    if start_strategi < 0 or start_elm < 0:
        raise SystemExit("Could not locate structured section headings in docx.")

    sections = {
        "strategi-planlasdirma": parse_structured_section(
            paras, start_strategi, start_elm, nested_lists=False
        ),
        "elm-saheleri-tovsiyeler": parse_structured_section(
            paras, start_elm, len(paras), nested_lists=True
        ),
    }
    out = ROOT / "helpers" / "data" / "sessions_structured_az.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(sections, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
