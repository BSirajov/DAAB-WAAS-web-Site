#!/usr/bin/env python3
"""Download thumbnails using Playwright session + markdown URL order."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

PAGE_URL = (
    "https://sites.google.com/view/alimler-derneyi/"
    "bak%C4%B1-forumu-2024/foto-qalereya/"
    "m%C3%BCzakir%C9%99l%C9%99r"
)
MD = ROOT / "helpers" / "_cache_discussions_page.md"
URL_CACHE = ROOT / "helpers" / "_cache_discussions_gallery_urls.txt"
THUMB_DIR = ROOT / "helpers" / "_cache_discussions_gallery_thumbs"


def gallery_urls() -> list[str]:
    text = MD.read_text(encoding="utf-8")
    urls = re.findall(
        r"^!\[\]\((https://lh3\.googleusercontent\.com/sitesv/[^)]+)\)",
        text,
        re.MULTILINE,
    )
    return [re.sub(r"=w\d+", "=w1280", u) for u in urls if "=w16383" not in u]


def main() -> None:
    from playwright.sync_api import sync_playwright

    urls = gallery_urls()
    URL_CACHE.write_text("\n".join(urls) + "\n", encoding="utf-8")
    THUMB_DIR.mkdir(parents=True, exist_ok=True)
    for old in THUMB_DIR.glob("*.jpg"):
        old.unlink()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(PAGE_URL, wait_until="networkidle", timeout=120_000)
        page.wait_for_timeout(2000)
        ctx = page.context
        ok = 0
        for i, url in enumerate(urls, start=1):
            dest = THUMB_DIR / f"{i:03d}.jpg"
            resp = ctx.request.get(url, timeout=60_000)
            if resp.ok:
                dest.write_bytes(resp.body())
                ok += 1
                if i <= 3 or i % 40 == 0 or i == len(urls):
                    print(f"  {i}/{len(urls)} OK ({len(resp.body())} bytes)")
            else:
                print(f"  {i}/{len(urls)} HTTP {resp.status}")
        browser.close()

    print(f"Thumbnails: {ok}/{len(urls)}")


if __name__ == "__main__":
    main()
