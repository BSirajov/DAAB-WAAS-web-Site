"""Extract Complex Topics approach DOCX files in document order."""
from __future__ import annotations

import json
import re
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph

ROOT = Path(r"C:\dev\DAAB-WAAS-web-Site")
DOCS = ROOT / "documents"
OUT = Path(r"C:\Users\BSira\AppData\Local\Temp")


def para_text(p: Paragraph) -> str:
    return "".join(r.text or "" for r in p.runs).replace("\xa0", " ").strip()


def is_list(p: Paragraph) -> bool:
    pPr = p._p.pPr
    return bool(pPr is not None and pPr.numPr is not None)


def list_level(p: Paragraph) -> int:
    pPr = p._p.pPr
    if pPr is None or pPr.numPr is None:
        return 0
    ilvl = pPr.numPr.ilvl
    if ilvl is None or ilvl.val is None:
        return 0
    return int(ilvl.val)


def heading_level(style: str) -> int | None:
    if not style:
        return None
    m = re.match(r"Heading (\d+)", style, re.I)
    if m:
        return int(m.group(1))
    if style.lower() in {"title", "heading"}:
        return 0
    return None


def looks_heading(p: Paragraph, text: str) -> int | None:
    style = p.style.name if p.style else ""
    lvl = heading_level(style)
    if lvl is not None:
        return lvl
    if not text:
        return None
    # Numbered chapter titles often styled as Normal + bold
    bold = any(r.bold for r in p.runs if (r.text or "").strip())
    if bold and re.match(r"^(\d+(\.\d+){0,3}|Əlavə|Appendix|Qeyd|Note)\b", text):
        dots = text.split()[0].count(".")
        if text.startswith(("Əlavə", "Appendix")):
            return 1
        return min(dots + 1, 4)
    return None


def cell_text(cell) -> str:
    parts = []
    for p in cell.paragraphs:
        t = para_text(p)
        if t:
            parts.append(t)
    return " / ".join(parts).strip()


def table_data(table: Table) -> list[list[str]]:
    rows = []
    for row in table.rows:
        rows.append([cell_text(c) for c in row.cells])
    return rows


def extract(path: Path) -> dict:
    doc = Document(str(path))
    items = []
    for child in doc.element.body.iterchildren():
        tag = child.tag.split("}")[-1]
        if tag == "p":
            p = Paragraph(child, doc)
            text = para_text(p)
            if not text:
                continue
            style = p.style.name if p.style else ""
            items.append(
                {
                    "type": "p",
                    "style": style,
                    "text": text,
                    "list": is_list(p),
                    "list_level": list_level(p) if is_list(p) else 0,
                    "heading": looks_heading(p, text),
                    "bold": any(r.bold for r in p.runs if (r.text or "").strip()),
                }
            )
        elif tag == "tbl":
            table = Table(child, doc)
            items.append({"type": "table", "rows": table_data(table)})
        elif tag == "sdt":
            texts = [t.text for t in child.findall(".//" + qn("w:t")) if t.text]
            joined = "".join(texts).strip()
            if joined:
                items.append({"type": "sdt", "text": joined, "parts": texts})
    return {
        "file": path.name,
        "paras": sum(1 for i in items if i["type"] == "p"),
        "tables": sum(1 for i in items if i["type"] == "table"),
        "items": items,
    }


def outline(data: dict) -> list[str]:
    lines = []
    for i, item in enumerate(data["items"]):
        if item["type"] == "table":
            r, c = len(item["rows"]), len(item["rows"][0]) if item["rows"] else 0
            first = item["rows"][0][0][:60] if item["rows"] and item["rows"][0] else ""
            lines.append(f"{i:04d} TABLE {r}x{c} {first}")
        elif item["type"] == "sdt":
            lines.append(f"{i:04d} SDT {item['text'][:80]}")
        else:
            h = item["heading"]
            mark = f"H{h}" if h is not None else ("LI" if item["list"] else "P")
            lines.append(f"{i:04d} {mark:3} [{item['style']}] {item['text']}")
    return lines


def main() -> None:
    for name in (
        "Complex_Topics_Clear_Explanations_AZ.docx",
        "Complex_Topics_Clear_Explanations_EN.docx",
    ):
        data = extract(DOCS / name)
        stem = "ctce_az" if "_AZ" in name else "ctce_en"
        (OUT / f"{stem}.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        (OUT / f"{stem}_outline.txt").write_text(
            "\n".join(outline(data)), encoding="utf-8"
        )
        print(name, "items", len(data["items"]), "paras", data["paras"], "tables", data["tables"])


if __name__ == "__main__":
    main()
