# -*- coding: utf-8 -*-
"""Apply batch1 AZ out JSON to Word CVs (optionally rebuild from part modules)."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from docx import Document

from _cv_az_lib import AZ_CV_DIR, META_AZ_RE, apply_cv, ensure_awards_table, extract_cv

OUT_PATH = Path(__file__).resolve().parent / "_cv_az_batch1_out.json"
EN_PATH = Path(__file__).resolve().parent / "_cv_az_batch1_en.json"


def _norm_section(s: str) -> str:
    s = (s or "").strip().lower()
    s = re.sub(r"\s+", " ", s)
    return s


def _section_key(s: str) -> str:
    n = _norm_section(s)
    if n.startswith("təhsil"):
        return "edu"
    if n.startswith("elmi və peşəkar"):
        return "pos"
    if n.startswith("mükafatlar"):
        return "awards"
    if n.startswith("qrantlar"):
        return "grants"
    if n.startswith("elmi göstəricilər") or n.startswith("tədqiqat göstəriciləri"):
        return "metrics"
    if n.startswith("tədris"):
        return "teach"
    if n.startswith("elmi rəhbərlik") or n == "rəhbərlik" or n.startswith("rəhbərlik"):
        return "sup"
    if n.startswith("dillər"):
        return "lang"
    if n.startswith("daab"):
        return "daab"
    return n


def reorder_tables_for_doc(edit: dict, az_sections: list[str]) -> dict:
    by_key: dict[str, dict] = {}
    for t in edit.get("tables") or []:
        by_key[_section_key(t["section"])] = t
    ordered = []
    for sec in az_sections:
        k = _section_key(sec)
        if k in by_key:
            src = by_key[k]
            ordered.append({"section": sec, "rows": src["rows"]})
    out = dict(edit)
    out["tables"] = ordered
    return out


def validate(edit: dict, en: dict) -> list[str]:
    errs = []
    if not edit["header"] or edit["header"][0] != "ELMİ CV":
        errs.append("header[0] must be ELMİ CV")
    if len(edit["header"]) != len(en["header"]):
        errs.append(f"header len {len(edit['header'])} != {len(en['header'])}")
    if len(edit["tables"]) != len(en["tables"]):
        errs.append(f"tables len {len(edit['tables'])} != {len(en['tables'])}")
    else:
        for i, (et, nt) in enumerate(zip(en["tables"], edit["tables"])):
            if len(et["rows"]) != len(nt["rows"]):
                errs.append(
                    f"table[{i}] rows {len(nt['rows'])} != en {len(et['rows'])} ({nt['section']})"
                )
            else:
                for r_i, (er, nr) in enumerate(zip(et["rows"], nt["rows"])):
                    if len(er) != len(nr):
                        errs.append(
                            f"table[{i}].r{r_i} cols {len(nr)} != en {len(er)}"
                        )
    blob = edit.get("profile", "") + " " + " ".join(
        c for t in edit["tables"] for r in t["rows"] for c in r
    )
    if META_AZ_RE.search(blob):
        errs.append("meta phrase detected")
    return errs


def load_edits(rebuild: bool) -> list[dict]:
    if rebuild:
        from _cv_az_batch1_out_part0 import PART as PART0
        from _cv_az_batch1_out_part1 import PART as PART1
        from _cv_az_batch1_out_part2 import PART as PART2

        return PART0 + PART1 + PART2
    return json.loads(OUT_PATH.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--rebuild",
        action="store_true",
        help="Rebuild out JSON from part0/1/2 modules before apply",
    )
    ap.add_argument("--apply-only", action="store_true", help="Skip rewrite of out JSON")
    args = ap.parse_args()

    en_list = json.loads(EN_PATH.read_text(encoding="utf-8"))
    edits = load_edits(args.rebuild)
    if len(edits) != len(en_list):
        print(f"FAIL count edits={len(edits)} en={len(en_list)}")
        return 1

    en_by_base = {e["base"]: e for e in en_list}
    out = []
    val_failures = []
    for en in en_list:
        edit = next(e for e in edits if e["base"] == en["base"])
        errs = validate(edit, en)
        if errs:
            val_failures.append((edit["base"], errs))
        out.append(edit)

    if not args.apply_only or args.rebuild:
        OUT_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"wrote {OUT_PATH} count={len(out)}")

    if val_failures:
        print("VALIDATION FAILURES:")
        for base, errs in val_failures:
            print(f"  {base}: {errs}")
        return 1

    translated = len(out)
    applied = 0
    failures: list[str] = []

    for edit in out:
        path = AZ_CV_DIR / edit["az_file"]
        try:
            if not path.exists():
                failures.append(f"{edit['base']}: missing {path.name}")
                continue
            has_awards_tr = any(
                _section_key(t["section"]) == "awards" for t in edit["tables"]
            )
            cur = extract_cv(path)
            az_has_awards = any(
                _section_key(t["section"]) == "awards" for t in cur["tables"]
            )
            if has_awards_tr and not az_has_awards:
                doc = Document(str(path))
                ensure_awards_table(doc)
                tmp = path.with_name(f"__tmp_aw_{path.name}")
                doc.save(str(tmp))
                tmp.replace(path)
                cur = extract_cv(path)

            az_sections = [t["section"] for t in cur["tables"]]
            aligned = reorder_tables_for_doc(edit, az_sections)
            aligned["header"] = edit["header"]
            aligned["profile"] = edit["profile"]
            changes = apply_cv(path, aligned)
            applied += 1
            print(
                f"OK {edit['base']} changes={len(changes)} "
                f"tables_applied={len(aligned['tables'])}"
            )
        except Exception as exc:  # noqa: BLE001
            failures.append(f"{edit['base']}: {exc}")
            print(f"FAIL {edit['base']}: {exc}")

    print("---")
    print(f"translated={translated}")
    print(f"applied={applied}")
    print(f"failures={len(failures)}")
    for f in failures:
        print(f"  {f}")
    return 0 if not failures else 2


if __name__ == "__main__":
    sys.exit(main())
