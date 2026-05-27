#!/usr/bin/env python3
"""Write gallery URL cache from _cache_book_exhibition_page.md (standalone photos only)."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

MD = ROOT / "helpers" / "_cache_book_exhibition_page.md"
URL_CACHE = ROOT / "helpers" / "_cache_book_exhibition_gallery_urls.txt"


def main() -> None:
    text = MD.read_text(encoding="utf-8")
    urls = re.findall(
        r"^!\[\]\((https://lh3\.googleusercontent\.com/sitesv/[^)]+)\)",
        text,
        re.MULTILINE,
    )
    urls = [re.sub(r"=w\d+", "=w1280", u) for u in urls if "=w16383" not in u]
    URL_CACHE.write_text("\n".join(urls) + "\n", encoding="utf-8")
    print(f"Wrote {len(urls)} URLs -> {URL_CACHE}")


if __name__ == "__main__":
    main()
