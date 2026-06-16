#!/usr/bin/env python3
"""Rebuild presentations TOC and inject author photos beside main-feed titles."""
from __future__ import annotations

import html
import re
from pathlib import Path

from bs4 import BeautifulSoup

from _paths import ROOT
from _speech_photos_lib import photo_src


def toc_item(article_id: str, author: str, title: str, photo: str) -> str:
    if photo:
        img = (
            f'<span class="presentation-toc-photo-frame">'
            f'<img class="presentation-toc-photo" src="{photo}" alt="" width="44" height="44" '
            f'loading="lazy" decoding="async" aria-hidden="true"/>'
            f"</span>"
        )
    else:
        img = (
            '<span class="presentation-toc-photo-frame presentation-toc-photo-frame--empty" '
            'aria-hidden="true"></span>'
        )
    return (
        f'<li><a class="presentation-toc-link" href="#{html.escape(article_id, quote=True)}">'
        f'<span class="presentation-toc-author">{img}'
        f'<span class="presentation-toc-name">{html.escape(author)}</span></span>'
        f'<span class="presentation-toc-title">{html.escape(title)}</span>'
        f"</a></li>"
    )


def inject_main_feed_photos(soup: BeautifulSoup) -> int:
    """Wrap each article's presentation title (card-lead) with author photo when available."""
    count = 0
    for article in soup.select("main.news-feed article.news-card"):
        aid = article.get("id", "")
        if not aid:
            continue
        body = article.select_one(".card-body")
        if not body:
            continue
        lead = body.select_one(":scope > .presentation-lead-row > .card-lead")
        if not lead:
            lead = body.select_one(":scope > .card-lead")
        if not lead:
            continue
        if lead.find_parent(class_="presentation-lead-row"):
            continue

        title_el = article.select_one(".card-title")
        author = title_el.get_text(" ", strip=True) if title_el else aid
        photo = photo_src(aid)

        row = soup.new_tag("div", attrs={"class": "presentation-lead-row"})
        if photo:
            frame = soup.new_tag("span", attrs={"class": "presentation-card-photo-frame"})
            img = soup.new_tag(
                "img",
                attrs={
                    "class": "presentation-card-photo",
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

        lead.extract()
        row.append(lead)
        body.insert(0, row)
    return count


def presentation_lead_el(article) -> object | None:
    """First presentation title in card body (direct or inside photo row)."""
    body = article.select_one(".card-body")
    if not body:
        return None
    return body.select_one(":scope > .presentation-lead-row > .card-lead") or body.select_one(
        ":scope > .card-lead"
    )


def sync_photo_urls(soup: BeautifulSoup) -> int:
    """Point existing sidebar + main-feed portrait imgs at the current photo_src."""
    updated = 0
    for article in soup.select("main.news-feed article.news-card"):
        aid = article.get("id", "")
        if not aid:
            continue
        src = photo_src(aid)
        if not src:
            continue
        for img in article.select(".presentation-card-photo"):
            if img.get("src") != src:
                img["src"] = src
                updated += 1
        toc_img = soup.select_one(f'#presentationsTOC a[href="#{aid}"] .presentation-toc-photo')
        if toc_img and toc_img.get("src") != src:
            toc_img["src"] = src
            updated += 1
    return updated


def build_toc_from_html(page_html: str) -> str:
    soup = BeautifulSoup(page_html, "html.parser")
    items: list[str] = []
    for article in soup.select("main.news-feed article.news-card"):
        aid = article.get("id", "")
        if not aid:
            continue
        title_el = article.select_one(".card-title")
        lead_el = presentation_lead_el(article)
        author = title_el.get_text(" ", strip=True) if title_el else aid
        pres_title = lead_el.get_text(" ", strip=True) if lead_el else author
        items.append(toc_item(aid, author, pres_title, photo_src(aid)))
    return "\n".join(items)


def refresh_page(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(text, "html.parser")
    photos = inject_main_feed_photos(soup)
    synced = sync_photo_urls(soup)
    toc = build_toc_from_html(str(soup))
    ul = soup.select_one("#presentationsTOC")
    if not ul:
        raise SystemExit(f"No #presentationsTOC in {path}")
    ul.clear()
    ul.append(BeautifulSoup(toc, "html.parser"))
    path.write_text(str(soup), encoding="utf-8", newline="\n")
    print(
        f"  {path.relative_to(ROOT)} "
        f"({len(ul.find_all('li'))} toc items, {photos} new feed photos, {synced} urls synced)"
    )


def main() -> None:
    for rel in ("az/forum/2024/presentations.html", "en/forum/2024/presentations.html"):
        refresh_page(ROOT / rel)


if __name__ == "__main__":
    main()
