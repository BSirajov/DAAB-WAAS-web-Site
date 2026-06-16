#!/usr/bin/env python3
"""Find public assets not reachable from live site pages (HTML crawl)."""
from __future__ import annotations

import json
import re
from collections import deque
from pathlib import Path

from _paths import ROOT

PAGE_GLOBS = ("*.html", "az/**/*.html", "en/**/*.html", "cv/**/*.html")
ASSET_ROOTS = ("css", "js", "images", "i18n", "cv", "fonts", "video", "audio")

# Capture full quoted path; strip ?query in resolve_ref.
HREF_SRC = re.compile(
    r"""<(?:link|script|a|img|source|video|audio|iframe)\b[^>]*?\b(?:href|src)=["']([^"']+)["']""",
    re.I | re.S,
)
SCRIPT_SRC = re.compile(r"""<script\b[^>]*?\bsrc=["']([^"']+)["']""", re.I | re.S)
LINK_HREF = re.compile(r"""<link\b[^>]*?\bhref=["']([^"']+)["']""", re.I | re.S)
CSS_URL = re.compile(r"""url\(\s*['"]?([^'")]+)""", re.I)
CSS_IMPORT = re.compile(r"""@import\s+["']([^"']+)["']""", re.I)
JS_PATH = re.compile(
    r"""["'](\.\./(?:i18n|js|images|css)/[^"']+)["']|"""
    r"""["']((?:i18n|js|images|css)/[^"']+)["']""",
    re.I,
)
JSON_PATH = re.compile(
    r"""["'](\.\./(?:images|i18n|js|css)/[^"']+)["']|"""
    r"""["'](images/[^"']+)["']|"""
    r"""["'](\.\./\.\./images/[^"']+)["']""",
    re.I,
)
HTML_IN_TEXT = re.compile(r"""<(?:img|source)\b[^>]*?\bsrc=["']([^"']+)["']""", re.I)

SKIP_PREFIXES = (
    "http://",
    "https://",
    "//",
    "mailto:",
    "tel:",
    "data:",
    "javascript:",
    "#",
)

# i18n fetched at runtime when shell JS is present on a page.
RUNTIME_I18N = (
    "routes.json",
    "ui.json",
    "nav.json",
    "search-index.json",
    "page-subtitles.json",
    "anchor-aliases.json",
    "scientists-profiles.json",
    "scientists-profiles-en.json",
    "person-names-en.json",
    "page-panel-summaries.json",
)

RUNTIME_JS_MARKERS = (
    "daab-i18n.js",
    "daab-primary-nav.js",
    "daab-search.js",
    "daab-page-subtitle.js",
    "daab-lang-position.js",
    "scientists-list-preview.js",
)


def site_pages() -> list[Path]:
    seen: set[Path] = set()
    for pattern in PAGE_GLOBS:
        for path in ROOT.glob(pattern):
            if path.is_file() and "Deployment" not in path.parts:
                seen.add(path.resolve())
    return sorted(seen)


def resolve_ref(from_file: Path, ref: str) -> Path | None:
    ref = ref.strip().split("#")[0].split("?")[0]
    if not ref or ref.startswith(SKIP_PREFIXES):
        return None
    if ref.startswith("/"):
        return (ROOT / ref.lstrip("/")).resolve()
    return (from_file.parent / ref).resolve()


