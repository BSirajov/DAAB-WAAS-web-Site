# -*- coding: utf-8 -*-
"""
Batch-convert EN/AZ Word CVs to HTML using the Abbasova/Sirajov visual template.

Usage:
  python helpers/_build_cv_html.py
  python helpers/_build_cv_html.py --lang en
  python helpers/_build_cv_html.py --only Abbasova_Dinara
"""
from __future__ import annotations

import argparse
import html
import re
import unicodedata
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph

ROOT = Path(__file__).resolve().parents[1]
PHOTO_DIR = ROOT / "images" / "scientists-photos"

# Word → HTML output dirs (Windows case-insensitive; matches existing Html folders)
OUT = {
    "en": ROOT / "en" / "scientists" / "CV" / "Html",
    "az": ROOT / "az" / "scientists" / "CV" / "Html",
}
WORD = {
    "en": ROOT / "en" / "scientists" / "CV" / "Word",
    "az": ROOT / "az" / "scientists" / "CV" / "Word",
}

# Relative from en|az/scientists/CV/Html/ to images/scientists-photos/
PHOTO_HREF_PREFIX = "../../../../images/scientists-photos/"

LABELS = {
    "en": {
        "contact": "Contact",
        "profile": "Profile",
        "work": "Work experience",
        "education": "Education",
        "awards": "Awards & recognitions",
        "languages": "Languages",
        "grants": "Grants & projects",
        "metrics": "Research metrics",
        "teaching": "Teaching",
        "supervision": "Supervision",
        "publications": "Publications",
        "daab": "WAAS / DAAB activity",
        "other": "Additional information",
    },
    "az": {
        "contact": "Əlaqə",
        "profile": "Profil",
        "work": "İş təcrübəsi",
        "education": "Təhsil",
        "awards": "Mükafatlar və təltiflər",
        "languages": "Dillər",
        "grants": "Qrantlar və layihələr",
        "metrics": "Elmi göstəricilər",
        "teaching": "Tədris",
        "supervision": "Elmi rəhbərlik",
        "publications": "Nəşrlər",
        "daab": "DAAB fəaliyyəti",
        "other": "Əlavə məlumat",
    },
}

