"""Build az/forum/2024/ pages from PDF extract + legacy forum_2024 HTML."""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

OUT_DIR = ROOT / "az" / "forum" / "2024"
LEGACY = ROOT / "forum_2024"
DATA = ROOT / "data" / "forum-2024-extract.json"
PDF_REL = "forum_2024/Forum_haqqinda_kitab_ (27.04.2026).pdf"
ASSET = "../../../"
AZ = "../.."

SHELL_SCRIPTS = """
<script src="{a}js/daab-mobile.js?v=1" defer></script>
<script src="{a}js/daab-back-to-top.js?v=2" defer></script>
<script src="{a}js/daab-i18n.js?v=12" defer></script>
<script src="{a}js/daab-lang-position.js?v=7" defer></script>
<script src="{a}js/daab-nav.js?v=8" defer></script>
<script src="{a}js/daab-primary-nav.js?v=9" defer></script>
<script src="{a}js/daab-breadcrumbs.js?v=6" defer></script>
<script src="{a}js/daab-section-nav.js?v=4" defer></script>
<script src="{a}js/daab-shell.js?v=11" defer></script>
<script src="{a}js/daab-search.js?v=4" defer></script>
"""

from _embed_static_nav import forum_nav_strip


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def body_to_html(body: str) -> str:
    parts: list[str] = []
    for block in re.split(r"\n\s*\n", body.strip()):
        block = block.strip()
        if not block:
            continue
        lines = [ln.strip() for ln in block.split("\n") if ln.strip()]
        if len(lines) == 1 and len(lines[0]) < 90 and lines[0].isupper():
            parts.append(f'<h3 class="section-subhead">{esc(lines[0])}</h3>')
            continue
        if re.match(r"^\d{1,2}\s+SENTYABR|^08:00|^09:00|^10:00", block, re.I):
            rows = []
            for ln in lines:
                m = re.match(r"^(\d{1,2}:\d{2}(?:\s*[–-]\s*\d{1,2}:\d{2})?)\s+(.+)$", ln)
                if m:
                    rows.append((m.group(1), m.group(2)))
                elif rows:
                    prev_t, prev_d = rows[-1]
                    rows[-1] = (prev_t, prev_d + " " + ln)
            if rows:
                trs = "".join(
                    f"<tr><td>{esc(t)}</td><td>{esc(d)}</td></tr>" for t, d in rows
                )
                parts.append(
                    '<div class="program-table-wrap"><table class="program-table">'
                    "<thead><tr><th>Vaxt</th><th>Tədbir</th></tr></thead>"
                    f"<tbody>{trs}</tbody></table></div>"
                )
                continue
        para = " ".join(lines)
        parts.append(f"<p>{esc(para)}</p>")
    return "\n".join(parts)


def article_card(n: int, sid: str, title: str, body_html: str, subtitle: str = "") -> str:
    sub = f'<p class="story-subtitle">{esc(subtitle)}</p>' if subtitle else ""
    return f"""
<article class="story-card" id="{esc(sid)}">
  <div class="story-number">{n:02d}</div>
  <div class="story-content">
    <header class="story-head">
      <h2>{esc(title)}</h2>
      {sub}
    </header>
    <div class="story-body">{body_html}</div>
  </div>
</article>"""


