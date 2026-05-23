# -*- coding: utf-8 -*-
"""Rebuild HTML CVs from PDFs — full content, Afina design system."""
from __future__ import annotations

import html
import json
import re
import sys
from collections import Counter
from pathlib import Path

import fitz

ROOT = Path(r"c:\Users\BSira\Documents\GitHub\DAAB-WAAS web site")
PDF_DIR = ROOT / "cv" / "Named CV"
CV_DIR = ROOT / "cv"
AFINA = CV_DIR / "afina_barmanbay.html"
CATALOG = ROOT / "js" / "scientists-catalog-data.js"
EXTRACT_DIR = ROOT / "helpers" / "_pdf_extract"

EXTRA_CSS = """
    .cv-content { padding: 18px 22px; font-size: 14.5px; line-height: 1.75; color: var(--body-text); }
    .cv-content p { margin: 0 0 12px; }
    .cv-content ul, .cv-content ol { margin: 0 0 14px 22px; }
    .cv-content li { margin-bottom: 6px; }
    .cv-content h3.cv-subhead { font-size: 15px; font-weight: 700; color: var(--blue-dark); margin: 18px 0 8px; border-bottom: 1px solid var(--blue-light); padding-bottom: 4px; }
    .cv-content pre.cv-pre { white-space: pre-wrap; word-wrap: break-word; font-family: 'Times New Roman', Times, serif; background: var(--bg); border: 1px solid #d0dde8; padding: 14px 16px; border-radius: 3px; font-size: 13.5px; line-height: 1.65; margin: 0 0 14px; overflow-x: auto; }
"""

CV_REGISTRY = [
    {"slug": "afina_barmanbay.html", "single": "CV Afina Barmanbay (no phone).pdf", "email": "afina.barmanbay@kafkas.edu.tr"},
    {"slug": "aygul_isayeva.html", "en": "CV Aygul Isayeva (EN) (no phone).pdf", "az": "CV Aygul Isayeva (AZ) (no phone).pdf", "email": "isayevaaygul2003@yahoo.com"},
    {"slug": "aytekin_huseynli.html", "single": "CV Ayt\u0259kin H\u00fcseynli (no phone).pdf"},
    {"slug": "bakhtiyar_sirajov.html", "single": "CV Bakhtiyar Sirajov.pdf"},
    {"slug": "eldar_veliyev.html", "single": "CV Eldar V\u0259liyev (no phone).pdf"},
    {"slug": "elshad_allahyarov.html", "single": "CV Elshad Allahyarov.pdf"},
    {"slug": "elvin_afandi.html", "single": "CV Elvin Afandi (no phone).pdf"},
    {"slug": "emil_ahmadov.html", "single": "CV Emil \u018fhm\u0259dov (no phone).pdf"},
    {"slug": "emirulla_memmedov.html", "en": "CV \u018fmirulla M\u0259mm\u0259dov (EN) (no phone).pdf", "az": "CV \u018fmirulla M\u0259mm\u0259dov (AZ) (no phone).pdf"},
    {"slug": "gunel_seferova.html", "single": "CV G\u00fcnel S\u0259f\u0259rova (no phone).pdf"},
    {"slug": "hacali_necefoglu.html", "single": "CV Hacal\u0131 N\u0259c\u0259fo\u011flu.pdf"},
    {"slug": "ilham_akhundov.html", "single": "CV Ilham Akhundov.pdf"},
    {"slug": "ilkin_qulusoy.html", "single": "CV Ilkin Qulusoy (no phone).pdf"},
    {"slug": "ismayil_aliyev.html", "single": "CV \u0130smay\u0131l \u018fliyev.pdf"},
    {"slug": "ismixan_bayramov.html", "single": "CV \u0130smixan Bayramoglu (EN).pdf", "email": "ismihan.bayramoglu@ieu.edu.tr"},
    {"slug": "jamila_javadova_spitzberg.html", "single": "CV Jamila Javadova.pdf"},
    {"slug": "kamal_akbarov.html", "single": "CV Kamal Akbarov.pdf", "email": "kamal.akbarov@gmail.com"},
    {"slug": "kamran_rustemov.html", "single": "CV Kamran R\u00fcst\u0259mov.pdf"},
    {"slug": "mehdi_genceli.html", "single": "CV Mehdi Genceli (no phone).pdf", "email": "mehdi.genceli@marmara.edu.tr"},
    {"slug": "mehmet_riza_heyet.html", "single": "CV Mehmet R\u0131za Hey\u0259t.pdf", "email": "mrheyet@gmail.com"},
    {"slug": "mesud_efendiyev.html", "single": "CV M\u0259sud \u018ff\u0259ndiyev.pdf", "email": "messoud.efendiyev@gmail.com"},
    {"slug": "murad_abuzerli.html", "single": "CV Murad Abuz\u0259rli.pdf", "email": "murad.abuzarli@univie.ac.at"},
    {"slug": "murad_omarov.html", "single": "CV Murad Omarov (no phone).pdf", "email": "murad.omarov@nure.ua"},
    {"slug": "natiq_atakishiyev.html", "single": "CV Natiq Ataki\u015fiyev.pdf", "email": "natig_atakishiyev@hotmail.com"},
    {"slug": "nigar_masumova.html", "single": "CV Nigyar Masumovapdf.pdf", "email": "masumova@mail.ru"},
    {"slug": "lev_eppelbaum.html", "single": "CV Lev Eppelbaum (no phone).pdf", "email": "levap@tauex.tau.ac.il"},
    {"slug": "makbule_sabziyeva.html", "single": "CV Makbule Sabziyeva (TR) (no phone).pdf", "email": "makbulesabziyeva@anadolu.edu.tr"},
    {"slug": "mark_applebaum.html", "single": "CV Mark Applebaum (no phone).pdf", "email": "applebaum.mark@gmail.com"},
    {"slug": "sevda_kerimova.html", "single": "CV Karimova Sevda.pdf", "email": "sevda.aydin.k@gmail.com"},
    {"slug": "xelil_kelenter.html", "single": "CV K K\u00e4l\u00e4nt\u00e4r.pdf", "email": "gosx2020@gmail.com"},
]

