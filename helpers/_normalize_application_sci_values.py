#!/usr/bin/env python3
"""Align AZ membership application sci checkbox values with EN canonical slugs."""
from __future__ import annotations

from pathlib import Path

from _paths import ROOT

AZ_TO_EN = {
    "filologiya": "philology",
    "felsefe": "philosophy",
    "tarix": "history",
    "arxeologiya": "archaeology",
    "etnologiya": "ethnology",
    "siyasi": "political",
    "sosiologiya": "sociology",
    "psixologiya": "psychology",
    "pedoqogika": "pedagogy",
    "jurnalistika": "journalism",
    "huquq": "law",
    "iqtisadiyyat": "economics",
    "beynelxalq": "international",
    "riyaziyyat": "mathematics",
    "mentiq": "logic",
    "kibernetika": "cybernetics",
    "fizika": "physics",
    "kimya": "chemistry",
    "geologiya": "geology",
    "cografiya": "geography",
    "astronomiya": "astronomy",
    "informatika": "cs",
    "elektronika": "electronics",
    "avtomatika": "robotics",
    "neftqaz": "petroleum",
    "tikinti": "construction",
    "energetika": "energy",
    "mexanika": "mechanics",
    "material": "materials",
    "neqliyyat": "transport",
    "aerokosmik": "aerospace",
    "tibb": "medicine",
    "derman": "pharmacy",
    "baytarlik": "veterinary",
    "biotex": "biotech",
    "aqronomluq": "agronomy",
    "torpaq": "soil",
    "meyvecilik": "horticulture",
    "mesecilik": "forestry",
    "suteserrufati": "water",
    "zooinjineriya": "animal",
    "baliqcilik": "fishery",
    "musiqisunaslik": "musicology",
    "teatr": "theatre",
    "ressamliq": "finearts",
    "medeniyyet": "culturalhistory",
}


def main() -> None:
    path = ROOT / "az" / "application.html"
    text = path.read_text(encoding="utf-8")
    count = 0
    for az_val, en_val in AZ_TO_EN.items():
        old = f'value="{az_val}"'
        new = f'value="{en_val}"'
        if old in text:
            text = text.replace(old, new)
            count += 1
    path.write_text(text, encoding="utf-8")
    print(f"Updated {count} sci values in {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
