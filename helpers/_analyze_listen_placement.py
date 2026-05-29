#!/usr/bin/env python3
"""Estimate which profile cards may place the Listen button under the portrait."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

PHOTO_HEIGHT_PX = 176
HEADER_MARGIN_PX = 8
META_BOX_PX = 70


def estimate_header_px(body: str) -> tuple[int, dict]:
    has_role = "card-role" in body
    name_m = re.search(r'class="card-name">(.+?)</span>', body, re.S)
    title_m = re.search(r'class="card-title">([^<]*)', body)
    name_text = re.sub(r"<[^>]+>", " ", name_m.group(1) if name_m else "")
    name_text = re.sub(r"\s+", " ", name_text).strip()
    title_text = (title_m.group(1).strip() if title_m else "")

    name_lines = max(1, (len(name_text) + 39) // 40)
    title_lines = max(0, (len(title_text) + 54) // 55) if title_text else 0

    px = (
        name_lines * 22
        + 18  # country
        + title_lines * 20
        + (20 if has_role else 0)
        + META_BOX_PX
        + HEADER_MARGIN_PX
    )
    return px, {
        "name": name_text,
        "title_len": len(title_text),
        "title_lines": title_lines,
        "has_role": has_role,
    }


def main() -> None:
    html = (ROOT / "az" / "scientists" / "profiles.html").read_text(encoding="utf-8")
    pattern = re.compile(
        r'<div class="card" id="([^"]+)"[^>]*>.*?<div class="card-body">(.*?)</div>\s*<a class="card-qr-link"',
        re.S,
    )
    cards = pattern.findall(html)
    print(f"Cards parsed: {len(cards)}")
    print(f"Photo height reference: {PHOTO_HEIGHT_PX}px\n")

    risky: list[tuple[int, str, dict]] = []
    for slug, body in cards:
        px, meta = estimate_header_px(body)
        if px < PHOTO_HEIGHT_PX:
            risky.append((px, slug, meta))

    risky.sort()
    print(f"Cards with estimated header shorter than photo ({len(risky)}):")
    for px, slug, meta in risky:
        role = " +role" if meta["has_role"] else ""
        print(
            f"  ~{px:3d}px  {slug:42s}  title={meta['title_len']:3d} chars{role}"
        )
        print(f"           {meta['name'][:72]}")

    # Shortest affiliation titles — Listen often sits beside lower portrait area
    titles = re.findall(
        r'id="([^"]+)".*?card-title">([^<]+)</p>',
        html,
        re.S,
    )
    short_titles = sorted(
        ((len(t.strip()), slug, t.strip()) for slug, t in titles),
        key=lambda x: (x[0], x[1]),
    )
    print("\nShortest card-title text (most likely 'Listen under photo' visually):")
    for ln, slug, text in short_titles[:15]:
        print(f"  {ln:2d} chars  {slug:42s}  {text}")


if __name__ == "__main__":
    main()
