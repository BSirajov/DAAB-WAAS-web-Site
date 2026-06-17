#!/usr/bin/env python3
"""One-off artifact consistency audit (temporary helper)."""
from __future__ import annotations

import json
import html as html_lib
import re
import sys
from pathlib import Path

from _paths import ROOT
from _deploy_assets import BUILD_ONLY_CSS, DYNAMIC_JS, OPTIONAL_JS

FINDINGS: list[tuple[str, str, str]] = []  # severity, area, message


def add(severity: str, area: str, message: str) -> None:
    FINDINGS.append((severity, area, message))


def audit_routes_nav_ui() -> None:
    routes = json.loads((ROOT / "i18n/routes.json").read_text(encoding="utf-8"))
    nav = json.loads((ROOT / "i18n/nav.json").read_text(encoding="utf-8"))
    ui = json.loads((ROOT / "i18n/ui.json").read_text(encoding="utf-8"))

    for p in routes.get("pages", []):
        for lang in ("az", "en"):
            rel = p.get(lang)
            if rel and not (ROOT / rel).is_file():
                add("error", "routes", f"Missing file for {p['id']} ({lang}): {rel}")

    route_ids = {p["id"] for p in routes["pages"]}
    nav_ids: set[str] = set()

    def collect(items):
        for item in items or []:
            if not isinstance(item, dict):
                continue
            if item.get("id"):
                nav_ids.add(item["id"])
            if item.get("landingId"):
                nav_ids.add(item["landingId"])
            collect(item.get("children"))

    collect(nav.get("primary"))
    for sec in nav.get("sections", {}).values():
        nav_ids.update(sec.get("pages", []))
        if sec.get("landingId"):
            nav_ids.add(sec["landingId"])

    group_ids: set[str] = set()

    def collect_groups(items):
        for item in items or []:
            if not isinstance(item, dict):
                continue
            if item.get("type") == "group" and item.get("id"):
                group_ids.add(item["id"])
            collect_groups(item.get("children"))

    collect_groups(nav.get("primary"))
    for nid in sorted(nav_ids - route_ids - group_ids):
        add("warn", "nav", f"nav.json references unknown route id: {nid}")

    for item in nav.get("primary", []):
        lk = item.get("labelKey")
        if lk:
            for lang in ("az", "en"):
                if lk not in ui.get("nav", {}).get(lang, {}):
                    add("error", "ui", f"Missing ui.nav.{lang}.{lk}")
        if item.get("type") == "group":
            for sec in item.get("children", []):
                sk = sec.get("labelKey")
                if sk:
                    for lang in ("az", "en"):
                        if sk not in ui["nav"][lang]:
                            add("error", "ui", f"Missing ui.nav.{lang}.{sk}")

    i18n_js = (ROOT / "js/daab-i18n.js").read_text(encoding="utf-8")
    m = re.search(r'nav\.json"\)\s*\+\s*"\?v=(\d+)"', i18n_js)
    nav_cache = m.group(1) if m else None
    nav_ver = str(nav.get("version"))
    if nav_cache and nav_ver != nav_cache:
        add(
            "warn",
            "i18n",
            f"nav.json version is {nav_ver} but daab-i18n.js loads nav.json?v={nav_cache}",
        )


def audit_search_index() -> None:
    routes = json.loads((ROOT / "i18n/routes.json").read_text(encoding="utf-8"))
    si = json.loads((ROOT / "i18n/search-index.json").read_text(encoding="utf-8"))
    entries = si.get("entries", si if isinstance(si, list) else [])
    si_ids: set[str] = set()
    for e in entries:
        for k in ("id", "pageId", "navId"):
            if e.get(k):
                si_ids.add(e[k])

    for p in routes["pages"]:
        if p.get("navGroup") and p["id"] not in si_ids:
            add("info", "search", f"Page {p['id']} not in search-index.json")

    for e in entries:
        title = e.get("title")
        if isinstance(title, dict):
            title_en = title.get("en", "")
        else:
            title_en = e.get("titleEn") or (title if isinstance(title, str) else "")
        nav_id = e.get("pageId") or e.get("navId") or ""
        if nav_id in ("membership-value", "membership-application") and title_en:
            if title_en == nav_id or nav_id.replace("-", " ") in title_en.lower():
                if "-" in title_en and title_en.count(" ") < 2:
                    add("warn", "search", f"Raw id in EN search title for {nav_id}: {title_en!r}")


