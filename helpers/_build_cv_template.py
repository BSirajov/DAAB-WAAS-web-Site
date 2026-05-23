# -*- coding: utf-8 -*-
"""Generate cv/cv_template.html — master DAAB bilingual CV reference template."""
from pathlib import Path
import re

ROOT = Path(r"c:\Users\BSira\Documents\GitHub\DAAB-WAAS web site")
AFINA = ROOT / "cv" / "afina_barmanbay.html"
OUT = ROOT / "cv" / "cv_template.html"

EXTRA_CSS = """
    /* ── Extended template components ── */
    .kv-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px 32px; padding: 20px 22px; }
    .kv-item dt { font-size: 11px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--blue-mid); margin-bottom: 4px; }
    .kv-item dd { font-size: 14.5px; color: var(--body-text); margin: 0; line-height: 1.6; }
    .awards-block { padding: 18px 22px; }
    .awards-list { margin: 0; padding-left: 22px; font-size: 14.5px; line-height: 1.75; }
    .awards-list li { margin-bottom: 8px; }
    .ref-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; padding: 20px 22px; }
    .ref-card { background: var(--bg); border: 1px solid #d0dde8; border-left: 4px solid var(--blue-dark); padding: 16px 18px; border-radius: 3px; font-size: 14px; line-height: 1.65; }
    .ref-card strong { display: block; color: var(--blue-dark); margin-bottom: 6px; font-size: 15px; }
    .badge-row { display: flex; flex-wrap: wrap; gap: 8px; padding: 0 22px 20px; }
    .badge { display: inline-block; padding: 5px 12px; background: var(--blue-light); color: var(--blue-dark); border: 1px solid var(--blue-accent); border-radius: 999px; font-size: 13px; font-weight: 600; }
    .template-banner { background: #fff8e6; border: 1px solid #e6d9a8; color: #6b5a1e; padding: 14px 18px; border-radius: 4px; margin-bottom: 20px; font-size: 14px; line-height: 1.6; }
    .template-banner code { background: rgba(0,0,0,0.06); padding: 1px 6px; border-radius: 3px; }
    @media (max-width: 760px) { .kv-grid, .ref-grid { grid-template-columns: 1fr; } }
"""

afina = AFINA.read_text(encoding="utf-8")
css_m = re.search(r"<style>(.*?)</style>", afina, re.S)
css = css_m.group(1).strip()
if ".kv-grid" not in css:
    css += EXTRA_CSS

def bi(en, az):
    return f'<span class="lang en">{en}</span><span class="lang az">{az}</span>'

def bib(en, az):
    return f'<span class="lang en block">{en}</span><span class="lang az block">{az}</span>'

def section(title_en, title_az, inner):
    return f'''  <section class="section">
    <h2 class="section-title">{bi(title_en, title_az)}</h2>
{inner}
  </section>'''

def lang_block(sections_html):
    return f'  <div class="lang en block">\n{sections_html}\n  </div>'

