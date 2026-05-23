# -*- coding: utf-8 -*-
"""
Map scientist PDF CVs to structured template sections with DAAB UI/UX.
Preserves full source content; skips empty template sections (no placeholders).
"""
from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

# Reuse PDF extraction and page shell from rebuild pipeline
from rebuild_all_cvs_from_pdf import (
    CV_DIR,
    CV_REGISTRY,
    EXTRACT_DIR,
    EXTRA_CSS,
    build_footer,
    build_hero,
    build_page,
    clean_lines,
    dominant_size,
    esc,
    extract_html_parts,
    extract_lines,
    lines_to_sections,
    load_catalog,
    render_lines,
    resolve_pdf,
)

ROOT = Path(__file__).resolve().parent.parent
GUNEL = ROOT / "helpers" / "_build_gunel_cv.py"

# Template section order (international CV template semantics)
SECTION_ORDER = [
    "personal",
    "summary",
    "expertise",
    "competencies",
    "experience",
    "education",
    "certifications",
    "publications",
    "grants",
    "teaching",
    "supervision",
    "presentations",
    "awards",
    "fellowships",
    "memberships",
    "editorial",
    "patents",
    "languages",
    "technical",
    "volunteer",
    "development",
    "references",
    "additional",
]

SECTION_TITLES = {
    "personal": ("Personal Information", "Şəxsi məlumat"),
    "summary": ("Academic Profile", "Akademik profil"),
    "expertise": ("Research Interests", "Tədqiqat sahələri"),
    "competencies": ("Core Competencies", "Əsas kompetensiyalar"),
    "experience": ("Professional Experience", "Peşəkar fəaliyyət"),
    "education": ("Education", "Təhsil"),
    "certifications": ("Certifications & Licenses", "Sertifikatlar və lisenziyalar"),
    "publications": ("Publications", "Nəşrlər"),
    "grants": ("Research Grants & Projects", "Tədqiqat layihələri və qrantlar"),
    "teaching": ("Teaching & Training", "Tədris və təlim"),
    "supervision": ("Supervision & Mentoring", "Elmi rəhbərlik"),
    "presentations": ("Conferences & Presentations", "Konfranslar və məruzələr"),
    "awards": ("Awards & Honors", "Mükafatlar və fəxri adlar"),
    "fellowships": ("Fellowships & Visiting Appointments", "Stipendiyalar və ezamiyyələr"),
    "memberships": ("Professional Memberships", "Peşəkar üzvlüklər"),
    "editorial": ("Editorial & Review Activities", "Redaktorluq və rəyçilik"),
    "patents": ("Patents & Intellectual Property", "Patentlər"),
    "languages": ("Languages", "Dillər"),
    "technical": ("Technical & Software Skills", "Texniki bacarıqlar"),
    "volunteer": ("Volunteer & Community Engagement", "Könüllülük fəaliyyəti"),
    "development": ("Professional Development", "Peşəkar inkişaf"),
    "references": ("References", "Referanslar"),
    "additional": ("Additional Information", "Əlavə məlumat"),
}