# CV basename (Last_First) → photo stem
PHOTO_MAP = {
    "Abbasova_Dinara": "dinara-abbasova",
    "Abdullayev_Azer": "azer-abdullayev",
    "Abdullayev_Rauf": "rauf-abdullayev",
    "Abdullayev_Shuay": "suay-abdullayev",
    "Abuzerli_Murad": "murad-abuzerli",
    "Ahmadov_Emil": "emil-ahmadov",
    "Ahmedoglu_Shahin": "sahin-ehmedoglu",
    "Akbarov_Kamal": "kamal-ekberov",
    "Akhundov_Ilham": "ilham-axundov",
    "Alaferdov_Akif": "akif-alaferdov",
    "Aliyev_Ismayil": "ismayil-eliyev",
    "Aliyev_Ramin": "ramin-eliyev",
    "Allahverdiyev_Aladdin": "eleddin-allahverdiyev",
    "Allahverdiyev_Oruc": "oruc-allahverdiyev",
    "Allahverdiyev_Suleyman": "suleyman-allahverdiyev",
    "Allahyarov_Elshad": "elsad-allahyarov",
    "Applebaum_Mark": "mark-applebaum",
    "Asgerova_Sevinj": "sevinc-esgerova",
    "Atakishiyev_Natig": "natiq-agakisiyev",
    "Aydarov_Tofig": "tofiq-aydarov",
    "Badalov_Elchin": "elcin-bedelov",
    "Bayramov_Ismikhan": "ismixan-bayramov",
    "Efendi_Elvin": "elvin-efendi",
    "Efendiyev_Messoud": "messoud-efendiyev",
    "Eppelbaum_Lev": "lev-v-eppelbaum",
    "Gadimov_Vahid": "vahid-qedimov",
    "Gayibli_Khagani": "xaqani-qayibli",
    "Genceli_Mehdi": "mehdi-genceli-ismayilov",
    "Gojayev_Zahid": "zahid-qocayev",
    "Guliyev_Arif": "arif-quliyev",
    "Guliyeva_Aynur": "aynur-quliyeva",
    "Gulusoy_Ilkin": "ilkin-qulusoy",
    "Hasanova_Reyhan": "reyhan-hesenova",
    "Heyet_Mehmet_Riza": "mehmet-riza-heyet",
    "Huseynli_Aytakin": "aytekin-huseynli",
    "Ibrahimov_Rovshan": "rovsen-ibrahimov",
    "Isayeva_Aygul": "aygul-isayeva",
    "Isgandarova_Sabina": "sebine-isgenderova",
    "Ismayil_Togrul": "togrul-ismayil",
    "Jannataliyev_Rasim": "rasim-cenneteliyev",
    "Javadova-Spitzberg_Jamila": "cemile-cavadova-spitzberq",
    "Kalantar_Khalil": "xelil-kelenter",
    "Kalantarov_Varga": "varqa-kelenterov",
    "Karimi_Saadat": "saadat-karimi",
    "Karimov_Toghrul": "togrul-karimov",
    "Karimova_Sevda": "sevda-kerimova",
    "Khalilova_Saida": "seide-xelilova",
    "Kurban_Vefa": "vefa-qurban",
    "Mammadli_Barmanbay_Afina": "afina-memmedli-barmanbay",
    "Mammadov_Agamali": "agamali-memmedov",
    "Mammadov_Nizami": "nizami-memmedov",
    "Mammadova_Sevinj": "sevinj-mammadova",
    "Masumova_Nigar": "nigar-masimova",
    "Mehdiyev_Gafar": "qafar-caxmaqli-mehdiyev",
    "Mehmedov_Emirullah": "emirulla-memmedov",
    "Moridi_Reza": "reza-moridi",
    "Mukhtarov_Shehriyar": "sehriyar-muxtarov",
    "Murshudov_Garib": "qerib-mursudov",
    "Musayev_Yashar": "yasar-musayev",
    "Mutallimov_Mirza": "mirze-mutellimov",
    "Najafoglu_Hajali": "hacali-necefoglu",
    "Omarov_Murad": "murad-omerov",
    "Osmanli_Zarifa": "zerife-osmanli",
    "Rahimov_Aliheydar": "eliheyder-rehimov",
    "Rahimov_Yulduz": "yulduz-rahimov",
    "Rustamov_Kamran": "kamran-rustemov",
    "Rustamov_Valeh": "valeh-rustemov",
    "Rzayev_Teymur": "teymur-rzayev",
    "Sabziyeva_Makbule": "meqbule-sebziyeva",
    "Safarova_Gunel": "gunel-seferova",
    "Salamov_Asaf": "asef-salamov",
    "Sirajov_Bakhtiyar": "bakhtiyar-sirajov",
    "Suleymanov_Akif": "akif-suleymanov",
    "Suleymanov_Ebulfez": "ebulfez-suleymanov",
    "Sultansoy_Saleh": "saleh-sultansoy",
    "Talishinskiy_Toghrul": "togrul-talisinski",
    "Veliyev_Eldar": "eldar-veliyev",
    "Zeynalova_Khadija": "xedice-zeynalova",
}


def esc(s: str) -> str:
    return html.escape(s or "", quote=True)


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def iter_blocks(doc: Document):
    for child in doc.element.body.iterchildren():
        if child.tag == qn("w:p"):
            yield ("p", Paragraph(child, doc))
        elif child.tag == qn("w:tbl"):
            yield ("t", Table(child, doc))


def is_main_publications_heading(title: str) -> bool:
    """True for the top-level Publications / Nəşrlər heading only."""
    return bool(re.match(r"^(publications|nəşrlər)\s*$", (title or "").strip(), re.I))


def classify_section(title: str, lang: str) -> str | None:
    """Return a section key only for real headings; None for body text."""
    t = (title or "").strip()
    if not t:
        return None
    # Numbered bibliography lines are never headings
    if re.match(r"^\d+[\.\)]\s", t):
        return None
    # Long prose is never a section heading
    if len(t) > 90:
        return None
    low = t.lower()
    if re.search(r"^date of last update|^son yenilənmə", low):
        return None
    if lang == "az":
        rules = [
            (r"^əlaqə\b", "contact"),
            (r"^profil xülasəsi\b", "profile"),
            (r"^təhsil\b", "education"),
            (r"^elmi və peşəkar", "work"),
            (r"^mükafatlar\b", "awards"),
            (r"^qrantlar\b", "grants"),
            (r"^(elmi|tədqiqat) göstəricilər", "metrics"),
            (r"^tədris\b", "teaching"),
            (r"^(elmi rəhbərlik|rəhbərlik)\b", "supervision"),
            (r"^dillər\b", "languages"),
            (r"^daab\b", "daab"),
            (
                r"^(nəşrlər|kitablar?\b|kitab fəsilləri|rəylənmiş|konfrans məqalələri|"
                r"dəvətli məruzələr|patentlər?\b)\b",
                "publications",
            ),
        ]
    else:
        rules = [
            (r"^contact\b", "contact"),
            (r"^profile summary\b", "profile"),
            (r"^education\b", "education"),
            (r"^academic and professional", "work"),
            (r"^awards\b", "awards"),
            (r"^grants\b", "grants"),
            (r"^research metrics\b", "metrics"),
            (r"^teaching\b", "teaching"),
            (r"^supervision\b", "supervision"),
            (r"^languages\b", "languages"),
            (r"^participation in daab\b", "daab"),
            (
                r"^(publications|books?\b|book chapters|peer-reviewed|conference papers|"
                r"invited talks|patents?\b)\b",
                "publications",
            ),
        ]
    for pat, key in rules:
        if re.search(pat, low, re.I):
            return key
    return None


