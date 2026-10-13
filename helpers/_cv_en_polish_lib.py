# -*- coding: utf-8 -*-
"""Extract / apply English CV polish for header, profile, and non-publication tables."""
from __future__ import annotations

import json
import re
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph

ROOT = Path(__file__).resolve().parents[1]
EN_CV_DIR = ROOT / "en" / "scientists" / "CV" / "Word"

PUBLICATION_HEADINGS = re.compile(
    r"^(publications|books?\b|book chapters|peer-reviewed|conference papers|"
    r"invited talks|patents?\b|software\b)",
    re.I,
)
EDITABLE_TABLE_HEADINGS = re.compile(
    r"^(education|academic and professional positions|awards|"
    r"grants and research projects|research metrics|teaching|supervision|"
    r"languages|participation in daab)",
    re.I,
)
CONTACT_HEADING = re.compile(r"^contact\b", re.I)
PROFILE_HEADING = re.compile(r"^profile summary\b", re.I)
SECTION_HEADING = re.compile(
    r"^(contact\b|profile summary\b|education\b|academic and professional|"
    r"awards\b|grants\b|research metrics\b|teaching\b|supervision\b|"
    r"languages\b|participation in daab|publications\b|books?\b|"
    r"book chapters\b|peer-reviewed|conference papers|invited talks|"
    r"patents?\b|date of last update)",
    re.I,
)

META_PHRASE_RE = re.compile(
    r"\b("
    r"the cv (states|lists|gives|reports|mentions|does not|notes|spells|title is)|"
    r"the employment record (states|says|lists)|"
    r"year not stated|"
    r"years? not (stated|given)|"
    r"without titles|"
    r"are mentioned, without|"
    r"the dissertation is recorded|"
    r"postgraduate study is recorded"
    r")\b",
    re.I,
)


def iter_blocks(doc: Document):
    for child in doc.element.body.iterchildren():
        if child.tag == qn("w:p"):
            yield ("p", Paragraph(child, doc))
        elif child.tag == qn("w:tbl"):
            yield ("t", Table(child, doc))


def set_paragraph_text(paragraph: Paragraph, text: str) -> None:
    runs = paragraph.runs
    if runs:
        runs[0].text = text
        for run in runs[1:]:
            run.text = ""
    else:
        paragraph.add_run(text)


def set_cell_text_keep_links_if_url(cell, new_text: str, old_text: str) -> None:
    """Replace cell text. If value looks like a URL and matches old, leave alone."""
    if new_text == old_text:
        return
    # Prefer simple text replace; contact URLs are handled elsewhere and usually unchanged.
    paragraphs = cell.paragraphs
    if not paragraphs:
        cell.add_paragraph(new_text)
        return
    set_paragraph_text(paragraphs[0], new_text)
    for extra in paragraphs[1:]:
        set_paragraph_text(extra, "")


def extract_cv(path: Path) -> dict:
    doc = Document(str(path))
    blocks = list(iter_blocks(doc))

    header: list[str] = []
    profile = ""
    tables: list[dict] = []
    in_publications = False
    current_section = ""

    i = 0
    # Header: paragraphs before Contact
    while i < len(blocks):
        kind, obj = blocks[i]
        if kind == "p":
            text = (obj.text or "").strip()
            if CONTACT_HEADING.match(text):
                break
            if text:
                header.append(text)
        i += 1

    # Walk remaining for profile + editable tables
    while i < len(blocks):
        kind, obj = blocks[i]
        if kind == "p":
            text = (obj.text or "").strip()
            if not text:
                i += 1
                continue
            if SECTION_HEADING.match(text) or PUBLICATION_HEADINGS.match(text):
                current_section = text
                if PUBLICATION_HEADINGS.match(text):
                    in_publications = True
                elif EDITABLE_TABLE_HEADINGS.match(text) or PROFILE_HEADING.match(text) or CONTACT_HEADING.match(text):
                    in_publications = False
                if PROFILE_HEADING.match(text):
                    # next non-empty paragraph is profile body
                    j = i + 1
                    while j < len(blocks):
                        k2, o2 = blocks[j]
                        if k2 == "p":
                            t2 = (o2.text or "").strip()
                            if t2 and not SECTION_HEADING.match(t2):
                                profile = t2
                                break
                            if t2 and SECTION_HEADING.match(t2):
                                break
                        elif k2 == "t":
                            break
                        j += 1
            i += 1
            continue

        # table
        if in_publications or CONTACT_HEADING.match(current_section):
            i += 1
            continue
        if not EDITABLE_TABLE_HEADINGS.match(current_section):
            i += 1
            continue

        rows = []
        for r_i, row in enumerate(obj.rows):
            cells = [c.text.strip() for c in row.cells]
            rows.append(cells)
        tables.append({"section": current_section, "rows": rows})
        i += 1

    return {
        "file": path.name,
        "header": header,
        "profile": profile,
        "tables": tables,
        "needs_meta_cleanup": bool(META_PHRASE_RE.search(profile)),
    }


