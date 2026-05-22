"""Fix url fields left as broken strings after Google Sites URL removal."""
import re
from pathlib import Path

from _paths import ROOT

# Prefer _sync_list_view_data.py for list HTML after catalog JS changes.
for name in ("js/scientists-catalog-data.js",):
    path = ROOT / name
    text = path.read_text(encoding="utf-8")
    text = re.sub(r'"url":\s*"\s*\n', '"url": ""\n', text)
    path.write_text(text, encoding="utf-8", newline="")
    print("fixed", name)
