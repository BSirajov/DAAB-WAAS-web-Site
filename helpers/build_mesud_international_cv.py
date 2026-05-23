# -*- coding: utf-8 -*-
"""Build cv/mesud_efendiyev.html from PDF using international CV template."""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "templates" / "international-cv-template.html"
OUT = ROOT / "cv" / "mesud_efendiyev.html"


def esc(s: str) -> str:
    return html.escape(s, quote=False)


def load_css() -> str:
    text = TEMPLATE.read_text(encoding="utf-8")
    m = re.search(r"<style>(.*?)</style>", text, re.S)
    if not m:
        raise ValueError("CSS not found in template")
    return m.group(1).strip()


def section(h2_id: str, title: str, inner: str) -> str:
    return f"""  <section id="{h2_id}" aria-labelledby="heading-{h2_id}">
    <h2 id="heading-{h2_id}">{esc(title)}</h2>
{inner}
  </section>"""


def entry(org: str, location: str, dates: str, role: str, details: str) -> str:
    return f"""    <article class="entry">
      <div class="entry-header">
        <div class="org">
          <h3>{org}</h3>
          <span class="location">{location}</span>
        </div>
        <time class="dates">{dates}</time>
      </div>
      <span class="role">{role}</span>
      <div class="details">{details}</div>
    </article>"""


CSS = load_css()

