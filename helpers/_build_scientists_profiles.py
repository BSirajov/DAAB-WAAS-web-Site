"""Build az/en scientist profile catalog sections from i18n/scientists-profiles.json."""
from __future__ import annotations

import argparse

try:
    from _paths import AZ_SCIENTISTS_PROFILES, EN_SCIENTISTS_PROFILES, ROOT
    from scientists_profiles_core import (
        PROFILES_JSON,
        build_catalog_section,
        load_profiles,
        replace_catalog_in_page,
    )
except ImportError:
    from helpers._paths import AZ_SCIENTISTS_PROFILES, EN_SCIENTISTS_PROFILES, ROOT  # type: ignore
    from helpers.scientists_profiles_core import (  # type: ignore
        PROFILES_JSON,
        build_catalog_section,
        load_profiles,
        replace_catalog_in_page,
    )


def build_az() -> None:
    profiles = load_profiles()
    catalog = build_catalog_section(profiles, "az", asset_prefix="../../")
    replace_catalog_in_page(AZ_SCIENTISTS_PROFILES, catalog)
    print(f"Built AZ catalog ({len(profiles)} cards) -> {AZ_SCIENTISTS_PROFILES.relative_to(ROOT)}")


def build_en() -> None:
    profiles = load_profiles()
    catalog = build_catalog_section(profiles, "en", asset_prefix="../../")
    replace_catalog_in_page(EN_SCIENTISTS_PROFILES, catalog)
    print(f"Built EN catalog ({len(profiles)} cards) -> {EN_SCIENTISTS_PROFILES.relative_to(ROOT)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Render scientist profile cards from JSON")
    parser.add_argument("--az", action="store_true", help="Build az/scientists/profiles.html catalog only")
    parser.add_argument("--en", action="store_true", help="Build en/scientists/profiles.html catalog only")
    args = parser.parse_args()

    if not PROFILES_JSON.is_file():
        raise SystemExit(
            f"Missing {PROFILES_JSON.relative_to(ROOT)} — run: python helpers/_export_scientists_profiles_json.py"
        )

    if args.az and not args.en:
        build_az()
    elif args.en and not args.az:
        build_en()
    else:
        build_az()
        build_en()


if __name__ == "__main__":
    main()
