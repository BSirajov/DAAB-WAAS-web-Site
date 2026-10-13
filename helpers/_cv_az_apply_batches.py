# -*- coding: utf-8 -*-
"""Apply translated AZ batch JSON files to Word CVs."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from docx import Document

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _cv_az_lib import (
    AZ_CV_DIR,
    META_AZ_RE,
    apply_cv,
    ensure_awards_table,
    extract_cv,
)

HELPERS = Path(__file__).resolve().parent


def load_outs() -> list[dict]:
    items = []
    for i in range(4):
        p = HELPERS / f"_cv_az_batch{i}_out.json"
        if not p.exists():
            print("missing", p.name)
            continue
        chunk = json.loads(p.read_text(encoding="utf-8"))
        print(f"loaded {p.name}: {len(chunk)}")
        items.extend(chunk)
    return items


def ensure_awards_if_needed(az_file: str, tables: list[dict]) -> None:
    wants_awards = any(
        (t.get("section") or "").lower().startswith("mükafatlar") for t in tables
    )
    if not wants_awards:
        return
    path = AZ_CV_DIR / az_file
    cur = extract_cv(path)
    has = any(
        (t.get("section") or "").lower().startswith("mükafatlar") for t in cur["tables"]
    )
    if has:
        return
    doc = Document(str(path))
    ensure_awards_table(doc)
    tmp = path.with_name(f"__tmp_{path.name}")
    try:
        doc.save(str(tmp))
        tmp.replace(path)
    except OSError:
        alt = path.with_name(f"__tmp2_{path.name}")
        doc.save(str(alt))
        alt.replace(path)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    items = load_outs()
    if not items:
        raise SystemExit("no batch out files")

    applied = 0
    failed = []
    for item in items:
        az_file = item["az_file"]
        path = AZ_CV_DIR / az_file
        if not path.exists():
            failed.append((az_file, "missing file"))
            continue
        edit = {
            "header": item["header"],
            "profile": item["profile"],
            "tables": item["tables"],
        }
        if args.dry_run:
            print("DRY", az_file, "tables", len(item["tables"]))
            continue
        try:
            ensure_awards_if_needed(az_file, item["tables"])
            changes = apply_cv(path, edit)
            applied += 1
            print("OK", az_file, "changes", len(changes))
        except Exception as e:
            failed.append((az_file, str(e)))
            print("FAIL", az_file, e)

    # verify
    meta = []
    no_awards = []
    for path in sorted(AZ_CV_DIR.glob("*_CV_AZ.docx")):
        data = extract_cv(path)
        if data.get("has_meta") or META_AZ_RE.search(data.get("profile") or ""):
            meta.append(path.name)
        if not any(
            (t.get("section") or "").lower().startswith("mükafatlar")
            for t in data["tables"]
        ):
            no_awards.append(path.name)

    print(
        f"applied={applied}/{len(items)} failed={len(failed)} "
        f"meta_left={len(meta)} no_awards={len(no_awards)}"
    )
    if failed:
        print("failures:", failed[:10])
    if meta:
        print("meta sample:", meta[:15])


if __name__ == "__main__":
    main()
