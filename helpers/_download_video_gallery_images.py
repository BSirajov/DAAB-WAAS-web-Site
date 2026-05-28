"""Download video gallery thumbnails via Playwright network capture (Google CDN blocks direct fetch)."""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

from _paths import HELPERS, ROOT

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    raise SystemExit("Install: pip install playwright && playwright install chromium")

DATA_JS = ROOT / "js" / "video-gallery-data.json"
DATA_SCRAPE = HELPERS / "_video_gallery_items.json"
IMG_DIR = ROOT / "images" / "videos-gallery"
WEB_PREFIX = "images/videos-gallery/"

SITES_PAGE = (
    "https://sites.google.com/view/alimler-derneyi/bak%C4%B1-forumu-2024/video-qalereya"
)

EXTRACT_PAIRS_JS = """
() => {
  const out = [];
  for (const img of document.querySelectorAll('img[src*="googleusercontent.com/sitesv"]')) {
    let block = img.closest('.oKdM2c');
    if (!block) continue;
    let sib = block.nextElementSibling;
    for (let n = 0; n < 6 && sib; n++, sib = sib.nextElementSibling) {
      const a = sib.querySelector('a[href*="youtube.com"], a[href*="youtu.be"]');
      if (a) {
        out.push({ key: img.src.match(/\\/sitesv\\/(AA5AbU[^=]+)/)?.[1] || img.src, link: a.href });
        break;
      }
    }
  }
  return out;
}
"""


def youtube_id(link: str) -> str:
    m = re.search(r"(?:youtu\.be/|v=)([A-Za-z0-9_-]{6,})", link)
    return m.group(1) if m else ""


def local_name(index: int, link: str) -> str:
    vid = youtube_id(link)
    suffix = f"-{vid}" if vid else ""
    return f"video-{index:03d}{suffix}.jpg"


def sitesv_key(url: str) -> str:
    m = re.search(r"/sitesv/(AA5AbU[^=/?]+)", url)
    return m.group(1) if m else url


def is_image_bytes(data: bytes) -> bool:
    return len(data) > 1000 and data[:2] == b"\xff\xd8"


def load_items() -> list[dict]:
    """Prefer scrape file when it still has remote Google URLs."""
    if DATA_SCRAPE.is_file():
        scrape = json.loads(DATA_SCRAPE.read_text(encoding="utf-8"))
        if scrape and is_remote(scrape[0].get("image", "")):
            return scrape
    if DATA_JS.is_file():
        items = json.loads(DATA_JS.read_text(encoding="utf-8"))
        if items:
            return items
    raise SystemExit(f"Missing {DATA_JS}; run helpers/_scrape_video_gallery.py first")


def is_remote(url: str) -> bool:
    return url.startswith("http://") or url.startswith("https://")


def capture_images() -> tuple[dict[str, bytes], list[dict]]:
    captured: dict[str, bytes] = {}

    def on_response(response) -> None:
        url = response.url
        if "googleusercontent.com/sitesv" not in url:
            return
        if response.request.resource_type not in ("image", "imageset"):
            return
        try:
            if response.status != 200:
                return
            body = response.body()
            if not is_image_bytes(body):
                return
            key = sitesv_key(url)
            if key not in captured or len(body) > len(captured[key]):
                captured[key] = body
        except Exception:
            return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1400, "height": 2400})
        page.on("response", on_response)
        print("Loading Google Sites page and scrolling to fetch thumbnails…")
        page.goto(SITES_PAGE, wait_until="networkidle", timeout=180000)
        height = page.evaluate("() => document.body.scrollHeight")
        step = 700
        for y in range(0, max(height, 1), step):
            page.evaluate("(y) => window.scrollTo(0, y)", y)
            page.wait_for_timeout(250)
        page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(1500)
        pairs = page.evaluate(EXTRACT_PAIRS_JS)
        browser.close()

    print(f"Captured {len(captured)} image bodies, {len(pairs)} video blocks on page")
    return captured, pairs


def main() -> None:
    items = load_items()
    need_remote = any(is_remote(it.get("image", "")) for it in items)

    captured: dict[str, bytes] = {}
    if need_remote:
        captured, pairs = capture_images()
        pair_by_yt = {youtube_id(p["link"]): p["key"] for p in pairs if youtube_id(p["link"])}
    else:
        pair_by_yt = {}

    IMG_DIR.mkdir(parents=True, exist_ok=True)
    updated: list[dict] = []
    downloaded = 0
    skipped = 0
    missing: list[str] = []

    for i, item in enumerate(items, start=1):
        link = item["link"]
        caption = item["caption"]
        filename = local_name(i, link)
        dest = IMG_DIR / filename
        rel = WEB_PREFIX + filename
        vid = youtube_id(link)

        if dest.is_file() and dest.stat().st_size > 1000:
            skipped += 1
        elif need_remote:
            key = sitesv_key(item.get("image", ""))
            if not key or key not in captured:
                key = pair_by_yt.get(vid, "")
            body = captured.get(key)
            if body:
                dest.write_bytes(body)
                downloaded += 1
                print(f"  [{i:03d}] saved {filename}")
            else:
                missing.append(f"{i} {caption} ({vid})")
                continue
        else:
            if not dest.is_file():
                missing.append(f"{i} {caption} (file missing)")
                continue
            skipped += 1

        entry: dict = {"image": rel, "link": link, "caption": caption}
        if item.get("description"):
            entry["description"] = item["description"]
        updated.append(entry)

    if missing:
        raise SystemExit(
            "Could not capture thumbnails for:\n  " + "\n  ".join(missing[:10])
            + (f"\n  … and {len(missing) - 10} more" if len(missing) > 10 else "")
        )

    DATA_JS.write_text(
        json.dumps(updated, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"Done: {downloaded} downloaded, {skipped} reused, {len(updated)} items")
    print(f"Wrote {DATA_JS}")


if __name__ == "__main__":
    main()
