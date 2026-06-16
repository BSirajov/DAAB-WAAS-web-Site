#!/usr/bin/env python3
"""Shared helpers: Forum 2024 speech pages — speaker photos in TOC and profile headers."""
from __future__ import annotations

import html
import re
from pathlib import Path

from bs4 import BeautifulSoup

from _paths import ROOT

ASSET = "../../../"
PHOTO_DIRS = (
    ROOT / "images" / "scientists-photos",
    ROOT / "images" / "board-members-photos",
)

PHOTO_ALIASES: dict[str, str] = {
    "isa-hebibbeyli": "isa-habibbayli",
    "rasim-eliquliyev": "rasim-aliquliyev",
    "mesud-efendiyev": "messoud-efendiyev",
    "togrul-kerimov": "togrul-karimov",
    "bextiyar-siracov": "bakhtiyar-sirajov",
    "nigar-mesumova": "nigar-masimova",
    "seadet-kerimi": "saadat-karimi",
    "seymur-nesirov": "seymur-nasirov",
    "yulduz-rehimov": "yulduz-rahimov",
    "mehdi-genceli": "mehdi-genceli-ismayilov",
    "edalet-muradov": "adalat-muradov",
    "elcin-babayev": "elchin-babayev",
    "gulcohre-memmedova": "gulchohra-mammadova",
    "natiq-eliyev": "natiq-aliyev",
    "rufet-ezizov": "rufat-azizov",
    "sahin-bayramov": "shahin-bayramov",
    "vazeh-eskerov": "vazeh-asgarov",
    "vilayet-veliyev": "vilayat-veliyev",
    "yaqub-piriyev": "yagub-piriyev",
    "hamlet-isakhanli": "hamlet-isaxanli",
    "gulchora-mammadova": "gulchohra-mammadova",
    "vilayat-valiyev": "vilayat-veliyev",
    "vazeh-askarov": "vazeh-asgarov",
    "rufat-azizov": "rufat-azizov",
    # Official addresses — article id → portrait file base
    "ilham-eliyev": "farah-aliyeva",
    "eziz-sancar": "aziz-sancar",
    "alimlerimiz": "address-to-president",
}

SPECIAL_PHOTO_FILES: dict[str, str] = {
    "rufet-ezizov": "rufat-azizov.png",
    "rufat-azizov": "rufat-azizov.png",
}

SPEECH_PHOTOS_CSS = (
    '<link href="../../../css/daab-speech-photos.css?v=2" rel="stylesheet"/>\n'
)
SPEECH_PHOTOS_CSS_RE = re.compile(
    r'<link href="\.\./\.\./\.\./css/daab-speech-photos\.css\?v=\d+" rel="stylesheet"/>\n?'
)


PHOTO_EXTS = (".png", ".jpg", ".jpeg")


def _resolve_photo_name(folder: Path, base: str) -> Path | None:
    for ext in PHOTO_EXTS:
        exact = folder / f"{base}{ext}"
        if exact.is_file():
            return exact
    matches: list[Path] = []
    for ext in PHOTO_EXTS:
        matches.extend(folder.glob(f"{base}*{ext}"))
    matches = sorted(matches, key=lambda p: (" 1" in p.stem, p.name))
    return matches[0] if matches else None


def _photo_path(slug: str) -> Path | None:
    if slug in SPECIAL_PHOTO_FILES:
        name = SPECIAL_PHOTO_FILES[slug]
        for folder in PHOTO_DIRS:
            path = folder / name
            if path.is_file():
                return path
            alt = _resolve_photo_name(folder, Path(name).stem)
            if alt:
                return alt

    bases: list[str] = []
    for candidate in (PHOTO_ALIASES.get(slug, slug), slug):
        if candidate not in bases:
            bases.append(candidate)

    for base in bases:
        for folder in PHOTO_DIRS:
            resolved = _resolve_photo_name(folder, base)
            if resolved:
                return resolved
    return None


def photo_src(slug: str) -> str:
    path = _photo_path(slug)
    if not path:
        return ""
    rel = path.relative_to(ROOT).as_posix()
    return f"{ASSET}{rel}"


def speech_title_from_article(article) -> str:
    """First in-body speech heading (e.g. ANAS leadership speech-body-lead)."""
    lead = article.select_one(".speech-body-lead strong")
    if lead:
        return lead.get_text(" ", strip=True)
    lead = article.select_one(".speech-body-lead")
    if lead:
        return lead.get_text(" ", strip=True)
    return ""