def parse_cv(path: Path, lang: str) -> dict:
    doc = Document(str(path))
    blocks = list(iter_blocks(doc))
    header: list[str] = []
    contact: list[tuple[str, str]] = []
    profile = ""
    sections: dict[str, list] = {
        "education": [],
        "work": [],
        "awards": [],
        "grants": [],
        "metrics": [],
        "teaching": [],
        "supervision": [],
        "languages": [],
        "daab": [],
        "publications": [],
        "other": [],
    }

    i = 0
    while i < len(blocks):
        kind, obj = blocks[i]
        if kind == "p":
            text = (obj.text or "").strip()
            if classify_section(text, lang) == "contact" or re.match(
                r"^(contact|əlaqə)\b", text, re.I
            ):
                break
            if text:
                header.append(text)
        i += 1

    current = ""
    while i < len(blocks):
        kind, obj = blocks[i]
        if kind == "p":
            text = (obj.text or "").strip()
            if not text:
                i += 1
                continue
            key = classify_section(text, lang)
            if key:
                # Publication category headings (Books, Book chapters, …) classify as
                # "publications" too; keep them as subheads instead of dropping them.
                if key == "publications" and not is_main_publications_heading(text):
                    current = "publications"
                    sections["publications"].append({"type": "subhead", "text": text})
                    i += 1
                    continue
                current = key
                i += 1
                continue
            if current == "profile":
                if not profile:
                    profile = text
                else:
                    profile = profile + " " + text
            elif current in {"publications", "other", "daab"}:
                sections[current].append({"type": "p", "text": text})
            i += 1
            continue

        # table
        rows = [[c.text.strip() for c in row.cells] for row in obj.rows]
        if current == "contact":
            for row in rows:
                if len(row) >= 2 and (row[0] or row[1]):
                    contact.append((row[0], row[1]))
        elif current in sections:
            sections[current].append({"type": "table", "rows": rows})
        i += 1

    return {
        "header": header,
        "contact": contact,
        "profile": profile,
        "sections": sections,
    }


def contact_value(contact: list[tuple[str, str]], *keys: str) -> str:
    for label, val in contact:
        low = label.lower()
        if any(k in low for k in keys) and val:
            return val
    return ""


def table_data_rows(tables: list[dict]) -> list[list[str]]:
    out = []
    for block in tables:
        if block.get("type") != "table":
            continue
        rows = block.get("rows") or []
        if not rows:
            continue
        # skip header-ish first row
        start = 1 if len(rows) > 1 else 0
        for row in rows[start:]:
            if any(cell.strip() for cell in row):
                out.append(row)
    return out


def has_content_rows(tables: list[dict]) -> bool:
    return bool(table_data_rows(tables))


def icon_svg(kind: str) -> str:
    icons = {
        "pin": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#323b4c" d="M12 2.2a7.2 7.2 0 0 0-7.2 7.2c0 5.4 7.2 12.4 7.2 12.4s7.2-7 7.2-12.4A7.2 7.2 0 0 0 12 2.2zm0 9.7a2.5 2.5 0 1 1 0-5 2.5 2.5 0 0 1 0 5z"/></svg>',
        "mail": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#323b4c" d="M3.5 6.5h17a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1h-17a1 1 0 0 1-1-1v-9a1 1 0 0 1 1-1zm8.5 6.1L4.7 8.2v7.8h14.6V8.2L12 12.6zm0-1.5 7.1-4.1H4.9L12 11.1z"/></svg>',
        "web": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#323b4c" d="M12 2.5a9.5 9.5 0 1 0 0 19 9.5 9.5 0 0 0 0-19zm0 1.5c1.7 0 3.3.6 4.5 1.5H7.5A7.9 7.9 0 0 1 12 4zm-6.6 3h13.2c.5.8.9 1.7 1.1 2.7H4.3c.2-1 .6-1.9 1.1-2.7zM4.2 11.2h15.6c0 .3.1.6.1.9s0 .6-.1.9H4.2c0-.3-.1-.6-.1-.9s0-.6.1-.9zm.1 3.6h15.4c-.2 1-.6 1.9-1.1 2.7H7.5c1.2.9 2.8 1.5 4.5 1.5a7.9 7.9 0 0 0 4.5-1.5H5.4c-.5-.8-.9-1.7-1.1-2.7z"/></svg>',
        "link": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#323b4c" d="M10.5 13.5a3.5 3.5 0 0 0 5 0l2.1-2.1a3.5 3.5 0 0 0-5-5L11.4 7.6l1.1 1.1 1.2-1.2a2 2 0 1 1 2.8 2.8l-2.1 2.1a2 2 0 0 1-2.8 0l-1.1 1.1zm3-3a3.5 3.5 0 0 0-5 0L6.4 12.6a3.5 3.5 0 0 0 5 5l1.2-1.2-1.1-1.1-1.2 1.2a2 2 0 1 1-2.8-2.8l2.1-2.1a2 2 0 0 1 2.8 0l1.1-1.1z"/></svg>',
    }
    return icons.get(kind, icons["link"])


