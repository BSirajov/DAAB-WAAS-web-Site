"""Repository root paths for DAAB maintenance scripts."""
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HELPERS = Path(__file__).resolve().parent

# Canonical live pages under az/ and en/.
AZ_SCIENTISTS_LIST = ROOT / "az" / "scientists" / "list.html"
AZ_SCIENTISTS_PROFILES = ROOT / "az" / "scientists" / "profiles.html"
EN_SCIENTISTS_LIST = ROOT / "en" / "scientists" / "list.html"
EN_SCIENTISTS_PROFILES = ROOT / "en" / "scientists" / "profiles.html"

# Public site name already used by the domain (daab-waas.com) and the DAAB / WAAS brand.
SITE_NAME = "DAAB-WAAS"
BUILD_NUMBER_FILE = ROOT / "build_number.txt"

# Previous footer sentences. Replaced in place; not a build number (the year is a calendar stamp).
LEGACY_FOOTER_COPYRIGHTS = (
    "© 2026 WAAS — All Rights Reserved",
    "© 2026 WAAS — All rights reserved",
    "© 2026 DAAB — Bütün hüquqlar qorunur",
    "© 2026 DAAB / WAAS — All Rights Reserved",
    "© 2026 DAAB — All Rights Reserved",
)


def read_build_number() -> int:
    """Return the stored deployment build counter, or 0 when none has been issued."""
    if not BUILD_NUMBER_FILE.is_file():
        return 0
    raw = BUILD_NUMBER_FILE.read_text(encoding="utf-8").strip()
    if raw.isdigit():
        return int(raw)
    return 0


def write_build_number(number: int) -> None:
    BUILD_NUMBER_FILE.write_text(f"{number}\n", encoding="utf-8", newline="\n")


def bump_build_number() -> int:
    """Retired. The footer build token is a timestamp; this counter is not incremented."""
    return read_build_number()


def current_build_stamp() -> str:
    """Local date and time when the deployment script runs: YYYYMMDD - HHmm."""
    return datetime.now().strftime("%Y%m%d - %H%M")


def footer_copyright_line(build: str | None = None) -> str:
    """English copyright row for every locale. Build token is local date and time."""
    stamp = current_build_stamp() if build is None else build
    return f"© {SITE_NAME} - All rights reserved | Build {stamp}"


FOOTER_COPYRIGHT_AZ = footer_copyright_line()
FOOTER_COPYRIGHT_EN = FOOTER_COPYRIGHT_AZ