# Semantic classification: (section_key, keyword fragments in normalized title)
CLASS_RULES: list[tuple[str, tuple[str, ...]]] = [
    ("personal", (
        "personal information", "personal data", "personal details", "contact information",
        "şəxsi məlumat", "şəxsi", "contacts", "contact",
    )),
    ("summary", (
        "professional summary", "executive summary", "profile", "academic profile",
        "about", "overview", "biography", "bio", "career objective", "research profile",
        "akademik profil", "profil", "xülasə", "haqqında",
    )),
    ("expertise", (
        "research interest", "research area", "areas of expertise", "expertise",
        "specialization", "field of", "research focus", "scientific interest",
        "tədqiqat sah", "ixtisaslaşma", "elmi maraq",
    )),
    ("competencies", (
        "competenc", "skill", "qualification", "core strength", "ability",
        "bacarıq", "kompetens", "bacariq",
    )),
    ("experience", (
        "professional experience", "work experience", "employment", "career history",
        "work history", "positions held", "appointments", "occupation", "professional activity",
        "peşəkar fəaliyyət", "iş təcrüb", "təcrübə", "əmək fəaliyy", "work experience",
        "teaching experience", "administrative experience", "industrial experience",
        "akademik görev", "akademik gorev", "akademikgörev", "akademikgorev",
        "idari görev", "idari gorev", "idarigörev", "idarigorev",
        "iş deneyim", "mesleki", "çalışma", "calisma", "employment history",
    )),
    ("education", (
        "education", "academic background", "degrees", "training background",
        "təhsil", "öğrenim", "ogrenim", "öğrenim bilgisi", "ogrenim bilgisi", "formation",
    )),
    ("certifications", (
        "certification", "certificate", "license", "licence", "credential",
        "sertifikat", "lisenziya",
    )),
    ("publications", (
        "publication", "bibliography", "selected publication", "journal article",
        "peer review", "monograph", "book chapter", "scientific work",
        "nəşr", "nesr", "yayın", "yayin", "yayim", "eserler", "eser",
        "makale", "kitap", "edebiyat", "monografi", "dergi", "yayimlanan",
        "sanat", "etkinlik", "tekniknot", "arastirma", "araştırma",
        "yazilan", "yazılan", "bölüm", "bolum", "kitaplarda",
    )),
    ("grants", (
        "grant", "funded project", "research project", "project funding", "sponsored",
        "qrant", "layihə", "layihe", "proje", "funding",
    )),
    ("teaching", (
        "teaching", "courses taught", "instruction", "pedagog", "curriculum",
        "tədris", "tedris", "dersler", "ders ", "course",
    )),
    ("supervision", (
        "supervision", "supervised", "thesis", "dissertation", "phd student", "graduate student",
        "mentoring", "advisee", "rəhbərlik", "dissertasiya", "doktora",
        "yönetilen tez", "yonetilen tez", "tezler", "mezun",
    )),
    ("presentations", (
        "invited talk", "keynote", "lecture delivered", "oral communication",
        "symposium paper", "conference paper", "conference presentation",
        "konfrans", "məruzə", "meruze", "bildiri", "bildiri sun",
    )),
    ("awards", (
        "award", "honor", "honour", "prize", "distinction", "medal", "recognition",
        "mükafat", "mukafat", "fəxri", "ferxi", "təltif", "ödül", "odul", "ödüller", "oduller",
    )),
    ("fellowships", (
        "fellowship", "visiting", "visiting professor", "visiting scholar", "sabbatical",
        "stipend", "ezamiyy", "misafir",
    )),
    ("memberships", (
        "membership", "member of", "professional affiliation", "society", "association",
        "academy", "union", "üzvlük", "uzvluk", "cəmiyyət",
    )),
    ("editorial", (
        "editorial", "editor", "reviewer", "referee", "examiner", "peer review activity",
        "redaktor", "rəyçi", "reyçi", "hakem", "editörlük", "editorluk",
    )),
    ("patents", (
        "patent", "intellectual property", "invention",
    )),
    ("languages", (
        "language", "linguistic", "foreign language", "dil ", "dillər", "diller",
    )),
    ("technical", (
        "technical skill", "software", "computer skill", "programming", "it skill",
        "laboratory skill", "instrument", "texniki", "proqram",
    )),
    ("volunteer", (
        "volunteer", "community service", "civic", "social activity",
        "könüllü", "konullu", "ictimai",
    )),
    ("development", (
        "professional development", "continuing education", "workshop attended", "training course",
        "peşəkar inkişaf", "təkmilləşdirmə",
    )),
    ("references", (
        "reference", "referee contact", "referans",
    )),
    ("additional", (
        "additional information", "miscellaneous", "other information", "further information",
        "hobbies", "interest", "əlavə",
    )),
]


