#!/usr/bin/env python3
"""Extract inline <style> blocks into css/daab-*-page.css and link from locale HTML."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

STYLE_BLOCK = re.compile(r"\s*<style>.*?</style>\s*", re.DOTALL | re.IGNORECASE)
BACK_TO_TOP = '<link href="{root}css/daab-back-to-top.css?v=1" rel="stylesheet"/>'

MIGRATIONS: list[dict] = [
    {
        "css": "daab-charter-page.css",
        "version": 1,
        "source": "en/charter.html",
        "pages": ["en/charter.html", "az/charter.html"],
    },
    {
        "css": "daab-foundation-page.css",
        "version": 1,
        "source": "en/foundation.html",
        "pages": ["en/foundation.html", "az/foundation.html"],
    },
    {
        "css": "daab-mission-page.css",
        "version": 1,
        "source": "en/mission.html",
        "pages": ["en/mission.html", "az/mission.html"],
    },
    {
        "css": "daab-membership-page.css",
        "version": 1,
        "source": "en/membership.html",
        "pages": ["en/membership.html", "az/membership.html"],
    },
    {
        "css": "daab-activities-page.css",
        "version": 1,
        "source": "en/activities.html",
        "pages": ["en/activities.html", "az/activities.html"],
    },
    {
        "css": "daab-scientists-list-page.css",
        "version": 1,
        "source": "en/scientists/list.html",
        "pages": ["en/scientists/list.html", "az/scientists/list.html"],
    },
    {
        "css": "daab-scientists-profiles-page.css",
        "version": 1,
        "source": "en/scientists/profiles.html",
        "pages": ["en/scientists/profiles.html", "az/scientists/profiles.html"],
    },
]


def asset_root_for(html_path: Path) -> str:
    rel = html_path.relative_to(ROOT)
    depth = len(rel.parts) - 1
    return "../" * depth if depth else "./"


def extract_style(html: str) -> str | None:
    m = re.search(r"<style>(.*?)</style>", html, re.DOTALL | re.IGNORECASE)
    return m.group(1).strip() if m else None


def css_banner(css_name: str, source: str) -> str:
    return (
        f"/**\n"
        f" * Extracted from inline <style> on {source}.\n"
        f" * Shared by AZ/EN locale pages — do not duplicate in HTML.\n"
        f" */\n\n"
    )


def main() -> None:
    for mig in MIGRATIONS:
        src = ROOT / mig["source"]
        css_text = extract_style(src.read_text(encoding="utf-8"))
        if not css_text:
            print("skip (no style):", mig["source"])
            continue

        out = ROOT / "css" / mig["css"]
        if mig.get("overwrite") or not out.exists():
            out.write_text(css_banner(mig["css"], mig["source"]) + css_text + "\n", encoding="utf-8")
            print("wrote", out.relative_to(ROOT))

        link_name = mig["css"]
        ver = mig["version"]
        for page_rel in mig["pages"]:
            page = ROOT / page_rel
            text = page.read_text(encoding="utf-8")
            root = asset_root_for(page)
            link = f'<link href="{root}css/{link_name}?v={ver}" rel="stylesheet"/>\n'
            link_id = f'css/{link_name}'

            if link_id in text and STYLE_BLOCK.search(text):
                text = STYLE_BLOCK.sub("\n", text, count=1)
            elif STYLE_BLOCK.search(text):
                text = STYLE_BLOCK.sub("\n" + link, text, count=1)
            elif link_id not in text:
                anchor = BACK_TO_TOP.format(root=root)
                if anchor in text:
                    text = text.replace(anchor, anchor + "\n" + link.strip())
                else:
                    print("warn: no anchor", page_rel)
                    continue
            else:
                continue

            page.write_text(text, encoding="utf-8")
            print("updated", page_rel)


if __name__ == "__main__":
    main()
