#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import re
import shutil
from pathlib import Path

from playwright.sync_api import sync_playwright

from _paths import ROOT

PAGE = (
    "https://sites.google.com/view/alimler-derneyi/"
    "bak%C4%B1-forumu-2024/foto-qalereya/"
    "f%C9%99xri-xiyaban-%C5%9F%C9%99hidl%C9%99r-xiyaban%C4%B1"
)
THUMB = ROOT / "helpers" / "_cache_alley_gallery_thumbs" / "01.jpg"

spec = importlib.util.spec_from_file_location(
    "matcher", ROOT / "helpers" / "_match_alley_of_honor_gallery.py"
)
matcher = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(matcher)


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(PAGE, wait_until="networkidle", timeout=120_000)
        page.wait_for_timeout(2000)
        urls = page.eval_on_selector_all(
            "img[src*='googleusercontent.com/sitesv']",
            "els => els.map(e => e.src)",
        )
        gallery = [
            re.sub(r"=w\d+", "=w1280", u)
            for u in urls
            if "sitesv/" in u and "=w16383" not in u
        ]
        print(f"Gallery images in DOM: {len(gallery)}")
        url_cache = matcher.load_gallery_urls()
        u = url_cache[0]
        print(f"Using cached URL[0]: {u[:72]}…")
        resp = page.context.request.get(u, timeout=60_000)
        print(f"Download: HTTP {resp.status}, {len(resp.body()) if resp.ok else 0} bytes")
        if not resp.ok and gallery:
            u = gallery[0]
            print("Fallback to first DOM img")
            resp = page.context.request.get(u, timeout=60_000)
            print(f"Fallback: HTTP {resp.status}, {len(resp.body()) if resp.ok else 0} bytes")
        if resp.ok:
            THUMB.write_bytes(resp.body())
        browser.close()

    if not THUMB.is_file():
        print("No thumbnail saved")
        return

    manifest = json.loads(matcher.MANIFEST.read_text(encoding="utf-8"))
    used = {
        matcher.LOCAL_FOTOLAR / e["source"]
        for e in manifest
        if e.get("matched")
    }
    local_index = matcher.build_local_index()
    wh = matcher.hash_file(THUMB)
    best_path, dist = matcher.best_match(wh, local_index, used)
    print(f"Match: {best_path.name if best_path else None} dist={dist}")
    if best_path and dist <= 19:
        dest = matcher.OUT_DIR / f"alley-of-honor-01{best_path.suffix.lower()}"
        shutil.copy2(best_path, dest)
        print(f"Copied -> {dest.name}")
        for entry in manifest:
            if entry.get("index") == 1:
                entry.update(
                    {
                        "matched": True,
                        "distance": int(dist),
                        "source": best_path.name,
                        "dest": dest.name,
                        "source_bytes": best_path.stat().st_size,
                    }
                )
                entry.pop("skipped", None)
                entry.pop("reason", None)
                break
        matcher.MANIFEST.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