def load_daab_css() -> str:
    text = GUNEL.read_text(encoding="utf-8")
    m = re.search(r"<style>(.*?)</style>", text, re.S)
    if not m:
        raise FileNotFoundError("DAAB CSS not found in _build_gunel_cv.py")
    css = m.group(1).strip()
    css += EXTRA_CSS
    css += """
    .awards-block { padding: 18px 22px; }
    .awards-block ul, .awards-block ol { margin: 0; padding-left: 22px; font-size: 14.5px; line-height: 1.75; }
    .awards-block li { margin-bottom: 8px; }
"""
    return css


def repair_title(title: str) -> str:
    t = title.strip()
    words = t.split()
    if len(words) >= 4 and sum(len(w) for w in words) / len(words) <= 2.5:
        t = re.sub(r"\s+", "", t)
    return t


def normalize_title(title: str) -> str:
    t = repair_title(title).lower().strip().strip(":").strip()
    t = re.sub(r"^[ivx]+\.\s*", "", t)
    t = re.sub(r"^[a-z0-9]\.\s*", "", t)
    t = re.sub(r"\s+", " ", t)
    return t


def should_skip_section(title: str) -> bool:
    raw = repair_title(title).strip()
    norm = normalize_title(title)
    if len(norm) < 2:
        return True
    if norm in {"cv", "curriculum vitae", "resume", "vita", "biodata", "ozgecmis"}:
        return True
    letters = [c for c in raw if c.isalpha()]
    if letters and len(raw) < 48:
        upper = sum(1 for c in letters if c.isupper() or c in "İŞÇĞÖÜƏ")
        if upper / len(letters) > 0.85 and " " in raw and not any(
            kw in norm for kw in ("section", "bölüm", "part", "chapter")
        ):
            return True
    return False


def classify_section(title: str) -> str | tuple[str, str]:
    norm = normalize_title(title)
    for key, keywords in CLASS_RULES:
        if any(kw in norm for kw in keywords):
            return key
    return ("other", title.strip())


def bi(en: str, az: str) -> str:
    return f'<span class="lang en">{esc(en)}</span><span class="lang az">{esc(az)}</span>'


def section_shell(title_en: str, title_az: str, inner: str) -> str:
    return (
        '<section class="section">\n'
        f'  <h2 class="section-title">{bi(title_en, title_az)}</h2>\n'
        f'{inner}\n'
        "</section>"
    )


def wrap_content(html: str, wrapper: str) -> str:
    if not html.strip():
        return ""
    if wrapper == "callout":
        return f'  <div class="callout section-body">{html}</div>'
    if wrapper == "timeline":
        return f'  <div class="timeline section-body"><div class="cv-content">{html}</div></div>'
    if wrapper == "education":
        return f'  <div class="education-grid section-body"><div class="cv-content" style="grid-column:1/-1;padding:20px 22px">{html}</div></div>'
    if wrapper == "pub":
        return f'  <div class="pub-block section-body"><div class="pub-category"><div class="cv-content">{html}</div></div></div>'
    if wrapper == "competency":
        return f'  <div class="competency-grid section-body"><div class="comp-group" style="grid-column:1/-1"><div class="cv-content">{html}</div></div></div>'
    if wrapper == "awards":
        return f'  <div class="awards-block section-body">{html}</div>'
    return f'  <div class="cv-content section-body">{html}</div>'


WRAPPER_BY_KEY = {
    "summary": "callout",
    "experience": "timeline",
    "education": "education",
    "fellowships": "timeline",
    "volunteer": "timeline",
    "publications": "pub",
    "grants": "pub",
    "teaching": "pub",
    "supervision": "pub",
    "presentations": "pub",
    "memberships": "pub",
    "editorial": "pub",
    "patents": "pub",
    "development": "pub",
    "references": "pub",
    "competencies": "competency",
    "expertise": "competency",
    "technical": "competency",
    "languages": "competency",
    "awards": "awards",
    "certifications": "pub",
    "additional": "pub",
    "personal": "pub",
}


