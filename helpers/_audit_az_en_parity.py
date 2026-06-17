#!/usr/bin/env python3
"""Compare AZ/EN page pairs for structural and content parity issues."""
from __future__ import annotations

import json
import re
import sys
from html import unescape
from pathlib import Path

from _paths import ROOT

ROUTES_PATH = ROOT / "i18n" / "routes.json"
SUBTITLES_PATH = ROOT / "i18n" / "page-subtitles.json"
ANCHOR_ALIASES_PATH = ROOT / "i18n" / "anchor-aliases.json"

# Lang-specific asset pairs (AZ vs EN) — compare by canonical key, not filename.
JS_EQUIV: dict[str, str] = {
    "scientists-catalog-data-en.js": "scientists-catalog-data.js",
}

# AZ/EN pages that intentionally use different image files (e.g. localized covers).
KNOWN_IMAGE_PAIR_DIFFS: dict[str, tuple[frozenset[str], frozenset[str]]] = {
    "activities-news": (
        frozenset({"072-garuslu-azerbaycanda-kimlik-cover.jpg"}),
        frozenset({"071-garuslu-azerbaijan-north-south-cover.jpg"}),
    ),
}


def canonical_js_versions(js_versions: list[tuple[str, str]]) -> dict[str, str]:
    out: dict[str, str] = {}
    for name, ver in js_versions:
        key = JS_EQUIV.get(name, name)
        out[key] = ver
    return out


def norm_ws(text: str) -> str:
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", text))).strip()


def extract_metrics(html: str) -> dict:
    page_id_m = re.search(r'data-daab-page-id="([^"]+)"', html)
    img_srcs = sorted(set(re.findall(r'(?:src|href)="([^"]*images/[^"]+)"', html)))
    return {
        "page_id": page_id_m.group(1) if page_id_m else None,
        "articles": len(re.findall(r"<article\b", html, re.I)),
        "sections": len(re.findall(r"<section\b", html, re.I)),
        "h2": len(re.findall(r"<h2\b", html, re.I)),
        "h3": len(re.findall(r"<h3\b", html, re.I)),
        "news_cards": len(re.findall(r'class="[^"]*news-card', html)),
        "form_inputs": len(re.findall(r"<(?:input|select|textarea)\b", html, re.I)),
        "img_basenames": sorted(Path(p.split("?")[0]).name for p in img_srcs),
        "section_ids": re.findall(r'<section[^>]*\sid="([^"]+)"', html, re.I),
        "article_ids": re.findall(r'<article[^>]*\sid="([^"]+)"', html, re.I),
        "tier_cards": len(re.findall(r'class="[^"]*tier-card', html)),
        "css_versions": sorted(set(re.findall(r"/css/([a-z0-9_-]+\.css)\?v=(\d+)", html, re.I))),
        "js_versions": sorted(set(re.findall(r"/js/([a-z0-9_-]+\.js)\?v=(\d+)", html, re.I))),
        "has_breadcrumbs_js": "daab-breadcrumbs.js" in html,
        "has_static_bc": "forum-breadcrumbs" in html or "daab-breadcrumbs" in html,
        "section_eyebrows": [
            norm_ws(x)
            for x in re.findall(r'section-eyebrow[^>]*>(.*?)<', html, re.S)
        ],
    }


