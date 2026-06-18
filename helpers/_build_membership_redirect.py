"""Maintain az/en membership.html legacy redirect stubs (noindex + canonical to membership_value)."""
from __future__ import annotations

from _paths import ROOT

PAGES = {
    ROOT / "az" / "membership.html": {
        "lang": "az",
        "title": "DAAB — Üzvlük",
        "site": "DAAB",
        "canonical": "https://daab-waas.com/az/membership_value.html",
        "skip": "Məzmuna keç",
        "link": "Üzvlük səhifəsinə keçid",
        "locale": "az_AZ",
        "locale_alt": "en_US",
    },
    ROOT / "en" / "membership.html": {
        "lang": "en",
        "title": "WAAS — Membership",
        "site": "WAAS",
        "canonical": "https://daab-waas.com/en/membership_value.html",
        "skip": "Skip to content",
        "link": "Continue to membership page",
        "locale": "en_US",
        "locale_alt": "az_AZ",
    },
}


def page_html(cfg: dict) -> str:
    return f"""<!DOCTYPE html>
<html lang="{cfg["lang"]}" data-daab-legacy-redirect="1">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
<meta name="robots" content="noindex, follow"/>
<meta http-equiv="refresh" content="0; url=membership_value.html"/>
<link href="../css/daab-mobile.css?v=13" rel="stylesheet"/>
<title>{cfg["title"]}</title>
<!-- daab-seo -->
<link rel="icon" href="../images/daab-logo.png" type="image/png"/>
<link rel="canonical" href="{cfg["canonical"]}"/>
<meta property="og:type" content="website"/>
<meta property="og:site_name" content="{cfg["site"]}"/>
<meta property="og:title" content="{cfg["title"]}"/>
<meta property="og:url" content="{cfg["canonical"]}"/>
<meta property="og:locale" content="{cfg["locale"]}"/>
<meta property="og:locale:alternate" content="{cfg["locale_alt"]}"/>
<meta name="twitter:card" content="summary"/>
<meta name="twitter:title" content="{cfg["title"]}"/>
<!-- /daab-seo -->
</head>
<body>
<a class="skip" href="#content">{cfg["skip"]}</a>
<p id="content"><a href="membership_value.html">{cfg["link"]}</a></p>
</body>
</html>
"""


def main() -> int:
    for path, cfg in PAGES.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(page_html(cfg), encoding="utf-8", newline="\n")
        print(f"Wrote {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
