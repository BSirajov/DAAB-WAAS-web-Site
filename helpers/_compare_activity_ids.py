"""Compare activity article IDs and timeline anchors between AZ and EN."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

ARTICLE_RE = re.compile(r'<article[^>]*\sid="([^"]+)"', re.I)
HREF_RE = re.compile(r'href="#([^"]+)"')


def extract(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    return {
        "articles": ARTICLE_RE.findall(text),
        "timeline_hrefs": HREF_RE.findall(text),
    }


def main() -> int:
    az = extract(ROOT / "az" / "activities.html")
    en = extract(ROOT / "en" / "activities.html")
    print(f"Articles AZ={len(az['articles'])} EN={len(en['articles'])}")
    az_set, en_set = set(az["articles"]), set(en["articles"])
    if az_set != en_set:
        print("Article ID set mismatch:")
        print("  only AZ:", sorted(az_set - en_set))
        print("  only EN:", sorted(en_set - az_set))
    if az["articles"] != en["articles"]:
        print("Article order/content mismatch:")
        for i, (a, e) in enumerate(zip(az["articles"], en["articles"])):
            if a != e:
                print(f"  [{i}] az={a!r} en={e!r}")
        if len(az["articles"]) != len(en["articles"]):
            print(f"  length az={len(az['articles'])} en={len(en['articles'])}")
    else:
        print("Article IDs match (order + values)")

    tl_az, tl_en = set(az["timeline_hrefs"]), set(en["timeline_hrefs"])
    if tl_az != tl_en:
        print("Timeline href mismatch:")
        print("  only AZ:", sorted(tl_az - tl_en))
        print("  only EN:", sorted(tl_en - tl_az))
    else:
        print(f"Timeline anchors OK ({len(tl_az)} links)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
