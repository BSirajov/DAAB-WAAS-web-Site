import importlib.util
import re

from _paths import AZ_SCIENTISTS_PROFILES, HELPERS, ROOT

_spec = importlib.util.spec_from_file_location(
    "build_cv_enrichment", HELPERS / "_build_cv_enrichment.py"
)
_enrich = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_enrich)
norm = _enrich.norm
card_display_name = _enrich.card_display_name

cv = AZ_SCIENTISTS_PROFILES.read_text(encoding="utf-8")
chunks = re.split(r'(?=<div class="card")', cv)[1:]
for chunk in chunks:
    d = card_display_name(chunk)
    if any(x in d for x in ("Barmanbay", "Səbzi", "Gəncəli", "Çaxmaq")):
        print(repr(d), "->", norm(d))
