#!/usr/bin/env python3
"""Stamp one deploy build id onto local asset URLs in a site tree.

Called from helpers/_build_deployment_folder.py after the Deployment package
is copied. Does not rename files. Page paths, hashes, and non-asset query
strings (language, filters) are left alone.

    python helpers/_stamp_asset_versions.py --self-check
"""
from __future__ import annotations

import argparse
import re
import sys
import tempfile
from pathlib import Path

from _paths import ROOT

ASSET_EXTS = (
    r"css|js|mjs|json|png|jpe?g|gif|webp|svg|ico|woff2?|ttf|otf|eot|map"
)
STAMP_SUFFIXES = {".html", ".css", ".js"}
SKIP_DIR_NAMES = {"vendor", "node_modules", ".git"}

# "?v=" + PHOTO_VER   and   file.json?v=" + VERSION
CONCAT_V_RE = re.compile(
    r"""\?v=(['"])\s*\+\s*[A-Za-z_][A-Za-z0-9_]*"""
)
# ROUTES_URL + "?v=22"
LONE_V_RE = re.compile(
    r"""(?P<q>['"])\?v=[^'"\s#&]*(?P=q)"""
)
QUOTED_ASSET_RE = re.compile(
    rf"""(?P<q>['"])(?P<url>(?!https?:)(?!//)(?!data:)(?!mailto:)(?!tel:)[^'"\s]*?\.(?:{ASSET_EXTS}))(?P<query>\?[^'"\s#]*)?(?P<hash>#[^'"\s]*)?(?P=q)""",
    re.IGNORECASE,
)
URL_FUNC_RE = re.compile(
    rf"""url\(\s*(?P<url>(?!['"])(?!https?:)(?!//)(?!data:)[^)'"\s]*?\.(?:{ASSET_EXTS}))(?P<query>\?[^)'"\s#]*)?(?P<hash>#[^)'"\s]*)?\s*\)""",
    re.IGNORECASE,
)


def build_id_from_stamp(stamp: str) -> str:
    """Footer stamp is 'YYYYMMDD - HHmm'. Query tokens cannot contain spaces."""
    return stamp.replace(" - ", "-").replace(" ", "")


def _with_version(query: str | None, build_id: str) -> str:
    if not query:
        return "?v=" + build_id
    parts = [part for part in query[1:].split("&") if part]
    found = False
    out: list[str] = []
    for part in parts:
        if part == "v" or part.startswith("v="):
            out.append("v=" + build_id)
            found = True
        else:
            out.append(part)
    if not found:
        out.append("v=" + build_id)
    return "?" + "&".join(out)


def _rewrite_quoted(match: re.Match[str], build_id: str) -> str:
    url = match.group("url")
    query = _with_version(match.group("query"), build_id)
    frag = match.group("hash") or ""
    quote = match.group("q")
    return f"{quote}{url}{query}{frag}{quote}"


def _rewrite_url_func(match: re.Match[str], build_id: str) -> str:
    url = match.group("url")
    query = _with_version(match.group("query"), build_id)
    frag = match.group("hash") or ""
    return f"url({url}{query}{frag})"


def stamp_text(text: str, build_id: str) -> str:
    """Return text with local asset references pinned to build_id."""
    if not build_id or not re.fullmatch(r"[A-Za-z0-9._~-]+", build_id):
        raise ValueError(f"Unsafe build id: {build_id!r}")

    def concat(match: re.Match[str]) -> str:
        return "?v=" + build_id + match.group(1)

    def lone(match: re.Match[str]) -> str:
        quote = match.group("q")
        return f"{quote}?v={build_id}{quote}"

    text = CONCAT_V_RE.sub(concat, text)
    text = LONE_V_RE.sub(lone, text)
    text = QUOTED_ASSET_RE.sub(lambda m: _rewrite_quoted(m, build_id), text)
    text = URL_FUNC_RE.sub(lambda m: _rewrite_url_func(m, build_id), text)
    return text


def _should_stamp(path: Path, root: Path) -> bool:
    if path.suffix.lower() not in STAMP_SUFFIXES:
        return False
    if path.name.endswith(".min.js"):
        return False
    try:
        rel_parts = path.relative_to(root).parts
    except ValueError:
        rel_parts = path.parts
    return not any(part in SKIP_DIR_NAMES for part in rel_parts)


def stamp_tree(root: Path, build_id: str) -> int:
    """Rewrite asset versions under root. Returns the number of files changed."""
    changed = 0
    for path in root.rglob("*"):
        if not path.is_file() or not _should_stamp(path, root):
            continue
        raw = path.read_bytes()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            continue
        updated = stamp_text(text, build_id)
        if updated != text:
            path.write_bytes(updated.encode("utf-8"))
            changed += 1
    return changed