def contact_icon(label: str) -> str:
    low = label.lower()
    if any(k in low for k in ["email", "e-mail", "e‑mail", "poçt"]):
        return "mail"
    if any(k in low for k in ["country", "ölkə", "city", "şəhər", "residence", "ünvan"]):
        return "pin"
    if any(k in low for k in ["orcid", "linkedin", "scholar", "website", "vebsayt", "researchgate", "academia"]):
        return "web"
    return "link"


def maybe_link(val: str) -> str:
    v = val.strip()
    if re.match(r"^https?://", v, re.I) or v.lower().startswith("www."):
        href = v if v.lower().startswith("http") else "https://" + v
        return f'<a href="{esc(href)}">{esc(v)}</a>'
    if "@" in v and " " not in v:
        return f'<a href="mailto:{esc(v)}">{esc(v)}</a>'
    if re.match(r"^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$", v, re.I):
        return f'<a href="https://orcid.org/{esc(v)}">{esc(v)}</a>'
    return esc(v)


def render_contacts(contact: list[tuple[str, str]], lang: str) -> str:
    # Prefer useful rows; skip name duplicates
    skip = {
        "full name",
        "tam ad",
        "name in azerbaijani",
        "azərbaycan dilində ad",
        "scientific field",
        "elmi sahə",
        "institution",
        "təşkilat",
    }
    items = []
    for label, val in contact:
        if not val.strip():
            continue
        low = label.lower()
        if any(s in low for s in skip):
            continue
        # shorten label display for known fields
        display_val = val
        if "country" in low or "ölkə" in low:
            display_val = val
        icon = contact_icon(label)
        items.append(
            f"<li>{icon_svg(icon)}<span>{maybe_link(display_val)}</span></li>"
        )
    if not items:
        return ""
    L = LABELS[lang]
    return (
        f"<h2>{esc(L['contact'])}</h2><div class=\"rule\"></div>"
        f"<ul class=\"contacts\">{''.join(items)}</ul>"
    )


def render_award_items(tables: list[dict]) -> str:
    lis = []
    for row in table_data_rows(tables):
        year = row[0] if len(row) > 0 else ""
        honor = row[1] if len(row) > 1 else ""
        body = row[2] if len(row) > 2 else ""
        if not honor and not body:
            continue
        parts = [p for p in [honor, body] if p]
        text = " — ".join(parts)
        if year:
            text = f"{esc(text)} ({esc(year)})"
        else:
            text = esc(text)
        lis.append(f"<li>{text}</li>")
    return "\n".join(lis)


def render_lang_items(tables: list[dict]) -> str:
    lis = []
    for row in table_data_rows(tables):
        lang = row[0] if row else ""
        level = row[1] if len(row) > 1 else ""
        if not lang:
            continue
        text = f"{lang} ({level})" if level else lang
        lis.append(f"<li>{esc(text)}</li>")
    return "\n".join(lis)


def render_jobs(tables: list[dict]) -> str:
    parts = []
    for row in table_data_rows(tables):
        years = row[0] if len(row) > 0 else ""
        position = row[1] if len(row) > 1 else ""
        dept = row[2] if len(row) > 2 else ""
        org = row[3] if len(row) > 3 else ""
        if not any([years, position, dept, org]):
            continue
        title = org or position or "—"
        role = position if org else dept
        details = []
        if dept and org:
            details.append(dept)
        if org and position and org != title:
            pass
        li = "".join(f"<li>{esc(d)}</li>" for d in details if d)
        ul = f"<ul>{li}</ul>" if li else ""
        parts.append(
            f"""<article class="job">
        <span class="dot"></span>
        <div class="job-top">
          <h3>{esc(title)}</h3>
          <span class="when">{esc(years)}</span>
        </div>
        {f'<p class="role">{esc(role)}</p>' if role else ''}
        {ul}
      </article>"""
        )
    return "\n".join(parts)