SKIP_TITLES = {"curriculum vitae", "cv", "resume", "vita", "ozgecmis", "ozgecmi\u015f", "t\u0259rc\u00fcmeyi-hal", "biodata"}
LIST_RE = re.compile(r"^(\u2022|\u2023|\u25cf|\u25aa|\u2013|\u2014|\-|\*|\u25cb)\s+|\d+[\.\)]\s+|[a-z][\.\)]\s+", re.I)
PAGE_RE = re.compile(r"^\s*\d+\s*$|,\s*Ph\.?D\.?,?\s*Professor\s*\d+\s*$", re.I)
EMAIL_RE = re.compile(r"[\w.+-]+@[\w.-]+\.\w+")

PHOTO_BY_EMAIL = {
    "afina.barmanbay@kafkas.edu.tr": "afina-memmedli-barmanbay.png",
    "isayevaaygul2003@yahoo.com": "aygul-isayeva.png",
    "d.abbasova@gmail.com": "dinara-abbasova.png",
    "mehdi.genceli@marmara.edu.tr": "mehdi-genceli-ismayilov.png",
    "mrheyet@gmail.com": "mehmet-riza-heyet.png",
    "messoud.efendiyev@gmail.com": "messoud-efendiyev.png",
    "murad.abuzarli@univie.ac.at": "murad-abuzerli.png",
    "murad.omarov@nure.ua": "murad-omerov.png",
    "natig_atakishiyev@hotmail.com": "natiq-agakisiyev.png",
    "masumova@mail.ru": "nigar-masimova.png",
    "levap@tauex.tau.ac.il": "lev-v-eppelbaum.png",
    "makbulesabziyeva@anadolu.edu.tr": "meqbule-sebziyeva.png",
    "applebaum.mark@gmail.com": "mark-applebaum.png",
    "sevda.aydin.k@gmail.com": "sevda-kerimova.png",
    "gosx2020@gmail.com": "xelil-kelenter.png",
    "kamal.akbarov@gmail.com": "kamal-ekberov.png",
    "aliev.05@mail.ru": "ismayil-eliyev.png",
    "iakhundo@uwaterloo.ca": "ilham-axundov.png",
    "ilkingulusoy@gmail.com": "ilkin-qulusoy.png",
    "ismihan.bayramoglu@ieu.edu.tr": "ismixan-bayramov.png",
    "alinecef@hotmail.com": "hacali-necefoglu.png",
}


