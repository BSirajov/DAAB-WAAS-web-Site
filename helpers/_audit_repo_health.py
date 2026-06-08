#!/usr/bin/env python3
"""Site health audit: broken refs, orphan assets, version drift, duplicate HTML attrs."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

from _paths import ROOT

IMPORTED_VIA_COMMON = frozenset(
    {
        "daab-tokens.css",
        "daab-site-background.css",
    }
)
BUILD_ONLY_CSS = frozenset(
    {
        "daab-forum-book.css",
        "daab-application-embed-az.css",
        "daab-application-embed-en.css",
        "daab-application-membership-value-embed.css",
        "daab-membership-page.css",  # membership.html is a redirect stub; CSS kept for reuse
    }
)
DEPLOY_PACKAGED_CSS = frozenset(
    {
        "daab-sticky-chrome.css",  # optional deploy bundle; not linked per-page
    }
)
OPTIONAL_JS = frozenset(
    {
        "daab-story-tts.js",  # stories TTS — CSS hooks exist; not linked on live pages
    }
)


def collect_deploy_html() -> list[Path]:
    paths: list[Path] = []
    for base in (ROOT / "az", ROOT / "en"):
        if not base.is_dir():
            continue
        for path in base.rglob("*.html"):
            if path.parent.name == "application" and path.parent.parent.name in ("az", "en"):
                continue
            paths.append(path)
    return sorted(paths)


def html_blob(paths: list[Path]) -> str:
    return "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in paths)


def orphan_assets(blob: str) -> tuple[list[str], list[str]]:
    orphan_css: list[str] = []
    orphan_js: list[str] = []
    for css in sorted((ROOT / "css").glob("*.css")):
        name = css.name
        if name in IMPORTED_VIA_COMMON or name in BUILD_ONLY_CSS or name in DEPLOY_PACKAGED_CSS:
            continue
        if name not in blob:
            orphan_css.append(name)
    for js in sorted((ROOT / "js").glob("*.js")):
        name = js.name
        if name in OPTIONAL_JS:
            continue
        if name not in blob:
            orphan_js.append(name)
    return orphan_css, orphan_js


def version_drift(paths: list[Path]) -> dict[str, set[int]]:
    versions: dict[str, set[int]] = {}
    pat = re.compile(r"(daab-[a-z0-9-]+\.(?:css|js)|scientists-[a-z0-9-]+\.(?:css|js))\?v=(\d+)")
    for path in paths:
        for m in pat.finditer(path.read_text(encoding="utf-8", errors="replace")):
            versions.setdefault(m.group(1), set()).add(int(m.group(2)))
    return {k: v for k, v in versions.items() if len(v) > 1}


def duplicate_lang_attrs(paths: list[Path]) -> list[str]:
    bad: list[str] = []
    for path in paths:
        if 'lang="az" lang="az"' in path.read_text(encoding="utf-8", errors="replace"):
            bad.append(str(path.relative_to(ROOT)))
    return bad


def main() -> int:
    paths = collect_deploy_html()
    blob = html_blob(paths)
    orphan_css, orphan_js = orphan_assets(blob)
    drift = version_drift(paths)
    dup_lang = duplicate_lang_attrs(paths)

    print("DAAB repository health audit")
    print(f"  Deploy HTML pages: {len(paths)}")

    validate = subprocess.run(
        [sys.executable, str(ROOT / "helpers" / "_validate_site.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    print(validate.stdout.strip() or validate.stderr.strip())
    if validate.returncode != 0:
        print("  Path validation: FAILED")
    else:
        print("  Path validation: OK")

    if drift:
        print(f"\nAsset ?v= drift ({len(drift)} files with multiple versions):")
        for name in sorted(drift)[:25]:
            print(f"  {name}: {sorted(drift[name])}")
        if len(drift) > 25:
            print(f"  … and {len(drift) - 25} more")
    else:
        print("\nAsset ?v= drift: none")

    if orphan_css:
        print(f"\nCSS not linked from deploy HTML ({len(orphan_css)}):")
        for name in orphan_css:
            print(f"  - {name}")
    if orphan_js:
        print(f"\nJS not linked from deploy HTML ({len(orphan_js)}):")
        for name in orphan_js:
            print(f"  - {name}")

    if OPTIONAL_JS:
        print("\nOptional / inactive JS (documented, not errors):")
        for name in sorted(OPTIONAL_JS):
            print(f"  - {name}")

    if dup_lang:
        print(f"\nDuplicate lang attributes ({len(dup_lang)}):")
        for rel in dup_lang:
            print(f"  - {rel}")

    issues = validate.returncode != 0 or bool(drift) or bool(dup_lang)
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