def audit_slim_nav_placeholders() -> None:
    """Live pages must not embed the mega-menu in #primaryNavMenu (runtime builds from nav.json)."""
    from _sync_primary_nav import MINIMAL_NAV_INNER, needs_slim_nav, should_patch

    bloated: list[str] = []
    for path in sorted(ROOT.rglob("*.html")):
        if not should_patch(path):
            continue
        html = path.read_text(encoding="utf-8")
        if needs_slim_nav(html):
            bloated.append(path.relative_to(ROOT).as_posix())
        elif "nav-mega-heading" in html:
            m = re.search(
                r'<div class="nav-menu"[^>]*\bid="primaryNavMenu"[^>]*>(.*?)</div>\s*(?:<div class="nav-actions\b|</div>\s*</nav>)',
                html,
                re.S | re.I,
            )
            if m and "nav-mega-heading" in m.group(1):
                bloated.append(path.relative_to(ROOT).as_posix())
    if bloated:
        add(
            "error",
            "static-nav",
            f"{len(bloated)} page(s) still embed mega-menu in #primaryNavMenu "
            f"(run python helpers/_sync_primary_nav.py). Examples: {bloated[:5]}",
        )
    expected = MINIMAL_NAV_INNER.strip()
    for lang in ("az", "en"):
        page_html = (ROOT / lang / "index.html").read_text(encoding="utf-8")
        m = re.search(
            r'id="primaryNavMenu"[^>]*>(.*?)</div>\s*(?:<div class="nav-actions"|</div>\s*</nav>)',
            page_html,
            re.S | re.I,
        )
        if not m or m.group(1).strip() != expected:
            add(
                "error",
                "static-nav",
                f"{lang}/index.html #primaryNavMenu is not the slim placeholder",
            )


def audit_scientists_list_labels() -> None:
    for lang in ("en", "az"):
        html = (ROOT / lang / "scientists/list.html").read_text(encoding="utf-8")
        th_country = re.search(
            r'data-col="yasadigi_olke"[^>]*>([^<]+(?:<br[^>]*>[^<]+)?)',
            html,
        )
        filter_block = re.search(r'<select id="filterCountry"[^>]*>(.*?)</select>', html, re.S)
        filter_opt = None
        if filter_block:
            filter_opt = re.search(
                r'<option value="">((?:[^<]|<[^/][^>]*>[^<]*)*)</option>',
                filter_block.group(1),
                re.S,
            )
        sort_block = re.search(r'<select id="sortBy"[^>]*>(.*?)</select>', html, re.S)
        sort_country = None
        if sort_block:
            m = re.search(r'value="yasadigi_olke"[^>]*>([^<]+)', sort_block.group(1))
            if m:
                sort_country = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        if lang == "en" and filter_opt and sort_country:
            filter_text = re.sub(r"<[^>]+>", "", filter_opt.group(1)).strip()
            if "Country of residence" in filter_text and sort_country != "Country of residence":
                add(
                    "warn",
                    "scientists-list",
                    f"EN filter says 'Country of residence' but Sort by option still {sort_country!r}",
                )
        if lang == "az" and filter_opt and sort_country and th_country:
            filter_text = re.sub(r"<[^>]+>", "", filter_opt.group(1)).strip()
            th_text = re.sub(r"<[^>]+>", "", th_country.group(1)).strip()
            sort_text = sort_country
            if filter_text != th_text or sort_text != th_text:
                filter_norm = filter_text.lstrip("🌍 ").strip()
                if filter_norm == th_text and sort_text == th_text:
                    continue
                add(
                    "warn",
                    "scientists-list",
                    f"AZ country column naming: filter={filter_text!r} sort={sort_text!r} th={th_text!r}",
                )


def audit_helper_versions() -> None:
    swc = (ROOT / "helpers/_site_wide_cleanup.py").read_text(encoding="utf-8")
    spn = (ROOT / "helpers/_sync_primary_nav.py").read_text(encoding="utf-8")
    for asset in (
        "daab-primary-nav.js",
        "daab-common.css",
        "daab-i18n.js",
        "daab-nav.js",
        "daab-breadcrumbs.js",
        "daab-shell.js",
    ):
        swc_m = re.search(rf'"{asset}":\s*(\d+)', swc)
        spn_m = re.search(rf'"{asset}":\s*(\d+)', spn)
        if swc_m and spn_m and swc_m.group(1) != spn_m.group(1):
            add(
                "warn",
                "helpers",
                f"{asset} version: _site_wide_cleanup={swc_m.group(1)} "
                f"_sync_primary_nav={spn_m.group(1)}",
            )