def page_shell(
    page_id: str,
    title: str,
    description: str,
    breadcrumb_label: str,
    hero_title: str,
    hero_lead: str,
    main_html: str,
    toc_html: str = "",
    hero_extra: str = "",
    hero_panel: str = "",
    *,
    active_nav_id: str | None = None,
) -> str:
    layout = "forum-layout" if toc_html else ""
    toc_block = (
        f'<aside class="forum-toc" aria-label="Mündəricat"><h2 class="forum-toc-title">Mündəricat</h2>'
        f'<nav class="forum-toc-list">{toc_html}</nav></aside>'
        if toc_html
        else ""
    )
    return f"""<!DOCTYPE html>
<html lang="az" data-daab-lang="az" data-daab-asset-root="{ASSET}" data-daab-page-id="{esc(page_id)}" data-daab-nav-mount="1">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
<title>{esc(title)} — DAAB</title>
<meta name="description" content="{esc(description)}"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Playfair+Display:wght@700;800&display=swap" rel="stylesheet"/>
<link href="{ASSET}css/daab-common.css?v=24" rel="stylesheet"/>
<link href="{ASSET}css/daab-mobile.css?v=5" rel="stylesheet"/>
<link href="{ASSET}css/daab-search.css?v=3" rel="stylesheet"/>
<link href="{ASSET}css/daab-back-to-top.css?v=1" rel="stylesheet"/>
<link href="{ASSET}css/daab-lang.css?v=10" rel="stylesheet"/>
<link href="{ASSET}css/daab-nav-mega.css?v=12" rel="stylesheet"/>
<link href="{ASSET}css/daab-forum-book.css?v=2" rel="stylesheet"/>
<link href="{ASSET}css/daab-hero-summary.css?v=1" rel="stylesheet"/>
{SHELL_SCRIPTS.format(a=ASSET)}
</head>
<body>
<a class="skip" href="#content">Məzmuna keç</a>
{forum_nav_strip("az", active_nav_id=active_nav_id or page_id)}
<main id="content">
<header class="forum-hero">
  <div class="forum-hero-wrap">
    <section>
      <h1>{hero_title}</h1>
      <p class="forum-hero-lead">{esc(hero_lead)}</p>
      {hero_extra}
    </section>
    {hero_panel}
  </div>
</header>
<div class="forum-main">
  <div class="{layout}">
    {toc_block}
    <div class="forum-flow">
      {main_html}
    </div>
  </div>
</div>
</main>
</body>
</html>
"""


def rewrite_legacy(text: str) -> str:
    repl = [
        ('data-daab-asset-root="../"', f'data-daab-asset-root="{ASSET}"'),
        ('href="../css/', f'href="{ASSET}css/'),
        ('href="../js/', f'href="{ASSET}js/'),
        ('src="../js/', f'src="{ASSET}js/'),
        ('src="../images/', f'src="{ASSET}images/'),
        ("url('../images/", f"url('{ASSET}images/"),
        ('href="index.html"', f'href="{AZ}/index.html"'),
        ('href="activities.html"', f'href="{AZ}/activities.html"'),
        ('href="foundation.html"', f'href="{AZ}/foundation.html"'),
        ('href="membership.html"', f'href="{AZ}/membership.html"'),
        ('href="scientists/list.html"', f'href="{AZ}/scientists/list.html"'),
        ('href="scientists/profiles.html"', f'href="{AZ}/scientists/profiles.html"'),
        ('data-daab-page-id="forum-reports"', 'data-daab-page-id="forum-presentations"'),
        ('data-daab-page-id="forum-impressions"', 'data-daab-page-id="forum-impressions"'),
        ("daab-breadcrumbs.js?v=4", "daab-breadcrumbs.js?v=5"),
        ("daab-lang-position.js?v=5", "daab-lang-position.js?v=7"),
        ("daab-common.css?v=21", "daab-common.css?v=24"),
        ("daab-mobile.css?v=4", "daab-mobile.css?v=5"),
        ("daab-nav-mega.css?v=11", "daab-nav-mega.css?v=12"),
    ]
    for old, new in repl:
        text = text.replace(old, new)
    # Inject forum book CSS if missing
    if "daab-forum-book.css" not in text:
        text = text.replace(
            '<link href="' + ASSET + 'css/daab-nav-mega.css?v=12" rel="stylesheet"/>',
            '<link href="' + ASSET + 'css/daab-nav-mega.css?v=12" rel="stylesheet"/>\n'
            '<link href="' + ASSET + 'css/daab-forum-book.css?v=1" rel="stylesheet"/>',
        )
    # Fix breadcrumbs to forum hub
    text = re.sub(
        r'<div class="breadcrumbs">.*?</div>',
        f'<div class="breadcrumbs"><a href="{AZ}/index.html">Ana səhifə</a><span>›</span>'
        f'<a href="{AZ}/activities.html">Fəaliyyətimiz</a><span>›</span>'
        f'<a href="index.html">Forum 2024</a><span>›</span><span id="forum-bc-tail"></span></div>',
        text,
        count=1,
        flags=re.DOTALL,
    )
    return text