def load_catalog() -> dict:
    text = CATALOG.read_text(encoding="utf-8")
    data = json.loads(text.split("=", 1)[1].strip().rstrip(";"))
    return {r.get("email", "").lower(): r for r in data if r.get("email")}


def load_css() -> str:
    text = AFINA.read_text(encoding="utf-8")
    m = re.search(r"<style>(.*?)</style>", text, re.S)
    css = m.group(1).strip()
    if ".cv-content" not in css.split("/* Full PDF")[0]:
        css += EXTRA_CSS
    return css


def esc(s: str) -> str:
    return html.escape(s, quote=False)


def extract_lines(pdf_path: Path) -> list[dict]:
    doc = fitz.open(pdf_path)
    raw = []
    for pi, page in enumerate(doc):
        for block in page.get_text("dict").get("blocks", []):
            if block.get("type") != 0:
                continue
            for line in block.get("lines", []):
                spans = line.get("spans", [])
                if not spans:
                    continue
                text = "".join(s["text"] for s in spans).strip()
                if not text:
                    continue
                max_size = max(s["size"] for s in spans)
                bold = any(s.get("flags", 0) & 2 for s in spans)
                raw.append({"text": text, "size": max_size, "bold": bold, "page": pi, "y": line["bbox"][1]})
    doc.close()
    raw.sort(key=lambda r: (r["page"], r["y"], r["text"]))
    return raw


def dominant_size(lines: list[dict]) -> float:
    c = Counter(round(l["size"], 1) for l in lines)
    return c.most_common(1)[0][0] if c else 9.0


def clean_lines(lines: list[dict]) -> list[dict]:
    out = []
    for ln in lines:
        t = ln["text"].strip()
        if PAGE_RE.match(t):
            continue
        if t.lower().strip(": ") in SKIP_TITLES:
            continue
        out.append(ln)
    return out


def is_major_heading(ln: dict, body: float) -> bool:
    t = ln["text"].strip()
    if len(t) < 3 or len(t) > 120:
        return False
    if ln["size"] >= body + 2.0:
        return True
    if ln["size"] >= body + 1.0 and ln["bold"]:
        return True
    letters = [c for c in t if c.isalpha()]
    if not letters:
        return False
    upper = sum(1 for c in letters if c.isupper() or c in "İŞÇĞÖÜƏ")
    if upper / len(letters) > 0.85 and ln["size"] >= body + 0.5 and len(t) < 80:
        low = t.lower()
        if low in SKIP_TITLES:
            return False
        keywords = ("education", "experience", "publication", "award", "research", "employment",
                    "membership", "language", "reference", "conference", "project", "training",
                    "t\u0259hsil", "f\u0259aliyy\u0259t", "n\u0259\u015fr", "m\u00fckafat", "t\u0259cr\u00fcb\u0259",
                    "g\u00f6rev", "\u00f6\u011frenim", "yayin", "eser", "b\u00f6l\u00fcm", "work", "skills")
        if any(k in low for k in keywords):
            return True
        if re.match(r"^[A-Z]\.\s+", t) or re.match(r"^[IVX]+\.\s+", t):
            return True
    return False


def is_subheading(ln: dict, body: float) -> bool:
    t = ln["text"].strip()
    if is_major_heading(ln, body):
        return False
    if ln["bold"] and ln["size"] >= body + 0.3 and len(t) < 100:
        return True
    if t.endswith(":") and len(t) < 90:
        return True
    if re.match(r"^[A-Z]\.\s+[A-Za-z\u0130\u018f\u0259\u015e\u00c7\u011e\u00d6\u00dc].{2,100}$", t):
        return True
    return False


def is_list_line(text: str) -> bool:
    return bool(LIST_RE.match(text.strip()))


def is_table_line(text: str) -> bool:
    return bool(re.search(r"\S\s{2,}\S", text)) and len(text) > 8


def lines_to_sections(lines: list[dict]) -> list[dict]:
    body = dominant_size(lines)
    sections = [{"title": "Curriculum Vitae", "lines": []}]
    for ln in lines:
        if is_major_heading(ln, body):
            sections.append({"title": ln["text"].strip().strip(":"), "lines": []})
        else:
            sections[-1]["lines"].append(ln)
    return [s for s in sections if s["lines"] or s["title"] != "Curriculum Vitae"]


