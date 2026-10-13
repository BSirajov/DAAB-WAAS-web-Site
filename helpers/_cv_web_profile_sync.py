# -*- coding: utf-8 -*-
"""
Sync missing web-profile facts into EN Word CVs.

Compares i18n/scientists-profiles-en.json (+ catalog emails) to
en/scientists/CV/Word/*_CV_EN.docx and applies curated, high-confidence
inserts (awards rows, profile sentences, header notes) without inventing facts.

Usage:
  python helpers/_cv_web_profile_sync.py --dry-run
  python helpers/_cv_web_profile_sync.py
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from copy import deepcopy
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _cv_en_polish_lib import (
    EN_CV_DIR,
    PUBLICATION_HEADINGS,
    SECTION_HEADING,
    apply_cv,
    extract_cv,
    iter_blocks,
    set_paragraph_text,
)
from _normalize_cv_contact_links import contact_table, set_cell_text

ROOT = Path(__file__).resolve().parents[1]
SUMMARY_PATH = Path(__file__).with_name("_cv_web_profile_sync_summary.json")

# Curated updates: only facts present on the EN web profile and missing from the Word CV.
# award: {year, honor, body}
# profile_append: sentence(s) appended to Profile summary
# header_extra: optional extra header line after affiliation (or merge into title line)
UPDATES: dict[str, dict] = {
    "Rzayev_Teymur_CV_EN.docx": {
        "header_title": "Professor; Honored Artist of the Republic of Azerbaijan; Member of the WAAS Executive Board",
        "awards": [
            {
                "year": "2022",
                "honor": "Special medal for services to the Azerbaijani diaspora",
                "body": "Republic of Azerbaijan",
            },
            {
                "year": "2016",
                "honor": "Order “For Service to the Motherland”, III degree",
                "body": "Republic of Azerbaijan",
            },
            {
                "year": "2015",
                "honor": "Gold medal “For service to the Academy”",
                "body": "Russian Academy of Arts",
            },
            {
                "year": "2013",
                "honor": "Shuvalov medal",
                "body": "Russian Academy of Arts",
            },
            {
                "year": "2011",
                "honor": "Honored Artist of the Republic of Azerbaijan",
                "body": "Republic of Azerbaijan",
            },
        ],
        "profile_append": (
            "He is a member of the WAAS Executive Board and was elected a member of the "
            "Coordinating Council of Azerbaijanis Living Abroad."
        ),
    },
    "Zeynalova_Khadija_CV_EN.docx": {
        "awards": [
            {
                "year": "2026",
                "honor": "Progress (Tərəqqi) medal",
                "body": "President of the Republic of Azerbaijan",
            },
            {
                "year": "2025",
                "honor": "Honorary Decree for promoting Azerbaijani musical culture internationally (1st Forum of Azerbaijani Culture Ambassadors, Antalya)",
                "body": "",
            },
        ],
    },
    "Efendiyev_Messoud_CV_EN.docx": {
        "awards": [
            {
                "year": "2022",
                "honor": "Honored Scientist of the Republic of Azerbaijan",
                "body": "President of the Republic of Azerbaijan",
            },
        ],
        "profile_append": (
            "In 2023 he received the Lifetime Achievement Award of the Fields Institute."
        ),
    },
    "Safarova_Gunel_CV_EN.docx": {
        "awards": [
            {
                "year": "2020",
                "honor": "Medal “For service in diaspora activity”",
                "body": "Republic of Azerbaijan",
            },
        ],
    },
    "Salamov_Asaf_CV_EN.docx": {
        "profile_append": (
            "He is a member of the American Association for the Advancement of Science (AAAS). "
            "In 2014–2020 he was listed among the world’s most cited scientists by Clarivate Analytics."
        ),
    },
    "Omarov_Murad_CV_EN.docx": {
        "profile_append": (
            "He holds 12 copyright certificates and invention patents of Ukraine. "
            "Since 2019 he has chaired the ICONAT conference series."
        ),
    },
    "Gojayev_Zahid_CV_EN.docx": {
        "awards": [
            {
                "year": "2011",
                "honor": "Honored Machine Builder of Russia badge",
                "body": "Russian Federation",
            },
        ],
        "profile_append": (
            "He has received a letter of thanks from the President of the Russian Federation "
            "and honorary decrees of federal ministries."
        ),
    },
    "Aliyev_Ramin_CV_EN.docx": {
        "profile_append": (
            "He is a member of the American Psychological Association and of the Turkish "
            "Psychological Counseling and Guidance Association."
        ),
    },
    "Musayev_Yashar_CV_EN.docx": {
        "profile_append": (
            "He is a member of the Association of German Engineers (VDI) and has served as "
            "Chairman of the Board of BalticNet-Plasmatech e.V."
        ),
    },
    "Mutallimov_Mirza_CV_EN.docx": {
        "profile_append": "He is a Fellow of the European Society of Cardiology (FESC).",
    },
    "Karimi_Saadat_CV_EN.docx": {
        "awards": [
            {
                "year": "2022",
                "honor": "Medal for contribution to the promotion of the Azerbaijani language and culture abroad",
                "body": "Republic of Azerbaijan",
            },
        ],
    },
    "Bayramov_Ismikhan_CV_EN.docx": {
        "profile_append": (
            "He serves on the editorial boards of several international journals and as "
            "editor-in-chief of the Statistics journal."
        ),
    },
    "Eppelbaum_Lev_CV_EN.docx": {
        "profile_append": (
            "He is a member of the international geophysical commission “Rotation of the Earth” "
            "and of the WebmedCentral Ecology Advisory Board."
        ),
    },
    "Gadimov_Vahid_CV_EN.docx": {
        "profile_append": "He is a member of the international scientific societies GAMM and EUROMECH.",
    },
    "Sultansoy_Saleh_CV_EN.docx": {
        "profile_append": (
            "His works have been cited more than 81,000 times in Web of Science, more than "
            "275,000 times in Google Scholar, and more than 235,000 times in HEP Inspire."
        ),
    },
    "Rahimov_Yulduz_CV_EN.docx": {
        "profile_append": (
            "She served on the program committees of INFOCOMP 2013 (Lisbon) and INFOCOMP 2015 (Brussels)."
        ),
    },
    "Najafoglu_Hajali_CV_EN.docx": {
        "header_title": (
            "Professor of Inorganic Chemistry; Head of the Foreign Relations Office; "
            "Member of the University Board, Kafkas University"
        ),
        "profile_append": (
            "At Kafkas University he has served as head of the Foreign Relations Office and as a "
            "member of the University Board, and has headed Caucasus and Central Asia–related academic units. "
            "He has supervised 11 PhD students and 19 master’s students. "
            "His Google Scholar metrics include an h-index of 25 and an i10-index of 82."
        ),
    },
    "Asgerova_Sevinj_CV_EN.docx": {
        "profile_append": (
            "She is a full member of the European Society of Plastic and Reconstructive Ophthalmological "
            "Surgeons (ESOPRS) and holds memberships connected with the American Society of Ophthalmologists "
            "and the International Dacryological Society."
        ),
    },
    "Abdullayev_Azer_CV_EN.docx": {
        "profile_append": (
            "His record includes more than 70 scientific articles, 2 teaching-methodical materials, "
            "and 6 invention patents."
        ),
    },
    "Abuzerli_Murad_CV_EN.docx": {
        "profile_append": (
            "In 2023 he began a Marie Skłodowska-Curie Actions (MSCA) postdoctoral fellowship "
            "at the University of Vienna on the NEOVITA project (2023–2026)."
        ),
    },
    "Isayeva_Aygul_CV_EN.docx": {
        "profile_append": (
            "She has served on the Board of Directors of the International Black Sea University and "
            "as director of the Maarif organization, implementing education projects for Georgian Azerbaijanis."
        ),
    },
    "Heyet_Mehmet_Riza_CV_EN.docx": {
        "profile_append": (
            "He has chaired the organizing committee of 11 scientific symposia and spoken at "
            "8 international scientific conferences."
        ),
    },
    "Khalilova_Saida_CV_EN.docx": {
        "profile_append": (
            "She has developed more than 20 programs and served as author and artistic director of about "
            "20 projects, competitions, and concerts, with appearances at the embassies of Japan, Turkey, "
            "France, and Russia."
        ),
    },
}


def save_doc(path: Path, doc: Document) -> None:
    tmp = path.with_name(f"__tmp_{path.name}")
    try:
        doc.save(str(tmp))
        tmp.replace(path)
    except OSError:
        alt = path.with_name(f"__tmp2_{path.name}")
        doc.save(str(alt))
        alt.replace(path)


def clone_row(table: Table, row_idx: int = -1):
    row = table.rows[row_idx]
    new_tr = deepcopy(row._tr)
    table._tbl.append(new_tr)
    return table.rows[-1]


def find_section_table(doc: Document, heading_prefix: str) -> tuple[Paragraph | None, Table | None]:
    blocks = list(iter_blocks(doc))
    for i, (kind, obj) in enumerate(blocks):
        if kind != "p":
            continue
        text = (obj.text or "").strip()
        if text.lower().startswith(heading_prefix.lower()):
            if i + 1 < len(blocks) and blocks[i + 1][0] == "t":
                return obj, blocks[i + 1][1]
            return obj, None
    return None, None


def ensure_awards_table(doc: Document) -> Table:
    heading, table = find_section_table(doc, "Awards")
    if table is not None:
        return table
    # Insert before first publication heading, else before Date of last update, else at end.
    blocks = list(iter_blocks(doc))
    insert_before = None
    for kind, obj in blocks:
        if kind != "p":
            continue
        text = (obj.text or "").strip()
        if PUBLICATION_HEADINGS.match(text) or text.lower().startswith("date of last update"):
            insert_before = obj._p
            break
    body = doc.element.body
    # heading paragraph
    h = doc.add_paragraph("Awards, honors and fellowships")
    h_el = h._p
    body.remove(h_el)
    if insert_before is not None:
        insert_before.addprevious(h_el)
    else:
        body.append(h_el)
    # create 3-col table after heading
    table = doc.add_table(rows=1, cols=3)
    tbl_el = table._tbl
    body.remove(tbl_el)
    h_el.addnext(tbl_el)
    hdr = table.rows[0].cells
    set_cell_text(hdr[0], "Year")
    set_cell_text(hdr[1], "Award / honor")
    set_cell_text(hdr[2], "Awarding body")
    return table


def award_exists(table: Table, year: str, honor: str) -> bool:
    hn = re.sub(r"[^a-z0-9]+", " ", honor.lower())
    tokens = [t for t in hn.split() if len(t) > 3][:5]
    for row in table.rows[1:]:
        cells = [c.text.strip() for c in row.cells]
        row_text = " ".join(cells).lower()
        if year and year[:4] in row_text:
            if sum(1 for t in tokens if t in row_text) >= max(1, min(2, len(tokens))):
                return True
        if tokens and sum(1 for t in tokens if t in row_text) >= min(3, len(tokens)):
            return True
    return False


def add_awards(doc: Document, awards: list[dict]) -> list[str]:
    changes = []
    if not awards:
        return changes
    table = ensure_awards_table(doc)
    for award in awards:
        year = award.get("year") or ""
        honor = award.get("honor") or ""
        body = award.get("body") or ""
        if award_exists(table, year, honor):
            continue
        # insert after header
        row = clone_row(table, 0)
        set_cell_text(row.cells[0], year)
        set_cell_text(row.cells[1], honor)
        set_cell_text(row.cells[2], body)
        # move new row to position 1 (right after header) by reordering
        # currently appended at end; for awards, chronological newest-first preferred
        # leave at end if many rows; for new tables only header+new. OK.
        changes.append(f"award:{year}:{honor[:60]}")
    # Re-sort data rows by year descending when possible
    _sort_awards_table(table)
    return changes


def _sort_awards_table(table: Table) -> None:
    if len(table.rows) <= 2:
        return
    rows = list(table.rows)[1:]
    def key(r):
        y = (r.cells[0].text or "").strip()
        m = re.search(r"((?:19|20)\d{2})", y)
        return int(m.group(1)) if m else 0
    rows_sorted = sorted(rows, key=key, reverse=True)
    # rebuild order: detach all data rows then re-append
    for r in rows:
        table._tbl.remove(r._tr)
    for r in rows_sorted:
        table._tbl.append(r._tr)


def append_profile(profile: str, extra: str) -> str:
    extra = (extra or "").strip()
    if not extra:
        return profile
    p = (profile or "").rstrip()
    pl = p.lower()
    el = extra.lower()
    # Skip only when a distinctive multi-word phrase from the new sentence is present.
    distinctive = []
    for phrase in re.findall(r"[A-Za-z][A-Za-z\-]+(?:\s+[A-Za-z][A-Za-z\-]+){1,5}", extra):
        phrase_l = phrase.lower().strip()
        if len(phrase_l) < 18:
            continue
        if phrase_l in {
            "he is a member of the",
            "she is a member of the",
            "he has served on the",
            "she has served on the",
        }:
            continue
        distinctive.append(phrase_l)
    if any(d in pl for d in distinctive[:6]):
        return profile
    # acronyms / short unique markers
    for marker in re.findall(r"\b[A-Z]{3,}\b", extra):
        if marker.lower() in pl:
            return profile
    if not p.endswith("."):
        p += "."
    return p + " " + extra


def update_header_title(header: list[str], new_title: str) -> list[str]:
    if not header or not new_title:
        return header
    out = list(header)
    # typical: [CURRICULUM VITAE, Name, Title, Affiliation]
    if len(out) >= 3:
        out[2] = new_title
    elif len(out) == 2:
        out.append(new_title)
    return out


def apply_one(path: Path, upd: dict, *, dry_run: bool) -> dict:
    data = extract_cv(path)
    doc = Document(str(path))
    changes: list[str] = []

    # header via extract/apply for title line
    if upd.get("header_title"):
        new_header = update_header_title(data["header"], upd["header_title"])
        if new_header != data["header"]:
            data["header"] = new_header
            changes.append("header_title")

    if upd.get("profile_append"):
        new_profile = append_profile(data["profile"], upd["profile_append"])
        if new_profile != data["profile"]:
            data["profile"] = new_profile
            changes.append("profile_append")

    # Apply header/profile text first through apply_cv (tables left as-is here)
    if not dry_run and (upd.get("header_title") or upd.get("profile_append")):
        apply_cv(path, {"header": data["header"], "profile": data["profile"], "tables": data["tables"]})
        doc = Document(str(path))

    award_changes = []
    if upd.get("awards"):
        if dry_run:
            _, table = find_section_table(doc, "Awards")
            for a in upd["awards"]:
                if table is None or not award_exists(table, a.get("year", ""), a.get("honor", "")):
                    award_changes.append(f"award:{a.get('year')}:{a.get('honor','')[:60]}")
        else:
            award_changes = add_awards(doc, upd["awards"])
            if award_changes:
                save_doc(path, doc)

    changes.extend(award_changes)
    return {"file": path.name, "changes": changes, "changed": bool(changes)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", action="append", default=[], help="Limit to CV filename(s)")
    args = ap.parse_args()

    items = UPDATES
    if args.only:
        items = {k: v for k, v in UPDATES.items() if k in set(args.only)}

    summary = []
    for name, upd in items.items():
        path = EN_CV_DIR / name
        if not path.exists():
            summary.append({"file": name, "error": "missing"})
            continue
        result = apply_one(path, upd, dry_run=args.dry_run)
        summary.append(result)
        status = "DRY" if args.dry_run else ("OK" if result["changed"] else "SKIP")
        print(f"{status} {name}: {result['changes'] or ['no changes']}")

    SUMMARY_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    changed = sum(1 for s in summary if s.get("changed"))
    print(f"done changed={changed}/{len(summary)} dry_run={args.dry_run}")
    print("summary", SUMMARY_PATH)


if __name__ == "__main__":
    main()