def toc_item(
    section_id: str,
    name: str,
    titles: str,
    photo: str,
    speech_title: str = "",
) -> str:
    if photo:
        img = (
            f'<span class="rector-toc-photo-frame">'
            f'<img class="rector-toc-photo" src="{photo}" alt="" width="44" height="44" '
            f'loading="lazy" decoding="async"/>'
            f"</span>"
        )
    else:
        img = ""
    titles_html = (
        f'<span class="rector-toc-titles">{html.escape(titles)}</span>'
        if titles
        else ""
    )
    speech_html = (
        f'<span class="rector-toc-speech-title">{html.escape(speech_title)}</span>'
        if speech_title
        else ""
    )
    return (
        f'<li><a class="rector-toc-link" href="#{html.escape(section_id, quote=True)}">'
        f"{img}"
        f'<span class="rector-toc-text">'
        f'<span class="rector-toc-name">{html.escape(name)}</span>'
        f"{titles_html}{speech_html}</span></a></li>"
    )


def inject_speech_profiles(soup: BeautifulSoup) -> int:
    count = 0
    for article in soup.select("main.news-feed article.news-card"):
        aid = article.get("id", "")
        if not aid:
            continue
        photo = photo_src(aid)
        if not photo:
            continue
        header = article.select_one(".card-header")
        if not header or header.select_one(".speech-profile-row"):
            continue

        title = header.select_one(".card-title")
        subtitle = header.select_one(".card-subtitle")
        speaker = title.get_text(" ", strip=True) if title else aid

        row = soup.new_tag("div", attrs={"class": "speech-profile-row"})
        frame = soup.new_tag("span", attrs={"class": "speech-card-photo-frame"})
        img = soup.new_tag(
            "img",
            attrs={
                "class": "speech-card-photo",
                "src": photo,
                "alt": speaker,
                "width": "80",
                "height": "80",
                "loading": "lazy",
                "decoding": "async",
            },
        )
        frame.append(img)
        row.append(frame)

        meta = soup.new_tag("div", attrs={"class": "speech-profile-meta"})
        if title:
            title.extract()
            meta.append(title)
        if subtitle:
            subtitle.extract()
            meta.append(subtitle)
        row.append(meta)

        header.clear()
        classes = header.get("class", [])
        if isinstance(classes, str):
            classes = classes.split()
        if "speech-card-header" not in classes:
            classes.append("speech-card-header")
        header["class"] = classes
        header.append(row)
        count += 1
    return count


def sync_photo_urls(soup: BeautifulSoup, toc_id: str) -> int:
    updated = 0
    for article in soup.select("main.news-feed article.news-card"):
        aid = article.get("id", "")
        if not aid:
            continue
        src = photo_src(aid)
        if not src:
            continue
        for img in article.select(".speech-card-photo"):
            if img.get("src") != src:
                img["src"] = src
                updated += 1
        toc_img = soup.select_one(f"#{toc_id} a[href='#{aid}'] .rector-toc-photo")
        if toc_img and toc_img.get("src") != src:
            toc_img["src"] = src
            updated += 1
    return updated


def build_toc(soup: BeautifulSoup) -> str:
    items: list[str] = []
    for article in soup.select("main.news-feed article.news-card"):
        aid = article.get("id", "")
        if not aid:
            continue
        title_el = article.select_one(".card-title")
        name = title_el.get_text(" ", strip=True) if title_el else aid
        sub_el = article.select_one(".card-subtitle")
        titles = sub_el.get_text(" ", strip=True) if sub_el else ""
        speech_title = speech_title_from_article(article)
        items.append(toc_item(aid, name, titles, photo_src(aid), speech_title))
    return "\n".join(items)


def ensure_speech_photos_css(soup: BeautifulSoup) -> None:
    head = soup.find("head")
    if not head:
        return
    if soup.find("link", href=re.compile(r"daab-speech-photos\.css")):
        return
    anchor = head.find("link", href=re.compile(r"daab-forum-content\.css"))
    if anchor:
        new_link = BeautifulSoup(SPEECH_PHOTOS_CSS, "html.parser").link
        anchor.insert_after(new_link)
        anchor.insert_after("\n")
    else:
        head.append(BeautifulSoup(SPEECH_PHOTOS_CSS, "html.parser"))


def refresh_page(path: Path, toc_id: str) -> None:
    text = path.read_text(encoding="utf-8")
    text = SPEECH_PHOTOS_CSS_RE.sub("", text)
    soup = BeautifulSoup(text, "html.parser")
    profiles = inject_speech_profiles(soup)
    synced = sync_photo_urls(soup, toc_id)
    toc = build_toc(soup)
    ul = soup.select_one(f"#{toc_id}")
    if not ul:
        raise SystemExit(f"No #{toc_id} in {path}")
    ul.clear()
    ul.append(BeautifulSoup(toc, "html.parser"))
    ensure_speech_photos_css(soup)
    path.write_text(str(soup), encoding="utf-8", newline="\n")
    missing = sum(
        1
        for article in soup.select("main.news-feed article.news-card")
        if article.get("id") and not photo_src(article["id"])
    )
    print(
        f"  {path.relative_to(ROOT)} "
        f"({len(ul.find_all('li'))} toc, {profiles} profiles, {synced} synced"
        f"{f', {missing} without photo' if missing else ''})"
    )
