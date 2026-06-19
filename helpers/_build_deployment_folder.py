#!/usr/bin/env python3
"""Build a production-ready /Deployment folder from the repo (respects .deployignore).

Run from repository root:
    python helpers/_build_deployment_folder.py
    python helpers/_build_deployment_folder.py --include-images   # full copy incl. images/

By default **images/** is not copied (unchanged on production). Existing
Deployment/images/ is preserved when rebuilding the package.
"""
from __future__ import annotations

import argparse
import fnmatch
import shutil
import sys
from pathlib import Path

from _paths import ROOT
from _deploy_assets import DEPLOYIGNORE_ASSET_PATHS

DEPLOY_DIR = ROOT / "Deployment"
DEPLOY_STAGING = ROOT / ".deployment-staging"
DEPLOYIGNORE = ROOT / ".deployignore"

# Always exclude (even if not listed in .deployignore)
HARD_EXCLUDES = {
    "Deployment",
    "deployment",
    ".deployment-staging",
    ".git",
    "node_modules",
    ".cursor",
    ".vscode",
    ".github",
    "__pycache__",
}

EXTRA_FILE_GLOBS = ("*.zip", "*.docx", "*.tmp", "~$*", "*.pyc", "*.pyo")
EXTRA_DIR_NAMES = {".git", "__pycache__", "node_modules"}

# Subfolder under Deployment/ left untouched when refreshing the package.
PRESERVE_DEPLOY_DIRS = frozenset({"images"})

# Build-only assets — must match helpers/_deploy_assets.py + .deployignore.
DEPLOY_EXCLUDED_ASSETS = frozenset(DEPLOYIGNORE_ASSET_PATHS)


def parse_deployignore(path: Path) -> tuple[list[str], list[str]]:
    excludes: list[str] = []
    includes: list[str] = []
    if not path.is_file():
        return excludes, includes
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("!"):
            includes.append(line[1:].strip())
        else:
            excludes.append(line)
    return excludes, includes


def _match_rule(rel_posix: str, rule: str) -> bool:
    rule = rule.replace("\\", "/").strip()
    if not rule:
        return False
    if rule.endswith("/"):
        return rel_posix.startswith(rule) or rel_posix + "/" == rule
    if rule.endswith("/*"):
        prefix = rule[:-2]
        return rel_posix == prefix or rel_posix.startswith(prefix + "/")
    if "/" in rule or "*" in rule or "?" in rule:
        return fnmatch.fnmatch(rel_posix, rule)
    # bare name: file at any depth or top-level segment
    if rel_posix == rule:
        return True
    if rel_posix.endswith("/" + rule):
        return True
    return rule in rel_posix.split("/")


def should_exclude(
    rel_posix: str,
    excludes: list[str],
    includes: list[str],
    *,
    skip_images: bool,
) -> bool:
    if skip_images and (rel_posix == "images" or rel_posix.startswith("images/")):
        return True
    if rel_posix in DEPLOY_EXCLUDED_ASSETS:
        return True
    parts = rel_posix.split("/")
    parts_lower = [p.lower() for p in parts]
    hard_excludes_lower = {name.lower() for name in HARD_EXCLUDES}
    extra_dir_names_lower = {name.lower() for name in EXTRA_DIR_NAMES}
    if parts_lower[0] in hard_excludes_lower or any(
        p in extra_dir_names_lower for p in parts_lower
    ):
        return True
    name = parts[-1]
    for pat in EXTRA_FILE_GLOBS:
        if fnmatch.fnmatch(name, pat):
            return True

    excluded = False
    for rule in excludes:
        if _match_rule(rel_posix, rule):
            excluded = True
            break

    if excluded:
        for rule in includes:
            if _match_rule(rel_posix, rule):
                return False
        return True
    return False


def collect_deploy_files(*, skip_images: bool) -> tuple[list[Path], list[Path]]:
    excludes, includes = parse_deployignore(DEPLOYIGNORE)
    included: list[Path] = []
    skipped: list[Path] = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        try:
            rel = path.relative_to(ROOT)
        except ValueError:
            continue
        rel_posix = rel.as_posix()
        if should_exclude(rel_posix, excludes, includes, skip_images=skip_images):
            skipped.append(path)
        else:
            included.append(path)
    return included, skipped


def clear_tree(path: Path, preserve_names: frozenset[str] = frozenset()) -> None:
    """Remove directory contents (Windows-safe when the folder itself is locked)."""
    if not path.is_dir():
        return
    for top in list(path.iterdir()):
        if top.name in preserve_names:
            continue
        if top.is_file() or top.is_symlink():
            top.unlink(missing_ok=True)
        elif top.is_dir():
            shutil.rmtree(top, ignore_errors=True)
    for child in sorted(path.rglob("*"), key=lambda p: len(p.parts), reverse=True):
        if any(part in preserve_names for part in child.relative_to(path).parts):
            continue
        if child.is_file() or child.is_symlink():
            child.unlink(missing_ok=True)
        elif child.is_dir():
            try:
                child.rmdir()
            except OSError:
                pass
