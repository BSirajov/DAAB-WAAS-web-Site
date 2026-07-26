#!/usr/bin/env python3
"""Download the original per-article thumbnails from Seymur Nasirov's Google Site.

The source page ("Fəaliyyətlərim") lays out one hosted image directly before
each outbound article link, so the images (in document order) map 1:1 onto the
RESOURCES list in `_build_seymur_media.py`. A trailing image that belongs to a
link-less text item is skipped by pairing each image with the article anchor
that follows it before the next image.

Run from repo root:
    python helpers/_download_seymur_thumbs.py
"""
from __future__ import annotations

import http.cookiejar
import json
import re
import urllib.request

from _paths import ROOT
from _scientist_media import media_thumb_dir

PAGE = "https://sites.google.com/view/seymurnasirov/f%C9%99aliyy%C9%99tl%C9%99rim"
OUT_DIR = media_thumb_dir("seymur-nasirov-media-thumbnails")
MANIFEST = ROOT / "helpers" / "_seymur_thumbs.json"

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0 Safari/537.36"
)

_opener = urllib.request.build_opener(
    urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar())
)


def fetch(url: str, referer: str | None = None) -> bytes:
    headers = {"User-Agent": UA, "Accept-Language": "az,en;q=0.8"}
    if referer:
        headers["Referer"] = referer
        headers["Accept"] = "image/avif,image/webp,image/apng,image/*,*/*;q=0.8"
    req = urllib.request.Request(url, headers=headers)
    with _opener.open(req, timeout=60) as resp:
        return resp.read()


def image_urls() -> list[str]:
    raw = fetch(PAGE).decode("utf-8", errors="ignore")

    imgs = [
        (m.start(), m.group(1))
        for m in re.finditer(
            r'<img\b[^>]*\bsrc="(https://sites\.google\.com/sitesv-images-rt/[^"]+)"',
            raw,
            flags=re.I,
        )
    ]
    links = [
        m.start()
        for m in re.finditer(r'<a class="XqQF9c" href="([^"]+)"', raw)
        if "safelinks" not in m.group(1) and "daab-waas.org" not in m.group(1)
    ]

    # Keep only images immediately followed by an article link (before next image).
    urls: list[str] = []
    seen: set[str] = set()
    for idx, (pos, url) in enumerate(imgs):
        nxt = imgs[idx + 1][0] if idx + 1 < len(imgs) else float("inf")
        if any(pos < lp < nxt for lp in links) and url not in seen:
            seen.add(url)
            urls.append(url)
    return urls


def ext_for(data: bytes) -> str:
    if data[:3] == b"\xff\xd8\xff":
        return "jpg"
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return "png"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "webp"
    if data[:6] in (b"GIF87a", b"GIF89a"):
        return "gif"
    return "jpg"


def main() -> int:
    urls = image_urls()
    print(f"Found {len(urls)} article thumbnail images in source order")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    manifest: list[str] = []
    for i, url in enumerate(urls, start=1):
        data = fetch(url, referer=PAGE)
        ext = ext_for(data)
        name = f"{i:02d}.{ext}"
        (OUT_DIR / name).write_bytes(data)
        manifest.append(name)
        print(f"  [{i:02d}] {len(data):>7} bytes -> {name}")

    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote manifest {MANIFEST.relative_to(ROOT)} ({len(manifest)} entries)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
