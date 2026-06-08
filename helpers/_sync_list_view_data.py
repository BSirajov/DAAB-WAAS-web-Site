"""Rebuild inline DATA in az/scientists/list.html from js/scientists-catalog-data.js."""
import json
import re
from pathlib import Path

from _paths import ROOT, AZ_SCIENTISTS_LIST

DATA_JS = ROOT / "js" / "scientists-catalog-data.js"
LIST_HTML = AZ_SCIENTISTS_LIST
MARKER = "// ── Azerbaijani alphabet sort ──"


def load_catalog():
    text = DATA_JS.read_text(encoding="utf-8")
    m = re.search(r"=\s*(\[.*\])\s*;", text, re.DOTALL)
    if not m:
        raise SystemExit("Could not parse scientists-catalog-data.js array")
    return json.loads(m.group(1))


def main():
    data = load_catalog()
    inline = json.dumps(data, ensure_ascii=False, separators=(", ", ": "))
    html = LIST_HTML.read_text(encoding="utf-8")
    pattern = re.compile(
        r"const DATA = \[.*?\n" + re.escape(MARKER),
        re.DOTALL,
    )
    if not pattern.search(html):
        raise SystemExit("Could not find const DATA block in list view HTML")
    new_html = pattern.sub(f"const DATA = {inline};\n{MARKER}", html, count=1)
    LIST_HTML.write_text(new_html, encoding="utf-8", newline="")
    print(f"Synced {len(data)} records into {LIST_HTML.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