body_en = """
<!-- Copy sections below into EN tab; remove unused blocks; keep bilingual pairs aligned where possible -->

""" + section("Personal Information", "Şəxsi məlumat",
    '''    <div class="kv-grid">
      <div class="kv-item"><dt>''' + bi("Full Name", "Ad, soyad") + '''</dt><dd>Dr. Example Scientist</dd></div>
      <div class="kv-item"><dt>''' + bi("Date of Birth", "Doğum tarixi") + '''</dt><dd>01 January 1970</dd></div>
      <div class="kv-item"><dt>''' + bi("Place of Birth", "Doğum yeri") + '''</dt><dd>''' + bi("Baku, Azerbaijan", "Bakı, Azərbaycan") + '''</dd></div>
      <div class="kv-item"><dt>''' + bi("Citizenship", "Vətəndaşlıq") + '''</dt><dd>''' + bi("Azerbaijan", "Azərbaycan") + '''</dd></div>
      <div class="kv-item"><dt>''' + bi("E-mail", "E-poçt") + '''</dt><dd>name@institution.edu</dd></div>
      <div class="kv-item"><dt>''' + bi("Phone", "Telefon") + '''</dt><dd>+XX XXX XXX XX XX</dd></div>
      <div class="kv-item"><dt>''' + bi("ORCID", "ORCID") + '''</dt><dd>0000-0000-0000-0000</dd></div>
      <div class="kv-item"><dt>''' + bi("Website", "Vebsayt") + '''</dt><dd>https://example.edu/profile</dd></div>
    </div>''') + "\n\n" + section("Academic Profile", "Akademik profil",
    '''    <div class="callout">''' + bib(
        "Concise narrative summary of scholarly identity, major contributions, research program, and international standing. Replace with content from the source CV without shortening.",
        "Elmi fəaliyyətin qısa xülasəsi: əsas töhfələr, tədqiqat istiqamətləri və beynəlxalq tanınma. Mənbə CV-dən tam mətni qoruyun.") + '''</div>
    <div class="stats">
      <div class="stat-item"><span class="stat-num">XX</span><span class="stat-label">''' + bi("Publications", "Nəşr") + '''</span></div>
      <div class="stat-item"><span class="stat-num">XX</span><span class="stat-label">''' + bi("Citations", "Sitat") + '''</span></div>
      <div class="stat-item"><span class="stat-num">h-XX</span><span class="stat-label">''' + bi("h-index", "h-indeks") + '''</span></div>
      <div class="stat-item"><span class="stat-num">XX+</span><span class="stat-label">''' + bi("Years", "İl") + '''</span></div>
    </div>''') + "\n\n" + section("Research Interests", "Tədqiqat sahələri",
    '''    <div class="badge-row">
      <span class="badge">''' + bi("Research area 1", "Tədqiqat sahəsi 1") + '''</span>
      <span class="badge">''' + bi("Research area 2", "Tədqiqat sahəsi 2") + '''</span>
      <span class="badge">''' + bi("Research area 3", "Tədqiqat sahəsi 3") + '''</span>
    </div>''') + "\n\n" + section("Core Competencies", "Əsas kompetensiyalar",
    '''    <div class="competency-grid">
      <div class="comp-group"><h3>''' + bi("Research", "Tədqiqat") + '''</h3><ul>
        <li>''' + bi("Competency item", "Kompetensiya") + '''</li>
        <li>''' + bi("Competency item", "Kompetensiya") + '''</li></ul></div>
      <div class="comp-group"><h3>''' + bi("Teaching", "Tədris") + '''</h3><ul>
        <li>''' + bi("Competency item", "Kompetensiya") + '''</li></ul></div>
      <div class="comp-group"><h3>''' + bi("Technical Skills", "Texniki bacarıqlar") + '''</h3><ul>
        <li>''' + bi("Software / methods", "Proqram / metod") + '''</li></ul></div>
      <div class="comp-group"><h3>''' + bi("Languages", "Dillər") + '''</h3><ul>
        <li>''' + bi("English — fluent", "İngilis — səlis") + '''</li>
        <li>''' + bi("Azerbaijani — native", "Azərbaycan — ana dili") + '''</li></ul></div>
    </div>''') + "\n\n" + section("Education", "Təhsil",
    '''    <div class="education-grid">
      <div class="edu-card"><div class="period">2010–2014</div><h3>Ph.D.</h3><p>''' + bi("Field, Institution, Country. Dissertation title; supervisor.", "İxtisas, qurum, ölkə. Dissertasiya mövzusu; rəhbər.") + '''</p></div>
      <div class="edu-card"><div class="period">2005–2007</div><h3>''' + bi("Master's", "Magistr") + '''</h3><p>''' + bi("Field, Institution.", "İxtisas, qurum.") + '''</p></div>
      <div class="edu-card"><div class="period">2000–2004</div><h3>''' + bi("Bachelor's", "Bakalavr") + '''</h3><p>''' + bi("Field, Institution.", "İxtisas, qurum.") + '''</p></div>
      <div class="edu-card"><div class="period">1995–2000</div><h3>''' + bi("Secondary / other", "Orta / digər") + '''</h3><p>''' + bi("School, location.", "Məktəb, yer.") + '''</p></div>
    </div>''') + "\n\n" + section("Professional Experience", "Peşəkar fəaliyyət",
    '''    <div class="timeline">
      <article class="item"><div class="period">2020–<br>''' + bi("Present", "indiyədək") + '''</div><div>
        <h3>''' + bi("Institution Name, City, Country", "Qurum adı, şəhər, ölkə") + '''</h3>
        <span class="role">''' + bi("Professor / Role title", "Professor / Vəzifə") + '''</span>
        <p>''' + bi("Full description of responsibilities, achievements, and scope.", "Vəzifə öhdəlikləri, nailiyyətlər və fəaliyyət sahəsinin tam təsviri.") + '''</p>
      </div></article>
      <article class="item"><div class="period">2015–2020</div><div>
        <h3>''' + bi("Previous institution", "Əvvəlki qurum") + '''</h3>
        <span class="role">''' + bi("Associate Professor", "Dosent") + '''</span>
        <p>''' + bi("Description.", "Təsvir.") + '''</p>
      </div></article>
    </div>''') + "\n\n" + section("Administrative Appointments", "İdarəetmə vəzifələri",
    '''    <div class="timeline">
      <article class="item"><div class="period">2018–2022</div><div>
        <h3>''' + bi("Department / Faculty", "Kafedra / fakültə") + '''</h3>
        <span class="role">''' + bi("Department Head", "Kafedra müdiri") + '''</span>
        <p>''' + bi("Administrative duties and outcomes.", "İnzibati öhdəliklər və nəticələr.") + '''</p>
      </div></article>
    </div>''') + "\n\n" + section("Research Projects & Grants", "Tədqiqat layihələri və qrantlar",
    '''    <div class="pub-block"><div class="pub-category"><ul>
      <li>''' + bi("Project title — Funding agency, role, dates, amount (if applicable).", "Layihə adı — maliyyələşdirmə qurumu, rol, tarixlər.") + '''</li>
    </ul></div></div>''') + "\n\n" + section("Teaching & Supervision", "Tədris və elmi rəhbərlik",
    '''    <div class="cv-content">
      <h3 class="cv-subhead">''' + bi("Courses Taught", "Tədris olunan fənlər") + '''</h3>
      <ul><li>''' + bi("Course name — level — institution — years.", "Fənn adı — səviyyə — qurum — illər.") + '''</li></ul>
      <h3 class="cv-subhead">''' + bi("Supervised Theses", "Rəhbərlik edilmiş dissertasiyalar") + '''</h3>
      <ol><li>''' + bi("Student name — degree — title — year — status.", "Tələbə adı — dərəcə — mövzu — il — status.") + '''</li></ol>
    </div>''') + "\n\n" + section("Publications", "Nəşrlər",
    '''    <div class="pub-block">
      <div class="pub-category"><h3>''' + bi("Books & Monographs", "Kitablar və monoqrafiyalar") + '''</h3><ol>
        <li><em>''' + bi("Book title</em>, Publisher, year.", "Kitab adı</em>, nəşriyyat, il.") + '''</li></ol></div>
      <div class="pub-category"><h3>''' + bi("Peer-Reviewed Journal Articles", "Respublikasiya olunan jurnal məqalələri") + '''</h3><ol>
        <li>''' + bi("Author(s). \"Article title.\" <em>Journal</em>, vol(issue), pages, year. DOI.", "Müəllif(lər). \"Məqalə.\" <em>Jurnal</em>, cild, səhifə, il. DOI.") + '''</li></ol></div>
      <div class="pub-category"><h3>''' + bi("Conference Proceedings", "Konfrans materialları") + '''</h3><ol>
        <li>''' + bi("Full conference citation.", "Tam konfrans sitatı.") + '''</li></ol></div>
      <div class="pub-category"><h3>''' + bi("Book Chapters", "Kitab fəsilləri") + '''</h3><ol>
        <li>''' + bi("Chapter citation.", "Fəsil sitatı.") + '''</li></ol></div>
      <div class="pub-category"><h3>''' + bi("Patents", "Patentlər") + '''</h3><ul>
        <li>''' + bi("Patent number, title, jurisdiction, year.", "Patent nömrəsi, ad, ölkə, il.") + '''</li></ul></div>
    </div>''') + "\n\n" + section("Awards & Honors", "Mükafatlar və fəxri adlar",
    '''    <div class="awards-block"><ul class="awards-list">
      <li>''' + bi("Award name — granting body — year.", "Mükafat adı — verən qurum — il.") + '''</li>
      <li>''' + bi("Honorary title — year.", "Fəxri ad — il.") + '''</li>
    </ul></div>''') + "\n\n" + section("Fellowships & Visiting Positions", "Stipendiyalar və ezamiyyə vəzifələri",
    '''    <div class="timeline">
      <article class="item"><div class="period">2019</div><div>
        <h3>''' + bi("Host institution, country", "Qəbul edən qurum, ölkə") + '''</h3>
        <span class="role">''' + bi("Visiting Professor / Fellow", "Visiting professor / Fellow") + '''</span>
        <p>''' + bi("Purpose and activities.", "Məqsəd və fəaliyyət.") + '''</p>
      </div></article>
    </div>''') + "\n\n" + section("Professional Memberships", "Peşəkar üzvlüklər",
    '''    <div class="pub-block"><ul>
      <li>''' + bi("Society / academy — role — years.", "Cəmiyyət / akademiya — rol — illər.") + '''</li>
    </ul></div>''') + "\n\n" + section("Editorial & Review Activities", "Redaktorluq və rəyçilik",
    '''    <div class="pub-block"><ul>
      <li>''' + bi("Editor / reviewer — journal or publisher — years.", "Redaktor / rəyçi — jurnal — illər.") + '''</li>
    </ul></div>''') + "\n\n" + section("Conference & Invited Presentations", "Konfrans və dəvətli məruzələr",
    '''    <div class="pub-block"><ol>
      <li>''' + bi("Presentation title — event — location — year.", "Məruzə — tədbir — yer — il.") + '''</li>
    </ol></div>''') + "\n\n" + section("Certifications & Licenses", "Sertifikatlar və lisenziyalar",
    '''    <div class="pub-block"><ul>
      <li>''' + bi("Certification — issuer — year.", "Sertifikat — verən — il.") + '''</li>
    </ul></div>''') + "\n\n" + section("References", "Referanslar",
    '''    <div class="ref-grid">
      <div class="ref-card"><strong>Prof. Reference Name</strong>''' + bi(
        "Title, Institution<br>E-mail: ref@uni.edu<br>Phone: +XX XXX XXX XX XX",
        "Vəzifə, qurum<br>E-poçt: ref@uni.edu<br>Telefon: +XX XXX XXX XX XX") + '''</div>
      <div class="ref-card"><strong>Dr. Reference Name</strong>''' + bi(
        "Title, Institution<br>E-mail: ref2@uni.edu",
        "Vəzifə, qurum<br>E-poçt: ref2@uni.edu") + '''</div>
    </div>''') + "\n\n" + section("Additional Information (PDF-style block)", "Əlavə məlumat (PDF tipli blok)",
    '''    <div class="cv-content">
      <p>''' + bi("Use this block for content extracted directly from PDF when structured parsing is impractical.", "Strukturlaşdırılmış parse mümkün olmadıqda PDF-dən birbaşa məzmun üçün bu bloku istifadə edin.") + '''</p>
      <h3 class="cv-subhead">''' + bi("Subsection heading", "Alt bölmə başlığı") + '''</h3>
      <ul><li>''' + bi("Bullet item from source document.", "Mənbə sənəddən element.") + '''</li></ul>
      <pre class="cv-pre">''' + bi("Tabular or multi-column text from PDF\nColumn A    Column B    Column C\nValue 1     Value 2     Value 3", "PDF-dən cədvəl tipli mətn\nSütun A    Sütun B    Sütun C") + '''</pre>
      <table class="cv-table"><thead><tr><th>''' + bi("Period", "Dövr") + '''</th><th>''' + bi("Institution", "Qurum") + '''</th><th>''' + bi("Role", "Rol") + '''</th></tr></thead>
      <tbody><tr><td>2020–2024</td><td>''' + bi("Example University", "Nümunə universitet") + '''</td><td>''' + bi("Professor", "Professor") + '''</td></tr></tbody></table>
    </div>''')

