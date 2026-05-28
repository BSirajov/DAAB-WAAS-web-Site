"""Scrape Google Sites video gallery page for images and links."""
from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen

from _paths import HELPERS, ROOT

URL = "https://sites.google.com/view/alimler-derneyi/bak%C4%B1-forumu-2024/video-qalereya"
OUT_HTML = HELPERS / "_tmp_video_gallery.html"
OUT_JSON = HELPERS / "_video_gallery_items.json"
DATA_JS = ROOT / "js" / "video-gallery-data.json"
AFTER_WINDOW = 8000


def fetch() -> str:
    req = Request(
        URL,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
        },
    )
    return urlopen(req, timeout=90).read().decode("utf-8", errors="replace")


def extract_urls(html: str) -> dict:
    patterns = {
        "googleusercontent": re.findall(
            r"https://[^\"'\s<>\\]+googleusercontent\.com[^\"'\s<>\\]+", html
        ),
        "youtube": re.findall(
            r"https?://(?:www\.)?(?:youtube\.com|youtu\.be)[^\"'\s<>\\]+", html
        ),
        "img_src": re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html, re.I),
        "href": re.findall(r'href=["\'](https?://[^"\']+)["\']', html, re.I),
    }
    for key in patterns:
        seen = []
        for u in patterns[key]:
            u = u.replace("\\u003d", "=").replace("\\u0026", "&")
            if u not in seen:
                seen.append(u)
        patterns[key] = seen
    return patterns


def extract_af_init(html: str) -> list:
    """Try to pull structured data from AF_initDataCallback blocks."""
    blocks = []
    for m in re.finditer(r"AF_initDataCallback\(\{[^}]*key:\s*'([^']+)'", html):
        blocks.append(m.group(1))
    return blocks


def normalize_img(url: str) -> str:
    """Strip size suffix for stable pairing."""
    url = url.split("?")[0]
    return re.sub(r"=w\d+(?:-h\d+)?$", "", url)


def strip_tags(fragment: str) -> str:
    text = re.sub(r"<[^>]+>", "", fragment)
    return re.sub(r"\s+", " ", text).strip()


def youtube_id(link: str) -> str:
    m = re.search(r"(?:youtu\.be/|v=)([A-Za-z0-9_-]{6,})", link)
    return m.group(1) if m else ""


def pair_items(html: str) -> list[dict]:
    """Pair thumbnails with YouTube link, outlet label, and description text below."""
    items: list[dict] = []
    parts = re.split(
        r'(<img src="https://lh3\.googleusercontent\.com/sitesv/[^"]+")',
        html,
    )
    seen_links: set[str] = set()
    for i in range(1, len(parts), 2):
        img_tag = parts[i]
        after = parts[i + 1][:AFTER_WINDOW] if i + 1 < len(parts) else ""
        img_m = re.search(r'src="(https://lh3[^"]+)"', img_tag)
        if not img_m:
            continue
        img = img_m.group(1).replace("&amp;", "&")
        links = re.findall(
            r'href="(https?://(?:www\.)?(?:youtube\.com|youtu\.be)[^"]+)"',
            after,
            re.I,
        )
        if not links:
            continue
        link = links[0].replace("&amp;", "&")
        if link in seen_links:
            continue
        seen_links.add(link)

        paragraphs: list[str] = []
        for block in re.findall(r"<p[^>]*>([\s\S]*?)</p>", after):
            plain = strip_tags(block)
            if plain and len(plain) > 1:
                paragraphs.append(plain)

        caption = paragraphs[0] if paragraphs else link
        description = ""
        if len(paragraphs) > 1:
            description = " ".join(paragraphs[1:])

        entry: dict = {"image": img, "link": link, "caption": caption}
        if description:
            entry["description"] = description
        items.append(entry)
    return items


def merge_into_site_data(scraped: list[dict]) -> list[dict]:
    """Keep local image paths; apply captions/descriptions from scrape by YouTube id."""
    by_yt = {youtube_id(it["link"]): it for it in scraped if youtube_id(it["link"])}
    if DATA_JS.is_file():
        current = json.loads(DATA_JS.read_text(encoding="utf-8"))
        merged: list[dict] = []
        for row in current:
            yt = youtube_id(row["link"])
            src = by_yt.get(yt, {})
            out = {
                "image": row["image"],
                "link": row["link"],
                "caption": src.get("caption", row.get("caption", "")),
            }
            desc = src.get("description", row.get("description", ""))
            if desc:
                out["description"] = desc
            merged.append(out)
        return merged
    return scraped


def main() -> None:
    html = fetch()
    OUT_HTML.write_text(html, encoding="utf-8")
    print(f"Saved {len(html)} bytes to {OUT_HTML}")

    scraped = pair_items(html)
    with_desc = sum(1 for it in scraped if it.get("description"))
    print(f"Paired items: {len(scraped)} ({with_desc} with description text)")

    OUT_JSON.write_text(
        json.dumps(scraped, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"Wrote {OUT_JSON}")

    items = merge_into_site_data(scraped)
    DATA_JS.write_text(json.dumps(items, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Merged text into {DATA_JS}")
    for it in items[:3]:
        print(f"  {it['caption']}")
        if it.get("description"):
            print(f"    → {it['description'][:80]}…")


if __name__ == "__main__":
    main()
