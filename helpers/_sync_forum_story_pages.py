#!/usr/bin/env python3
"""Migrate forum presentations/impressions pages to Activities-style layout (like official.html)."""
from __future__ import annotations

import re
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString

from _paths import ROOT

FORUM = ROOT / "az" / "forum" / "2024"
EN_FORUM = ROOT / "en" / "forum" / "2024"
TEMPLATE_AZ = FORUM / "official.html"
TEMPLATE_EN = EN_FORUM / "official.html"
LEGACY_AZ = {
    "presentations.html": ROOT / "forum_2024" / "Məruzələr.html",
    "impressions.html": ROOT / "forum_2024" / "Təəssüratlar.html",
}

PAGES = {
    "presentations.html": {
        "page_id": "forum-2024-presentations",
        "az": {
            "title": "Məruzələr — DAAB",
            "description": "Xaricdə Yaşayan Azərbaycanlı Alimlərin I Forumuna təqdim olunmuş elmi və akademik məruzələr.",
            "breadcrumb": "Məruzələr",
            "hero_h1": "Foruma təqdim olunmuş <span>məruzələr</span>",
            "panel_title": "Elm, strategiya və gələcək baxışı",
            "panel_copy": (
                "Bu səhifədə forum iştirakçılarının bioinformatika, süni intellekt, təhsil, "
                "ekologiya, mədəniyyət, beynəlxalq əməkdaşlıq və digər sahələr üzrə məruzələri "
                "vahid strukturda təqdim olunur."
            ),
            "sidebar_label": "📊 Məruzələr",
            "sidebar_aria": "Məruzələr menyusunu aç",
            "toc_id": "presentationsTOC",
        },
        "en": {
            "title": "Presentations — WAAS",
            "description": "Scientific and academic presentations from the First Forum of Azerbaijani Scientists Living Abroad.",
            "breadcrumb": "Presentations",
            "hero_h1": "Forum <span>presentations</span>",
            "panel_title": "Science, strategy and outlook",
            "panel_copy": (
                "Presentations from forum participants in bioinformatics, artificial intelligence, "
                "education, ecology, culture, international cooperation and related fields."
            ),
            "sidebar_label": "📊 Presentations",
            "sidebar_aria": "Open presentations menu",
            "toc_id": "presentationsTOC",
        },
    },
    "impressions.html": {
        "page_id": "forum-impressions",
        "az": {
            "title": "Təəssüratlar — DAAB",
            "description": "Xaricdə Yaşayan Azərbaycanlı Alimlərin I Forumu ilə bağlı iştirakçı təəssüratları.",
            "breadcrumb": "Təəssüratlar",
            "hero_h1": "Forumla bağlı <span>təəssüratlar</span>",
            "panel_title": "Elm, vətən və həmrəylik",
            "panel_copy": (
                "Bu səhifə forum iştirakçılarının elmi əməkdaşlıq, diaspor həmrəyliyi və "
                "Qarabağ səfəri ilə bağlı təəssüratlarını vahid, oxunaqlı formatda təqdim edir."
            ),
            "sidebar_label": "💬 Təəssüratlar",
            "sidebar_aria": "Təəssüratlar menyusunu aç",
            "toc_id": "impressionsTOC",
        },
        "en": {
            "title": "Impressions — WAAS",
            "description": "Participant impressions from the First Forum of Azerbaijani Scientists Living Abroad.",
            "breadcrumb": "Impressions",
            "hero_h1": "Forum <span>impressions</span>",
            "panel_title": "Science, homeland and solidarity",
            "panel_copy": (
                "Personal reflections from forum participants on scientific cooperation, "
                "diaspora unity and the Karabakh visit."
            ),
            "sidebar_label": "💬 Impressions",
            "sidebar_aria": "Open impressions menu",
            "toc_id": "impressionsTOC",
        },
    },
}

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
</script>
"""


def normalize_body_html(html: str) -> str:
    html = html.replace('class="section-subhead"', 'class="program-subhead"')
    html = html.replace('class="table-wrap"', 'class="program-table-wrap"')
    html = re.sub(r"<table(?![^>]*class=)", '<table class="program-table"', html)
    html = re.sub(
        r"<p(?![^>]*class=)",
        '<p class="card-text"',
        html,
    )
    html = re.sub(
        r"<blockquote",
        '<p class="card-quote"',
        html,
        flags=re.I,
    )
    html = html.replace("</blockquote>", "</p>")
    return html


def convert_article(article) -> str:
    aid = article.get("id", "")
    content = article.select_one(".story-content") or article
    head = content.select_one(".story-head")
    title = ""
    subtitle = ""
    if head:
        h2 = head.find("h2")
        if h2:
            title = h2.decode_contents().strip()
        sub = head.find(class_="story-subtitle")
        if sub:
            subtitle = sub.get_text(" ", strip=True)

    body_el = content.select_one(".story-body")
    body_parts: list[str] = []
    if body_el:
        body_parts.append(normalize_body_html(body_el.decode_contents()))

    lead = f'<p class="card-lead">{subtitle}</p>' if subtitle else ""
    body_inner = lead + "".join(body_parts)

    return (
        f'<article class="news-card" id="{aid}">\n'
        f'<div class="card-header">\n'
        f'<h2 class="card-title">{title}</h2>\n'
        f"</div>\n"
        f'<div class="card-body">\n'
        f"{body_inner}\n"
        f"</div>\n"
        f"</article>\n"
    )


def extract_articles(raw: str) -> list[str]:
    soup = BeautifulSoup(raw, "html.parser")
    story_cards = soup.select("article.story-card")
    if story_cards:
        return [convert_article(a) for a in story_cards]
    news_cards = soup.select("main.news-feed article.news-card")
    if news_cards:
        return [str(a) for a in news_cards]
    return []


def build_toc(articles_html: list[str], page_id: str = "") -> str:
    if page_id == "forum-2024-presentations":
        from _refresh_presentations_toc import photo_src, toc_item

        items: list[str] = []
        for block in articles_html:
            m = re.search(r'id="([^"]+)"', block)
            t = re.search(r'class="card-title">(.*?)</h2>', block, re.S)
            lead = re.search(r'class="card-lead">(.*?)</p>', block, re.S)
            if not m or not t:
                continue
            aid = m.group(1)
            author = BeautifulSoup(t.group(1), "html.parser").get_text(" ", strip=True)
            pres_title = (
                BeautifulSoup(lead.group(1), "html.parser").get_text(" ", strip=True)
                if lead
                else author
            )
            items.append(toc_item(aid, author, pres_title, photo_src(aid)))
        return "\n".join(items)

    items: list[str] = []
    for block in articles_html:
        m = re.search(r'id="([^"]+)"', block)
        t = re.search(r'class="card-title">(.*?)</h2>', block, re.S)
        if not m or not t:
            continue
        aid = m.group(1)
        title = BeautifulSoup(t.group(1), "html.parser").get_text(" ", strip=True)
        items.append(f'<li><a href="#{aid}">{title}</a></li>')
    return "\n".join(items)


def build_page(template_path: Path, out_path: Path, meta: dict, page_id: str, articles: list[str]) -> None:
    tpl = template_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(tpl, "html.parser")

    html = soup.find("html")
    if html:
        html["data-daab-page-id"] = page_id
        if out_path.parts[-3] == "en":
            html["lang"] = "en"
            html["data-daab-lang"] = "en"

    if soup.title:
        soup.title.string = meta["title"]
    desc = soup.find("meta", attrs={"name": "description"})
    if desc:
        desc["content"] = meta["description"]

    bc_current = soup.select_one(".forum-breadcrumbs-current")
    if bc_current:
        bc_current.string = meta["breadcrumb"]

    hero_h1 = soup.select_one(".page-hero h1")
    if hero_h1:
        hero_h1.clear()
        hero_h1.append(BeautifulSoup(meta["hero_h1"], "html.parser"))

    panel_title = soup.select_one(".page-hero .panel-title")
    if panel_title:
        panel_title.string = meta["panel_title"]
    panel_copy = soup.select_one(".page-hero .panel-copy")
    if panel_copy:
        panel_copy.clear()
        panel_copy.append(NavigableString(meta["panel_copy"]))
    hero_panel = soup.select_one(".page-hero .hero-panel")
    if hero_panel:
        hero_panel["aria-label"] = meta["panel_title"]

    toc_items = build_toc(articles, page_id=page_id)
    widget_head_span = soup.select_one(".sidebar-widget .widget-head span")
    if widget_head_span:
        widget_head_span.string = meta["sidebar_label"]
    toggle = soup.select_one(".events-menu-toggle")
    if toggle:
        toggle["aria-controls"] = meta["toc_id"]
        toggle["aria-label"] = meta["sidebar_aria"]
    toc_ul = soup.select_one(".timeline-list")
    if toc_ul:
        toc_ul["id"] = meta["toc_id"]
        toc_ul.clear()
        if toc_items.strip():
            toc_ul.append(BeautifulSoup(toc_items, "html.parser"))

    main = soup.select_one("main.news-feed")
    if main:
        main.clear()
        for art in articles:
            main.append(BeautifulSoup(art, "html.parser"))

    out_html = str(soup)
    if "timeline-list a[href^=\"#\"]" not in out_html and "</body>" in out_html:
        out_html = out_html.replace("</body>", SIDEBAR_SCRIPT + "\n</body>", 1)

    out_path.write_text(out_html, encoding="utf-8", newline="\n")
    print(f"wrote {out_path.relative_to(ROOT)}")


def migrate_file(filename: str) -> None:
    cfg = PAGES[filename]
    for lang, folder, tpl in (
        ("az", FORUM, TEMPLATE_AZ),
        ("en", EN_FORUM, TEMPLATE_EN),
    ):
        dest = folder / filename
        src = LEGACY_AZ.get(filename) or dest
        if not src.is_file():
            print(f"skip missing {src}")
            continue
        raw = src.read_text(encoding="utf-8")
        articles = extract_articles(raw)
        if not articles:
            print(f"skip {dest.relative_to(ROOT)} — no articles in {src.relative_to(ROOT)}")
            continue
        build_page(tpl, dest, cfg[lang], cfg["page_id"], articles)


PAIR_RE = re.compile(
    r'(html\[data-daab-page-id="forum-official"\])([^,{]+),\s*\n'
    r'(html\[data-daab-page-id="forum-program"\])(\2)',
    re.MULTILINE,
)


def expand_forum_page_selectors(css: str) -> str:
    """Add forum-2024-presentations and forum-impressions to paired official/program rules."""
    if "forum-2024-presentations" in css:
        return css

    def repl(m: re.Match[str]) -> str:
        suffix = m.group(2)
        return (
            f'html[data-daab-page-id="forum-official"]{suffix},\n'
            f'html[data-daab-page-id="forum-2024-presentations"]{suffix},\n'
            f'html[data-daab-page-id="forum-program"]{suffix},\n'
            f'html[data-daab-page-id="forum-impressions"]{suffix}'
        )

    css = PAIR_RE.sub(repl, css)
    css = re.sub(
        r'(html\[data-daab-page-id="forum-official"\]),\s*\n'
        r'(html\[data-daab-page-id="forum-program"\])\{',
        r'\1,\nhtml[data-daab-page-id="forum-2024-presentations"],\n\2,\n'
        r'html[data-daab-page-id="forum-impressions"]{',
        css,
        count=1,
    )
    return css


def patch_forum_css() -> None:
    path = ROOT / "css" / "daab-forum-content.css"
    text = expand_forum_page_selectors(path.read_text(encoding="utf-8"))

    extra = """
