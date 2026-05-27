#!/usr/bin/env python3
"""Retry Alley of Honor gallery items that failed first pass (borderline dHash distance)."""
from __future__ import annotations

import importlib.util
import json
import shutil
from pathlib import Path

from _paths import ROOT

spec = importlib.util.spec_from_file_location(
    "matcher",
    ROOT / "helpers" / "_match_alley_of_honor_gallery.py",
)
matcher = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(matcher)

RETRY_MAX_DIST = 19
INDICES = [1, 11, 22, 37, 47, 67]


def refetch_thumb_1() -> None:
    url = matcher.load_gallery_urls()[0]
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return
    dest = matcher.THUMB_DIR / "01.jpg"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context()
        resp = ctx.request.get(url, timeout=60_000)
        if resp.ok:
            dest.write_bytes(resp.body())
            print(f"Refetched thumb 1: {len(resp.body())} bytes")
        else:
            print(f"Thumb 1 HTTP {resp.status}")
        browser.close()


def main() -> None:
    manifest = json.loads(matcher.MANIFEST.read_text(encoding="utf-8"))
    used = {
        matcher.LOCAL_FOTOLAR / e["source"]
        for e in manifest
        if e.get("matched")
    }
    urls = matcher.load_gallery_urls()
    local_index = matcher.build_local_index()

    refetch_thumb_1()

    for i in INDICES:
        thumb = matcher.THUMB_DIR / f"{i:02d}.jpg"
        if not thumb.is_file() or thumb.stat().st_size < 1000:
            print(f"{i}: still no thumbnail")
            continue
        wh = matcher.hash_file(thumb)
        best_path, dist = matcher.best_match(wh, local_index, used)
        name = best_path.name if best_path else "?"
        print(f"{i}: best={name} dist={dist}")
        if best_path is None or dist > RETRY_MAX_DIST:
            continue
        used.add(best_path)
        dest = matcher.OUT_DIR / f"alley-of-honor-{i:02d}{best_path.suffix.lower()}"
        shutil.copy2(best_path, dest)
        print(f"  -> copied {dest.name}")
        for entry in manifest:
            if entry.get("index") == i:
                entry.update(
                    {
                        "matched": True,
                        "distance": int(dist),
                        "source": best_path.name,
                        "dest": dest.name,
                        "source_bytes": best_path.stat().st_size,
                        "retry": True,
                    }
                )
                entry.pop("skipped", None)
                entry.pop("reason", None)
                break
        else:
            manifest.append(
                {
                    "index": i,
                    "url": urls[i - 1],
                    "matched": True,
                    "distance": int(dist),
                    "source": best_path.name,
                    "dest": dest.name,
                    "source_bytes": best_path.stat().st_size,
                    "retry": True,
                }
            )

    matcher.MANIFEST.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    matched = sum(1 for e in manifest if e.get("matched"))
    print(f"Manifest: {matched}/{len(urls)} matched")


if __name__ == "__main__":
    main()
