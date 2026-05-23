from pathlib import Path
import re

ROOT = Path(r"c:\Users\BSira\Documents\GitHub\DAAB-WAAS web site")

CATALOG_URLS = {
    "Sevda Kərimova": "../../cv/sevda_kerimova.html",
    "Kamal Əkbərov": "../../cv/kamal_akbarov.html",
    "İlham Axundov": "../../cv/ilham_akhundov.html",
    "İsmayıl Əliyev": "../../cv/ismayil_aliyev.html",
    "Kamran Rüstəmov": "../../cv/kamran_rustemov.html",
    "Hacıəli Nəcəfoğlu ": "../../cv/hacali_necefoglu.html",
    "Hacıəli Nəcəfoğlu": "../../cv/hacali_necefoglu.html",
    "İlkin Gulusoy": "../../cv/ilkin_qulusoy.html",
    "İsmixan Bayramov": "../../cv/ismixan_bayramov.html",
    "Xəlil Kələntər": "../../cv/xelil_kelenter.html",
}

PROFILE_LINKS = [
    ("sevda.aydin.k@gmail.com", None, "sevda_kerimova.html"),
    ("kamal.akbarov@gmail.com", None, "kamal_akbarov.html"),
    ("iakhundo@uwaterloo.ca", None, "ilham_akhundov.html"),
    ("aliev.05@mail.ru", "İqtisadiyyat", "ismayil_aliyev.html"),
    ("aliev.05@mail.ru", "Mühəndis", "kamran_rustemov.html"),
    ("alinecef@hotmail.com", None, "hacali_necefoglu.html"),
    ("ilkingulusoy@gmail.com", None, "ilkin_qulusoy.html"),
    ("ismihan.bayramoglu@ieu.edu.tr", None, "ismixan_bayramov.html"),
    ("gosx2020@gmail.com", None, "xelil_kelenter.html"),
]


def link_catalog(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    for name, url in CATALOG_URLS.items():
        pattern = rf'("ad_soyad": "{re.escape(name)}",\s*\n(?:.*?\n)*?"url": )""'
        text, n = re.subn(pattern, rf'\1"{url}"', text, count=1)
        if n:
            print(f"  catalog {path.name}: {name}")
    path.write_text(text, encoding="utf-8")


def link_profiles(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    for email, ixt, slug in PROFILE_LINKS:
        if ixt:
            card_re = rf'(<div class="card"[^>]*data-email="{re.escape(email)}"[^>]*data-ixtilas="{re.escape(ixt)}"[^>]*>.*?<span class="card-name">)'
        else:
            card_re = rf'(<div class="card"[^>]*data-email="{re.escape(email)}"[^>]*>.*?<span class="card-name">)'
        if 'href="/cv/' in re.search(card_re, text, re.S).group(0) if re.search(card_re, text, re.S) else "":
            continue
        text = re.sub(card_re, rf'\1<a class="card-name" href="/cv/{slug}">', text, count=1, flags=re.S)
        text = re.sub(
            rf'(<a class="card-name" href="/cv/{re.escape(slug)}">[^<]*(?:<span class="cred">[^<]*</span>)?)</span>',
            r"\1</a>",
            text,
            count=1,
            flags=re.S,
        )
        print(f"  profile {path.name}: {slug}")
    path.write_text(text, encoding="utf-8")


for cat in [ROOT / "js/scientists-catalog-data.js", ROOT / "js/scientists-catalog-data-en.js"]:
    link_catalog(cat)
for prof in [ROOT / "az/scientists/profiles.html", ROOT / "en/scientists/profiles.html"]:
    link_profiles(prof)
print("done")
