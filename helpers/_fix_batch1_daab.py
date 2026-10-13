# -*- coding: utf-8 -*-
"""Normalize DAAB section headings and re-apply DAAB tables for batch1 edge cases."""
from __future__ import annotations

import json
import re
import sys
from copy import deepcopy
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _cv_az_lib import AZ_CV_DIR, apply_cv, extract_cv, iter_blocks, set_paragraph_text
from _normalize_cv_contact_links import set_cell_text

DAAB_HEADING_RE = re.compile(r"^daab\b", re.I)
OUT = json.loads(
    Path(__file__).with_name("_cv_az_batch1_out.json").read_text(encoding="utf-8")
)


def _trim_table(table, n_rows: int) -> None:
    while len(table.rows) > n_rows:
        table._tbl.remove(table.rows[-1]._tr)


def _ensure_rows(table, n_rows: int) -> None:
    while len(table.rows) < n_rows:
        row = table.rows[0]
        table._tbl.append(deepcopy(row._tr))


def fix_one(base: str) -> list[str]:
    item = next(x for x in OUT if x["base"] == base)
    path = AZ_CV_DIR / item["az_file"]
    doc = Document(str(path))
    changes: list[str] = []

    # Rename any DAAB* heading to canonical
    for kind, obj in iter_blocks(doc):
        if kind != "p":
            continue
        text = (obj.text or "").strip()
        if DAAB_HEADING_RE.match(text) and text != "DAAB-da iştirak":
            set_paragraph_text(obj, "DAAB-da iştirak")
            changes.append(f"heading:{text!r}->DAAB-da iştirak")

    # Find DAAB table and rewrite rows exactly
    daab = next(
        t for t in item["tables"] if (t.get("section") or "").lower().startswith("daab")
    )
    blocks = list(iter_blocks(doc))
    for i, (kind, obj) in enumerate(blocks):
        if kind != "p":
            continue
        text = (obj.text or "").strip()
        if text != "DAAB-da iştirak":
            continue
        if i + 1 >= len(blocks) or blocks[i + 1][0] != "t":
            continue
        table = blocks[i + 1][1]
        rows = daab["rows"]
        _ensure_rows(table, len(rows))
        _trim_table(table, len(rows))
        for r_i, row_vals in enumerate(rows):
            row = table.rows[r_i]
            # ensure column count by writing into existing cells only
            for c_i, val in enumerate(row_vals):
                if c_i >= len(row.cells):
                    break
                if row.cells[c_i].text.strip() != val:
                    set_cell_text(row.cells[c_i], val)
                    changes.append(f"daab.r{r_i}c{c_i}")
        break

    if changes:
        tmp = path.with_name(f"__tmp_daab_{path.name}")
        doc.save(str(tmp))
        tmp.replace(path)

    # Re-apply full edit (header/profile/other tables) for consistency
    edit = {
        "header": item["header"],
        "profile": item["profile"],
        "tables": item["tables"],
    }
    more = apply_cv(path, edit)
    changes.extend(more)
    return changes


def main() -> None:
    for base in ["Ibrahimov_Rovshan", "Isayeva_Aygul"]:
        ch = fix_one(base)
        cur = extract_cv(AZ_CV_DIR / next(x["az_file"] for x in OUT if x["base"] == base))
        secs = [t["section"] for t in cur["tables"]]
        print(base, "changes", len(ch), "sections", secs)
        daab = [t for t in cur["tables"] if (t["section"] or "").lower().startswith("daab")]
        print("  daab rows", daab[0]["rows"] if daab else None)


if __name__ == "__main__":
    main()