BODY = """
  <header class="cv-header">
    <h1>Messoud A. Efendiyev, Ph.D.</h1>
    <p class="tagline">Rector&rsquo;s Distinguished Visiting Professor &middot; Dynamical Systems &middot; Mathematical Biology</p>
    <div class="contact-grid">
      <div class="contact-item"><span class="label">Email</span><a href="mailto:messoud.efendiyev@gmail.com">messoud.efendiyev@gmail.com</a></div>
      <div class="contact-item"><span class="label">Email</span><a href="mailto:messoud.efendiyev@tum.de">messoud.efendiyev@tum.de</a></div>
      <div class="contact-item"><span class="label">Email</span><a href="mailto:m.efendiyev@marmara.edu.tr">m.efendiyev@marmara.edu.tr</a></div>
      <div class="contact-item"><span class="label">Phone</span><span>+90 555 147 4674</span></div>
      <div class="contact-item"><span class="label">Phone</span><span>+49 7144 809751</span></div>
      <div class="contact-item"><span class="label">Location</span><span>Istanbul, Turkey &middot; Munich, Germany</span></div>
      <div class="contact-item"><span class="label">Affiliation</span><span>Marmara University; Helmholtz Zentrum M&uuml;nchen; TUM Munich</span></div>
      <div class="contact-item"><span class="label">Institute</span><span>Istanbul Institute of Computational Biology (ICB)</span></div>
    </div>
  </header>

  <div class="metrics" role="group" aria-label="Research metrics">
    <div class="metric"><span class="value">8</span><span class="label">Books</span></div>
    <div class="metric"><span class="value">186</span><span class="label">Publications</span></div>
    <div class="metric"><span class="value">50+</span><span class="label">Years experience</span></div>
    <div class="metric"><span class="value">AZ</span><span class="label">Citizenship</span></div>
  </div>

""" + section(
    "additional",
    "Personal Information",
    """    <ul>
      <li><strong>Gender:</strong> Male</li>
      <li><strong>Date of Birth:</strong> October 21, 1953</li>
      <li><strong>Place of Birth:</strong> Zaqatala, Azerbaijan</li>
      <li><strong>Citizenship:</strong> Azerbaijan</li>
      <li><strong>Mailing Address:</strong> Amselweg 9, 71563 Affalterbach, Germany; Marmara University Guesthouse, Fahrettin Kerim Gokay St., Goztepe Campus, 34722 Kadikoy / Istanbul</li>
      <li><strong>Home Address:</strong> Amselweg 9, 71563 Affalterbach, Germany</li>
      <li><strong>Marital Status:</strong> Married; with a son and a daughter</li>
    </ul>""",
) + section(
    "education",
    "Education",
    entry(
        "Dr. Science (Habilitation)",
        "Freie Universit&auml;t Berlin, Germany",
        "1998",
        "",
        "<p>Habilitation, FU-Berlin.</p>",
    )
    + entry(
        "Ph.D.",
        "Lomonosov Moscow State University, USSR &mdash; Nr. 011859",
        "1980",
        "",
        "<p>PhD, Lomonosov MSU.</p>",
    )
    + entry(
        "Diploma (with distinction)",
        "Baku / Moscow &mdash; Lomonosov Moscow State University, USSR &mdash; Nr. 769810",
        "1975",
        "",
        "<p>Distinguish Diplom.</p>",
    ),
) + section(
    "experience",
    "Professional Experience",
    entry(
        "Marmara University",
        "Istanbul, Turkey",
        "2020 &ndash; Present",
        "Rector&rsquo;s Distinguished Visiting Professor",
        "",
    )
    + entry(
        "University of Waterloo, York University, University of Toronto and Fields Institute",
        "Canada",
        "2019 &ndash; 2020",
        "James D. Murray Distinguished Professor",
        "",
    )
    + entry(
        "University of Toronto and Fields Institute",
        "Canada",
        "2018",
        "Dean&rsquo;s Distinguished Professor",
        "",
    )
    + entry(
        "Helmholtz Center Munich / TUM Munich",
        "Germany",
        "2008 &ndash; Present",
        "Head of Dept. Dynamical Systems / Leading Professor / Guest Professor",
        "",
    )
    + entry(
        "TUM Munich",
        "Germany",
        "2005 &ndash; 2008",
        "Professor",
        "",
    )
    + entry(
        "University of Stuttgart",
        "Germany",
        "2000 &ndash; 2005",
        "Professor, Scientific Manager / SFB-404",
        "",
    )
    + entry(
        "WIAS Berlin",
        "Germany",
        "1999 &ndash; 2000",
        "Visiting Professor",
        "",
    )
    + entry(
        "Freie Universit&auml;t Berlin",
        "Germany",
        "1998 &ndash; 2000",
        "Visiting Professor",
        "",
    )
    + entry(
        "Free University Berlin",
        "Germany",
        "1994 &ndash; 1998",
        "Wissenschaftlicher Mitarbeiter",
        "",
    )
    + entry(
        "University of Stuttgart",
        "Germany",
        "1993 &ndash; 1994",
        "Visiting Professor",
        "",
    )
    + entry(
        "University of Stuttgart",
        "Germany",
        "1991 &ndash; 1993",
        "Alexander von Humboldt Fellowship",
        "",
    ),
) + section(
    "expertise",
    "Areas of Expertise",
    """    <ul class="skill-tags">
      <li>Infinite Dimensional Dynamical Systems and Applications</li>
      <li>Mathematical Biology and Mathematical Medicine</li>
      <li>Nonlinear Equations of Mathematical Physics</li>
      <li>Higher order models in Physics, Mechanics and Biology</li>
      <li>Chaotic Dynamics, Topological and Kolmogorov&rsquo;s Entropy</li>
      <li>Homogenisation of Attractors and Related Questions</li>
      <li>Topological Methods and its Applications</li>
    </ul>""",
) + section(
    "publications",
    "Publications",
    """    <h4>Books &amp; Monographs (Author of 8 books)</h4>
    <ol class="pub-list">
      <li>Analysis and Simulation of Multifield Problems (with W.L. Wendland). Springer-Verlag, 2003, 381 pages.</li>
      <li>Fredholm Structures, Topological Invariants and Applications. American Institute of Mathematical Sciences, Book series, vol. 3, 2009, 205 pages.</li>
      <li>Finite and Infinite Dimensional Attractors for Evolution Equations of Mathematical Physics. Gakkotoscho International Series, Tokyo, vol. 3, 2010, 239 pages.</li>
      <li>Evolution Equations Arising in the Modelling of Life Sciences. ISNM Series, Birkh&auml;user/Springer, vol. 163, 2013, 217 pages.</li>
      <li>Attractors for Degenerate Parabolic type Equations. American Mathematical Society; Mathematical Surveys and Monographs, vol. 192, 267 pages.</li>
      <li>Mathematical Modelling of Mitochondrial Swelling. Springer Nature Switzerland AG, 2018, 223 pages.</li>
      <li>Symmetrization and Stabilization Properties of Solutions of Nonlinear Elliptic Equations. Fields Institute Monographs 36, Springer, 2018, 258 pages.</li>
      <li>Linear and Nonlinear Non Fredholm Operators: Theory and Applications. Springer-Verlag, 2023, 208 pages.</li>
    </ol>
    <p>Author and coauthor of 186 journal and conference papers.</p>""",
) + section(
    "awards",
    "Awards, Honors &amp; Distinctions",
    """    <ul>
      <li><strong>2023</strong> &mdash; Fields Institute Fellow</li>
      <li><strong>2019&ndash;2020</strong> &mdash; James D. Murray Distinguished Professor, University of Waterloo</li>
      <li><strong>2018</strong> &mdash; Dean&rsquo;s Distinguished Professor, University of Toronto / Fields Institute</li>
      <li><strong>2015</strong> &mdash; Fedor Lynen Fellowship for Experienced Researchers (Germany)</li>
      <li><strong>2009</strong> &mdash; Otto Monsted Fellowship (Denmark)</li>
      <li><strong>2006</strong> &mdash; Japan Society Promotion of the Sciences</li>
      <li><strong>1991</strong> &mdash; Alexander von Humboldt Fellowship (Germany)</li>
    </ul>""",
) + section(
    "editorial",
    "Editorial, Reviewing &amp; Examining Activities",
    """    <ul>
      <li><strong>Editor in Chief</strong> &mdash; International Journal of Biomathematics and Biostatistics</li>
      <li><strong>Editor</strong> &mdash; Mathematical Methods in the Applied Sciences</li>
      <li><strong>Editor</strong> &mdash; Glasgow Journal of Mathematics</li>
      <li><strong>Editor</strong> &mdash; Journal of Nonautonomous and Stochastic Dynamical Systems</li>
      <li><strong>Editor</strong> &mdash; Mathematische Nachrichten</li>
      <li><strong>Editor</strong> &mdash; Zentralblatt f&uuml;r Mathematik</li>
      <li><strong>Editor</strong> &mdash; Advances of Mathematical Sciences and Applications</li>
      <li><strong>Editor</strong> &mdash; Discrete and Continous Dynamical Systems, DCDS-S</li>
      <li><strong>Editor</strong> &mdash; American Institute of Mathematical Sciences (AIMS): Book series &ldquo;Differential Equations and Dynamical Systems&rdquo;</li>
      <li><strong>Editor</strong> &mdash; International Journal of Mathematical Sciences</li>
      <li><strong>Editor</strong> &mdash; Azerbaijan Journal of Mathematics, Azerbaijan</li>
      <li><strong>Editor</strong> &mdash; Journal of Coupled Systems and Multi-Scale Dynamics</li>
    </ul>""",
) + section(
    "memberships",
    "Professional Memberships &amp; Affiliations",
    """    <h4>Scientific Boards, Councils and Committees</h4>
    <ul>
      <li>Coordinator, The Thematic Program &ldquo;On emerging Challenges in Mathematical Biology&rdquo;, Fields Institute 2018/2019.</li>
      <li>Chairman, The International Conference &ldquo;Applied Mathematics, Modelling and Life Science Problems&rdquo;, 2018, Istanbul, Turkey.</li>
      <li>Chairman, The German-Japan Conference &ldquo;Evolution Equations and Related Topics&rdquo;, 2012, Tokyo, Japan.</li>
      <li>Global Organizing and Scientific Committee, &ldquo;Int. Conference Colloque en l&rsquo;honneur de Henri Berestycki&rdquo;, 2011, Paris, France.</li>
      <li>Chairman, The German-Japan Conference &ldquo;Evolution Equations and Related Topics&rdquo;, 2009, Munich, Germany.</li>
      <li>Global Organizing Committee, &ldquo;Int. Conference Mathematical Methods in Biosciences&rdquo;, 2008, Munich, Germany.</li>
      <li>Global Organizing Committee, &ldquo;Int. Conference Dynamic Days&rdquo;, 2006, Poitiers, France.</li>
      <li>Organizing Committee, &ldquo;International Conference dedicated to O. A. Ladyzhenskaya&rdquo;, 2005.</li>
      <li>Scientific Committee, &ldquo;International Conference&rdquo;, NPDE 2003, Alusta, Ukraine.</li>
      <li>Scientific Committee, &ldquo;International Conference on Multifield Problems&rdquo;, 2002, Stuttgart, Germany.</li>
      <li>Scientific Committee and main Speaker, International Conference dedicated to the 80th birthday of M. I. Vishik, 2001, Berlin, Germany.</li>
      <li>Scientific Committee, &ldquo;ISAAC&rdquo; Congress, 2001, Berlin, Germany.</li>
      <li>Scientific Committee, &ldquo;International Conference dedicated to the 60th birthday of R. Temam&rdquo;, 2000, Paris and Poitier, France.</li>
      <li>Referee for Humboldt Fellowship (Germany); Referee for PhD thesis (Ecole Normal Superieure Cachan, Ecole Polytechnique; Universities: Paris, Marseille, Poitier, Bordeaux, France); Referee for DFG (Germany); Referee for VW-Foundation.</li>
      <li>Scientific and Local Organizer Committee, &ldquo;Equadiff&rdquo;-99, Berlin, Germany.</li>
      <li>Scientific Committee, &ldquo;Section 9 Dynamical systems and ODE&rdquo;, ICM 98, Berlin, Germany.</li>
    </ul>
    <h4>National Committees</h4>
    <ul>
      <li>Scientific Advisory Committee, &ldquo;Centre of Mathematical Medicine&rdquo;, Fields Institute, Toronto, Canada &mdash; at present.</li>
      <li>Member, Habilitation Thesis Committee, University of Paris-13, 2021.</li>
      <li>Member, PhD Thesis Committee, University of Waterloo, Canada, 2021.</li>
      <li>Programme Committee, German-Japan Conference &ldquo;Evolution Equations and Related Topics&rdquo;, Tokyo, 2012.</li>
      <li>Programme Committee, German-Japan Conference &ldquo;Evolution Equations and Related Topics&rdquo;, Munich, 2009.</li>
      <li>Programme Committee, &ldquo;Int. Conf. Mathematics in Biosciences&rdquo;, Munich, 2008.</li>
      <li>Programme Committee, &ldquo;Int. Conf. on Multifield Problems&rdquo;, Stuttgart, 2002.</li>
      <li>Programme Committee, &ldquo;ISAAC&rdquo; Congress, Berlin, 2001.</li>
      <li>Programme and Organizing Committee, Equadiff-99, Berlin, 1999.</li>
      <li>Programme Committee, World Congress 1998, Berlin, Section 9 and Dynamical Systems.</li>
    </ul>""",
) + section(
    "presentations",
    "Invited Talks &amp; Conference Presentations",
    """    <p><em>Invited Colloquia, Lectures and Seminars (2006&ndash;2023) &mdash; Not Complete List</em></p>
    <ul>
      <li>Main Speaker, Int. Conference in honour of Prof. Yihong Du (Sydney, Australia) &mdash; 2022</li>
      <li>James D. Murray Distinguished Professor, University of Waterloo, York University, University of Toronto and Fields Institute, WS (2019) &ndash; SS (2020).</li>
      <li>Main Speaker, Int. Conference on Chemotaxis, in honour of Prof. Takasi Senba, Japan, 2019.</li>
      <li>Dean&rsquo;s Distinguished Professor, University of Toronto, Fields Institute, (WS) Canada, 2018.</li>
      <li>Keynote Speaker, Int. Conference, Istanbul, Turkey, 2017.</li>
      <li>Stanford University, Princeton, NYU and Virginia Tech, USA, 2016.</li>
      <li>Hong Kong Polytechnic University, 2016.</li>
      <li>Courant Institute, 2013, 2014, 2015, 2016.</li>
      <li>Princeton, USA, 2014, 2015.</li>
      <li>Fields Institute, York University, Canada, 2015.</li>
      <li>German University of Technology, Oman, 2015.</li>
      <li>DTU, Copenhagen, 2009, 2010, 2011, 2012, 2013, 2014, 2015.</li>
      <li>Masterclass in the &ldquo;First Forum of World Young Scientists&rdquo;, Baku, Azerbaijan, 2014.</li>
      <li>Masterclass in the &ldquo;First Forum of European Young Scientists&rdquo;, Baku, Azerbaijan, 2013.</li>
      <li>Ecole Normale Superieure, Cachan, France, 2013.</li>
      <li>Courant Institute, NYU, Virginia Tech, USA, 2012.</li>
      <li>Universite Paris-13, France, 2012.</li>
      <li>Waseda University, Tokyo, Japan, 2012.</li>
      <li>Universite Paris-5, France, 2011.</li>
      <li>Waseda University, Tokyo, Japan, 2010.</li>
      <li>Courant Institute, NYU and Princeton, 2009.</li>
      <li>Universite Paris-Est, CERMICS, 2008, 2009.</li>
      <li>EHESS, Paris, France, 2008, 2009.</li>
      <li>Marseille University, France, 2007.</li>
      <li>Universities: Waseda, Osaka and Chiba, Japan, 2007.</li>
      <li>JSPS-Fellow, Osaka, Japan, 2006.</li>
      <li>Address to the Annual Meeting of Mathematical Society of Japan, Okayama, Japan, 2005.</li>
    </ul>""",
) + """
  <footer class="cv-footer">
    <span>Messoud A. Efendiyev &middot; Curriculum Vitae &middot; Marmara University &middot; TUM Munich</span>
  </footer>
"""

PAGE = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="Curriculum Vitae of Messoud A. Efendiyev" />
  <title>Curriculum Vitae &mdash; Messoud A. Efendiyev</title>
  <style>
{CSS}
  </style>
</head>
<body>
<article class="cv" aria-label="Curriculum Vitae">
{BODY}
</article>
</body>
</html>
"""

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(PAGE, encoding="utf-8", newline="\n")
print(f"Wrote {OUT} ({OUT.stat().st_size:,} bytes)")
