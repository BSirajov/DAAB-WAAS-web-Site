#!/usr/bin/env python3
"""Smoke test for scientists catalogue multi-select filters."""
from __future__ import annotations

from playwright.sync_api import sync_playwright

URLS = [
    "http://127.0.0.1:8010/en/scientists/list.html",
    "http://127.0.0.1:8010/en/scientists/profiles.html",
]


def main() -> None:
    failed = 0
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        for url in URLS:
            page.goto(url, wait_until="networkidle")
            page.wait_for_timeout(400)
            toggle = page.locator(".catalog-toolbar__toggle")
            if toggle.count():
                if toggle.get_attribute("aria-expanded") != "true":
                    toggle.click()
                    page.wait_for_timeout(200)
            trigger = page.locator("#filterCountryMsTrigger")
            if not trigger.count():
                print(f"FAIL {url} — multiselect trigger missing")
                failed += 1
                continue
            trigger.click()
            page.wait_for_timeout(150)
            panel = page.locator("#filterCountryMsPanel.is-open")
            if not panel.count():
                print(f"FAIL {url} — panel did not open")
                failed += 1
                continue
            options = panel.locator(".ms-filter-option:not(.ms-filter-option--select-all) input[type=checkbox]")
            total = options.count()
            if total < 2:
                print(f"FAIL {url} — expected multiple country options, got {total}")
                failed += 1
                continue
            options.nth(0).click()
            options.nth(1).click()
            page.wait_for_timeout(120)
            label = trigger.locator(".ms-filter-trigger__label").inner_text()
            active = page.locator(".ms-filter-wrap.active").count() > 0
            rows = page.locator("tbody tr:not(.catalog-group-row)").count() if "list" in url else page.locator(".card:not(.is-filtered-out)").count()
            print(f"PASS {url} label={label!r} active={active} visible={rows}")
            page.keyboard.press("Escape")
            page.wait_for_timeout(80)
        browser.close()
    if failed:
        raise SystemExit(f"{failed} test(s) failed")
    print("Multi-select filter smoke tests passed.")


if __name__ == "__main__":
    main()