def build_section_page(
    filename: str,
    page_id: str,
    title: str,
    description: str,
    hero_html: str,
    hero_lead: str,
    sections: list[dict],
) -> None:
    toc = "".join(
        f'<a class="forum-toc-link" href="#{esc(s["id"])}"><span>{esc(s["title"])}</span></a>'
        for s in sections
    )
    cards = []
    for i, s in enumerate(sections, 1):
        cards.append(
            article_card(i, s["id"], s["title"], body_to_html(s["body"]))
        )
    intro = (
        f'<section class="forum-intro"><p class="forum-source-note">Mənbə: kitab səh. '
        f'<strong>24–115</strong> və <strong>176–203</strong> '
        f'(<a href="{ASSET}{PDF_REL}">PDF</a>).</p></section>'
    )
    html_out = page_shell(
        page_id,
        title,
        description,
        title,
        hero_html,
        hero_lead,
        intro + "\n" + "\n".join(cards),
        toc,
        hero_extra=(
            f'<div class="forum-hero-actions">'
            f'<a class="btn btn-secondary" href="index.html">Forum 2024</a></div>'
        ),
    )
    (OUT_DIR / filename).write_text(html_out, encoding="utf-8", newline="\n")


def build_index() -> None:
    cards = [
        ("official.html", "Rəsmi müraciətlər", "Prezident, Nobel laureatları və alimlərin müraciəti (kitab səh. 24–28)."),
        ("program.html", "Forumun proqramı", "9–11 sentyabr 2024 tədbir cədvəli (kitab səh. 31–35)."),
        ("speeches.html", "Nitqlər və müzakirələr", "Dövlət, universitet və diaspora çıxışları (kitab səh. 36–69)."),
        ("presentations.html", "Məruzələr", "Foruma təqdim olunmuş elmi məruzələr (kitab səh. 70–114)."),
        ("impressions.html", "Təəssüratlar", "İştirakçıların şəxsi təəssüratları (kitab səh. 176–203)."),
        (f"{AZ}/scientists/profiles.html", "Alimlər kataloqu", "Tam akademik profillər (sayt kataloqu)."),
    ]
    grid = "".join(
        f'<a class="forum-hub-link" href="{href}"><h3>{esc(t)}</h3><p>{esc(d)}</p></a>'
        for href, t, d in cards
    )
    pdf_btn = (
        f'<a class="btn btn-primary" href="{ASSET}{PDF_REL}" download>'
        "Kitabı PDF yüklə</a>"
    )
    hero_panel = """
<aside class="hero-panel" aria-label="Forum haqqında qısa məlumat">
  <div class="panel-card">
    <h2 class="panel-title">I Forum — kitab arxivi</h2>
    <div class="panel-copy">9–11 sentyabr 2024, Bakı – Xankəndi – Şuşa. Rəsmi çıxışlar, proqram, nitqlər, məruzələr (səh. 24–115) və iştirakçı təəssüratları (səh. 176–203) bu bölmədə strukturlaşdırılıb.</div>
  </div>
</aside>"""
    main = f"""
<section class="forum-hub-card">
  <h2>Xaricdə Yaşayan Azərbaycanlı Alimlərin I Forumu</h2>
  <p>9–11 sentyabr 2024, Bakı – Xankəndi – Şuşa. Bu bölmədə forum kitabından seçilmiş məzmun — 
  <strong>səhifə 24–115</strong> (rəsmi çıxışlar, proqram, nitqlər, məruzələr) və 
  <strong>səhifə 176–203</strong> (iştirakçı təəssüratları) — DAAB saytında strukturlaşdırılıb.</p>
  <div class="forum-hub-grid">{grid}</div>
</section>"""
    html_out = page_shell(
        "forum-2024",
        "Forum 2024",
        "Xaricdə Yaşayan Azərbaycanlı Alimlərin I Forumu — kitab məzmunu və arxiv.",
        "Forum 2024",
        'Forum <span>2024</span>',
        "Kitabdan seçilmiş rəsmi mətnlər, proqram, məruzələr və iştirakçı təəssüratları.",
        main,
        hero_extra=f'<div class="forum-hero-actions">{pdf_btn}</div>',
        hero_panel=hero_panel,
    )
    hub = OUT_DIR / "index.html"
    if hub.is_file():
        print(f"skip hub (hand-maintained home UX): {hub.relative_to(ROOT)}")
    else:
        (OUT_DIR / "index.html").write_text(html_out, encoding="utf-8", newline="\n")