def render_education(tables: list[dict]) -> str:
    parts = []
    for row in table_data_rows(tables):
        years = row[0] if len(row) > 0 else ""
        degree = row[1] if len(row) > 1 else ""
        field = row[2] if len(row) > 2 else ""
        inst = row[3] if len(row) > 3 else ""
        if not any([years, degree, field, inst]):
            continue
        title = degree or field or "—"
        lines = []
        if field and degree:
            lines.append(f"<p>{esc(field)}</p>")
        if inst:
            lines.append(f"<p>{esc(inst)}</p>")
        parts.append(
            f"""<article class="edu-item">
        <span class="dot"></span>
        <div class="edu-top">
          <h3>{esc(title)}</h3>
          <span class="when">{esc(years)}</span>
        </div>
        {''.join(lines)}
      </article>"""
        )
    return "\n".join(parts)


def render_generic_table(tables: list[dict], as_list: bool = True) -> str:
    """Render non-empty table rows as list items or compact lines."""
    items = []
    for row in table_data_rows(tables):
        cells = [c for c in row if c.strip()]
        if not cells:
            continue
        items.append(f"<li>{esc(' — '.join(cells))}</li>")
    if not items:
        return ""
    return f'<ul class="plain">{"".join(items)}</ul>'


def render_publications(blocks: list[dict]) -> str:
    if not blocks:
        return ""
    parts = []
    for b in blocks:
        btype = b.get("type")
        if btype in {"p", "subhead"}:
            text = (b.get("text") or "").strip()
            if not text:
                continue
            if btype == "subhead" or (
                len(text) < 80 and not re.match(r"^\d+[\.\)]\s", text)
            ):
                parts.append(f'<h3 class="pub-sub">{esc(text)}</h3>')
            else:
                parts.append(f'<p class="pub-item">{esc(text)}</p>')
        elif btype == "table":
            parts.append(render_generic_table([b]))
    return "\n".join(parts)


def section_block(lang: str, key: str, inner: str, icon: str = "") -> str:
    if not (inner or "").strip():
        return ""
    L = LABELS[lang]
    title = L.get(key, key)
    icon_html = ""
    if icon:
        icon_html = f'<div class="icon icon-{icon}" aria-hidden="true">{ICON_SVGS[icon]}</div>'
    return f"""<section class="sec {key}">
      {icon_html}
      <h2>{esc(title)}</h2>
      <div class="rule"></div>
      {inner}
    </section>"""


ICON_SVGS = {
    "profile": '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="12" fill="#323b4c"/><circle cx="12" cy="9.1" r="3.15" fill="#fdfdfd"/><path fill="#fdfdfd" d="M6.1 18.4c.9-3.05 3-4.5 5.9-4.5s5 1.45 5.9 4.5A8.9 8.9 0 0 1 12 20.6a8.9 8.9 0 0 1-5.9-2.2z"/></svg>',
    "work": '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="12" fill="#323b4c"/><path fill="#fdfdfd" d="M9.1 8.15V7.25c0-.7.55-1.25 1.25-1.25h3.3c.7 0 1.25.55 1.25 1.25v.9h1.55c.72 0 1.3.58 1.3 1.3v6.05c0 .72-.58 1.3-1.3 1.3H7.55c-.72 0-1.3-.58-1.3-1.3V9.45c0-.72.58-1.3 1.3-1.3H9.1zm1.35 0h3.1V7.4h-3.1v.75zM7.7 12.15h8.6v.95H7.7v-.95z"/></svg>',
    "edu": '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="12" fill="#323b4c"/><path fill="#fdfdfd" d="M12 5.7 4.4 9.15 12 12.6l6.2-2.8v3.15h1.15V8.9L12 5.7zM7.7 12.15v2.15c0 1.45 1.9 2.6 4.3 2.6s4.3-1.15 4.3-2.6v-2.15l-4.3 1.95-4.3-1.95z"/></svg>',
    "globe": '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.3" fill="#fdfdfd" stroke="#323b4c" stroke-width="1.35"/><ellipse cx="12" cy="12" rx="3.5" ry="8.3" fill="none" stroke="#323b4c" stroke-width="1.15"/><path d="M3.8 12h16.4M5.1 8.15h13.8M5.1 15.85h13.8" fill="none" stroke="#323b4c" stroke-width="1.15"/></svg>',
}