body_az = body_en.replace('lang en', 'LANG_EN_PLACEHOLDER').replace('lang az', 'lang en').replace('LANG_EN_PLACEHOLDER', 'lang az')
# Fix: AZ block should mirror structure - for template, duplicate EN structure with AZ labels already in bi() - both blocks same is OK for template

html = f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>DAAB CV Template — Reference</title>
  <style>
{css}
  </style>
</head>
<body>
<main class=\"page\">

  <div class=\"template-banner\">
    <strong>DAAB CV master template.</strong> Reference file only — not linked on the public site.
    Copy sections as needed; preserve full source content; use <code>cv/cv_template.html</code> for styling patterns.
    Bilingual fields use <code>.lang.en</code> / <code>.lang.az</code>. Remove unused sections rather than summarizing content.
  </div>

  <div class=\"lang-switch\">
    <button id=\"btn-en\" type=\"button\" onclick=\"setLang('en')\">English</button>
    <button id=\"btn-az\" type=\"button\" onclick=\"setLang('az')\">Az\u0259rbaycan</button>
  </div>

  <header class=\"hero\">
    <div class=\"hero-top\">
      <div class=\"hero-text\">
        <span class=\"cv-label\">{bi("Curriculum Vitae", "T\u0259rc\u00fcmeyi-hal")}</span>
        <h1>{bi("Full Name, Ph.D.", "Ad Soyad, Ph.D.")}</h1>
        <p class=\"subtitle\">{bib(
          "One-paragraph professional summary: field, institution, specialization, and distinguishing achievements.",
          "Peşəkar x\u00fclas\u0259: ixtisas, qurum, ixtisasla\u015fma sah\u0259si v\u0259 f\u0259rql\u0259ndirici nailiyy\u0259tl\u0259r.")}</p>
      </div>
      <figure class=\"hero-photo\">
        <img src=\"../images/scientists-photos/placeholder.png\" alt=\"Photo\" width=\"160\" height=\"200\" loading=\"eager\" />
      </figure>
    </div>
    <dl class=\"rank-bar\">
      <div class=\"rank-item\"><dt>{bi("Academic Rank", "Akademik r\u00fctb\u0259")}</dt><dd>{bi("Prof. Dr.", "Prof. dr.")}</dd></div>
      <div class=\"rank-item\"><dt>{bi("Institution", "Qurum")}</dt><dd>{bi("University Name", "Universitet ad\u0131")}</dd></div>
      <div class=\"rank-item\"><dt>{bi("Department", "Kafedra")}</dt><dd>{bi("Department / Institute", "Kafedra / institut")}</dd></div>
      <div class=\"rank-item\"><dt>{bi("Location", "Yer")}</dt><dd>{bi("City, Country", "\u015c\u0259h\u0259r, \u00f6lk\u0259")}</dd></div>
      <div class=\"rank-item\"><dt>{bi("E-mail", "E-po\u00e7t")}</dt><dd>name@institution.edu</dd></div>
      <div class=\"rank-item\"><dt>{bi("Phone", "Telefon")}</dt><dd>+XX XXX XXX XX XX</dd></div>
      <div class=\"rank-item\"><dt>ORCID</dt><dd>0000-0000-0000-0000</dd></div>
      <div class=\"rank-item\"><dt>{bi("Website", "Vebsayt")}</dt><dd>https://example.edu</dd></div>
    </dl>
  </header>

{lang_block(body_en)}

{lang_block(body_en)}

  <footer>
    <span class=\"lang en\">Full Name &ensp;\u00b7&ensp; Curriculum Vitae &ensp;\u00b7&ensp; Institution, Country</span>
    <span class=\"lang az\">Ad Soyad &ensp;\u00b7&ensp; T\u0259rc\u00fcmeyi-hal &ensp;\u00b7&ensp; Qurum, \u00f6lk\u0259</span>
  </footer>

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

OUT.write_text(html, encoding="utf-8")
print(f"Wrote {OUT} ({OUT.stat().st_size // 1024} KB)")
