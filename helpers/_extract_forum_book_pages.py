"""Extract forum book PDF text for book pages 24–115 and 176–203."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pypdf import PdfReader

PDF = ROOT / "forum_2024" / "Forum_haqqinda_kitab_ (27.04.2026).pdf"
OUT = ROOT / "data" / "forum-2024-extract.json"

# Book page → PDF index (from printed headers in the PDF).
RANGE_MAIN = (13, 58)   # book ~24–114
RANGE_IMPRESSIONS = (89, 101)  # book ~176–203

HEADER_RE = re.compile(
    r"^\d+\s+\d+\s*\n?"
    r"XARİCDƏ YAŞAYAN AZƏRBAYCANLI ALİMLƏRİN FORUMU.*?\n",
    re.IGNORECASE | re.DOTALL,
)
FOOTER_RE = re.compile(r"9–11 sentyabr 2024.*$", re.IGNORECASE | re.DOTALL)


def clean_page(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = HEADER_RE.sub("", text.strip())
    text = FOOTER_RE.sub("", text).strip()
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text


def extract_range(reader: PdfReader, start: int, end: int) -> str:
    chunks: list[str] = []
    for i in range(start - 1, end):
        chunks.append(clean_page(reader.pages[i].extract_text() or ""))
    return "\n\n".join(c for c in chunks if c)


def split_sections(text: str, markers: list[tuple[str, str]]) -> list[dict]:
    """Split on marker regex; first section uses preamble before first marker."""
    sections: list[dict] = []
    positions: list[tuple[int, str, str]] = []
    for sid, title, pattern in markers:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            positions.append((m.start(), sid, title))
    positions.sort(key=lambda x: x[0])
    if not positions:
        return [{"id": "content", "title": "Məzmun", "body": text.strip()}]
    for idx, (start, sid, title) in enumerate(positions):
        end = positions[idx + 1][0] if idx + 1 < len(positions) else len(text)
        body = text[start:end].strip()
        body = re.sub(rf"^{re.escape(title)}\s*", "", body, flags=re.IGNORECASE).strip()
        if body:
            sections.append({"id": sid, "title": title, "body": body})
    return sections


MAIN_MARKERS = [
    (
        "president",
        "Prezidentin müraciəti",
        r"CƏNAB İLHAM ƏLİYEVİN\s+İŞTİRAKÇILARA MÜRACİƏTİ",
    ),
    ("nobel-sancar", "Əziz Sancarın müraciəti", r"ƏZİZ SANCARIN İŞTİRAKÇILARA MÜRACİƏTİ"),
    ("nobel-varshel", "Arye Varşelin müraciəti", r"ARYE VARŞELİN İŞTİRAKÇILARA MÜRACİƏTİ"),
    (
        "scientists-appeal",
        "Alimlərimizin müraciəti",
        r"ALİMLƏRİMİZİN AZƏRBAYCAN RESPUBLİKASININ PREZİDENTİ",
    ),
    ("program", "Forumun proqramı", r"FORUMUN PROQRAMI"),
    ("muradov", "Fuad Muradovun nitqi", r"Fuad Muradov"),
    ("efendiyev", "Məsud Əfəndiyevin nitqi", r"Məsud Əfəndiyev"),
    ("rectors", "Rektorların nitqləri", r"Ceyran MAHMUDOV"),
    ("diaspora-science", "Elmi diasporun təşkilatlanması", r"Elmi diasporun təşkilatlanması|İsa HƏBİBBƏYLİ"),
    ("roadmap", "Elm və təhsil yol xəritəsi", r"yol xəritəsi|Rasim ƏLİQULİYEV"),
    ("presentations-intro", "Foruma təqdim olunmuş məruzələr", r"FORUMA TƏQDİM OLUNMUŞ"),
]

IMPRESSION_MARKERS = [
    ("impressions", "Forum haqqında təəssüratlar", r"FORUM HAQQINDA TƏƏSSÜRATLAR"),
]


def main() -> None:
    reader = PdfReader(str(PDF))
    main_text = extract_range(reader, *RANGE_MAIN)
    impressions_text = extract_range(reader, *RANGE_IMPRESSIONS)
    payload = {
        "source": str(PDF.relative_to(ROOT)),
        "bookPages": {"main": "24–115", "impressions": "176–203"},
        "pdfPages": {"main": list(RANGE_MAIN), "impressions": list(RANGE_IMPRESSIONS)},
        "main": split_sections(main_text, MAIN_MARKERS),
        "impressionsRaw": impressions_text,
        "impressions": split_sections(impressions_text, IMPRESSION_MARKERS),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")
    print(f"  main sections: {len(payload['main'])}")
    print(f"  impressions chars: {len(impressions_text)}")


if __name__ == "__main__":
    main()
