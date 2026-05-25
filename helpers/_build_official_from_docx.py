"""Build az/forum/2024/official.html from forum_2024/Rəsmi_müraciətlər.docx (Yeniliklər UI)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

from docx import Document

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

DOCX = ROOT / "forum_2024" / "Rəsmi_müraciətlər.docx"
OUT = ROOT / "az" / "forum" / "2024" / "official.html"
ASSET = "../../../"
PRESIDENT_IMAGE = f"{ASSET}images/forum/Prezidentin_müraciəti.jpg"
SCIENTISTS_IMAGE_1 = f"{ASSET}images/forum/Aimlərimizin_müraciəti_Xankəndi_1.jpg"
SCIENTISTS_IMAGE_2 = f"{ASSET}images/forum/Aimlərimizin_müraciəti_Xankəndi_2.jpg"

from _embed_static_nav import forum_nav_strip  # noqa: E402

SECTION_META = [
    (
        "ilham-eliyev",
        "AZƏRBAYCAN RESPUBLİKASININ PREZİDENTİ CƏNAB İLHAM ƏLİYEVİN İŞTİRAKÇILARA MÜRACİƏTİ",
        "PREZİDENTİ CƏNAB İLHAM",
    ),
    (
        "eziz-sancar",
        "KİMYA ÜZRƏ NOBEL MÜKAFATI LAUREATI ƏZİZ SANCARIN İŞTİRAKÇILARA MÜRACİƏTİ",
        "ƏZİZ SANCARIN",
    ),
    (
        "arye-varshel",
        "KİMYA ÜZRƏ NOBEL MÜKAFATI LAUREATI ARYE VARŞELİN İŞTİRAKÇILARA MÜRACİƏTİ",
        "ARYE VARŞEL",
    ),
    (
        "alimlerimiz",
        "ALİMLƏRİMİZİN AZƏRBAYCAN RESPUBLİKASININ PREZİDENTİ CƏNAB İLHAM ƏLİYEVƏ MÜRACİƏTİ",
        "ALİMLƏRİMİZİN",
    ),
]

SIGNOFF_RE = re.compile(
    r"^(Hörmətlə,?\s*$|İlham ƏLİYEV|Əziz SANCAR|Arye VARŞEL|Bakı,|Xankəndi,|"
    r"\d{1,2}\s+sentyabr|Sarah Graham|Department of|University of|Member, National)",
    re.I,
)

SIDEBAR_SCRIPT = """
<script>
(function () {
  const links = Array.from(document.querySelectorAll('.timeline-list a[href^="#"]'));
  const ids = links.map(a => a.getAttribute('href').slice(1));
  const cards = ids.map(id => document.getElementById(id)).filter(Boolean);
  const eventsWidget = document.querySelector('.sidebar-widget');
  const eventsToggle = document.querySelector('.events-menu-toggle');
  const mobileQuery = window.matchMedia('(max-width: 1060px)');

  function activate(link) {
    links.forEach(a => a.classList.remove('tl-active'));
    if (link) link.classList.add('tl-active');
  }

  function closeEventsMenu() {
    if (!eventsWidget || !eventsToggle) return;
    eventsWidget.classList.remove('events-open');
    eventsToggle.setAttribute('aria-expanded', 'false');
  }

  function toggleEventsMenu() {
    if (!eventsWidget || !eventsToggle) return;
    const open = eventsWidget.classList.toggle('events-open');
    eventsToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
  }

  function jumpToTarget(event) {
    const link = event.currentTarget;
    const id = link.getAttribute('href').slice(1);
    const target = document.getElementById(id);
    if (!target) return;
    event.preventDefault();
    activate(link);
    const Pos = window.DAAB_LANG_POSITION;
    if (Pos && Pos.scrollToAnchor) {
      Pos.scrollToAnchor(id, false);
    } else {
      target.scrollIntoView({ block: 'start', behavior: 'auto' });
    }
    history.pushState(null, '', link.getAttribute('href'));
    if (mobileQuery.matches) closeEventsMenu();
  }

  function onScroll() {
    const mid = window.scrollY + window.innerHeight * 0.35;
    let active = null;
    for (let i = cards.length - 1; i >= 0; i--) {
      if (cards[i] && cards[i].offsetTop <= mid) {
        active = i;
        break;
      }
    }
    activate(active !== null ? links[ids.indexOf(cards[active].id)] : null);
  }

  links.forEach(link => link.addEventListener('click', jumpToTarget));
  if (eventsToggle) {
    eventsToggle.addEventListener('click', event => {
      event.stopPropagation();
      toggleEventsMenu();
    });
  }
  document.addEventListener('click', event => {
    if (!mobileQuery.matches || !eventsWidget || !eventsWidget.classList.contains('events-open')) return;
    if (eventsWidget.contains(event.target)) return;
    closeEventsMenu();
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') closeEventsMenu();
  });
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
})();
</script>"""


def esc(s: str) -> str:
    import html

    return html.escape(s, quote=True)


def parse_sections() -> list[dict]:
    doc = Document(str(DOCX))
    raw: list[dict] = []
    cur: dict | None = None
    for para in doc.paragraphs:
        text = para.text.replace("\r", "").strip()
        if not text:
            continue
        if para.style and str(para.style.name).startswith("Heading"):
            if cur:
                raw.append(cur)
            cur = {"heading": text, "paras": []}
        elif cur is not None:
            cur["paras"].append(text)
    if cur:
        raw.append(cur)

    sections: list[dict] = []
    for block, (sid, title, needle) in zip(raw, SECTION_META):
        if needle not in block["heading"].upper():
            raise SystemExit(f"unexpected heading: {block['heading']!r}")
        paras = block["paras"]
        subtitle = ""
        body = paras
        if paras and (
            paras[0].startswith("Müraciəti ")
            or paras[0].startswith("Xaricdə Yaşayan Azərbaycanlı Alimlərin Forumunun iştirakçıları")
        ):
            subtitle = paras[0]
            body = paras[1:]
        sections.append(
            {
                "id": sid,
                "title": title,
                "subtitle": subtitle,
                "body": body,
            }
        )
    return sections


def paras_to_html(paras: list[str]) -> str:
    parts: list[str] = []
    for text in paras:
        if text == "Tanrı Türkü qorusun!":
            parts.append(f'<p class="card-quote">{esc(text)}</p>')
        elif SIGNOFF_RE.match(text):
            parts.append(f'<p class="card-signoff">{esc(text)}</p>')
        else:
            parts.append(f'<p class="card-text">{esc(text)}</p>')
    return "\n".join(parts)


def news_card(section: dict) -> str:
    lead = (
        f'<p class="card-lead">{esc(section["subtitle"])}</p>'
        if section["subtitle"]
        else ""
    )
    image_block = ""
    if section["id"] == "ilham-eliyev":
        image_block = (
            '<div class="card-gallery single">'
            f'<img src="{PRESIDENT_IMAGE}" alt="Azərbaycan Respublikasının Prezidenti İlham Əliyev" '
            'width="900" height="520" loading="lazy" decoding="async"/>'
            "</div>"
        )
    elif section["id"] == "alimlerimiz":
        image_block = (
            '<div class="card-gallery double">'
            f'<img src="{SCIENTISTS_IMAGE_1}" alt="Alimlərimizin müraciəti — Xankəndi" '
            'loading="lazy" decoding="async"/>'
            f'<img src="{SCIENTISTS_IMAGE_2}" alt="Alimlərimizin müraciəti — Xankəndi" '
            'loading="lazy" decoding="async"/>'
            "</div>"
        )
    return f"""