def audit_orphan_assets() -> None:
    blob = ""
    for base in ("az", "en"):
        for p in (ROOT / base).rglob("*.html"):
            blob += p.read_text(encoding="utf-8", errors="replace") + "\n"
    for css in sorted((ROOT / "css").glob("*.css")):
        name = css.name
        if name in ("daab-tokens.css", "daab-site-background.css"):
            continue
        if name in BUILD_ONLY_CSS:
            add("info", "assets", f"Build-only/unlinked CSS: {name}")
            continue
        if name not in blob and f"@import" not in (ROOT / "css/daab-common.css").read_text():
            if name not in blob:
                # check import in common
                common = (ROOT / "css/daab-common.css").read_text(encoding="utf-8")
                if name not in common and name not in blob:
                    add("warn", "assets", f"CSS not referenced in az/en HTML: {name}")
    js_optional = OPTIONAL_JS | DYNAMIC_JS
    for js in sorted((ROOT / "js").glob("*.js")):
        if js.name in OPTIONAL_JS:
            add("info", "assets", f"Optional/unlinked JS: {js.name}")
        elif js.name in DYNAMIC_JS:
            add("info", "assets", f"Dynamically loaded JS: {js.name}")
        elif js.name not in blob and js.parent.name == "js":
            add("warn", "assets", f"JS not referenced in az/en HTML: {js.name}")


def audit_membership_routes() -> None:
    routes = json.loads((ROOT / "i18n/routes.json").read_text(encoding="utf-8"))
    nav = json.loads((ROOT / "i18n/nav.json").read_text(encoding="utf-8"))
    mem_pages = nav["sections"]["membership"]["pages"]
    if "membership" in mem_pages or any(
        p["id"] == "membership" for p in routes["pages"]
    ):
        add("info", "routes", "Legacy membership.html route may still be referenced")
    # membership terms in nav?
    for item in nav["primary"]:
        if item.get("id") == "membership" or item.get("labelKey") == "membership":
            children = item.get("children", [])
            child_ids = [c.get("id") for c in children if c.get("id")]
            if "membership" not in child_ids and len(children) == 3:
                add(
                    "info",
                    "nav",
                    "Membership nav has 3 items (why, application, flyer) — no standalone terms page",
                )


def audit_design_system() -> None:
    ds = json.loads((ROOT / "i18n/design-system.json").read_text(encoding="utf-8"))
    page_map = ds.get("pageStylesheets") or {}
    checks = [
        ("en/membership_value.html", "pageMembershipValue", "daab-membership-value.css"),
        ("en/membership_flyer.html", "pageMembershipFlyer", "daab-membership-flyer.css"),
        ("en/encyclopedia.html", "pageEncyclopedia", "daab-encyclopedia-page.css"),
    ]
    for rel, key, expected_css in checks:
        path = ROOT / rel
        if not path.is_file():
            continue
        html = path.read_text(encoding="utf-8")
        mapped = page_map.get(key, "")
        if mapped and Path(mapped).name not in html:
            add(
                "warn",
                "design-system",
                f"{rel} missing {Path(mapped).name} from design-system key {key}",
            )
        if expected_css not in html:
            add("info", "design-system", f"{rel} uses css but design-system key {key} maps to {mapped}")


def audit_docs_stale() -> None:
    stale_phrases = [
        "daab-section-nav.js",
        "section pills",
        ".daab-section-nav",
    ]
    skip_docs = {
        "DAAB-Site-Cleanup-Audit-2026-05.md",
        "DAAB-Website-UI-Terminology-Reference.md",
    }
    for doc in (ROOT / "documents").glob("*.md"):
        if doc.name in skip_docs:
            continue
        text = doc.read_text(encoding="utf-8", errors="replace")
        hits = [p for p in stale_phrases if p in text]
        if hits:
            add("info", "docs", f"{doc.name} still mentions removed nav: {hits[:2]}")


def audit_sitemap() -> None:
    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    for lang in ("az", "en"):
        idx = f"{lang}/index.html"
        if idx not in sm and f"/{lang}/" not in sm:
            add("warn", "sitemap", f"May not include {lang} pages")
    if "membership.html" in sm:
        add("info", "sitemap", "sitemap still lists membership.html redirect stubs")


def main() -> None:
    audit_routes_nav_ui()
    audit_search_index()
    audit_slim_nav_placeholders()
    audit_scientists_list_labels()
    audit_helper_versions()
    audit_orphan_assets()
    audit_membership_routes()
    audit_design_system()
    audit_docs_stale()
    audit_sitemap()

    by_sev = {"error": [], "warn": [], "info": []}
    for sev, area, msg in FINDINGS:
        by_sev[sev].append((area, msg))

    print("ARTIFACT CONSISTENCY AUDIT\n")
    for sev in ("error", "warn", "info"):
        items = by_sev[sev]
        print(f"=== {sev.upper()} ({len(items)}) ===")
        for area, msg in items:
            print(f"  [{area}] {msg}")
        print()

    print(f"Total findings: {len(FINDINGS)}")
    return 1 if by_sev["error"] else 0


if __name__ == "__main__":
    sys.exit(main())
