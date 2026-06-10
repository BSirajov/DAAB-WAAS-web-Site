#!/usr/bin/env python3
"""Apply P1/P2 fixes from comprehensive codebase review (June 2026)."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT
from _site_wide_cleanup import SCRIPT_VERSIONS, STYLE_VERSIONS, bump_asset_versions

TARGET_BLANK_RE = re.compile(
    r'(<a\b(?![^>]*\brel=)[^>]*\btarget="_blank")',
    re.IGNORECASE,
)


def iter_live_html() -> list[Path]:
    paths: list[Path] = []
    gateway = ROOT / "index.html"
    if gateway.is_file():
        paths.append(gateway)
    for base in (ROOT / "az", ROOT / "en"):
        if not base.is_dir():
            continue
        for path in base.rglob("*.html"):
            if path.parent.name == "application" and path.parent.parent.name in ("az", "en"):
                continue
            paths.append(path)
    return sorted(paths)


def add_noopener(html: str) -> str:
    def repl(match: re.Match[str]) -> str:
        tag_start = match.group(1)
        return tag_start + ' rel="noopener noreferrer"'

    return TARGET_BLANK_RE.sub(repl, html)


def fix_activities_https(html: str) -> str:
    return html.replace('href="http://bsu.edu.az/', 'href="https://bsu.edu.az/')


def fix_gateway_versions(html: str) -> str:
    return bump_asset_versions(html)


def fix_application_success(path: Path, html: str) -> str:
    if path.name != "application.html":
        return html
    if path.parent.name == "az":
        old = (
            "      <h2>Müraciətiniz qəbul olundu!</h2>\n"
            "      <p>\n"
            "        DAAB-a üzvlük müraciətiniz uğurla göndərildi. Tezliklə sizinlə əlaqə saxlanılacaq.<br><br>\n"
            "      </p>"
        )
        new = (
            "      <h2>Müraciətiniz qeydə alındı</h2>\n"
            "      <p>\n"
            "        Form məlumatlarınız brauzerinizdə yoxlanılıb. Hazırda müraciət avtomatik serverə ötürülmür — "
            "zəhmət olmasa müraciətinizi tamamlamaq üçün foto və CV-nizi "
            "<a href=\"mailto:info@daab-waas.com\">info@daab-waas.com</a> ünvanına göndərin.<br><br>\n"
            "        Mövzu sətirində <em>«DAAB üzvlük — [Ad Soyad]»</em> yazın. Tezliklə sizinlə əlaqə saxlanılacaq.\n"
            "      </p>"
        )
    else:
        old = (
            "      <h2>Application Submitted Successfully!</h2>\n"
            "      <p>\n"
            "        Thank you for applying to join the World Association of Azerbaijani Scientists (WAAS).\n"
            "        Your application has been received and we will be in touch with you shortly.<br><br>\n"
            "        Please remember to send your <strong>photo and CV</strong> to\n"
            "        <a href=\"mailto:info@daab-waas.com\" style=\"color:var(--blue-700);\">info@daab-waas.com</a>.\n"
            "      </p>"
        )
        new = (
            "      <h2>Application recorded locally</h2>\n"
            "      <p>\n"
            "        Thank you for completing the WAAS membership form. Your answers were validated in the browser.\n"
            "        Applications are <strong>not sent to our server automatically yet</strong> — please email your\n"
            "        <strong>photo and CV</strong> to\n"
            "        <a href=\"mailto:info@daab-waas.com\" style=\"color:var(--blue-700);\">info@daab-waas.com</a>\n"
            "        to complete your submission.<br><br>\n"
            "        Use the subject line <em>\"WAAS Membership — [Your Full Name]\"</em>. We will contact you shortly.\n"
            "      </p>"
        )
    if old not in html:
        return html
    return html.replace(old, new, 1)


def main() -> None:
    updated: list[str] = []
    for path in iter_live_html():
        text = path.read_text(encoding="utf-8")
        original = text
        text = add_noopener(text)
        if path.name == "activities.html":
            text = fix_activities_https(text)
        if path == ROOT / "index.html":
            text = fix_gateway_versions(text)
        text = fix_application_success(path, text)
        if text != original:
            path.write_text(text, encoding="utf-8", newline="\n")
            updated.append(str(path.relative_to(ROOT)))
    print(f"Updated {len(updated)} file(s):")
    for rel in updated:
        print(f"  - {rel}")
    if not updated:
        print("  (no changes needed)")


if __name__ == "__main__":
    main()