<article class="news-card" id="{esc(section["id"])}">
<div class="card-header">
<h2 class="card-title">{esc(section["title"])}</h2>
</div>
<div class="card-body">
{image_block}
{lead}
{paras_to_html(section["body"])}
</div>
</article>"""


def build() -> None:
    sections = parse_sections()
    toc_items = "".join(
        f'<li><a href="#{esc(s["id"])}">{esc(s["title"])}</a></li>' for s in sections
    )
    cards = "\n".join(news_card(s) for s in sections)
    nav = forum_nav_strip("az", active_nav_id="forum-2024")

    html = f"""<!DOCTYPE html>
<html lang="az" data-daab-lang="az" data-daab-asset-root="{ASSET}" data-daab-page-id="forum-official" data-daab-nav-mount="1">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
<title>Rəsmi müraciətlər — DAAB</title>
<meta name="description" content="Forum 2024 — Prezident və Nobel laureatlarının müraciətləri, alimlərin müraciəti."/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Playfair+Display:wght@700;800&display=swap" rel="stylesheet"/>
<link href="{ASSET}css/daab-common.css?v=24" rel="stylesheet"/>
<link href="{ASSET}css/daab-mobile.css?v=5" rel="stylesheet"/>
<link href="{ASSET}css/daab-search.css?v=1" rel="stylesheet"/>
<link href="{ASSET}css/daab-back-to-top.css?v=1" rel="stylesheet"/>
<link href="{ASSET}css/daab-lang.css?v=10" rel="stylesheet"/>
<link href="{ASSET}css/daab-nav-mega.css?v=13" rel="stylesheet"/>
<link href="{ASSET}css/daab-hero-summary.css?v=1" rel="stylesheet"/>
<link href="{ASSET}css/daab-sidebar-widget.css?v=3" rel="stylesheet"/>
<link href="{ASSET}css/daab-activities-layout.css?v=7" rel="stylesheet"/>
<link href="{ASSET}css/daab-forum-content.css?v=12" rel="stylesheet"/>
<script src="{ASSET}js/daab-mobile.js?v=1" defer></script>
<script src="{ASSET}js/daab-back-to-top.js?v=2" defer></script>
<script src="{ASSET}js/daab-i18n.js?v=12" defer></script>
<script src="{ASSET}js/daab-lang-position.js?v=7" defer></script>
<script src="{ASSET}js/daab-nav.js?v=9" defer></script>
<script src="{ASSET}js/daab-primary-nav.js?v=9" defer></script>
<script src="{ASSET}js/daab-section-nav.js?v=5" defer></script>
<script src="{ASSET}js/daab-shell.js?v=11" defer></script>
<script src="{ASSET}js/daab-search.js?v=4" defer></script>
</head>
<body>
<a class="skip" href="#content">Məzmuna keç</a>
{nav}
<div class="breadcrumbs forum-breadcrumbs" role="navigation" aria-label="Səhifə yolu">
<a href="../../index.html">Ana səhifə</a><span aria-hidden="true">›</span><a href="../../activities.html">Fəaliyyətimiz</a><span aria-hidden="true">›</span><a href="index.html">Forum 2024</a><span aria-hidden="true">›</span><span class="forum-breadcrumbs-current" aria-current="page">Rəsmi müraciətlər</span>
</div>
<header class="page-hero">
<div class="hero-wrap shell">
<section class="hero-copy">
<h1>Rəsmi <span>müraciətlər</span></h1>
</section>
<aside aria-label="Rəsmi müraciətlər haqqında qısa məlumat" class="hero-panel">
<div class="panel-card">
<h2 class="panel-title">Rəsmi müraciətlər</h2>
<div class="panel-copy">Bu səhifədə Prezident İlham Əliyevin təbriki, Nobel laureatları Əziz Sancar və Arye Varşelin müraciətləri və alimlərimizin prezidentə müraciəti yerləşdirilmişdir.</div>
</div>
</aside>
</div>
</header>
<div class="content-wrap">
<aside class="sidebar">
<div class="sidebar-widget">
<div class="widget-head"><span>📋 Müraciətlər</span><button aria-controls="officialTOC" aria-expanded="false" aria-label="Müraciətlər menyusunu aç" class="events-menu-toggle" type="button"><span></span><span></span><span></span></button></div>
<div class="widget-body">
<ul class="timeline-list" id="officialTOC">
{toc_items}
</ul>
</div>
</div>
</aside>
<main class="news-feed main" id="content">
{cards}
</main>
</div>
<footer class="footer-pro">
<div class="footer-inner">
<div class="footer-brand"><h3>Dünya Azərbaycanlı Alimlər Birliyi</h3></div>
<div class="footer-grid">
<div class="footer-col"><h4 class="footer-title">Əlaqə</h4><div class="footer-item">✉ <a href="mailto:bilik.birlik@gmail.com">bilik.birlik@gmail.com</a></div><div class="footer-item">☎ <span>+90 555 147 46 74</span></div><div class="footer-item">🌐 <a href="https://daab-waas.com" rel="noopener noreferrer" target="_blank">daab-waas.com</a></div></div>
<div class="footer-col"><h4 class="footer-title">Ünvan</h4><p class="footer-address">Feneryolu Mahallesi<br/>Gazi Muhtar Paşa Sokak No:44<br/>Kadıköy, İstanbul, Türkiyə</p></div>
<div class="footer-col"><h4 class="footer-title">Rəhbərlik</h4><p class="footer-leader"><strong>Prof. Dr. Məsud Əfəndiyev</strong><br/>DAAB İdarə Heyətinin Sədri<br/>Germany — James D. Murray Distinguished Professor</p></div>
</div>
</div>
<div class="footer-bottom">© 2026 DAAB / WAAS — All Rights Reserved</div>
</footer>
{SIDEBAR_SCRIPT}
</body>
</html>
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8", newline="\n")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(sections)} sections)")


if __name__ == "__main__":
    build()