def replace_deploy_dir(
    staging: Path, target: Path, preserve_names: frozenset[str] = frozenset()
) -> None:
    """Swap staging build into Deployment/, falling back to in-place refresh."""
    target.mkdir(parents=True, exist_ok=True)
    try:
        if target.exists() and any(target.iterdir()):
            clear_tree(target, preserve_names=preserve_names)
    except OSError:
        pass

    staged_rel_paths: set[str] = set()
    for src in staging.rglob("*"):
        if not src.is_file():
            continue
        rel = src.relative_to(staging)
        staged_rel_paths.add(rel.as_posix())
        dest = target / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)

    # Drop stale files left from older deployment packages.
    preserve_lower = {name.lower() for name in preserve_names}
    for existing in list(target.rglob("*")):
        if not existing.is_file():
            continue
        rel = existing.relative_to(target)
        if rel.as_posix() in staged_rel_paths:
            continue
        if any(part.lower() in preserve_lower for part in rel.parts):
            continue
        existing.unlink(missing_ok=True)
    for existing in sorted(target.rglob("*"), key=lambda p: len(p.parts), reverse=True):
        if existing.is_dir():
            try:
                existing.rmdir()
            except OSError:
                pass

    clear_tree(staging)
    try:
        staging.rmdir()
    except OSError:
        pass


def validate_deployment_tree(deploy_root: Path | None = None) -> int:
    import _paths
    import _validate_site as vs

    root = deploy_root or DEPLOY_DIR
    _paths.ROOT = root
    vs.ROOT = root
    vs.BILINGUAL_PAGES = vs.bilingual_html_files()
    return vs.main()


def validate_forbidden_assets(deploy_root: Path) -> list[str]:
    """Return relative paths of build-only assets that must not ship in Deployment/."""
    found: list[str] = []
    for rel in sorted(DEPLOY_EXCLUDED_ASSETS):
        if (deploy_root / rel).is_file():
            found.append(rel)
    return found


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Build production Deployment/ package.")
    p.add_argument(
        "--include-images",
        action="store_true",
        help="Copy images/ from repo (default: skip; keep server copy)",
    )
    return p.parse_args()


def main() -> int:
    args = parse_args()
    skip_images = not args.include_images

    print("DAAB deployment package builder\n")
    print(f"  Source: {ROOT}")
    print(f"  Output: {DEPLOY_DIR}")
    print(f"  Images: {'copy from repo' if not skip_images else 'skip (preserve Deployment/images if present)'}\n")

    # Preflight on source
    print("→ Validating source site…")
    pre = __import__("subprocess").run(
        [sys.executable, str(ROOT / "helpers" / "_validate_site.py")],
        cwd=ROOT,
    )
    if pre.returncode != 0:
        print("Source validation failed — fix errors before building Deployment/.")
        return 1

    included, skipped = collect_deploy_files(skip_images=skip_images)

    if DEPLOY_STAGING.exists():
        print("→ Clearing previous staging …")
        clear_tree(DEPLOY_STAGING)
    DEPLOY_STAGING.mkdir(parents=True, exist_ok=True)

    copied = 0
    bytes_total = 0
    for src in included:
        rel = src.relative_to(ROOT)
        dest = DEPLOY_STAGING / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        copied += 1
        bytes_total += src.stat().st_size

    htaccess_src = DEPLOY_DIR / ".htaccess"
    if htaccess_src.is_file():
        shutil.copy2(htaccess_src, DEPLOY_STAGING / ".htaccess")
        copied += 1

    print(f"→ Staged {copied} files ({bytes_total / (1024 * 1024):.1f} MB)")
    print(f"→ Skipped {len(skipped)} non-deploy paths\n")

    forbidden = validate_forbidden_assets(DEPLOY_STAGING)
    if forbidden:
        print("ERROR — forbidden assets in staging package:")
        for rel in forbidden[:20]:
            print(f"  ✗ {rel}")
        if len(forbidden) > 20:
            print(f"  … and {len(forbidden) - 20} more")
        return 1

    # Spot-check required roots (staging)
    required = [
        "index.html",
        "az/index.html",
        "en/index.html",
        "css/daab-common.css",
        "js/daab-nav.js",
        "js/daab-mobile.js",
        "i18n/nav.json",
    ]
    if not skip_images:
        required.append("images/daab-logo.png")
    missing_roots = [p for p in required if not (DEPLOY_STAGING / p).is_file()]
    if missing_roots:
        print("ERROR — deployment package missing required files:")
        for p in missing_roots:
            print(f"  ✗ {p}")
        return 1

    if skip_images:
        print("→ Link check: skipped on staging (images omitted; source site validated OK).")
    else:
        print("→ Validating staging link integrity…")
        if validate_deployment_tree(DEPLOY_STAGING) != 0:
            print("\nDeployment package validation FAILED.")
            return 1

    preserve = PRESERVE_DEPLOY_DIRS if skip_images else frozenset()
    print("→ Publishing to Deployment/ …")
    replace_deploy_dir(DEPLOY_STAGING, DEPLOY_DIR, preserve_names=preserve)

    forbidden_live = validate_forbidden_assets(DEPLOY_DIR)
    if forbidden_live:
        print("ERROR — forbidden assets remain in Deployment/:")
        for rel in forbidden_live[:20]:
            print(f"  ✗ {rel}")
        return 1

    if skip_images:
        img_dir = DEPLOY_DIR / "images"
        if img_dir.is_dir() and any(img_dir.rglob("*")):
            n = sum(1 for _ in img_dir.rglob("*") if _.is_file())
            print(f"  (kept existing Deployment/images/ — {n} files)")
        else:
            print(
                "  NOTE: Deployment/images/ is empty. Production must already have images/, "
                "or run with --include-images once."
            )

    print(f"\nOK — Deployment/ is ready ({copied} files).")
    print("Upload everything inside Deployment/ to your production web root.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
