from pathlib import Path
import re

ROOT = Path(r"c:\Users\BSira\Documents\GitHub\DAAB-WAAS web site")

# EN Kamran cards - link by photo
en = ROOT / "en/scientists/profiles.html"
t = en.read_text(encoding="utf-8")

pairs = [
    ("ismayil-eliyev.png", "ismayil_aliyev.html"),
    ("kamran-rustemov.png", "kamran_rustemov.html"),
]
for photo, slug in pairs:
    pat = rf'(<div class="card"[^>]*>.*?scientists-photos/{re.escape(photo)}[^>]*>.*?<span class="card-name">)'
    if re.search(pat, t, re.S) and f'href="/cv/{slug}"' not in re.search(pat, t, re.S).group(0):
        t = re.sub(pat, rf'\1<a class="card-name" href="/cv/{slug}">', t, count=1, flags=re.S)
        t = re.sub(
            rf'(<a class="card-name" href="/cv/{re.escape(slug)}">[^<]*(?:<span class="cred">[^<]*</span>)?)</span>',
            r"\1</a>",
            t,
            count=1,
            flags=re.S,
        )
        print("linked en", slug)

en.write_text(t, encoding="utf-8")

CATALOG_EN = {
    "Sevda Kerimova": "sevda_kerimova.html",
    "Kamal Akbarov": "kamal_akbarov.html",
    "Ilham Akhundov": "ilham_akhundov.html",
    "Ismayil Aliyev": "ismayil_aliyev.html",
    "Kamran Rustamov": "kamran_rustemov.html",
    "Hacieli Necefoglu": "hacali_necefoglu.html",
    "Ilkin Gulusoy": "ilkin_qulusoy.html",
    "Ismikhan Bayramov": "ismixan_bayramov.html",
    "Khalil Kelenter": "xelil_kelenter.html",
}

p = ROOT / "js/scientists-catalog-data-en.js"
t = p.read_text(encoding="utf-8")
for name, slug in CATALOG_EN.items():
    old = f'"ad_soyad": "{name}",'
    idx = t.find(old)
    if idx == -1:
        print("missing", name)
        continue
    chunk = t[idx:idx+400]
    if f'"url": "../../cv/{slug}"' in chunk:
        continue
    chunk2 = chunk.replace('"url": ""', f'"url": "../../cv/{slug}"', 1)
    t = t[:idx] + chunk2 + t[idx+400:]
    print("catalog-en", name)
p.write_text(t, encoding="utf-8")
print("done")