def extract_refs(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []

    refs: list[str] = []
    suffix = path.suffix.lower()
    if suffix in (".html", ".htm"):
        refs.extend(HREF_SRC.findall(text))
        refs.extend(SCRIPT_SRC.findall(text))
        refs.extend(LINK_HREF.findall(text))
        # Inline url(...) in style attributes or embedded CSS
        refs.extend(CSS_URL.findall(text))
    elif suffix == ".css":
        refs.extend(CSS_URL.findall(text))
        refs.extend(CSS_IMPORT.findall(text))
    elif suffix == ".js":
        refs.extend(JS_PATH.findall(text))
        # fetch("../i18n/foo.json") — flatten tuples from alternation
        for m in re.finditer(r"""fetch\s*\(\s*["']([^"']+)["']""", text):
            refs.append(m.group(1))
    elif suffix == ".json":
        for m in JSON_PATH.finditer(text):
            refs.extend(g for g in m.groups() if g)
        refs.extend(extract_json_profile_assets(path, text))

    out: list[str] = []
    for item in refs:
        if isinstance(item, tuple):
            out.extend(x for x in item if x)
        else:
            out.append(item)
    return out


def extract_json_profile_assets(path: Path, text: str) -> list[str]:
    """Resolve scientist/profile photo filenames and inline HTML image src."""
    refs: list[str] = []
    name = path.name
    if name != "scientists-profiles.json":
        if name == "scientists-profiles-en.json":
            try:
                data = json.loads(text)
            except json.JSONDecodeError:
                return refs
            profiles = data.get("profiles", {})
            if isinstance(profiles, dict):
                for blob in profiles.values():
                    if isinstance(blob, dict):
                        refs.extend(HTML_IN_TEXT.findall(blob.get("bio_html") or ""))
        return refs
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return refs
    profiles = data.get("profiles", [])
    if not isinstance(profiles, list):
        return refs
    for profile in profiles:
        if not isinstance(profile, dict):
            continue
        photo = profile.get("photo")
        if photo:
            refs.append(f"../images/scientists-photos/{photo}")
        for key in ("bio_html_az", "bio_html_en", "html_az", "html_en"):
            blob = profile.get(key) or ""
            refs.extend(HTML_IN_TEXT.findall(blob))
    return refs


def seed_runtime_i18n(reachable: set[Path], queue: deque[Path]) -> None:
    js_names = {p.name for p in reachable if p.suffix.lower() == ".js"}
    if not any(marker in js_names for marker in RUNTIME_JS_MARKERS):
        return
    for filename in RUNTIME_I18N:
        path = (ROOT / "i18n" / filename).resolve()
        if path.exists() and path not in reachable:
            reachable.add(path)
            queue.append(path)


def seed_gallery_manifest_assets(reachable: set[Path]) -> None:
    manifest = ROOT / "js" / "photos-gallery-manifest.json"
    if not manifest.is_file():
        return
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return
    base = ROOT / "images" / "photos-gallery"
    for cat in data.get("categories", []):
        folder = cat.get("folder")
        if not folder:
            continue
        folder_path = base / folder
        if folder_path.is_dir():
            for path in folder_path.rglob("*"):
                if path.is_file():
                    reachable.add(path.resolve())
    thumbs = ROOT / "js" / "photos-gallery-thumbs.json"
    if thumbs.is_file():
        reachable.add(thumbs.resolve())


def seed_json_image_paths(reachable: set[Path], queue: deque[Path]) -> None:
    """Add image paths declared as root-relative strings inside JSON data files."""
    for path in list(reachable):
        if path.suffix.lower() != ".json":
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
            data = json.loads(text)
        except (OSError, json.JSONDecodeError):
            continue
        stack = [data]
        while stack:
            node = stack.pop()
            if isinstance(node, dict):
                stack.extend(node.values())
                image = node.get("image")
                if isinstance(image, str) and image.startswith("images/"):
                    target = (ROOT / image).resolve()
                    if target.exists():
                        reachable.add(target)
            elif isinstance(node, list):
                stack.extend(node)
            elif isinstance(node, str) and node.startswith("images/"):
                target = (ROOT / node).resolve()
                if target.exists():
                    reachable.add(target)


def seed_qr_assets(reachable: set[Path]) -> None:
    """QR PNGs referenced by photo slug from scientists profiles + home nav."""
    profiles = ROOT / "i18n" / "scientists-profiles.json"
    if not profiles.is_file():
        return
    try:
        data = json.loads(profiles.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return
    profile_list = data.get("profiles", [])
    if not isinstance(profile_list, list):
        return
    for lang in ("az", "en"):
        for profile in profile_list:
            if not isinstance(profile, dict):
                continue
            photo = (profile.get("photo") or "").strip()
            if not photo:
                continue
            stem = photo.rsplit("/", 1)[-1]
            slug = stem.rsplit(".", 1)[0] if "." in stem else stem
            p = (ROOT / "images" / "qr" / lang / f"{slug}.png").resolve()
            if p.exists():
                reachable.add(p)
    for lang in ("az", "en"):
        p = (ROOT / "images" / "qr" / f"home-{lang}.png").resolve()
        if p.exists():
            reachable.add(p)


def crawl_reachable() -> set[Path]:
    queue: deque[Path] = deque(site_pages())
    reachable: set[Path] = set(queue)
    crawlable = {".html", ".css", ".js", ".json"}

    while queue:
        current = queue.popleft()
        if not current.is_file():
            continue
        for ref in extract_refs(current):
            target = resolve_ref(current, ref)
            if target is None:
                continue
            try:
                target.relative_to(ROOT)
            except ValueError:
                continue
            if target in reachable or not target.exists():
                continue
            reachable.add(target)
            if target.suffix.lower() in crawlable:
                queue.append(target)
        if len(reachable) % 200 == 0:
            seed_runtime_i18n(reachable, queue)

    seed_runtime_i18n(reachable, queue)
    while queue:
        current = queue.popleft()
        if not current.is_file():
            continue
        for ref in extract_refs(current):
            target = resolve_ref(current, ref)
            if target is None:
                continue
            try:
                target.relative_to(ROOT)
            except ValueError:
                continue
            if target in reachable or not target.exists():
                continue
            reachable.add(target)
            if target.suffix.lower() in crawlable:
                queue.append(target)

    seed_qr_assets(reachable)
    seed_gallery_manifest_assets(reachable)
    seed_json_image_paths(reachable, queue)
    return reachable


def public_asset_files() -> set[Path]:
    files: set[Path] = set()
    for name in ASSET_ROOTS:
        base = ROOT / name
        if not base.is_dir():
            continue
        for path in base.rglob("*"):
            if path.is_file() and "Deployment" not in path.parts:
                files.add(path.resolve())
    return files


def main() -> int:
    pages = site_pages()
    reachable = crawl_reachable()
    public = public_asset_files()
    orphans = sorted(public - reachable, key=lambda p: p.as_posix())

    by_dir: dict[str, list[Path]] = {}
    for path in orphans:
        rel = path.relative_to(ROOT)
        key = rel.parts[0] if rel.parts else "."
        by_dir.setdefault(key, []).append(rel)

    print(f"Pages scanned: {len(pages)}")
    print(f"Reachable files (transitive): {len(reachable)}")
    print(f"Public asset files: {len(public)}")
    print(f"Unreferenced from pages: {len(orphans)}")
    print()
    print("=== By folder ===")
    for key in sorted(by_dir):
        print(f"  {key}/: {len(by_dir[key])}")
    print()
    print("=== Unreferenced files ===")
    for path in orphans:
        print(path.relative_to(ROOT).as_posix())
    return 0


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--debug":
        page = ROOT / "az" / "index.html"
        text = page.read_text(encoding="utf-8", errors="replace")
        print("has link css", "../css/daab-common.css" in text)
        print("LINK_HREF", LINK_HREF.findall(text)[:5])
        raise SystemExit(0)
    raise SystemExit(main())
