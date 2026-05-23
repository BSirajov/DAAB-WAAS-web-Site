"""Repository root paths for DAAB maintenance scripts."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HELPERS = Path(__file__).resolve().parent

# Canonical live pages (prefer az/ and en/ trees over root *_az.html stubs).
AZ_SCIENTISTS_LIST = ROOT / "az" / "scientists" / "list.html"
AZ_SCIENTISTS_PROFILES = ROOT / "az" / "scientists" / "profiles.html"
EN_SCIENTISTS_LIST = ROOT / "en" / "scientists" / "list.html"
EN_SCIENTISTS_PROFILES = ROOT / "en" / "scientists" / "profiles.html"

# Legacy bookmark URLs at repository root (thin redirects only).
LEGACY_SCIENTISTS_LIST = ROOT / "scientists_list_view_az.html"
LEGACY_SCIENTISTS_PROFILES = ROOT / "scientists_card_view_az.html"
