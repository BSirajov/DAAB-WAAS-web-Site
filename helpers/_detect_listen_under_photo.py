#!/usr/bin/env python3
"""Detect profile cards where the Listen button sits under the portrait (layout bug)."""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

from _paths import ROOT

URL = "http://127.0.0.1:8010/az/scientists/profiles.html"


def ensure_server() -> None:
    import urllib.error
    import urllib.request

    try:
        urllib.request.urlopen(URL, timeout=2)
        return
    except Exception:
        pass
    subprocess.Popen(
        [sys.executable, "-m", "http.server", "8010", "--bind", "127.0.0.1"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    for _ in range(30):
        try:
            urllib.request.urlopen(URL, timeout=2)
            return
        except Exception:
            time.sleep(0.25)
    raise RuntimeError("Could not start local server on port 8010")


def main() -> None:
    ensure_server()
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 900})
        page.goto(URL, wait_until="networkidle")
        page.wait_for_selector(".card-tts-btn", timeout=15000)

        results = page.evaluate(
            """() => {
              const cards = [...document.querySelectorAll('#scientists-catalog .card')];
              return cards.map((card) => {
                const photo = card.querySelector('.card-avatar');
                const listen = card.querySelector('.card-tts');
                if (!photo || !listen) {
                  return {
                    id: card.id,
                    missing: !listen ? 'listen' : 'photo',
                  };
                }
                const pr = photo.getBoundingClientRect();
                const lr = listen.getBoundingClientRect();
                const besidePhoto = lr.left >= pr.right - 8;
                const underPhotoLeft =
                  lr.left <= pr.left + 12 &&
                  lr.top >= pr.bottom - 10;
                const inPhotoColumn =
                  lr.left <= pr.right - 20 &&
                  lr.top >= pr.top + pr.height * 0.45;
                return {
                  id: card.id,
                  photo: { l: pr.left, t: pr.top, r: pr.right, b: pr.bottom, w: pr.width, h: pr.height },
                  listen: { l: lr.left, t: lr.top, r: lr.right, b: lr.bottom },
                  besidePhoto,
                  underPhotoLeft,
                  inPhotoColumn,
                };
              });
            }"""
        )
        browser.close()

    missing = [r for r in results if r.get("missing")]
    under = [r for r in results if r.get("underPhotoLeft")]
    in_col = [r for r in results if r.get("inPhotoColumn") and not r.get("besidePhoto")]
    beside = [r for r in results if r.get("besidePhoto")]

    print(f"Cards total: {len(results)}")
    print(f"Listen beside photo (expected): {len(beside)}")
    if missing:
        print(f"Missing controls: {missing}")
    print(f"\nListen under photo (left edge, below portrait) [{len(under)}]:")
    for r in under:
        print(f"  - {r['id']}")
    print(f"\nListen in photo column (lower half, not beside) [{len(in_col)}]:")
    for r in in_col:
        print(f"  - {r['id']}")

    out = ROOT / "helpers" / "_listen_placement_report.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\nFull report: {out}")


if __name__ == "__main__":
    main()