def apply_cv(path: Path, edit: dict) -> list[str]:
    """Apply header/profile/table text edits. Returns change log lines."""
    doc = Document(str(path))
    blocks = list(iter_blocks(doc))
    changes: list[str] = []

    new_header = edit.get("header")
    new_profile = edit.get("profile")
    new_tables = edit.get("tables")  # list aligned with extract order

    # Header paragraphs before Contact
    hi = 0
    i = 0
    while i < len(blocks):
        kind, obj = blocks[i]
        if kind == "p":
            text = (obj.text or "").strip()
            if CONTACT_HEADING.match(text):
                break
            if text and new_header is not None and hi < len(new_header):
                if text != new_header[hi]:
                    set_paragraph_text(obj, new_header[hi])
                    changes.append(f"header[{hi}]")
                hi += 1
        i += 1

    in_publications = False
    current_section = ""
    table_idx = 0

    while i < len(blocks):
        kind, obj = blocks[i]
        if kind == "p":
            text = (obj.text or "").strip()
            if text and (SECTION_HEADING.match(text) or PUBLICATION_HEADINGS.match(text)):
                current_section = text
                if PUBLICATION_HEADINGS.match(text):
                    in_publications = True
                elif EDITABLE_TABLE_HEADINGS.match(text) or PROFILE_HEADING.match(text) or CONTACT_HEADING.match(text):
                    in_publications = False
                if PROFILE_HEADING.match(text) and new_profile is not None:
                    j = i + 1
                    while j < len(blocks):
                        k2, o2 = blocks[j]
                        if k2 == "p":
                            t2 = (o2.text or "").strip()
                            if t2 and not SECTION_HEADING.match(t2):
                                if t2 != new_profile:
                                    set_paragraph_text(o2, new_profile)
                                    changes.append("profile")
                                break
                            if t2 and SECTION_HEADING.match(t2):
                                break
                        elif k2 == "t":
                            break
                        j += 1
            i += 1
            continue

        if in_publications or CONTACT_HEADING.match(current_section):
            i += 1
            continue
        if not EDITABLE_TABLE_HEADINGS.match(current_section):
            i += 1
            continue

        if new_tables is not None and table_idx < len(new_tables):
            edited = new_tables[table_idx]
            for r_i, row in enumerate(obj.rows):
                if r_i >= len(edited["rows"]):
                    break
                new_cells = edited["rows"][r_i]
                for c_i, cell in enumerate(row.cells):
                    if c_i >= len(new_cells):
                        break
                    old = cell.text.strip()
                    new = new_cells[c_i]
                    if old != new:
                        set_cell_text_keep_links_if_url(cell, new, old)
                        changes.append(f"table[{table_idx}].r{r_i}.c{c_i}")
        table_idx += 1
        i += 1

    if changes:
        tmp = path.with_suffix(path.suffix + ".tmp.docx")
        try:
            doc.save(str(tmp))
            tmp.replace(path)
        except OSError:
            alt = path.parent / f"__tmp_{path.name}"
            doc.save(str(alt))
            alt.replace(path)
        finally:
            if tmp.exists():
                try:
                    tmp.unlink()
                except OSError:
                    pass
    return changes


def extract_all(out_path: Path) -> list[dict]:
    items = []
    for path in sorted(EN_CV_DIR.glob("*.docx")):
        if path.name.startswith("~$"):
            continue
        items.append(extract_cv(path))
    out_path.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    return items


def apply_all(edits_path: Path) -> None:
    edits = json.loads(edits_path.read_text(encoding="utf-8"))
    for edit in edits:
        path = EN_CV_DIR / edit["file"]
        if not path.is_file():
            print("missing", edit["file"])
            continue
        changes = apply_cv(path, edit)
        if changes:
            print(f"UPDATED {edit['file']}: {', '.join(changes[:12])}" + ("…" if len(changes) > 12 else ""))
        else:
            print(f"unchanged {edit['file']}")


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--extract", type=Path)
    ap.add_argument("--apply", type=Path)
    args = ap.parse_args()
    if args.extract:
        items = extract_all(args.extract)
        meta = sum(1 for x in items if x["needs_meta_cleanup"])
        print(f"extracted {len(items)} CVs; meta_voice={meta}")
    elif args.apply:
        apply_all(args.apply)
    else:
        raise SystemExit("use --extract PATH or --apply PATH")
