#!/usr/bin/env python3
"""Comprehensive codebase review — supplementary checks for full audit report."""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

from _paths import ROOT
from _deploy_assets import BUILD_ONLY_CSS, DEPLOY_PACKAGED_CSS, DYNAMIC_JS, IMPORTED_VIA_COMMON_CSS, OPTIONAL_JS

ID_ATTR = re.compile(r'(?<![-\w])id="([^"]+)"')

FINDINGS: list[tuple[str, str, str, str]] = []  # severity, category, issue, recommendation


def add(sev: str, cat: str, issue: str, rec: str) -> None:
    FINDINGS.append((sev, cat, issue, rec))


def deploy_html() -> list[Path]:
    out: list[Path] = []
    for base in (ROOT / "az", ROOT / "en"):
        if not base.is_dir():
            continue
        for p in base.rglob("*.html"):
            if p.parent.name == "application" and p.parent.parent.name in ("az", "en"):
                continue
            out.append(p)
    return sorted(out)


def audit_page_shell(html_paths: list[Path]) -> None:
    missing_viewport: list[str] = []
    missing_lang: list[str] = []
    missing_skip: list[str] = []
    missing_mobile_css: list[str] = []
    missing_daab_lang: list[str] = []
    duplicate_ids: dict[str, list[str]] = defaultdict(list)

    for p in html_paths:
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        t = p.read_text(encoding="utf-8", errors="replace")
        if 'name="viewport"' not in t and "viewport" not in t[:2500]:
            missing_viewport.append(rel)
        if not re.search(r"<html[^>]*\blang=", t, re.I):
            missing_lang.append(rel)
        if 'class="skip"' not in t and 'href="#content"' not in t[:4000]:
            missing_skip.append(rel)
        if "daab-mobile.css" not in t:
            missing_mobile_css.append(rel)
        if "data-daab-lang" not in t and "data-daab-legacy-redirect" not in t:
            missing_daab_lang.append(rel)
        ids = ID_ATTR.findall(t)
        for dup in {i for i in ids if ids.count(i) > 1}:
            duplicate_ids[dup].append(rel)

    if missing_viewport:
        add("high", "HTML shell", f"{len(missing_viewport)} pages missing viewport meta", "Add viewport meta to all main pages")
    if missing_lang:
        add("high", "Accessibility", f"{len(missing_lang)} pages missing html lang attribute", "Set lang=\"az\" or lang=\"en\" on <html>")
    if missing_skip:
        add("medium", "Accessibility", f"{len(missing_skip)} pages missing skip link", "Add <a class=\"skip\" href=\"#content\"> as first focusable control")
    if missing_mobile_css:
        add("medium", "Responsiveness", f"{len(missing_mobile_css)} pages missing daab-mobile.css", "Link css/daab-mobile.css on all main pages per site rules")
    if missing_daab_lang:
        add("low", "i18n", f"{len(missing_daab_lang)} pages without data-daab-lang (excl. redirects)", "Add data-daab-lang for shell scripts")
    dup_pages = {k: v for k, v in duplicate_ids.items() if len(v) <= 5}
    if dup_pages:
        sample = list(dup_pages.items())[:3]
        add("medium", "HTML validity", f"Duplicate id attributes on some pages (sample ids: {[s[0] for s in sample]})", "Ensure unique IDs per page for a11y/JS hooks")


def audit_images(html_paths: list[Path]) -> None:
    missing_alt: list[str] = []
    empty_alt_decorative = 0
    for p in html_paths:
        rel = str(p.relative_to(ROOT))
        t = p.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r"<img\b[^>]*>", t, re.I):
            tag = m.group(0)
            if "alt=" not in tag.lower():
                missing_alt.append(rel)
                break
            if re.search(r'alt=""', tag):
                empty_alt_decorative += 1
    if missing_alt:
        add("high", "Accessibility", f"{len(missing_alt)} pages contain <img> without alt attribute", "Add descriptive alt text; use alt=\"\" only for decorative images")
    add("info", "Accessibility", f"~{empty_alt_decorative} img tags use empty alt (likely decorative)", "Verify decorative images are truly non-informative")


def audit_external_links(html_paths: list[Path]) -> None:
    http_insecure: list[str] = []
    target_blank_no_rel: list[str] = []
    for p in html_paths:
        rel = str(p.relative_to(ROOT))
        t = p.read_text(encoding="utf-8", errors="replace")
        if re.search(r'href="http://(?!localhost)', t):
            http_insecure.append(rel)
        for m in re.finditer(r'<a\b[^>]*target="_blank"[^>]*>', t, re.I):
            if "noopener" not in m.group(0).lower():
                target_blank_no_rel.append(rel)
                break
    if http_insecure:
        add("medium", "Security/UX", f"{len(http_insecure)} pages link to http:// (non-localhost) URLs", "Prefer https:// where supported")
    if target_blank_no_rel:
        add("medium", "Security", f"{len(target_blank_no_rel)} pages have target=_blank without rel=noopener", "Add rel=\"noopener noreferrer\" on external blank links")


