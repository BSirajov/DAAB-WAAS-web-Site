# -*- coding: utf-8 -*-
from pathlib import Path

ROOT = Path(r"c:\Users\BSira\Documents\GitHub\DAAB-WAAS web site")
TEMPLATE = ROOT / "cv" / "aytekin_huseynli.html"
OUT = ROOT / "cv" / "eldar_veliyev.html"

text = TEMPLATE.read_text(encoding="utf-8")
start = text.index("<main class=\"page\">")
end = text.index("</main>") + len("</main>")
prefix = text[:start]
suffix = text[end:]

main = r"""
  <div class="lang-switch">
    <button id="btn-en" type="button" onclick="setLang('en')">English</button>
    <button id="btn-az" type="button" onclick="setLang('az')">Azərbaycan</button>
  </div>

  <header class="hero">
    <div class="hero-top">
      <div class="hero-text">
        <span class="cv-label">
          <span class="lang en">Curriculum Vitae</span>
          <span class="lang az">Tərcümeyi-hal</span>
        </span>
        <h1>
          <span class="lang en">Eldar Veliyev, D.Sc., Professor</span>
          <span class="lang az">Eldar Vəliyev, elmlər doktoru, professor</span>
        </h1>
        <p class="subtitle">
          <span class="lang en">Radiophysicist and professor specializing in diffraction theory, electromagnetic wave scattering, integral equations, and fractional operators in applied electromagnetics. Vice-Rector for Scientific and Pedagogical Affairs at NTU &ldquo;Kharkiv Polytechnic Institute&rdquo;, Ukraine.</span>
          <span class="lang az">Difraksiya nəzəriyyəsi, elektromaqnit dalğaların səpilməsi, inteqral tənliklər və tətbiqi elektromaqnitikdə fraksional operatorlar üzrə ixtisaslaşmış radiophysicist və professor. Ukrayna Milli Texniki Universiteti &ldquo;Xarkov Politexnik İnstitutu&rdquo;nun elmi və pedaqoji işlər üzrə prorektoru.</span>
        </p>
      </div>
      <figure class="hero-photo">
        <img src="../images/scientists-photos/eldar-veliyev.png" alt="Eldar Veliyev" width="160" height="200" loading="eager" />
      </figure>
    </div>
    <dl class="rank-bar">
      <div class="rank-item">
        <dt><span class="lang en">Academic Rank</span><span class="lang az">Akademik rütbə</span></dt>
        <dd><span class="lang en">Doctor of Science, Professor</span><span class="lang az">Elmlər doktoru, professor</span></dd>
      </div>
      <div class="rank-item">
        <dt><span class="lang en">Institution</span><span class="lang az">Qurum</span></dt>
        <dd><span class="lang en">NTU &ldquo;Kharkiv Polytechnic Institute&rdquo;, Ukraine</span><span class="lang az">NTU &ldquo;Xarkov Politexnik İnstitutu&rdquo;, Ukrayna</span></dd>
      </div>
      <div class="rank-item">
        <dt><span class="lang en">E-mail</span><span class="lang az">E-poçt</span></dt>
        <dd>veliev51@gmail.com</dd>
      </div>
      <div class="rank-item">
        <dt><span class="lang en">Location</span><span class="lang az">Yer</span></dt>
        <dd><span class="lang en">Kharkiv, Ukraine</span><span class="lang az">Xarkov, Ukrayna</span></dd>
      </div>
    </dl>
  </header>
"""

# append remaining sections from external part file if present
part = ROOT / "helpers" / "eldar_veliyev_sections.html"
if part.exists():
    main += part.read_text(encoding="utf-8")

full = prefix + "<main class=\"page\">" + main + suffix
full = full.replace("Curriculum Vitae — Aytekin Huseynli", "Curriculum Vitae — Eldar Veliyev")
OUT.write_text(full, encoding="utf-8")
print("Wrote", OUT, OUT.stat().st_size)