def render_lines(lines: list[dict], body: float) -> str:
    parts = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        t = ln["text"].strip()
        if is_subheading(ln, body):
            parts.append(f'<h3 class="cv-subhead">{esc(t.rstrip(":"))}</h3>')
            i += 1
            continue
        if is_list_line(t):
            items = []
            while i < len(lines):
                cur = lines[i]["text"].strip()
                if not cur:
                    i += 1
                    break
                if is_major_heading(lines[i], body) or is_subheading(lines[i], body):
                    break
                if is_list_line(cur):
                    items.append(re.sub(LIST_RE, "", cur, count=1).strip())
                    i += 1
                elif items:
                    items[-1] += " " + cur
                    i += 1
                else:
                    break
            tag = "ol" if items and re.match(r"^\d+", items[0]) else "ul"
            parts.append(f"<{tag}>" + "".join(f"<li>{esc(x)}</li>" for x in items if x) + f"</{tag}>")
            continue
        if is_table_line(t):
            tbl = [t]
            i += 1
            while i < len(lines):
                cur = lines[i]["text"]
                if is_major_heading(lines[i], body) or is_subheading(lines[i], body) or is_list_line(cur.strip()):
                    break
                if is_table_line(cur) or (tbl and not is_list_line(cur.strip())):
                    tbl.append(cur.rstrip())
                    i += 1
                else:
                    break
            parts.append(f'<pre class="cv-pre">{esc(chr(10).join(tbl))}</pre>')
            continue
        para = [t]
        i += 1
        while i < len(lines):
            nxt = lines[i]
            nt = nxt["text"].strip()
            if not nt:
                i += 1
                break
            if is_major_heading(nxt, body) or is_subheading(nxt, body) or is_list_line(nt) or is_table_line(nt):
                break
            para.append(nt)
            i += 1
        parts.append(f"<p>{esc(' '.join(para))}</p>")
    return "\n".join(parts)


def render_sections_from_pdf(pdf_path: Path) -> str:
    lines = clean_lines(extract_lines(pdf_path))
    body = dominant_size(lines)
    sections = lines_to_sections(lines)
    chunks = []
    for sec in sections:
        body_html = render_lines(sec["lines"], body)
        if not body_html.strip():
            continue
        chunks.append(
            '<section class="section">\n'
            f'  <h2 class="section-title">{esc(sec["title"])}</h2>\n'
            f'  <div class="cv-content">\n    {body_html}\n  </div>\n</section>'
        )
    plain = "\n".join(l["text"] for l in lines)
    EXTRACT_DIR.mkdir(parents=True, exist_ok=True)
    (EXTRACT_DIR / (pdf_path.stem + ".txt")).write_text(plain, encoding="utf-8")
    return "\n\n  ".join(chunks)


def extract_html_parts(path: Path) -> dict | None:
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    title_m = re.search(r"<title>(.*?)</title>", text, re.S)
    hero_m = re.search(r"(<header class=\"hero\">.*?</header>)", text, re.S)
    footer_m = re.search(r"(<footer>.*?</footer>)", text, re.S)
    photo_m = re.search(r'scientists-photos/([^"\']+)', text)
    if hero_m and footer_m:
        return {"title": title_m.group(1).strip() if title_m else "Curriculum Vitae", "hero": hero_m.group(1), "footer": footer_m.group(1), "photo": photo_m.group(1) if photo_m else None}
    return None