def main() -> None:
    import _extract_forum_book_pages as extract  # noqa: PLC0415

    extract.main()
    data = json.loads(DATA.read_text(encoding="utf-8"))
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    by_id = {s["id"]: s for s in data["main"]}

    def pick(*ids: str) -> list[dict]:
        return [by_id[i] for i in ids if i in by_id]

    def official_sections() -> list[dict]:
        sections = []
        if "president" in by_id:
            sections.append(by_id["president"])
        combined = by_id.get("nobel-sancar", {}).get("body", "")
        if combined:
            m_var = re.search(r"ARYE\s*VARŞELİN İŞTİRAKÇILARA MÜRACİƏTİ", combined, re.I)
            m_app = re.search(
                r"ALİMLƏRİMİZİN AZƏRBAYCAN\s+RESPUBLİKASININ PREZİDENTİ",
                combined,
                re.I,
            )
            if m_var:
                sections.append(
                    {
                        "id": "nobel-sancar",
                        "title": "Əziz Sancarın müraciəti",
                        "body": combined[: m_var.start()].strip(),
                    }
                )
                tail = combined[m_var.start() :]
                if m_app:
                    sections.append(
                        {
                            "id": "nobel-varshel",
                            "title": "Arye Varşelin müraciəti",
                            "body": tail[: m_app.start()].strip(),
                        }
                    )
                    sections.append(
                        {
                            "id": "scientists-appeal",
                            "title": "Alimlərimizin müraciəti",
                            "body": tail[m_app.start() :].strip(),
                        }
                    )
                else:
                    sections.append(
                        {
                            "id": "nobel-varshel",
                            "title": "Arye Varşelin müraciəti",
                            "body": tail.strip(),
                        }
                    )
            else:
                sections.append(by_id["nobel-sancar"])
        return sections

    build_index()

    build_section_page(
        "official.html",
        "forum-official",
        "Rəsmi müraciətlər",
        "Forum 2024 — Prezident və Nobel laureatlarının müraciətləri, alimlərin müraciəti.",
        'Rəsmi <span>müraciətlər</span>',
        "Azərbaycan Respublikasının Prezidenti və beynəlxalq alimlərin forum iştirakçılarına müraciətləri.",
        official_sections(),
    )

    prog = pick("program")
    if prog:
        build_section_page(
            "program.html",
            "forum-program",
            "Forumun proqramı",
            "Xaricdə Yaşayan Azərbaycanlı Alimlərin Forumu — 9–11 sentyabr 2024 proqramı.",
            'Forum <span>proqramı</span>',
            "Bakı, Xankəndi və Şuşa üzrə üç günlük tədbir planı.",
            prog,
        )

    build_section_page(
        "speeches.html",
        "forum-speeches",
        "Nitqlər",
        "Forum 2024 plenar nitqləri və universitet çıxışları.",
        'Nitqlər və <span>müzakirələr</span>',
        "Dövlət, DAAB və universitet rəhbərlərinin çıxışları; diaspora və elm strategiyası.",
        pick(
            "muradov",
            "efendiyev",
            "rectors",
            "diaspora-science",
            "roadmap",
        ),
    )

    # Polished legacy pages for presentations & impressions
    for src_name, dst, page_id in (
        ("Foruma təqdim olunmuş məruzələr.html", "presentations.html", "forum-presentations"),
        ("Forumla bağlı təəssüratlar.html", "impressions.html", "forum-impressions"),
    ):
        src = LEGACY / src_name
        if src.exists():
            text = rewrite_legacy(src.read_text(encoding="utf-8"))
            if "data-daab-nav-placeholder" not in text:
                text = text.replace(
                    '<body>',
                    '<body>\n<div data-daab-nav-placeholder="1"></div>',
                    1,
                )
            text = text.replace(
                f'data-daab-page-id="{page_id}"',
                f'data-daab-page-id="{page_id}"',
            )
            (OUT_DIR / dst).write_text(text, encoding="utf-8", newline="\n")
            print(f"copied {dst}")

    print(f"built {OUT_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
