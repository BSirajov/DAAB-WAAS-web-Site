# -*- coding: utf-8 -*-
from pathlib import Path
import re

ROOT = Path(r"c:\Users\BSira\Documents\GitHub\DAAB-WAAS web site")

PROFILE_LINKS = [
    ("messoud.efendiyev@gmail.com", "mesud_efendiyev.html"),
    ("murad.abuzarli@univie.ac.at", "murad_abuzerli.html"),
    ("murad.omarov@nure.ua", "murad_omarov.html"),
    ("natig_atakishiyev@hotmail.com", "natiq_atakishiyev.html"),
    ("masumova@mail.ru", "nigar_masumova.html"),
    ("levap@tauex.tau.ac.il", "lev_eppelbaum.html"),
    ("makbulesabziyeva@anadolu.edu.tr", "makbule_sabziyeva.html"),
    ("mehdi.genceli@marmara.edu.tr", "mehdi_genceli.html"),
    ("mrheyet@gmail.com", "mehmet_riza_heyet.html"),
    ("applebaum.mark@gmail.com", "mark_applebaum.html"),
]


def link_profiles(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    for email, slug in PROFILE_LINKS:
        href = f"/cv/{slug}"
        card_re = re.compile(
            rf'(<div class="card"[^>]*data-email="{re.escape(email)}"[^>]*>.*?)'
            rf'<span class="card-name">(.*?<span class="cred">.*?</span>)\s*</span>',
            re.S,
        )
        m = card_re.search(text)
        if not m:
            print(f"  WARN: no card for {email} in {path.name}")
            continue
        if href in m.group(0):
            print(f"  skip {email}")
            continue
        inner = m.group(2)
        replacement = m.group(1) + f'<a class="card-name" href="{href}">{inner}</a>'
        text = text[: m.start()] + replacement + text[m.end() :]
        print(f"  linked {email} -> {slug}")
    path.write_text(text, encoding="utf-8")


def link_catalog(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    for email, slug in PROFILE_LINKS:
        idx = text.find(f'"email": "{email}"')
        if idx == -1:
            print(f"  WARN: no catalog entry for {email} in {path.name}")
            continue
        chunk_start = text.rfind("{", 0, idx)
        chunk_end = text.find("},", idx)
        if chunk_end == -1:
            chunk_end = text.find("}\n", idx)
        chunk = text[chunk_start : chunk_end + 1]
        target = f'"url": "../../cv/{slug}"'
        if target in chunk:
            print(f"  skip catalog {email}")
            continue
        new_chunk = chunk.replace('"url": ""', target, 1)
        if new_chunk == chunk:
            print(f"  WARN: could not set url for {email}")
            continue
        text = text[:chunk_start] + new_chunk + text[chunk_end + 1 :]
        print(f"  catalog {email} -> {slug}")
    path.write_text(text, encoding="utf-8")


for rel in ["az/scientists/profiles.html", "en/scientists/profiles.html"]:
    print(rel)
    link_profiles(ROOT / rel)

for rel in ["js/scientists-catalog-data.js", "js/scientists-catalog-data-en.js"]:
    print(rel)
    link_catalog(ROOT / rel)

print("done")