CSS = r"""
  :root {
    --ink: #323b4c;
    --rule: #163853;
    --side: #e3e3e3;
    --paper: #fdfdfd;
    --white: #fdfdfd;
    --line: #323b4c;
  }
  * { box-sizing: border-box; }
  html, body {
    margin: 0;
    padding: 0;
    background: #cfcfcf;
    color: var(--ink);
    font-family: Calibri, "Segoe UI", Arial, Helvetica, sans-serif;
  }
  .sheet {
    width: 210mm;
    min-height: 297mm;
    margin: 8mm auto;
    position: relative;
    overflow: visible;
    background: var(--paper);
    box-shadow: 0 2mm 6mm rgba(0, 0, 0, 0.28);
    display: grid;
    grid-template-columns: 74mm 1fr;
    grid-template-rows: 49.8mm auto;
  }
  .banner {
    grid-column: 1 / -1;
    position: relative;
    height: 49.8mm;
    background: linear-gradient(90deg,
      #000000 0%, #050514 12%, #100f3d 30%,
      #1a1966 50%, #27269a 75%, #3432c9 100%);
    z-index: 1;
  }
  .banner-text {
    position: absolute;
    left: 88mm;
    right: 8mm;
    top: 8.6mm;
    color: var(--white);
  }
  h1 {
    margin: 0;
    font-family: Bahnschrift, "Arial Narrow", "Segoe UI", Arial, sans-serif;
    font-weight: 700;
    font-stretch: condensed;
    font-size: 22pt;
    line-height: 1.08;
    letter-spacing: 0.01em;
    color: #fdfdfd;
  }
  .subtitle {
    margin: 2.6mm 0 0;
    font-family: Bahnschrift, "Segoe UI", Calibri, Arial, sans-serif;
    font-weight: 500;
    font-size: 12pt;
    line-height: 1.32;
    letter-spacing: 0.012em;
    color: #fdfdfd;
    text-transform: uppercase;
  }
  .photo {
    position: absolute;
    left: 3mm;
    top: 13mm;
    width: 68mm;
    height: 68mm;
    border-radius: 50%;
    overflow: hidden;
    z-index: 3;
    background: #111;
  }
  .photo img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: top center;
    display: block;
  }
  .side {
    background: var(--side);
    color: var(--ink);
    padding: 40mm 4.2mm 8mm 7.2mm;
    z-index: 2;
  }
  .side h2 {
    margin: 0;
    font-family: Bahnschrift, "Arial Narrow", "Segoe UI", Arial, sans-serif;
    font-weight: 700;
    font-stretch: condensed;
    font-size: 14pt;
    letter-spacing: 0.04em;
    line-height: 1.15;
    color: var(--ink);
    text-transform: uppercase;
  }
  .side .rule {
    height: 2.15mm;
    width: 50mm;
    background: var(--ink);
    margin: 1.5mm 0 3.2mm;
  }
  .contacts { list-style: none; margin: 0 0 6.5mm; padding: 0; }
  .contacts li {
    display: flex;
    align-items: flex-start;
    gap: 2.4mm;
    font-size: 10pt;
    line-height: 1.25;
    margin: 0 0 3.2mm;
    overflow-wrap: anywhere;
  }
  .contacts a { color: inherit; }
  .contacts svg {
    width: 4.2mm; height: 4.2mm; flex: 0 0 4.2mm; margin-top: 0.2mm;
  }
  .side .block { margin-top: 5.2mm; }
  .side ul.items {
    list-style: disc;
    margin: 0;
    padding: 0 0 0 3.4mm;
  }
  .side ul.items li {
    font-size: 10pt;
    line-height: 1.3;
    margin: 0 0 1.8mm;
  }
  .side ul.awards li {
    font-size: 10pt;
    line-height: 1.34;
    margin: 0 0 3.5mm;
  }
  .side ul.langs li { margin: 0 0 0.7mm; }
  .main {
    position: relative;
    z-index: 2;
    padding: 4mm 9.2mm 8mm 8mm;
  }
  .main::before {
    content: "";
    position: absolute;
    left: 7.5mm;
    top: 4mm;
    bottom: 8mm;
    width: 0.32mm;
    background: var(--line);
    z-index: 0;
  }
  .sec {
    position: relative;
    z-index: 1;
    padding-left: 13.2mm;
    margin-bottom: 4mm;
  }
  .sec h2 {
    margin: 0;
    font-family: Bahnschrift, "Arial Narrow", "Segoe UI", Arial, sans-serif;
    font-weight: 700;
    font-stretch: condensed;
    font-size: 14pt;
    letter-spacing: 0.045em;
    line-height: 1.1;
    color: var(--ink);
    text-transform: uppercase;
  }
  .sec .rule {
    height: 2.35mm;
    background: var(--rule);
    margin: 1mm 0 1.8mm;
  }
  .icon {
    position: absolute;
    left: 0;
    top: 0;
    width: 7.15mm;
    height: 7.15mm;
    z-index: 2;
  }
  .icon svg { width: 100%; height: 100%; display: block; }
  .profile p {
    margin: 0;
    font-size: 10pt;
    line-height: 1.4;
    text-align: left;
  }
  .job { position: relative; margin: 0 0 3mm; }
  .dot {
    position: absolute;
    left: -11.15mm;
    top: 0.85mm;
    width: 2.15mm;
    height: 2.15mm;
    border-radius: 50%;
    background: var(--paper);
    border: 0.48mm solid var(--line);
    z-index: 2;
  }
  .job-top, .edu-top {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    gap: 3mm;
  }
  .job-top h3, .edu-top h3 {
    margin: 0;
    font-size: 11pt;
    font-weight: 700;
    line-height: 1.25;
  }
  .when {
    font-size: 10pt;
    white-space: nowrap;
    line-height: 1.2;
  }
  .role {
    margin: 0.2mm 0 0.4mm;
    font-size: 11pt;
    line-height: 1.25;
  }
  .job ul, .plain {
    margin: 0;
    padding: 0 0 0 4.2mm;
    font-size: 10pt;
    line-height: 1.35;
  }
  .job li, .plain li { margin: 0 0 0.4mm; }
  .edu-item { position: relative; margin: 0 0 2mm; }
  .edu-item p {
    margin: 0.15mm 0 0;
    font-size: 10.5pt;
    line-height: 1.3;
  }
  .pub-sub {
    margin: 2.5mm 0 1mm;
    font-size: 11pt;
    font-weight: 700;
  }
  .pub-item {
    margin: 0 0 1.2mm;
    font-size: 9.5pt;
    line-height: 1.35;
  }
  @media print {
    html, body { background: #fff; }
    .sheet { margin: 0; box-shadow: none; }
    a { color: inherit; text-decoration: none; }
  }
  @page { size: A4; margin: 0; }
  @media screen and (max-width: 900px) {
    .sheet {
      width: 100%;
      grid-template-columns: 1fr;
      grid-template-rows: auto;
    }
    .banner { height: auto; min-height: 36mm; padding: 8mm 6mm 8mm 6mm; }
    .banner-text { position: static; }
    .photo {
      position: static;
      margin: -18mm auto 4mm;
      width: 50mm;
      height: 50mm;
    }
    .side { padding: 8mm 6mm; }
    .main { padding: 6mm; }
    .main::before { display: none; }
    .sec { padding-left: 0; }
    .icon { display: none; }
    .dot { display: none; }
    h1 { white-space: normal; font-size: 18pt; }
    .when { white-space: normal; }
  }
"""