def check_htaccess(path: Path) -> list[str]:
    """Return problems if HTML revalidation or versioned-asset caching is wrong."""
    raw = path.read_text(encoding="utf-8")
    text = "\n".join(
        line for line in raw.splitlines() if not line.strip().startswith("#")
    )
    problems: list[str] = []
    if 'Header set Cache-Control "no-cache, must-revalidate"' not in text:
        problems.append(f"{path}: HTML is missing no-cache, must-revalidate")
    if "public, max-age=31536000, immutable" not in text:
        problems.append(f"{path}: versioned assets are missing the immutable cache header")
    if "env=DAAB_VERSIONED" not in text:
        problems.append(f"{path}: immutable header is not limited to versioned requests")
    if re.search(r"FileETag\s+None", text, re.I):
        problems.append(f"{path}: ETag is disabled")
    if re.search(r"Header\s+unset\s+ETag", text, re.I):
        problems.append(f"{path}: ETag is unset")
    if re.search(r"Header\s+unset\s+Last-Modified", text, re.I):
        problems.append(f"{path}: Last-Modified is unset")
    immutable_lines = [
        line.strip() for line in text.splitlines() if "immutable" in line
    ]
    for line in immutable_lines:
        if "env=DAAB_VERSIONED" not in line:
            problems.append(f"{path}: immutable header is not conditional: {line}")
    return problems


def self_check() -> int:
    build_id = "20261010-1137"
    sample = """
<link href="css/daab-common.css?v=115" rel="stylesheet"/>
<img src="../images/daab-logo.webp" alt=""/>
<a href="mission.html#story">Mission</a>
<a href="scientists/list.html?sort=ad_soyad&amp;country=az">List</a>
<a href="https://example.com/app.js?v=1">ext</a>
<script src="js/daab-i18n.js?v=78"></script>
"""
    js = """
load(ROUTES_URL + "?v=22");
return assetRoot + "images/qr/" + lang + "/" + slug + ".webp?v=1";
return root + "images/scientists-photos/" + photo + "?v=" + PHOTO_VER;
var url = assetRoot() + "i18n/page-subtitles.json?v=" + VERSION;
location.href = "profiles.html#" + slug;
"""
    css = 'src: url("../fonts/Inter.woff2") format("woff2");\n'
    html = stamp_text(sample, build_id)
    js_out = stamp_text(js, build_id)
    css_out = stamp_text(css, build_id)
    errors: list[str] = []

    def need(cond: bool, message: str) -> None:
        if not cond:
            errors.append(message)

    need(f"css/daab-common.css?v={build_id}" in html, "css version was not replaced")
    need(f"../images/daab-logo.webp?v={build_id}" in html, "unversioned image was not stamped")
    need('href="mission.html#story"' in html, "page hash changed")
    need("list.html?sort=ad_soyad" in html, "filter query on a page link changed")
    need("https://example.com/app.js?v=1" in html, "external asset was rewritten")
    need(f'js/daab-i18n.js?v={build_id}' in html, "js version was not replaced")
    need(f'"?v={build_id}"' in js_out, "standalone ?v= string was not stamped")
    need(f".webp?v={build_id}" in js_out, "dynamic image suffix was not stamped")
    need(f"?v={build_id}" in js_out and "PHOTO_VER" not in js_out, "PHOTO_VER concatenation remains")
    need("VERSION" not in js_out, "VERSION concatenation remains")
    need("profiles.html#" in js_out, "in-page profile link changed")
    need(f'url("../fonts/Inter.woff2?v={build_id}")' in css_out, "font url was not stamped")

    root_ht = ROOT / ".htaccess"
    deploy_ht = ROOT / "Deployment" / ".htaccess"
    errors.extend(check_htaccess(root_ht))
    errors.extend(check_htaccess(deploy_ht))
    if root_ht.read_text(encoding="utf-8") != deploy_ht.read_text(encoding="utf-8"):
        errors.append("root .htaccess and Deployment/.htaccess differ")

    with tempfile.TemporaryDirectory() as tmp:
        tree = Path(tmp)
        page = tree / "index.html"
        page.write_text(sample, encoding="utf-8", newline="\n")
        vendor = tree / "js" / "vendor"
        vendor.mkdir(parents=True)
        (vendor / "lib.js").write_text('var x = "app.js?v=1";\n', encoding="utf-8", newline="\n")
        stamp_tree(tree, build_id)
        stamped = page.read_text(encoding="utf-8")
        need(f"?v={build_id}" in stamped, "stamp_tree did not update html")
        need("app.js?v=1" in (vendor / "lib.js").read_text(encoding="utf-8"), "vendor js was stamped")

    if errors:
        print("Asset version self-check FAILED:")
        for line in errors:
            print("  " + line)
        return 1
    print(f"Asset version self-check OK (sample build {build_id}).")
    print("HTML revalidation and versioned-asset cache rules match in both .htaccess files.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Stamp ?v=<build id> on local assets.")
    parser.add_argument("--self-check", action="store_true", help="Run in-memory checks and exit.")
    parser.add_argument("--root", type=Path, help="Tree to rewrite. Refuses the repo root.")
    parser.add_argument("--build-id", help="Token placed in ?v=. Required with --root.")
    args = parser.parse_args()
    if args.self_check:
        return self_check()
    if args.root is None or not args.build_id:
        parser.error("Pass --self-check, or both --root and --build-id.")
    root = args.root.resolve()
    if root == ROOT.resolve():
        print("Refusing to stamp the source tree. Stamp the Deployment staging copy.", file=sys.stderr)
        return 2
    count = stamp_tree(root, args.build_id)
    print(f"Stamped {count} file(s) under {root} with ?v={args.build_id}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
