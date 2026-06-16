#!/usr/bin/env python3
"""OBSOLETE — az/en/sponsors.html was removed in favour of sponsorship_partnership.html."""
from __future__ import annotations

import sys


def main() -> int:
    print(
        "This helper is retired.\n"
        "  Legacy pages: az/sponsors.html, en/sponsors.html (deleted)\n"
        "  Replacement:  az/sponsorship_partnership.html, en/sponsorship_partnership.html\n"
        "  CSS:          css/daab-sponsors-page.css (includes forum sponsorship rules)\n"
        "To rebuild sponsorship pages, edit the live HTML or add a dedicated builder."
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