def display_name(header: list[str]) -> str:
    # header[0] is CURRICULUM/ELMİ CV; [1] is name
    if len(header) >= 2:
        name = header[1]
        name = re.sub(r",\s*(PhD|DSc|EMBA|Dr\.-Ing\.|DMA|EdD).*$", "", name, flags=re.I)
        return name.strip()
    return "CV"


def subtitle_lines(header: list[str]) -> list[str]:
    # degrees from name line + title + affiliation
    lines = []
    if len(header) >= 2:
        m = re.search(r",\s*(.+)$", header[1])
        if m:
            lines.append(m.group(1).strip())
    if len(header) >= 3 and header[2].strip():
        lines.append(header[2].strip())
    if len(header) >= 4 and header[3].strip():
        lines.append(header[3].strip())
    return lines


def photo_for(base: str) -> str | None:
    stem = PHOTO_MAP.get(base)
    if stem and (PHOTO_DIR / f"{stem}.jpg").exists():
        return f"{PHOTO_HREF_PREFIX}{stem}.jpg"
    # fuzzy
    nbase = norm(base.replace("_", " "))
    for p in PHOTO_DIR.glob("*.jpg"):
        if all(tok in norm(p.stem) for tok in nbase.split() if len(tok) > 3):
            return f"{PHOTO_HREF_PREFIX}{p.name}"
    return None


