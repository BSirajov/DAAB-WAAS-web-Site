#!/usr/bin/env python3
"""Fetch Alley of Honor gallery URLs and thumbnails via Playwright (Google blocks raw HTTP)."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

PAGE_URL = (
    "https://sites.google.com/view/alimler-derneyi/"
    "bak%C4%B1-forumu-2024/foto-qalereya/"
    "f%C9%99xri-xiyaban-%C5%9F%C9%99hidl%C9%99r-xiyaban%C4%B1"
)
URL_CACHE = ROOT / "helpers" / "_cache_alley_gallery_urls.txt"
THUMB_DIR = ROOT / "helpers" / "_cache_alley_gallery_thumbs"


def extract_urls(html: str) -> list[str]:
    """Gallery photos only — exclude site logo (w16383) and nav embeds."""
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
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise SystemExit("Install: pip install playwright && playwright install chromium")

    THUMB_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(PAGE_URL, wait_until="networkidle", timeout=120_000)
        page.wait_for_timeout(3000)
        html = page.content()
        urls = extract_urls(html)
        if not urls:
            # fallback: img src from DOM
            urls = page.eval_on_selector_all(
                "img[src*='googleusercontent.com/sitesv']",
                "els => els.map(e => e.src)",
            )
            urls = [re.sub(r"=w\d+", "=w1280", u) for u in urls if "sitesv/" in u]

        print(f"Found {len(urls)} gallery URLs")
        URL_CACHE.write_text("\n".join(urls) + "\n", encoding="utf-8")

        ctx = page.context
        ok = 0
        for i, url in enumerate(urls, start=1):
            dest = THUMB_DIR / f"{i:02d}.jpg"
            if dest.is_file() and dest.stat().st_size > 5000:
                ok += 1
                continue
            try:
                resp = ctx.request.get(url, timeout=60_000)
                if resp.ok:
                    dest.write_bytes(resp.body())
                    ok += 1
                    print(f"  {i}/{len(urls)} OK ({len(resp.body())} bytes)")
                else:
                    print(f"  {i}/{len(urls)} HTTP {resp.status}")
            except Exception as exc:
                print(f"  {i}/{len(urls)} FAIL {exc}")
        browser.close()

    print(f"Thumbnails: {ok}/{len(urls)} -> {THUMB_DIR}")
    print(f"URL cache: {URL_CACHE}")


if __name__ == "__main__":
    main()
