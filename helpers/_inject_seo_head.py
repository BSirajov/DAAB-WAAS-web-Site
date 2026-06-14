#!/usr/bin/env python3
"""Inject favicon, canonical, hreflang, and Open Graph / Twitter meta into deploy HTML."""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

from _paths import ROOT
from _site_wide_cleanup import iter_deploy_html

SITE_ORIGIN = "https://daab-waas.com"
MARKER_START = "<!-- daab-seo -->"
MARKER_END = "<!-- /daab-seo -->"

RE_OLD_SEO = re.compile(
    r"\s*<!-- daab-seo -->.*?<!-- /daab-seo -->",
    re.DOTALL,
)

BROKEN_DESC_RE = re.compile(
    r'(name=["\']description["\'])\s*\n(<!-- daab-seo -->.*?<!-- /daab-seo -->)/>',
    re.DOTALL,
)

RE_TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.DOTALL)
RE_DESC_TAG = re.compile(
    r'<meta\s+[^>]*?\bname=["\']description["\'][^>]*/>',
    re.I,
)
RE_DESC_CONTENT = re.compile(
    r'\bcontent=["\']([^"\']*)["\']',
    re.I,
)
RE_ASSET_ROOT = re.compile(r'data-daab-asset-root="([^"]*)"', re.I)
RE_LANG = re.compile(r'data-daab-lang="(az|en)"|<html[^>]*\slang="(az|en)"', re.I)


def load_lang_pairs() -> dict[str, dict[str, str]]:
    pairs: dict[str, dict[str, str]] = {}
    routes = json.loads((ROOT / "i18n" / "routes.json").read_text(encoding="utf-8"))
    for page in routes["pages"]:
        az = page["az"].replace("\\", "/")
        en = page["en"].replace("\\", "/")
        entry = {"az": az, "en": en}
        pairs[az] = entry
        pairs[en] = entry

    az_root = ROOT / "az" / "prominent_figures"
    if az_root.is_dir():
        for az_path in az_root.rglob("*.html"):
            if az_path.name == "hazirlanir.html":
                continue
            rel = az_path.relative_to(ROOT / "az").as_posix()
            en_rel = f"en/{rel}"
            if not (ROOT / en_rel).is_file():
                continue
            entry = {"az": f"az/{rel}", "en": en_rel}
            pairs[f"az/{rel}"] = entry
            pairs[en_rel] = entry
    return pairs


def page_lang(path: Path, text: str) -> str:
    m = RE_LANG.search(text)
    if m:
        return m.group(1) or m.group(2) or "az"
    if path.parts and path.parts[0] == "en":
        return "en"
    if path.parts and path.parts[0] == "az":
        return "az"
    return "az"


def asset_root(path: Path, text: str) -> str:
    m = RE_ASSET_ROOT.search(text)
    if m:
        root = m.group(1)
        return root if root.endswith("/") else root + "/"
    depth = len(path.relative_to(ROOT).parts) - 1
    return "../" * depth if depth > 0 else "./"


def extract_title(text: str) -> str:
    m = RE_TITLE.search(text)
    if not m:
        return ""
    return re.sub(r"\s+", " ", m.group(1)).strip()


def extract_description(text: str) -> str:
    m = RE_DESC_TAG.search(text)
    if not m:
        return ""
    cm = RE_DESC_CONTENT.search(m.group(0))
    return cm.group(1).strip() if cm else ""


def repair_broken_description_meta(text: str) -> str:
    return BROKEN_DESC_RE.sub(r'\1/>\n\2', text)


def strip_existing_seo(text: str) -> str:
    text = repair_broken_description_meta(text)
    text = RE_OLD_SEO.sub("", text)
    text = re.sub(r'\s*<link rel="icon"[^>]*>', "", text, flags=re.I)
    text = re.sub(r'\s*<link rel="canonical"[^>]*>', "", text, flags=re.I)
    text = re.sub(r'\s*<link rel="alternate" hreflang="[^"]+"[^>]*>', "", text, flags=re.I)
    text = re.sub(r'\s*<meta property="og:[^"]+"[^>]*>', "", text, flags=re.I)
    text = re.sub(r'\s*<meta name="twitter:[^"]+"[^>]*>', "", text, flags=re.I)
    return text


def build_seo_block(
    *,
    rel_path: str,
    lang: str,
    title: str,
    description: str,
    asset: str,
    pair: dict[str, str] | None,
) -> str:
    canonical = f"{SITE_ORIGIN}/{rel_path}"
    esc_title = html.escape(title, quote=True)
    esc_desc = html.escape(description, quote=True) if description else esc_title
    og_locale = "az_AZ" if lang == "az" else "en_US"
    alt_locale = "en_US" if lang == "az" else "az_AZ"

    lines = [
        MARKER_START,
        f'<link rel="icon" href="{asset}images/daab-logo.svg" type="image/svg+xml"/>',
        f'<link rel="canonical" href="{canonical}"/>',
    ]
    if pair:
        az_url = f"{SITE_ORIGIN}/{pair['az']}"
        en_url = f"{SITE_ORIGIN}/{pair['en']}"
        lines.extend(
            [
                f'<link rel="alternate" hreflang="az" href="{az_url}"/>',
                f'<link rel="alternate" hreflang="en" href="{en_url}"/>',
                f'<link rel="alternate" hreflang="x-default" href="{az_url}"/>',
            ]
        )
    lines.extend(
        [
            '<meta property="og:type" content="website"/>',
            '<meta property="og:site_name" content="DAAB/WAAS"/>',
            f'<meta property="og:title" content="{esc_title}"/>',
            f'<meta property="og:description" content="{esc_desc}"/>',
            f'<meta property="og:url" content="{canonical}"/>',
            f'<meta property="og:locale" content="{og_locale}"/>',
            f'<meta property="og:locale:alternate" content="{alt_locale}"/>',
            '<meta name="twitter:card" content="summary"/>',
            f'<meta name="twitter:title" content="{esc_title}"/>',
            f'<meta name="twitter:description" content="{esc_desc}"/>',
            MARKER_END,
        ]
    )
    return "\n".join(lines)


def inject_seo(text: str, path: Path, pairs: dict[str, dict[str, str]]) -> str:
    rel_path = path.relative_to(ROOT).as_posix().replace("\\", "/")
    if rel_path == "index.html":
        return text

    text = strip_existing_seo(text)
    lang = page_lang(path, text)
    title = extract_title(text)
    description = extract_description(text)
    if not title and not description:
        return text

    block = build_seo_block(
        rel_path=rel_path,
        lang=lang,
        title=title or "DAAB/WAAS",
        description=description,
        asset=asset_root(path, text),
        pair=pairs.get(rel_path),
    )

    desc_match = RE_DESC_TAG.search(text)
    if desc_match:
        insert_at = desc_match.end()
        return text[:insert_at] + "\n" + block + text[insert_at:]

    title_match = RE_TITLE.search(text)
    if title_match:
        insert_at = title_match.end()
        return text[:insert_at] + "\n" + block + text[insert_at:]

    head_end = text.lower().find("</head>")
    if head_end == -1:
        return text
    return text[:head_end] + block + "\n" + text[head_end:]


def main() -> int:
    pairs = load_lang_pairs()
    updated = 0
    for path in iter_deploy_html():
        original = path.read_text(encoding="utf-8")
        repaired = repair_broken_description_meta(original)
        new = inject_seo(repaired, path, pairs)
        if new != original:
            path.write_text(new, encoding="utf-8", newline="\n")
            updated += 1
    print(f"Injected SEO head block into {updated} HTML file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
