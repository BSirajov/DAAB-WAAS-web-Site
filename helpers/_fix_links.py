from pathlib import Path
import re

ROOT = Path(r"c:\Users\BSira\Documents\GitHub\DAAB-WAAS web site")

# Fix broken nested card-name markup
for rel in ["az/scientists/profiles.html", "en/scientists/profiles.html"]:
    p = ROOT / rel
    t = p.read_text(encoding="utf-8")
    t = t.replace('<span class="card-name"><a class="card-name"', '<a class="card-name"')
    t = re.sub(r'(<a class="card-name" href="/cv/[^"]+">[^<]*(?:<span class="cred">[^<]*</span>)?)</span>', r'\1</a>', t)
    p.write_text(t, encoding="utf-8")
    print("fixed", rel)

CATALOG = {
    "Sevda Kərimova": "sevda_kerimova.html",
    "Kamal Əkbərov": "kamal_akbarov.html",
    "İlham Axundov": "ilham_akhundov.html",
    "İsmayıl Əliyev": "ismayil_aliyev.html",
    "Kamran Rüstəmov": "kamran_rustemov.html",
    "Hacıəli Nəcəfoğlu ": "hacali_necefoglu.html",
    "İlkin Gulusoy": "ilkin_qulusoy.html",
    "İsmixan Bayramov": "ismixan_bayramov.html",
    "Xəlil Kələntər": "xelil_kelenter.html",
}

for rel in ["js/scientists-catalog-data.js", "js/scientists-catalog-data-en.js"]:
    p = ROOT / rel
    t = p.read_text(encoding="utf-8")
    for name, slug in CATALOG.items():
        old = f'"ad_soyad": "{name}",'
        idx = t.find(old)
        if idx == -1:
            continue
        chunk = t[idx:idx+400]
        if f'"url": "../../cv/{slug}"' in chunk:
            continue
        chunk2 = chunk.replace('"url": ""', f'"url": "../../cv/{slug}"', 1)
        t = t[:idx] + chunk2 + t[idx+400:]
        print("catalog", rel, name)
    p.write_text(t, encoding="utf-8")

print("done")