def bucket_sections(pdf_sections: list[dict]) -> tuple[dict[str, list[list[dict]]], list[tuple[str, list]]]:
    buckets: dict[str, list[list[dict]]] = defaultdict(list)
    others: list[tuple[str, list]] = []
    for sec in pdf_sections:
        title = repair_title(sec["title"])
        lines = sec["lines"]
        if not lines or should_skip_section(title):
            continue
        result = classify_section(title)
        if isinstance(result, tuple):
            _, orig = result
            others.append((orig, lines))
        else:
            buckets[result].append(lines)
    return buckets, others


def flatten_groups(groups: list[list[dict]]) -> list[dict]:
    out: list[dict] = []
    for i, grp in enumerate(groups):
        if i > 0 and grp:
            out.append({"text": "", "size": 9, "bold": False, "page": 0, "y": 0})
        out.extend(grp)
    return out


def render_bucket(key: str, lines: list[dict], body: float) -> str:
    html = render_lines(lines, body)
    if not html.strip():
        return ""
    wrapper = WRAPPER_BY_KEY.get(key, "content")
    inner = wrap_content(html, wrapper if wrapper != "content" else "content")
    title_en, title_az = SECTION_TITLES[key]
    return section_shell(title_en, title_az, inner)


def render_other(title: str, lines: list[dict], body: float) -> str:
    html = render_lines(lines, body)
    if not html.strip():
        return ""
    inner = wrap_content(html, "pub")
    return section_shell(title, title, inner)


def render_mapped_cv(pdf_path: Path) -> str:
    lines = clean_lines(extract_lines(pdf_path))
    body = dominant_size(lines)
    pdf_sections = lines_to_sections(lines)
    buckets, others = bucket_sections(pdf_sections)

    plain = "\n".join(l["text"] for l in lines)
    EXTRACT_DIR.mkdir(parents=True, exist_ok=True)
    (EXTRACT_DIR / (pdf_path.stem + ".txt")).write_text(plain, encoding="utf-8")

    chunks: list[str] = []
    for key in SECTION_ORDER:
        if key not in buckets:
            continue
        block = render_bucket(key, flatten_groups(buckets[key]), body)
        if block:
            chunks.append(block)

    for title, olines in others:
        block = render_other(title, olines, body)
        if block:
            chunks.append(block)

    return "\n\n  ".join(chunks)


def rebuild_one(entry: dict, css: str, catalog: dict) -> None:
    slug = entry["slug"]
    out = CV_DIR / slug
    parts = extract_html_parts(out)
    email = (entry.get("email") or "").lower()
    name = catalog.get(email, {}).get("ad_soyad", slug.replace("_", " ").replace(".html", ""))

    if entry.get("en") and entry.get("az"):
        pdf_en = resolve_pdf(entry["en"])
        pdf_az = resolve_pdf(entry["az"])
        body_en = render_mapped_cv(pdf_en)
        body_az = render_mapped_cv(pdf_az)
        hero_src = pdf_en
    else:
        pdf = resolve_pdf(entry["single"])
        body = render_mapped_cv(pdf)
        body_en = body
        body_az = body
        hero_src = pdf

    if parts:
        hero, footer, title = parts["hero"], parts["footer"], parts["title"]
    else:
        hero = build_hero(entry, catalog, hero_src)
        footer = build_footer(name)
        title = f"Curriculum Vitae — {name}"

    page = build_page(title, css, hero, body_en, body_az, footer)
    CV_DIR.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"OK {slug}: {out.stat().st_size // 1024} KB", flush=True)


def main() -> None:
    css = load_daab_css()
    catalog = load_catalog()
    ok = fail = 0
    for entry in CV_REGISTRY:
        try:
            rebuild_one(entry, css, catalog)
            ok += 1
        except Exception as e:
            fail += 1
            print(f"FAIL {entry['slug']}: {e}", file=sys.stderr, flush=True)
    print(f"Done: {ok}/{len(CV_REGISTRY)} OK, {fail} failed", flush=True)
    if fail:
        sys.exit(1)


if __name__ == "__main__":
    main()
