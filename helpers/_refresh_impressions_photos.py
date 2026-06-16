#!/usr/bin/env python3
"""Inject author photos into Forum 2024 impressions sidebar TOC and main feed."""
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
    "lev-eppelbaum": "lev-v-eppelbaum",
    "seymur-nesirov": "seymur-nasirov",
    "afina-memmedli-barmanbay-elave-yekun-dusunceler": "afina-memmedli-barmanbay",
}

IMPRESSION_PAGES = (
    ROOT / "az" / "forum" / "2024" / "impressions.html",
    ROOT / "en" / "forum" / "2024" / "impressions.html",
)

IMPRESSIONS_CSS = (
    '<link href="../../../css/daab-impressions-photos.css?v=1" rel="stylesheet"/>\n'
)
IMPRESSIONS_CSS_RE = re.compile(
    r'<link href="\.\./\.\./\.\./css/daab-impressions-photos\.css\?v=\d+" rel="stylesheet"/>\n?'
)


def photo_src(slug: str) -> str:
    for base in (PHOTO_ALIASES.get(slug, slug), slug):
        for folder in PHOTO_DIRS:
            for ext in (".png", ".jpg", ".jpeg"):
                if (folder / f"{base}{ext}").is_file():
                    rel = folder.relative_to(ROOT).as_posix()
                    return f"{ASSET}{rel}/{base}{ext}"
    return ""


def toc_item(article_id: str, author: str, photo: str) -> str:
    if photo:
        img = (
            f'<span class="impression-toc-photo-frame">'
            f'<img class="impression-toc-photo" src="{photo}" alt="" width="44" height="44" '
            f'loading="lazy" decoding="async" aria-hidden="true"/>'
            f"</span>"
        )
    else:
        img = ""
    return (
        f'<li><a class="impression-toc-link" href="#{html.escape(article_id, quote=True)}">'
        f'<span class="impression-toc-author">{img}'
        f'<span class="impression-toc-name">{html.escape(author)}</span></span>'
        f"</a></li>"
    )


def inject_main_feed_photos(soup: BeautifulSoup) -> int:
    count = 0
    for article in soup.select("main.news-feed article.news-card"):
        aid = article.get("id", "")
        if not aid or not photo_src(aid):
            continue
        body = article.select_one(".card-body")
        if not body:
            continue
        if body.select_one(":scope > .impression-lead-row"):
            continue
        lead = body.select_one(":scope > .card-lead")

        title_el = article.select_one(".card-title")
        author = title_el.get_text(" ", strip=True) if title_el else aid
        photo = photo_src(aid)

        row = soup.new_tag("div", attrs={"class": "impression-lead-row"})
        if not lead:
            row["class"] = "impression-lead-row impression-lead-row--photo-only"
        frame = soup.new_tag("span", attrs={"class": "impression-card-photo-frame"})
        img = soup.new_tag(
            "img",
            attrs={
                "class": "impression-card-photo",
                "src": photo,
                "alt": author,
                "width": "72",
                "height": "72",
                "loading": "lazy",
                "decoding": "async",
            },
        )
        frame.append(img)
        row.append(frame)
        count += 1

        if lead:
            lead.extract()
            row.append(lead)
        body.insert(0, row)
    return count


def sync_photo_urls(soup: BeautifulSoup) -> int:
    updated = 0
    for article in soup.select("main.news-feed article.news-card"):
        aid = article.get("id", "")
        if not aid:
            continue
        src = photo_src(aid)
        if not src:
            continue
        for img in article.select(".impression-card-photo"):
            if img.get("src") != src:
                img["src"] = src
                updated += 1
        toc_img = soup.select_one(f'#impressionsTOC a[href="#{aid}"] .impression-toc-photo')
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
        author = title_el.get_text(" ", strip=True) if title_el else aid
        items.append(toc_item(aid, author, photo_src(aid)))
    return "\n".join(items)


def ensure_impressions_css(soup: BeautifulSoup) -> None:
    head = soup.find("head")
    if not head:
        return
    html_tag = str(head)
    if "daab-impressions-photos.css" in html_tag:
        return
    anchor = head.find(
        "link",
        href=re.compile(r"daab-forum-content\.css"),
    )
    if anchor:
        new_link = BeautifulSoup(IMPRESSIONS_CSS, "html.parser").link
        anchor.insert_after(new_link)
        anchor.insert_after("\n")
    else:
        head.append(BeautifulSoup(IMPRESSIONS_CSS, "html.parser"))


def refresh_page(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = IMPRESSIONS_CSS_RE.sub("", text)
    soup = BeautifulSoup(text, "html.parser")
    photos = inject_main_feed_photos(soup)
    synced = sync_photo_urls(soup)
    toc = build_toc(soup)
    ul = soup.select_one("#impressionsTOC")
    if not ul:
        raise SystemExit(f"No #impressionsTOC in {path}")
    ul.clear()
    ul.append(BeautifulSoup(toc, "html.parser"))
    ensure_impressions_css(soup)
    path.write_text(str(soup), encoding="utf-8", newline="\n")
    print(
        f"  {path.relative_to(ROOT)} "
        f"({len(ul.find_all('li'))} toc items, {photos} feed photos, {synced} urls synced)"
    )


def main() -> None:
    for path in IMPRESSION_PAGES:
        refresh_page(path)


if __name__ == "__main__":
    main()
