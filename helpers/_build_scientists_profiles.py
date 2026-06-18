"""Build az/en scientist profile catalog sections from i18n/scientists-profiles.json."""
from __future__ import annotations

import argparse
import re

try:
    from _paths import AZ_SCIENTISTS_PROFILES, EN_SCIENTISTS_PROFILES, ROOT
    from _site_wide_cleanup import SCRIPT_VERSIONS, STYLE_VERSIONS
    from scientists_profiles_core import (
        PROFILES_JSON,
        build_catalog_section,
        build_catalog_shell,
        load_profiles,
        replace_catalog_in_page,
    )
except ImportError:
    from helpers._paths import AZ_SCIENTISTS_PROFILES, EN_SCIENTISTS_PROFILES, ROOT  # type: ignore
    from helpers._site_wide_cleanup import SCRIPT_VERSIONS, STYLE_VERSIONS  # type: ignore
    from helpers.scientists_profiles_core import (  # type: ignore
        PROFILES_JSON,
        build_catalog_section,
        build_catalog_shell,
        load_profiles,
        replace_catalog_in_page,
    )

RENDER_MARK = "scientists-profiles-render.js"
RENDER_SNIPPET = '<script defer src="{prefix}js/scientists-profiles-render.js?v={ver}"></script>\n'
FILTERS_MARK = "scientists-cv-filters.js"


def ensure_client_render_scripts(page_path, *, prefix: str = "../../") -> list[str]:
    changes: list[str] = []
    text = page_path.read_text(encoding="utf-8")
    render_ver = SCRIPT_VERSIONS.get("scientists-profiles-render.js", 1)
    filters_ver = SCRIPT_VERSIONS.get("scientists-cv-filters.js", 5)

    if RENDER_MARK not in text:
        anchor = FILTERS_MARK
        pos = text.find(anchor)
        if pos >= 0:
            line_start = text.rfind("\n", 0, pos) + 1
            insert = RENDER_SNIPPET.format(prefix=prefix, ver=render_ver)
            text = text[:line_start] + insert + text[line_start:]
            changes.append("render-js")

    new_text, n = re.subn(
        r"scientists-cv-filters\.js\?v=\d+",
        f"scientists-cv-filters.js?v={filters_ver}",
        text,
    )
    if n:
        text = new_text
        changes.append("filters-js")

    new_text, n = re.subn(
        r"scientists-profiles-render\.js\?v=\d+",
        f"scientists-profiles-render.js?v={render_ver}",
        text,
    )
    if n:
        text = new_text
        changes.append("render-js-v")

    page_css_ver = STYLE_VERSIONS.get("daab-scientists-profiles-page.css", 16)
    new_text, n = re.subn(
        r"daab-scientists-profiles-page\.css\?v=\d+",
        f"daab-scientists-profiles-page.css?v={page_css_ver}",
        text,
    )
    if n:
        text = new_text
        changes.append("page-css-v")

    if changes:
        page_path.write_text(text, encoding="utf-8", newline="\n")
    return changes


def build_az(*, embed: bool = False) -> None:
    profiles = load_profiles()
    catalog = (
        build_catalog_section(profiles, "az", asset_prefix="../../")
        if embed
        else build_catalog_shell("az")
    )
    replace_catalog_in_page(AZ_SCIENTISTS_PROFILES, catalog)
    script_changes = ensure_client_render_scripts(AZ_SCIENTISTS_PROFILES)
    mode = f"{len(profiles)} embedded cards" if embed else "client-render shell"
    extra = f", scripts: {', '.join(script_changes)}" if script_changes else ""
    print(f"Built AZ catalog ({mode}) -> {AZ_SCIENTISTS_PROFILES.relative_to(ROOT)}{extra}")


def build_en(*, embed: bool = False) -> None:
    profiles = load_profiles()
    catalog = (
        build_catalog_section(profiles, "en", asset_prefix="../../")
        if embed
        else build_catalog_shell("en")
    )
    replace_catalog_in_page(EN_SCIENTISTS_PROFILES, catalog)
    script_changes = ensure_client_render_scripts(EN_SCIENTISTS_PROFILES)
    mode = f"{len(profiles)} embedded cards" if embed else "client-render shell"
    extra = f", scripts: {', '.join(script_changes)}" if script_changes else ""
    print(f"Built EN catalog ({mode}) -> {EN_SCIENTISTS_PROFILES.relative_to(ROOT)}{extra}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Render scientist profile cards from JSON")
    parser.add_argument("--az", action="store_true", help="Build az/scientists/profiles.html catalog only")
    parser.add_argument("--en", action="store_true", help="Build en/scientists/profiles.html catalog only")
    parser.add_argument(
        "--embed",
        action="store_true",
        help="Embed full card HTML in page (legacy; default is client-render shell)",
    )
    args = parser.parse_args()

    if not PROFILES_JSON.is_file():
        raise SystemExit(
            f"Missing {PROFILES_JSON.relative_to(ROOT)} — run: python helpers/_export_scientists_profiles_json.py"
        )

    embed = args.embed
    if args.az and not args.en:
        build_az(embed=embed)
    elif args.en and not args.az:
        build_en(embed=embed)
    else:
        build_az(embed=embed)
        build_en(embed=embed)


if __name__ == "__main__":
    main()