def main() -> int:
    routes = json.loads(ROUTES_PATH.read_text(encoding="utf-8"))
    subtitles = json.loads(SUBTITLES_PATH.read_text(encoding="utf-8"))
    anchor_aliases = {}
    if ANCHOR_ALIASES_PATH.is_file():
        anchor_data = json.loads(ANCHOR_ALIASES_PATH.read_text(encoding="utf-8"))
        for page_key, page_map in anchor_data.get("pages", {}).items():
            az_to_en = page_map.get("az_to_en", {})
            anchor_aliases[page_key] = az_to_en

    issues: list[str] = []
    warnings: list[str] = []
    info: list[str] = []

    for page in routes["pages"]:
        pid = page["id"]
        az_path = ROOT / page["az"]
        en_path = ROOT / page["en"]
        if not az_path.is_file() or not en_path.is_file():
            issues.append(f"{pid}: missing file az={az_path.is_file()} en={en_path.is_file()}")
            continue

        az_html = az_path.read_text(encoding="utf-8")
        en_html = en_path.read_text(encoding="utf-8")
        az_m = extract_metrics(az_html)
        en_m = extract_metrics(en_html)

        if az_m["page_id"] != en_m["page_id"]:
            issues.append(f"{pid}: page-id mismatch az={az_m['page_id']} en={en_m['page_id']}")

        for key in (
            "articles",
            "sections",
            "h2",
            "h3",
            "news_cards",
            "form_inputs",
            "tier_cards",
        ):
            if az_m[key] != en_m[key]:
                warnings.append(f"{pid}: {key} count az={az_m[key]} en={en_m[key]}")

        if az_m["img_basenames"] != en_m["img_basenames"]:
            az_only = sorted(set(az_m["img_basenames"]) - set(en_m["img_basenames"]))
            en_only = sorted(set(en_m["img_basenames"]) - set(az_m["img_basenames"]))
            known = KNOWN_IMAGE_PAIR_DIFFS.get(pid)
            if known and frozenset(az_only) == known[0] and frozenset(en_only) == known[1]:
                pass
            elif az_only or en_only:
                warnings.append(
                    f"{pid}: image basename mismatch az_only={az_only[:6]} en_only={en_only[:6]}"
                )

        if canonical_js_versions(az_m["js_versions"]) != canonical_js_versions(en_m["js_versions"]):
            az_js = canonical_js_versions(az_m["js_versions"])
            en_js = canonical_js_versions(en_m["js_versions"])
            diff = sorted(set(az_js.items()) ^ set(en_js.items()))
            warnings.append(f"{pid}: JS version mismatch {diff[:4]}")

        if az_m["article_ids"] and en_m["article_ids"]:
            az_set = set(az_m["article_ids"])
            en_set = set(en_m["article_ids"])
            alias_map = anchor_aliases.get(pid, {})
            if alias_map:
                mapped_az = {alias_map.get(aid, aid) for aid in az_set}
                if mapped_az == en_set:
                    if az_m["article_ids"] != en_m["article_ids"]:
                        info.append(f"{pid}: article id order differs (alias-mapped set matches)")
                elif az_set != en_set:
                    warnings.append(f"{pid}: article id sets differ (alias map incomplete)")
            elif az_set != en_set:
                warnings.append(f"{pid}: article id sets differ")
            elif az_m["article_ids"] != en_m["article_ids"]:
                info.append(f"{pid}: article id order differs (same set)")

        if az_m["section_eyebrows"] and en_m["section_eyebrows"]:
            if len(az_m["section_eyebrows"]) != len(en_m["section_eyebrows"]):
                warnings.append(
                    f"{pid}: section eyebrow count az={len(az_m['section_eyebrows'])} "
                    f"en={len(en_m['section_eyebrows'])}"
                )

        css_diff = set(az_m["css_versions"]).symmetric_difference(set(en_m["css_versions"]))
        if css_diff:
            warnings.append(f"{pid}: CSS version mismatch {sorted(css_diff)[:4]}")

        if az_m["has_breadcrumbs_js"] != en_m["has_breadcrumbs_js"]:
            warnings.append(
                f"{pid}: breadcrumbs JS az={az_m['has_breadcrumbs_js']} en={en_m['has_breadcrumbs_js']}"
            )
        if az_m["has_static_bc"] != en_m["has_static_bc"]:
            warnings.append(
                f"{pid}: static breadcrumbs az={az_m['has_static_bc']} en={en_m['has_static_bc']}"
            )

        ps = subtitles.get("pages", {}).get(pid)
        if not ps:
            warnings.append(f"page-subtitles.json: missing entry for {pid}")
        elif "az" not in ps or "en" not in ps:
            warnings.append(f"page-subtitles.json: incomplete for {pid}")

        if pid == "scientists-profiles":
            az_cards = len(re.findall(r'<div class="card" id="', az_html))
            en_cards = len(re.findall(r'<div class="card" id="', en_html))
            if az_cards != en_cards:
                issues.append(f"scientists-profiles: card count az={az_cards} en={en_cards}")

        if pid == "membership-application":
            az_form = sorted(
                set(
                    re.findall(
                        r'(?:input|select|textarea)[^>]*id="([^"]+)"',
                        az_html,
                        re.I,
                    )
                )
            )
            en_form = sorted(
                set(
                    re.findall(
                        r'(?:input|select|textarea)[^>]*id="([^"]+)"',
                        en_html,
                        re.I,
                    )
                )
            )
            if az_form != en_form:
                issues.append("membership-application: form field ids differ")

    routed = {page[lang].replace("\\", "/") for page in routes["pages"] for lang in ("az", "en")}
    legacy = {"az/membership.html", "en/membership.html"}
    for lang in ("az", "en"):
        for path in (ROOT / lang).rglob("*.html"):
            rel = path.relative_to(ROOT).as_posix()
            if rel not in routed and rel not in legacy and path.stat().st_size > 500:
                info.append(f"HTML not in routes.json: {rel}")

    en_leaks = ("Join our Association", "Board of Directors", "Translation in progress")
    az_leaks = ("klikləyin", "Təsisat")
    for page in routes["pages"]:
        for lang, rel in (("az", page["az"]), ("en", page["en"])):
            path = ROOT / rel
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            if lang == "az":
                for phrase in en_leaks:
                    if phrase in text:
                        warnings.append(f'{rel}: English phrase leak "{phrase}"')
            else:
                for phrase in az_leaks:
                    if phrase in text:
                        warnings.append(f'{rel}: AZ phrase leak "{phrase}"')

    # Forum TOC/article parity on key long pages
    for pid in (
        "forum-impressions",
        "forum-2024-presentations",
        "forum-rector-speeches",
        "forum-anas-leadership-speeches",
        "forum-official",
    ):
        page = next(p for p in routes["pages"] if p["id"] == pid)
        az_n = len(
            re.findall(
                r"<article[^>]*class=\"[^\"]*news-card",
                (ROOT / page["az"]).read_text(encoding="utf-8"),
            )
        )
        en_n = len(
            re.findall(
                r"<article[^>]*class=\"[^\"]*news-card",
                (ROOT / page["en"]).read_text(encoding="utf-8"),
            )
        )
        if az_n != en_n:
            warnings.append(f"{pid}: news-card count az={az_n} en={en_n}")

    print(f"AZ/EN parity audit — {len(routes['pages'])} page pairs\n")
    print(f"ISSUES ({len(issues)})")
    for item in issues:
        print(f"  - {item}")
    print(f"\nWARNINGS ({len(warnings)})")
    for item in warnings:
        print(f"  - {item}")
    print(f"\nINFO ({len(info)})")
    for item in info[:20]:
        print(f"  - {item}")
    if len(info) > 20:
        print(f"  … and {len(info) - 20} more")

    # Footer language leaks
    az_en_footer = 0
    en_az_footer = 0
    for page in routes["pages"]:
        az_path = ROOT / page["az"]
        en_path = ROOT / page["en"]
        if az_path.is_file() and "All Rights Reserved" in az_path.read_text(encoding="utf-8"):
            az_en_footer += 1
        if en_path.is_file() and "Bütün hüquqlar" in en_path.read_text(encoding="utf-8"):
            en_az_footer += 1
    print(f"\nFOOTER LANGUAGE")
    print(f"  AZ pages with English footer text: {az_en_footer}")
    print(f"  EN pages with Azerbaijani footer text: {en_az_footer}")

    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
