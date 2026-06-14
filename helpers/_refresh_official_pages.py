#!/usr/bin/env python3
"""Refresh Forum 2024 official addresses pages from DOCX (AZ) and forum_en_official (EN)."""
from __future__ import annotations

import html
import re
from pathlib import Path

from bs4 import BeautifulSoup

from _official_content import (
    META_AZ,
    PANEL_COPY_AZ,
    cards_html_az,
    cards_html_en,
    parse_sections_az,
    reorder_official_sections,
)
from _paths import ROOT
from _refresh_presentations_toc import toc_item as presentation_toc_item
from _speech_photos_lib import inject_speech_profiles, photo_src
from forum_en_official import META_EN, OFFICIAL_EN_SECTIONS, PANEL_COPY_EN

OFFICIAL_SPEAKER_TOC: dict[str, dict[str, tuple[str, str]]] = {
    "ilham-eliyev": {
        "az": ("Fərəh Əliyeva", "Prezident Administrasiyası, Humanitar siyasət şöbəsinin müdiri"),
        "en": ("Farah Aliyeva", "Administration of the President — department head"),
    },
    "eziz-sancar": {
        "az": ("Əziz Sancar", "Kimya üzrə Nobel mükafatı laureatı"),
        "en": ("Aziz Sancar", "Nobel laureate in Chemistry"),
    },
    "arye-varshel": {
        "az": ("Arye Varşel", "Kimya üzrə Nobel mükafatı laureatı"),
        "en": ("Arye Varshel", "Nobel laureate in Chemistry"),
    },
    "alimlerimiz": {
        "az": ("Alimlərimizin müraciəti", "Prezidentə ünvanlanmış müraciət"),
        "en": ("Scientists' address", "Address to the President"),
    },
    "fuad-muradov": {
        "az": ("Fuad Muradov", "Diaspora Komitəsi sədri"),
        "en": ("Fuad Muradov", "Chair of the State Committee on Diaspora Affairs"),
    },
    "mesud-efendiyev": {
        "az": ("Məsud Əfəndiyev", "DAAB İdarə Heyətinin sədri"),
        "en": ("Messoud Efendiyev", "Chair of the WAAS Executive Board"),
    },
}

OFFICIAL_PHOTOS_CSS = (
    '<link href="../../../css/daab-speech-photos.css?v=3" rel="stylesheet"/>\n'
    '<link href="../../../css/daab-presentations-toc.css?v=10" rel="stylesheet"/>\n'
)

PAGES = (
    (ROOT / "az" / "forum" / "2024" / "official.html", "az"),
    (ROOT / "en" / "forum" / "2024" / "official.html", "en"),
)


def esc(s: str) -> str:
    return html.escape(s, quote=True)


OFFICIAL_SPEAKER_ALT: dict[str, dict[str, str]] = {
    "ilham-eliyev": {"az": "Fərəh Əliyeva", "en": "Farah Aliyeva"},
    "eziz-sancar": {"az": "Əziz Sancar", "en": "Aziz Sancar"},
    "arye-varshel": {"az": "Arye Varşel", "en": "Arye Varshel"},
    "alimlerimiz": {
        "az": "Alimlərimizin Prezidentə müraciəti",
        "en": "Scientists' address to the President",
    },
    "fuad-muradov": {"az": "Fuad Muradov", "en": "Fuad Muradov"},
    "mesud-efendiyev": {"az": "Məsud Əfəndiyev", "en": "Messoud Efendiyev"},
}


def fix_speaker_photo_alts(soup: BeautifulSoup, lang: str) -> None:
    for aid, names in OFFICIAL_SPEAKER_ALT.items():
        alt = names.get(lang, "")
        if not alt:
            continue
        article = soup.select_one(f'main.news-feed article.news-card#{aid}')
        if not article:
            continue
        for img in article.select(".speech-card-photo"):
            img["alt"] = alt


def build_official_toc(soup: BeautifulSoup, lang: str) -> str:
    items: list[str] = []
    for article in soup.select("main.news-feed article.news-card"):
        aid = article.get("id", "")
        if not aid:
            continue
        title_el = article.select_one(".card-title")
        title = title_el.get_text(" ", strip=True) if title_el else aid
        photo = photo_src(aid)
        if photo and aid in OFFICIAL_SPEAKER_TOC:
            name, role = OFFICIAL_SPEAKER_TOC[aid][lang]
            items.append(presentation_toc_item(aid, name, role, photo))
        else:
            items.append(f'<li><a href="#{esc(aid)}">{esc(title)}</a></li>')
    return "\n".join(items)


def ensure_official_photo_css(soup: BeautifulSoup) -> None:
    head = soup.find("head")
    if not head:
        return
    for link in head.find_all("link", href=re.compile(r"daab-speech-photos\.css")):
        link["href"] = "../../../css/daab-speech-photos.css?v=3"
    if "daab-speech-photos.css" in str(head):
        return
    anchor = head.find("link", href=re.compile(r"daab-forum-content\.css"))
    if anchor:
        block = BeautifulSoup(OFFICIAL_PHOTOS_CSS, "html.parser")
        for link in block.find_all("link"):
            anchor.insert_after(link)
        anchor.insert_after("\n")
    else:
        head.append(BeautifulSoup(OFFICIAL_PHOTOS_CSS, "html.parser"))


def patch_page(path: Path, lang: str) -> None:
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")

    if lang == "az":
        sections = parse_sections_az()
        main_html = cards_html_az(sections)
        panel = PANEL_COPY_AZ
        meta = META_AZ
    else:
        sections = reorder_official_sections(OFFICIAL_EN_SECTIONS)
        main_html = cards_html_en(sections)
        panel = PANEL_COPY_EN
        meta = META_EN

    main = soup.select_one("main#content")
    if not main:
        raise SystemExit(f"No main#content in {path}")
    main.clear()
    main.append(BeautifulSoup(main_html, "html.parser"))

    profiles = inject_speech_profiles(soup)
    fix_speaker_photo_alts(soup, lang)
    toc = build_official_toc(soup, lang)
    ul = soup.select_one("#officialTOC")
    if not ul:
        raise SystemExit(f"No #officialTOC in {path}")
    ul.clear()
    ul.append(BeautifulSoup(toc, "html.parser"))
    ensure_official_photo_css(soup)

    panel_el = soup.select_one(".hero-panel .panel-copy")
    if panel_el:
        panel_el.clear()
        panel_el.append(panel)

    meta_el = soup.find("meta", attrs={"name": "description"})
    if meta_el:
        meta_el["content"] = meta

    path.write_text(str(soup), encoding="utf-8", newline="\n")
    print(
        f"  {path.relative_to(ROOT)} ({len(sections)} sections, {profiles} speaker photos)"
    )


def main() -> None:
    for path, lang in PAGES:
        patch_page(path, lang)


if __name__ == "__main__":
    main()
