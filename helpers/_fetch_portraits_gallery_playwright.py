#!/usr/bin/env python3
"""Fetch Portretlər gallery URLs and thumbnails via Playwright."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

PAGE_URL = (
    "https://sites.google.com/view/alimler-derneyi/"
    "bak%C4%B1-forumu-2024/foto-qalereya/"
    "portretl%C9%99r"
)
URL_CACHE = ROOT / "helpers" / "_cache_portraits_gallery_urls.txt"
THUMB_DIR = ROOT / "helpers" / "_cache_portraits_gallery_thumbs"


def extract_urls(html: str) -> list[str]:
    found = re.findall(
        r"!\[\]\((https://lh3\.googleusercontent\.com/sitesv/[^)]+)\)",
        html,
    )
    if not found:
        found = re.findall(
            r"https://lh3\.googleusercontent\.com/sitesv/[^\"')\s]+",
            html,
        )
    gallery = [u for u in found if "=w16383" not in u and "sitesv/" in u]
    gallery = [re.sub(r"=w\d+", "=w1280", u) for u in gallery]
    seen: set[str] = set()
    out: list[str] = []
    for u in gallery:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def main() -> None:
    from playwright.sync_api import sync_playwright

    THUMB_DIR.mkdir(parents=True, exist_ok=True)
    for old in THUMB_DIR.glob("*.jpg"):
        old.unlink()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(PAGE_URL, wait_until="networkidle", timeout=120_000)
        page.wait_for_timeout(3000)
        urls = extract_urls(page.content())
        if not urls:
            urls = page.eval_on_selector_all(
                "img[src*='googleusercontent.com/sitesv']",
                "els => els.map(e => e.src).filter(u => !u.includes('w16383'))",
            )
            urls = [re.sub(r"=w\d+", "=w1280", u) for u in urls if "sitesv/" in u]

        print(f"Found {len(urls)} gallery URLs (logo excluded)")
        URL_CACHE.write_text("\n".join(urls) + "\n", encoding="utf-8")

        ctx = page.context
        ok = 0
        for i, url in enumerate(urls, start=1):
            dest = THUMB_DIR / f"{i:03d}.jpg"
            resp = ctx.request.get(url, timeout=60_000)
            if resp.ok:
                dest.write_bytes(resp.body())
                ok += 1
                if i <= 3 or i % 20 == 0 or i == len(urls):
                    print(f"  {i}/{len(urls)} OK ({len(resp.body())} bytes)")
            else:
                print(f"  {i}/{len(urls)} HTTP {resp.status}")
        browser.close()

    print(f"Thumbnails: {ok}/{len(urls)} -> {THUMB_DIR}")


if __name__ == "__main__":
    main()