def build_html(data: dict, lang: str, base: str) -> str:
    L = LABELS[lang]
    name = display_name(data["header"])
    subs = subtitle_lines(data["header"])
    photo = photo_for(base)
    sec = data["sections"]

    side_parts = [render_contacts(data["contact"], lang)]

    awards_html = render_award_items(sec["awards"])
    if awards_html:
        side_parts.append(
            f'<div class="block"><h2>{esc(L["awards"])}</h2><div class="rule"></div>'
            f'<ul class="items awards">{awards_html}</ul></div>'
        )

    langs_html = render_lang_items(sec["languages"])
    if langs_html:
        side_parts.append(
            f'<div class="block"><h2>{esc(L["languages"])}</h2><div class="rule"></div>'
            f'<ul class="items langs">{langs_html}</ul></div>'
        )

    # If sidebar still thin, put metrics there
    metrics_html = render_generic_table(sec["metrics"])
    if metrics_html and not awards_html:
        side_parts.append(
            f'<div class="block"><h2>{esc(L["metrics"])}</h2><div class="rule"></div>'
            f"{metrics_html}</div>"
        )
        metrics_html = ""  # consumed

    main_parts = []
    if data["profile"].strip():
        main_parts.append(
            section_block(
                lang,
                "profile",
                f"<p>{esc(data['profile'].strip())}</p>",
                "profile",
            )
        )

    jobs = render_jobs(sec["work"])
    if jobs:
        main_parts.append(section_block(lang, "work", jobs, "work"))

    edu = render_education(sec["education"])
    if edu:
        main_parts.append(section_block(lang, "education", edu, "edu"))

    for key, icon in [
        ("grants", "globe"),
        ("teaching", "edu"),
        ("supervision", "edu"),
        ("daab", "globe"),
    ]:
        body = render_generic_table(sec[key])
        if body:
            main_parts.append(section_block(lang, key, body, icon))

    if metrics_html:
        main_parts.append(section_block(lang, "metrics", metrics_html, "globe"))

    pubs = render_publications(sec["publications"])
    if pubs:
        main_parts.append(section_block(lang, "publications", pubs, "globe"))

    other = render_publications(sec["other"])
    if other:
        main_parts.append(section_block(lang, "other", other, "globe"))

    sub_html = "<br>".join(esc(s) for s in subs) if subs else ""
    photo_html = (
        f'<div class="photo"><img src="{esc(photo)}" alt="{esc(name)}"></div>'
        if photo
        else '<div class="photo" aria-hidden="true"></div>'
    )

    title_name = name
    subtitle_block = f'<p class="subtitle">{sub_html}</p>' if sub_html else ""
    return (
        "<!DOCTYPE html>\n"
        f'<html lang="{esc(lang)}">\n'
        "<head>\n"
        '<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"<title>{esc(title_name)} — CV</title>\n"
        "<style>\n"
        f"{CSS}\n"
        "</style>\n"
        "</head>\n"
        "<body>\n"
        '<article class="sheet sheet-1">\n'
        '  <header class="banner">\n'
        '    <div class="banner-text">\n'
        f"      <h1>{esc(name.upper())}</h1>\n"
        f"      {subtitle_block}\n"
        "    </div>\n"
        "  </header>\n"
        f"  {photo_html}\n"
        '  <aside class="side">\n'
        f"    {''.join(side_parts)}\n"
        "  </aside>\n"
        '  <main class="main">\n'
        f"    {''.join(main_parts)}\n"
        "  </main>\n"
        "</article>\n"
        "</body>\n"
        "</html>\n"
    )


def word_files(lang: str) -> list[Path]:
    folder = WORD[lang]
    suffix = "_CV_EN.docx" if lang == "en" else "_CV_AZ.docx"
    # Skip Word lock/temp files (~$...)
    return sorted(p for p in folder.glob(f"*{suffix}") if not p.name.startswith("~$"))


def out_name(word_path: Path, lang: str) -> str:
    base = word_path.name.replace("_CV_EN.docx", "").replace("_CV_AZ.docx", "")
    return f"{base}_CV.html"


def convert_one(word_path: Path, lang: str) -> Path:
    base = word_path.name.replace("_CV_EN.docx", "").replace("_CV_AZ.docx", "")
    data = parse_cv(word_path, lang)
    html_doc = build_html(data, lang, base)
    out_dir = OUT[lang]
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / out_name(word_path, lang)
    out_path.write_text(html_doc, encoding="utf-8")
    return out_path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", choices=["en", "az", "both"], default="both")
    ap.add_argument("--only", action="append", default=[])
    args = ap.parse_args()
    langs = ["en", "az"] if args.lang == "both" else [args.lang]
    only = set(args.only or [])

    total = 0
    for lang in langs:
        files = word_files(lang)
        for path in files:
            base = path.name.replace("_CV_EN.docx", "").replace("_CV_AZ.docx", "")
            if only and base not in only and path.name not in only:
                continue
            out = convert_one(path, lang)
            total += 1
            print("OK", lang, out.name, f"bytes={out.stat().st_size}")
    print(f"done total={total}")


if __name__ == "__main__":
    main()
