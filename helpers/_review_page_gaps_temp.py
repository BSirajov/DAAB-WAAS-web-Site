#!/usr/bin/env python3
from pathlib import Path
import re
ROOT = Path(__file__).resolve().parents[1]

for lang in ("az", "en"):
    print(f"--- forum {lang} ---")
    for p in sorted((ROOT / lang / "forum" / "2024").glob("*.html")):
        t = p.read_text(encoding="utf-8")
        has_skip = 'class="skip"' in t
        print(f"  {p.name}: breadcrumbs={'forum-breadcrumbs' in t} skip={has_skip} mobile={'daab-mobile.css' in t}")

for base in ("az", "en"):
    missing_skip = []
    missing_mobile = []
    for p in (ROOT / base).rglob("*.html"):
        if p.parent.name == "application":
            continue
        t = p.read_text(encoding="utf-8")
        if "data-daab-legacy-redirect" in t:
            continue
        if 'class="skip"' not in t:
            missing_skip.append(str(p.relative_to(ROOT)))
        if "daab-mobile.css" not in t:
            missing_mobile.append(str(p.relative_to(ROOT)))
    print(f"{base} missing skip ({len(missing_skip)}):", missing_skip)
    print(f"{base} missing mobile ({len(missing_mobile)}):", missing_mobile)

http = []
blank = []
for p in list((ROOT / "az").rglob("*.html")) + list((ROOT / "en").rglob("*.html")):
    t = p.read_text(encoding="utf-8")
    rel = str(p.relative_to(ROOT))
    if re.search(r'href="http://(?!localhost)', t):
        http.append(rel)
    for m in re.finditer(r'<a\b[^>]*target="_blank"[^>]*>', t, re.I):
        if "noopener" not in m.group(0).lower():
            blank.append(rel)
            break
print("http pages:", http)
print("blank without noopener:", blank)
