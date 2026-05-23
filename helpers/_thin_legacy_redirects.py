"""Replace root legacy *_az.html stubs with thin redirects to az/ canonical pages."""
from __future__ import annotations

import json

from _paths import ROOT

ROUTES = ROOT / "i18n" / "routes.json"

TEMPLATE = """<!DOCTYPE html>
<html lang="az">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
<meta http-equiv="refresh" content="0; url={target}"/>
<link rel="canonical" href="{target}"/>
<title>DAAB — yönləndirmə</title>
<!-- data-daab-legacy-redirect -->
<script>location.replace("{target}");</script>
</head>
<body>
<p>Səhifə köçürülüb. <a href="{target}">Davam et</a></p>
</body>
</html>
"""


def main() -> None:
    data = json.loads(ROUTES.read_text(encoding="utf-8"))
    redirects = data.get("legacyRedirects", {})
    for legacy_name, target in redirects.items():
        if legacy_name == "index.html":
            continue
        path = ROOT / legacy_name
        if not path.exists():
            print(f"skip missing {legacy_name}")
            continue
        path.write_text(TEMPLATE.format(target=target), encoding="utf-8", newline="\n")
        print(f"thinned {legacy_name} -> {target}")


if __name__ == "__main__":
    main()
