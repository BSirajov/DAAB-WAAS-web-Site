#!/usr/bin/env python3
"""Download thumbnails for URLs already in _cache_book_exhibition_gallery_urls.txt."""
from __future__ import annotations

from pathlib import Path

from _paths import ROOT

URL_CACHE = ROOT / "helpers" / "_cache_book_exhibition_gallery_urls.txt"
THUMB_DIR = ROOT / "helpers" / "_cache_book_exhibition_gallery_thumbs"


def main() -> None:
    from playwright.sync_api import sync_playwright

    urls = [ln.strip() for ln in URL_CACHE.read_text(encoding="utf-8").splitlines() if ln.strip()]
    THUMB_DIR.mkdir(parents=True, exist_ok=True)
    for old in THUMB_DIR.glob("*.jpg"):
        old.unlink()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(
            "https://sites.google.com/view/alimler-derneyi/"
            "bak%C4%B1-forumu-2024/foto-qalereya/kitab-s%C9%99rgisi",
            wait_until="networkidle",
            timeout=120_000,
        )
        ctx = page.context
        ok = 0
        for i, url in enumerate(urls, start=1):
            dest = THUMB_DIR / f"{i:02d}.jpg"
            resp = ctx.request.get(url, timeout=60_000)
            if resp.ok:
                dest.write_bytes(resp.body())
                ok += 1
                print(f"  {i}/{len(urls)} OK ({len(resp.body())} bytes)")
            else:
                print(f"  {i}/{len(urls)} HTTP {resp.status}")
        browser.close()
    print(f"Done: {ok}/{len(urls)}")


if __name__ == "__main__":
    main()