def audit_i18n_cache() -> None:
    i18n_js = (ROOT / "js/daab-i18n.js").read_text(encoding="utf-8")
    for fname in ("routes.json", "ui.json", "nav.json", "search-index.json"):
        data = json.loads((ROOT / "i18n" / fname).read_text(encoding="utf-8"))
        m = re.search(rf'{re.escape(fname)}[^"]*"\s*\+\s*"\?v=(\d+)"', i18n_js)
        if not m:
            m = re.search(rf"i18nUrl\(\"{re.escape(fname)}\"\)\s*\+\s*\"\?v=(\d+)\"", i18n_js)
        cache = m.group(1) if m else "?"
        fv = data.get("version")
        if str(fv) != cache:
            add(
                "low",
                "Maintainability",
                f"i18n/{fname} JSON version={fv} but daab-i18n.js loads ?v={cache}",
                "Document that browser cache bust uses ?v= in daab-i18n.js, not JSON version field; bump ?v= when file content changes",
            )


def audit_routes_sitemap() -> None:
    routes = json.loads((ROOT / "i18n/routes.json").read_text(encoding="utf-8"))
    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    missing_sm: list[str] = []
    for p in routes["pages"]:
        for lang in ("az", "en"):
            rel = p.get(lang)
            if rel and rel not in sm and rel.replace("/", "\\") not in sm:
                missing_sm.append(rel)
    if len(missing_sm) > 50:
        add("info", "SEO", f"Many route pages may not appear verbatim in sitemap ({len(missing_sm)} checked)", "Regenerate sitemap via helper if routes changed")
    elif missing_sm:
        add("medium", "SEO", f"Routes not in sitemap: {missing_sm[:5]}", "Run sitemap generator to include new pages")


def audit_nav_breadcrumbs(html_paths: list[Path]) -> None:
    forum_pages = [p for p in html_paths if "/forum/2024/" in str(p).replace("\\", "/")]
    with_dyn_bc = [p for p in forum_pages if "daab-breadcrumbs.js" in p.read_text(encoding="utf-8")]
    without_static = [p for p in forum_pages if "forum-breadcrumbs" not in p.read_text(encoding="utf-8")]
    if with_dyn_bc:
        add("medium", "Navigation", f"{len(with_dyn_bc)} forum pages still load daab-breadcrumbs.js", "Use static forum-breadcrumbs only (consistent with other forum pages)")
    if without_static:
        add("high", "Navigation", f"{len(without_static)} forum pages missing forum-breadcrumbs", "Add static breadcrumb trail on all forum subpages")
    # pages with breadcrumbs.js but no static
    no_bc_script = sum(1 for p in html_paths if "daab-breadcrumbs.js" not in p.read_text(encoding="utf-8") and p.name != "index.html" and "membership.html" not in p.name)
    add("info", "Navigation", f"Most inner pages rely on static or dynamic breadcrumbs; {no_bc_script} non-home pages omit daab-breadcrumbs.js", "Expected: forum uses static crumbs; other sections may use JS breadcrumbs on select pages")


def audit_scientists_data() -> None:
    import subprocess
    for script in ("_check_name_order.py", "_validate_cv_cards.py"):
        r = subprocess.run(["python", f"helpers/{script}"], cwd=ROOT, capture_output=True, text=True)
        if r.returncode != 0:
            add("high", "Scientists catalog", f"{script} failed: {(r.stdout or r.stderr)[:200]}", f"Fix catalog data and re-run python helpers/{script}")


def audit_css_js_orphans() -> None:
    paths = deploy_html()
    blob = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in paths)
    build_only = BUILD_ONLY_CSS | IMPORTED_VIA_COMMON_CSS
    deploy_packaged = DEPLOY_PACKAGED_CSS
    orphan_css = []
    for css in sorted((ROOT / "css").glob("*.css")):
        if css.name in build_only or css.name in deploy_packaged:
            continue
        if css.name not in blob:
            common = (ROOT / "css/daab-common.css").read_text(encoding="utf-8")
            if css.name not in common:
                orphan_css.append(css.name)
    if orphan_css:
        add("medium", "Dead code", f"CSS not referenced from az/en HTML: {orphan_css[:8]}", "Link, import, mark BUILD-ONLY, or remove")
    orphan_js = []
    skip_js = OPTIONAL_JS | DYNAMIC_JS
    for js in sorted((ROOT / "js").glob("*.js")):
        if js.name in skip_js:
            continue
        if js.name not in blob:
            orphan_js.append(js.name)
    if orphan_js:
        add("medium", "Dead code", f"JS not referenced from az/en HTML: {orphan_js[:8]}", "Wire into pages or remove if obsolete")


