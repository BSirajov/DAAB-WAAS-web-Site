"""Extract video caption + description from live Google Sites page via Playwright."""
from __future__ import annotations

import json

from playwright.sync_api import sync_playwright

from _paths import ROOT

PAGE = "https://sites.google.com/view/alimler-derneyi/bak%C4%B1-forumu-2024/video-qalereya"
DATA = ROOT / "js" / "video-gallery-data.json"

EXTRACT = """
() => {
  const out = [];
  for (const img of document.querySelectorAll('img[src*="googleusercontent.com/sitesv"]')) {
    const block = img.closest('.oKdM2c');
    if (!block) continue;
    let link = '';
    const texts = [];
    let sib = block;
    for (let n = 0; n < 10; n++) {
      sib = sib.nextElementSibling;
      if (!sib) break;
      const a = sib.querySelector('a[href*="youtube.com"], a[href*="youtu.be"]');
      if (a && !link) link = a.href;
      for (const p of sib.querySelectorAll('p')) {
        const t = (p.innerText || '').replace(/\\s+/g, ' ').trim();
        if (t) texts.push(t);
      }
      if (link && texts.length >= 1) {
        const more = sib.nextElementSibling;
        if (more) {
          for (const p of more.querySelectorAll('p')) {
            const t = (p.innerText || '').replace(/\\s+/g, ' ').trim();
            if (t && !texts.includes(t)) texts.push(t);
          }
        }
        break;
      }
    }
    if (!link) continue;
    const caption = texts[0] || '';
    const description = texts.slice(1).join(' ').trim();
    out.push({ link, caption, description });
  }
  return out;
}
"""


def yt_id(link: str) -> str:
    import re

    m = re.search(r"(?:youtu\.be/|v=)([A-Za-z0-9_-]{6,})", link)
    return m.group(1) if m else ""


def main() -> None:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1400, "height": 900})
        page.goto(PAGE, wait_until="networkidle", timeout=180000)
        height = page.evaluate("() => document.body.scrollHeight")
        for y in range(0, height, 700):
            page.evaluate("(y) => window.scrollTo(0, y)", y)
            page.wait_for_timeout(200)
        page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(1000)
        extracted = page.evaluate(EXTRACT)
        browser.close()

    by_yt = {yt_id(x["link"]): x for x in extracted if yt_id(x["link"])}
    data = json.loads(DATA.read_text(encoding="utf-8"))
    filled = 0
    for row in data:
        ex = by_yt.get(yt_id(row["link"]), {})
        if ex.get("caption"):
            row["caption"] = ex["caption"]
        if ex.get("description") and not row.get("description"):
            row["description"] = ex["description"]
            filled += 1
    DATA.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    missing = [r for r in data if not r.get("description")]
    print(f"Playwright extracted {len(extracted)} blocks; filled {filled} missing descriptions")
    print(f"Still without description: {len(missing)}")


if __name__ == "__main__":
    main()
