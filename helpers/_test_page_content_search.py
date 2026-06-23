#!/usr/bin/env python3
"""Smoke test for daab-page-content-search.js on activities and work-done pages."""
from __future__ import annotations

from playwright.sync_api import sync_playwright

TESTS = [
    ("http://127.0.0.1:8010/en/activities.html", "article.news-card", "Karabakh", 3, 27),
    ("http://127.0.0.1:8010/en/activities.html", "article.news-card", "zzznomatchxyz", 0, 27),
    ("http://127.0.0.1:8010/az/activities.html", "article.news-card", "Qarabağ", 3, 27),
    ("http://127.0.0.1:8010/en/work_done_2024_2026.html", "section.report-section", "Figure 1. Signing of the NDU", 1, 3),
    ("http://127.0.0.1:8010/en/work_done_2024_2026.html", "section.report-section", "zzznomatchxyz", 0, 3),
    ("http://127.0.0.1:8010/az/work_done_2024_2026.html", "section.report-section", "Şəkil 1.", 1, 3),
    ("http://127.0.0.1:8010/en/charter.html", "section.charter-card", "Executive Board", 2, 26),
    ("http://127.0.0.1:8010/en/charter.html", "section.charter-card", "zzznomatchxyz", 0, 26),
    ("http://127.0.0.1:8010/az/charter.html", "section.charter-card", "Ləğvetmə qaydaları", 1, 26),
]


def visible_count(page, selector: str) -> int:
    return page.locator(f"{selector}:not(.page-content-search__hidden)").count()


def main() -> None:
    failed = 0
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        for url, sel, query, expect_visible, expect_restored in TESTS:
            page.goto(url, wait_until="networkidle")
            page.fill("#pageContentSearch", query)
            page.wait_for_timeout(120)
            visible = visible_count(page, sel)
            empty_shown = page.locator("#pageContentSearchEmpty").is_visible()
            clear_shown = page.locator("#pageContentSearchClear").is_visible()
            ok = visible == expect_visible
            if expect_visible == 0:
                ok = ok and empty_shown
            else:
                ok = ok and clear_shown and not empty_shown
            label = "PASS" if ok else "FAIL"
            print(f"{label} {url} q={query!r} visible={visible} expect={expect_visible}")
            if not ok:
                failed += 1
            page.click("#pageContentSearchClear")
            page.wait_for_timeout(80)
            restored = visible_count(page, sel)
            if restored != expect_restored:
                print(f"  FAIL clear restore: got {restored}, expected {expect_restored}")
                failed += 1
            else:
                print(f"  clear restore OK ({restored} blocks)")
        page.set_viewport_size({"width": 390, "height": 844})
        page.goto("http://127.0.0.1:8010/en/activities.html", wait_until="networkidle")
        page.fill("#pageContentSearch", "forum")
        page.wait_for_timeout(120)
        mobile_visible = visible_count(page, "article.news-card")
        print(f"{'PASS' if mobile_visible > 0 else 'FAIL'} mobile viewport search visible={mobile_visible}")
        if mobile_visible <= 0:
            failed += 1
        browser.close()
    if failed:
        raise SystemExit(f"{failed} test(s) failed")
    print("All page content search tests passed.")


if __name__ == "__main__":
    main()