def build_hero(entry: dict, catalog: dict, pdf_path: Path | None = None) -> str:
    email = (entry.get("email") or "").lower()
    row = catalog.get(email, {})
    name = entry.get("name") or row.get("ad_soyad", entry["slug"].replace(".html", "").replace("_", " ").title())
    photo = PHOTO_BY_EMAIL.get(email, entry.get("photo", "img_001_p61.jpeg"))
    if pdf_path:
        lines = clean_lines(extract_lines(pdf_path))[:20]
        for ln in lines:
            em = EMAIL_RE.search(ln["text"])
            if em and not email:
                email = em.group(0).lower()
    rank = row.get("elmi_derece", "Ph.D.")
    cred = {"PhD": "Ph.D.", "Prof.Dr.": "Prof. Dr.", "Ed.D.": "Ed.D."}.get(rank, rank)
    return f'''<header class="hero">
    <div class="hero-top">
      <div class="hero-text">
        <span class="cv-label"><span class="lang en">Curriculum Vitae</span><span class="lang az">T\u0259rc\u00fcmeyi-hal</span></span>
        <h1><span class="lang en">{esc(name)}</span><span class="lang az">{esc(name)}</span></h1>
        <p class="subtitle"><span class="lang en block">{esc(row.get("ixtilas", ""))}</span><span class="lang az block">{esc(row.get("ixtilas", ""))}</span></p>
      </div>
      <figure class="hero-photo"><img src="../images/scientists-photos/{esc(photo)}" alt="{esc(name)}" width="160" height="200" loading="eager" /></figure>
    </div>
    <dl class="rank-bar">
      <div class="rank-item"><dt><span class="lang en">Academic Rank</span><span class="lang az">Akademik r\u00fctb\u0259</span></dt><dd>{esc(cred)}</dd></div>
      <div class="rank-item"><dt><span class="lang en">Country</span><span class="lang az">Ya\u015fad\u0131\u011f\u0131 \u00f6lk\u0259</span></dt><dd>{esc(row.get("yasadigi_olke", ""))}</dd></div>
      <div class="rank-item"><dt><span class="lang en">E-mail</span><span class="lang az">E-po\u00e7t</span></dt><dd>{esc(email)}</dd></div>
    </dl>
  </header>'''


def build_footer(name: str) -> str:
    return f'''<footer>
    <span class="lang en">{esc(name)} &ensp;\u00b7&ensp; Curriculum Vitae</span>
    <span class="lang az">{esc(name)} &ensp;\u00b7&ensp; T\u0259rc\u00fcmeyi-hal</span>
  </footer>'''


def build_page(title, css, hero, body_en, body_az, footer) -> str:
    return f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>{esc(title)}</title>
  <style>
{css}
  </style>
</head>
<body>
<main class=\"page\">
  <div class=\"lang-switch\">
    <button id=\"btn-en\" type=\"button\" onclick=\"setLang('en')\">English</button>
    <button id=\"btn-az\" type=\"button\" onclick=\"setLang('az')\">Az\u0259rbaycan</button>
  </div>
  {hero}
  <div class=\"lang en block\">{body_en}</div>
  <div class=\"lang az block\">{body_az}</div>
  {footer}
</main>
<script>
  function setLang(lang) {{
    document.documentElement.lang = lang;
    document.querySelectorAll('.lang').forEach(function(el) {{ el.classList.remove('active'); }});
    document.querySelectorAll('.lang.' + lang).forEach(function(el) {{ el.classList.add('active'); }});
    document.getElementById('btn-en').classList.toggle('active', lang === 'en');
    document.getElementById('btn-az').classList.toggle('active', lang === 'az');
  }}
  setLang('en');
</script>
</body>
</html>
"""


def resolve_pdf(name: str) -> Path:
    p = PDF_DIR / name
    if p.exists():
        return p
    alt = list(PDF_DIR.glob(name.replace(".pdf", "*.pdf")))
    if alt:
        return alt[0]
    raise FileNotFoundError(name)


def rebuild_one(entry: dict, css: str, catalog: dict) -> None:
    slug = entry["slug"]
    out = CV_DIR / slug
    parts = extract_html_parts(out)
    email = (entry.get("email") or "").lower()
    name = catalog.get(email, {}).get("ad_soyad", slug.replace("_", " ").replace(".html", ""))

    if entry.get("en") and entry.get("az"):
        pdf_en = resolve_pdf(entry["en"])
        pdf_az = resolve_pdf(entry["az"])
        body_en = render_sections_from_pdf(pdf_en)
        body_az = render_sections_from_pdf(pdf_az)
        hero_src = pdf_en
    else:
        pdf = resolve_pdf(entry["single"])
        body = render_sections_from_pdf(pdf)
        body_en = body
        body_az = body
        hero_src = pdf

    if parts:
        hero, footer, title = parts["hero"], parts["footer"], parts["title"]
    else:
        hero = build_hero(entry, catalog, hero_src)
        footer = build_footer(name)
        title = f"Curriculum Vitae \u2014 {name}"

    page = build_page(title, css, hero, body_en, body_az, footer)
    out.write_text(page, encoding="utf-8")
    print(f"OK {slug}: {out.stat().st_size // 1024} KB", flush=True)


def main() -> None:
    css = load_css()
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