html[data-daab-page-id="forum-impressions"] .card-body > .card-lead:first-child,
html[data-daab-page-id="forum-2024-presentations"] .card-body > .card-lead:first-child {
  font-weight: 700;
  color: var(--blue-700);
}
"""
    if ".card-body > .card-lead:first-child" not in text:
        text = text.rstrip() + "\n" + extra

    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"updated {path.relative_to(ROOT)}")


def patch_activities_layout_css() -> None:
    path = ROOT / "css" / "daab-activities-layout.css"
    text = expand_forum_page_selectors(path.read_text(encoding="utf-8"))
    path.write_text(text, encoding="utf-8", newline="\n")
    print(f"updated {path.relative_to(ROOT)}")


def patch_search_index() -> None:
    path = ROOT / "helpers" / "_build_search_index.py"
    text = path.read_text(encoding="utf-8")
    if "extract_forum_stories" in text and '"forum-2024-presentations": lambda' not in text:
        text = text.replace(
            '"forum-impressions": extract_forum_stories,',
            '"forum-impressions": lambda raw, lang: extract_forum_sections(raw, lang, "forum-impressions"),\n'
            '        "forum-2024-presentations": lambda raw, lang: extract_forum_sections(raw, lang, "forum-2024-presentations"),',
        )
        path.write_text(text, encoding="utf-8", newline="\n")
        print("updated _build_search_index.py")


def main() -> None:
    for name in PAGES:
        migrate_file(name)
    patch_forum_css()
    patch_activities_layout_css()
    patch_search_index()
    print("Done. Run: python helpers/_embed_static_nav.py && python helpers/_build_search_index.py && python helpers/_validate_site.py")


if __name__ == "__main__":
    main()
