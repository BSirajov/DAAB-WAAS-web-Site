"""Repository root paths for DAAB maintenance scripts."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HELPERS = Path(__file__).resolve().parent

# Canonical live pages under az/ and en/.
AZ_SCIENTISTS_LIST = ROOT / "az" / "scientists" / "list.html"
AZ_SCIENTISTS_PROFILES = ROOT / "az" / "scientists" / "profiles.html"
EN_SCIENTISTS_LIST = ROOT / "en" / "scientists" / "list.html"
EN_SCIENTISTS_PROFILES = ROOT / "en" / "scientists" / "profiles.html"

FOOTER_COPYRIGHT_AZ = "© 2026 DAAB — Bütün hüquqlar qorunur"
FOOTER_COPYRIGHT_EN = "© 2026 WAAS — All Rights Reserved"
