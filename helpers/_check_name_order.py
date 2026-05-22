import json
import re
from pathlib import Path

from _paths import ROOT


def norm(s: str) -> str:
    s = s.upper().strip()
    s = re.sub(r"\s+", " ", s)
    for a, b in [("İ", "I"), ("Ə", "E"), ("Ş", "S"), ("Ç", "C"), ("Ğ", "G"), ("Ö", "O"), ("Ü", "U")]:
        s = s.replace(a, b)
    return s


az = (ROOT / "scientists_list_view_az.html").read_text(encoding="utf-8")
data = json.loads(re.search(r"const DATA = (\[.*?\]);", az, re.S).group(1))
cv = (ROOT / "scientists_card_view_az.html").read_text(encoding="utf-8")
raw = re.findall(r'class="card-name">([^<]+)', cv)
names = [norm(re.sub(r"<span.*", "", n)) for n in raw]
data_names = [norm(r["ad_soyad"]) for r in data]
mism = [
    (i + 1, names[i], data_names[i])
    for i in range(min(len(names), len(data_names)))
    if names[i] != data_names[i]
]
print("cards", len(names), "data", len(data_names), "mismatches", len(mism))
for x in mism[:20]:
    print(x)
