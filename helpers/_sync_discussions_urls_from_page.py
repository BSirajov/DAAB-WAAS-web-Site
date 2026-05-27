#!/usr/bin/env python3
"""Sync Müzakirələr gallery URL list from cached page markdown (logo excluded)."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

MD = ROOT / "helpers" / "_cache_discussions_page.md"
URL_CACHE = ROOT / "helpers" / "_cache_discussions_gallery_urls.txt"


def gallery_urls() -> list[str]:
    text = MD.read_text(encoding="utf-8")
    urls = re.findall(
        r"^!\[\]\((https://lh3\.googleusercontent\.com/sitesv/[^)]+)\)",
        text,
        re.MULTILINE,
    )
    return [re.sub(r"=w\d+", "=w1280", u) for u in urls if "=w16383" not in u]


def main() -> None:
    urls = gallery_urls()
    URL_CACHE.write_text("\n".join(urls) + "\n", encoding="utf-8")
    print(f"Wrote {len(urls)} URLs -> {URL_CACHE}")


if __name__ == "__main__":
    main()