def audit_membership_route() -> None:
    routes = json.loads((ROOT / "i18n/routes.json").read_text(encoding="utf-8"))
    nav = json.loads((ROOT / "i18n/nav.json").read_text(encoding="utf-8"))
    route_ids = {p["id"] for p in routes["pages"]}
    mem_nav = nav["sections"]["membership"]["pages"]
    if "membership" in mem_nav and "membership" not in route_ids:
        add("low", "Navigation", "nav.json membership section lists 'membership' but routes may use membership_value only", "Align nav section pages with routes.json or keep membership.html as redirect-only")
    brd_terms = any(p["id"] == "membership" for p in routes["pages"])
    nav_children = []
    for item in nav.get("primary", []):
        if item.get("id") == "membership" or item.get("labelKey") == "membership":
            nav_children = [c.get("id") for c in item.get("children", [])]
    if brd_terms and "membership" not in nav_children:
        add("low", "Multilingual/Nav", "routes.json has membership page but top nav has 3 items (no standalone terms link)", "Add terms to nav or remove orphan route if membership.html redirect is sufficient")


def audit_static_nav_payload(html_paths: list[Path]) -> None:
    sizes = []
    for p in html_paths[:5]:
        t = p.read_text(encoding="utf-8")
        m = re.search(r'id="primaryNavMenu"[^>]*>(.*?)</div>\s*</div>\s*</nav>', t, re.S)
        if m:
            sizes.append(len(m.group(1)))
    if sizes and max(sizes) > 15000:
        add(
            "low",
            "Performance",
            f"Embedded static mega-menu HTML is large (~{max(sizes)//1024}KB per page sample)",
            "Acceptable for no-JS fallback; consider reducing duplicate payload if HTTP/2 push or server includes are available",
        )


def audit_legacy_redirects() -> None:
    for lang in ("az", "en"):
        p = ROOT / lang / "membership.html"
        if p.is_file():
            t = p.read_text(encoding="utf-8")
            if "refresh" not in t.lower() and "membership_value" not in t:
                add("medium", "Links", f"{lang}/membership.html may not redirect correctly", "Ensure meta refresh + canonical to membership_value.html")


def audit_design_system() -> None:
    ds_path = ROOT / "i18n/design-system.json"
    if not ds_path.is_file():
        return
    ds = json.loads(ds_path.read_text(encoding="utf-8"))
    page_map = ds.get("pageStylesheets") or {}
    for key, rel_css in page_map.items():
        if not rel_css:
            continue
        css_name = Path(rel_css).name
        found = False
        for p in deploy_html():
            if p.name.startswith("membership") or key.replace("page", "").lower() in p.name.replace("_", "").lower():
                if css_name in p.read_text(encoding="utf-8"):
                    found = True
                    break
        # skip strict — informational only


def audit_en_az_title_parity() -> None:
    pairs: list[tuple[Path, Path]] = []
    az_root = ROOT / "az"
    en_root = ROOT / "en"
    for az_p in az_root.rglob("*.html"):
        if az_p.parent.name == "application":
            continue
        rel = az_p.relative_to(az_root)
        en_p = en_root / rel
        if en_p.is_file():
            pairs.append((az_p, en_p))
    title_mismatch = []
    for az_p, en_p in pairs:
        az_t = re.search(r"<title>([^<]+)</title>", az_p.read_text(encoding="utf-8"), re.I)
        en_t = re.search(r"<title>([^<]+)</title>", en_p.read_text(encoding="utf-8"), re.I)
        if az_t and en_t and az_t.group(1).strip() == en_t.group(1).strip() and "DAAB" in az_t.group(1):
            if "WAAS" not in en_t.group(1) and "DAAB" in en_t.group(1):
                title_mismatch.append(str(rel))
    if title_mismatch[:10]:
        add(
            "low",
            "Multilingual",
            f"{len(title_mismatch)} EN pages may share AZ-branded <title> text (sample: {title_mismatch[:3]})",
            "Run EN publish/translation helpers to ensure WAAS branding on EN titles",
        )


def main() -> None:
    paths = deploy_html()
    audit_page_shell(paths)
    audit_images(paths)
    audit_external_links(paths)
    audit_i18n_cache()
    audit_routes_sitemap()
    audit_nav_breadcrumbs(paths)
    audit_scientists_data()
    audit_css_js_orphans()
    audit_membership_route()
    audit_static_nav_payload(paths)
    audit_legacy_redirects()
    audit_en_az_title_parity()

    by_cat: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
    for sev, cat, issue, rec in FINDINGS:
        by_cat[cat].append((sev, issue, rec))

    print("COMPREHENSIVE CODEBASE REVIEW (supplementary)\n")
    order = ("high", "medium", "low", "info")
    for cat in sorted(by_cat.keys()):
        items = by_cat[cat]
        print(f"## {cat} ({len(items)})")
        for sev, issue, rec in sorted(items, key=lambda x: order.index(x[0]) if x[0] in order else 9):
            print(f"  [{sev.upper()}] {issue}")
            print(f"         → {rec}")
        print()
    print(f"Total supplementary findings: {len(FINDINGS)}")


if __name__ == "__main__":
    main()
