#!/usr/bin/env python3
"""Build a production-ready /Deployment folder from the repo (respects .deployignore).

Run from repository root:
    python helpers/_build_deployment_folder.py
    python helpers/_build_deployment_folder.py --include-images   # full copy incl. images/

Always copies images/ and Books/ into Deployment/. Production is wiped and
replaced from this folder, so the package must contain every file the site needs.
"""
from __future__ import annotations

import argparse
import fnmatch
import re
import shutil
import sys
from pathlib import Path

from _paths import (
    LEGACY_FOOTER_COPYRIGHTS,
    ROOT,
    footer_copyright_line,
)
from _deploy_assets import DEPLOYIGNORE_ASSET_PATHS

FOOTER_COPY_RE = re.compile(r'(<div class="footer-copy">)(.*?)(</div>)', re.DOTALL)
STAMPED_COPYRIGHT_RE = re.compile(
    r"© DAAB-WAAS - All rights reserved \| Build (?:\d{8} - \d{4}|\d+)"
)
FOOTER_STAMP_SKIP = {
    "_paths.py",
    "_build_deployment_folder.py",
}

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

# Nothing under Deployment/ is host-managed. images/ and Books/ are copied
# from the repo on every rebuild.
PRESERVE_DEPLOY_DIRS = frozenset()

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
) -> bool:
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


def collect_deploy_files() -> tuple[list[Path], list[Path]]:
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
        if should_exclude(rel_posix, excludes, includes):
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


def _write_if_changed(path: Path, original: str, updated: str) -> bool:
    if updated == original:
        return False
    path.write_bytes(updated.encode("utf-8"))
    return True


def stamp_footer_copyrights(line: str) -> int:
    """Write the shared English copyright row into source footers and generator strings.

    Deployment/ is produced by the copy step, so it is not edited here.
    """
    changed = 0
    for folder in ("az", "en", "templates"):
        base = ROOT / folder
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.html")):
            original = path.read_bytes().decode("utf-8")
            updated = FOOTER_COPY_RE.sub(
                lambda match: match.group(1) + line + match.group(3),
                original,
            )
            if _write_if_changed(path, original, updated):
                changed += 1

    helpers = ROOT / "helpers"
    for path in sorted(helpers.rglob("*.py")):
        if path.name in FOOTER_STAMP_SKIP:
            continue
        raw = path.read_bytes()
        try:
            original = raw.decode("utf-8")
        except UnicodeDecodeError:
            continue
        if not any(legacy in original for legacy in LEGACY_FOOTER_COPYRIGHTS) and (
            "© DAAB-WAAS - All rights reserved | Build " not in original
        ):
            continue
        updated = original
        for legacy in LEGACY_FOOTER_COPYRIGHTS:
            updated = updated.replace(legacy, line)
        updated = STAMPED_COPYRIGHT_RE.sub(line, updated)
        if _write_if_changed(path, original, updated):
            changed += 1
    return changed


# The Register submenu stays linked in source so local preview can open
# register.html. This lock runs only on the staged Deployment copy and mutes
# that submenu. The Second Forum participant pill stays an active external link
# in both trees.
_FORUM_REGISTER_HTML = (
    "en/forum/2026/index.html",
    "az/forum/2026/index.html",
)
_PARTICIPANT_PILL_URL = "https://diaspor.gov.az/forum/"
_PARTICIPANT_PILL_ACTIVE = (
    '<a class="btn btn-primary" href="https://diaspor.gov.az/forum/" '
    'rel="noopener noreferrer" target="_blank">{label}</a>'
)
_PARTICIPANT_PILL_RE = re.compile(
    r'<p class="forum-register-cta">(.*?)</p>',
    re.DOTALL,
)
_PARTICIPANT_PILL_CONTROL_RE = re.compile(
    r'(?:<a class="btn btn-primary" href="(?:register\.html|https://diaspor\.gov\.az/forum/)"[^>]*>'
    r'|<button type="button" class="btn btn-primary"[^>]*>)'
    r'([^<]*)(?:</a>|</button>)'
)
_NAV_REGISTER_OBJECT_RE = re.compile(
    r'\{[^{}]*"id": "forum-2026-register"[^{}]*\}'
)
_ENABLED_NAV_FN = """\
  function appendDropdownPageLink(panel, childDef, routes, lang, ui, activeId) {
    var page = pageById(routes, childDef.id);
    if (!page) return false;
    var link = document.createElement("a");
    link.href = childPageHref(page, lang, childDef);
    link.className = "nav-dropdown-link";
    link.setAttribute("role", "menuitem");
    link.setAttribute("data-nav-id", childNavId(childDef));

    var iconKey = childIconKey(childDef, page);
    var title = document.createElement("span");
    title.className = "nav-dropdown-link-title";
    title.textContent = labelWithIcon(ui, iconKey, childLabel(ui, lang, childDef, page));
    link.appendChild(title);

    var descText = linkDescription(ui, lang, childDef, page);
    if (descText) {
      var desc = document.createElement("span");
      desc.className = "nav-dropdown-link-desc";
      desc.textContent = descText;
      link.appendChild(desc);
    }

    var active = childLinkIsActive(page, childDef, activeId);
    if (active) {
      link.classList.add("active");
      link.setAttribute("aria-current", "page");
    }
    panel.appendChild(link);
    return active;
  }
"""
_DISABLED_NAV_FN = """\
  function markNavLinkDisabled(link) {
    link.removeAttribute("href");
    link.setAttribute("aria-disabled", "true");
    link.setAttribute("tabindex", "-1");
    link.classList.add("nav-dropdown-link--disabled");
    link.style.setProperty("pointer-events", "none", "important");
    link.style.setProperty("cursor", "default", "important");
    link.style.setProperty("color", "#8b97a3", "important");
    link.style.setProperty("background", "transparent", "important");
    link.style.setProperty("opacity", "0.72", "important");
    var title = link.querySelector(".nav-dropdown-link-title");
    if (title) title.style.setProperty("color", "#8b97a3", "important");
    var desc = link.querySelector(".nav-dropdown-link-desc");
    if (desc) desc.style.setProperty("color", "#a8b3bd", "important");
    link.addEventListener("click", function (event) {
      event.preventDefault();
      event.stopPropagation();
    });
  }

  function appendDropdownPageLink(panel, childDef, routes, lang, ui, activeId) {
    var page = pageById(routes, childDef.id);
    if (!page) return false;
    var link = document.createElement("a");
    var navDisabled = !!(childDef.disabled || childDef.id === "forum-2026-register");
    if (!navDisabled) link.href = childPageHref(page, lang, childDef);
    link.className = "nav-dropdown-link";
    link.setAttribute("role", "menuitem");
    link.setAttribute("data-nav-id", childNavId(childDef));

    var iconKey = childIconKey(childDef, page);
    var title = document.createElement("span");
    title.className = "nav-dropdown-link-title";
    title.textContent = labelWithIcon(ui, iconKey, childLabel(ui, lang, childDef, page));
    link.appendChild(title);

    var descText = linkDescription(ui, lang, childDef, page);
    if (descText) {
      var desc = document.createElement("span");
      desc.className = "nav-dropdown-link-desc";
      desc.textContent = descText;
      link.appendChild(desc);
    }

    var active = childLinkIsActive(page, childDef, activeId);
    if (active && !navDisabled) {
      link.classList.add("active");
      link.setAttribute("aria-current", "page");
    }
    if (navDisabled) markNavLinkDisabled(link);
    panel.appendChild(link);
    return active && !navDisabled;
  }
"""
_NAV_DISABLED_CSS = """
.nav-menu .nav-dropdown-link.nav-dropdown-link--disabled,
.nav-menu .nav-dropdown--nested > .nav-dropdown-panel > .nav-dropdown-link.nav-dropdown-link--disabled,
.nav-menu .nav-dropdown-link.nav-dropdown-link--disabled:hover,
.nav-menu .nav-dropdown-link.nav-dropdown-link--disabled:focus,
.nav-menu .nav-dropdown-link.nav-dropdown-link--disabled:focus-visible,
.nav-menu .nav-dropdown-link.nav-dropdown-link--disabled.active {
  color: #8b97a3 !important;
  background: transparent !important;
  border-color: transparent !important;
  box-shadow: none !important;
  cursor: default !important;
  pointer-events: none !important;
  opacity: 0.72;
  text-decoration: none !important;
}
.nav-menu .nav-dropdown-link.nav-dropdown-link--disabled .nav-dropdown-link-title,
.nav-menu .nav-dropdown-link.nav-dropdown-link--disabled .nav-dropdown-link-desc,
.nav-menu .nav-dropdown-link.nav-dropdown-link--disabled:hover .nav-dropdown-link-desc,
.nav-menu .nav-dropdown-link.nav-dropdown-link--disabled.active .nav-dropdown-link-title,
.nav-menu .nav-dropdown-link.nav-dropdown-link--disabled.active .nav-dropdown-link-desc {
  color: #8b97a3 !important;
}
"""


def _with_source_newlines(original: str, updated: str) -> str:
    if "\r\n" in original and "\r\n" not in updated:
        return updated.replace("\n", "\r\n")
    return updated


def _lock_nav_json(text: str) -> str:
    match = _NAV_REGISTER_OBJECT_RE.search(text)
    if not match:
        raise SystemExit("Production lock: forum-2026-register entry missing from i18n/nav.json")
    block = match.group(0)
    if re.search(r'"disabled"\s*:\s*true', block):
        return text
    desc = re.search(r'("descKey": "[^"]*")(\s*)\}$', block)
    if not desc:
        raise SystemExit("Production lock: forum-2026-register entry has no descKey")
    indent = desc.group(2)
    if "\n" in indent:
        closing = indent[indent.rfind("\n") + 1 :]
        prop_indent = indent[: indent.rfind("\n") + 1] + closing + "  "
    else:
        prop_indent = "\n" + indent + "  "
        indent = "\n" + indent
    updated = (
        block[: desc.start()]
        + desc.group(1)
        + ","
        + prop_indent
        + '"disabled": true'
        + indent
        + "}"
    )
    return text[: match.start()] + updated + text[match.end() :]


def _lock_primary_nav_js(text: str) -> str:
    norm = text.replace("\r\n", "\n")
    if "function markNavLinkDisabled" in norm and 'childDef.id === "forum-2026-register"' in norm:
        return text
    if _ENABLED_NAV_FN not in norm:
        raise SystemExit(
            "Production lock: js/daab-primary-nav.js no longer matches the enabled registration function."
        )
    updated = norm.replace(_ENABLED_NAV_FN, _DISABLED_NAV_FN, 1)
    return _with_source_newlines(text, updated)


def _active_participant_pill(label: str) -> str:
    return _PARTICIPANT_PILL_ACTIVE.format(label=label)


def _lock_forum_html(text: str, rel: str) -> str:
    """Keep the participant pill enabled and linked. Do not mute it."""
    match = _PARTICIPANT_PILL_RE.search(text)
    if not match:
        raise SystemExit(f"Production lock: participant registration pill missing in {rel}")
    control = _PARTICIPANT_PILL_CONTROL_RE.search(match.group(1))
    if not control:
        raise SystemExit(f"Production lock: participant registration pill missing in {rel}")
    active = _active_participant_pill(control.group(1))
    if control.group(0) == active and "disabled" not in control.group(0):
        return text
    updated = (
        text[: match.start(1)]
        + match.group(1).replace(control.group(0), active, 1)
        + text[match.end(1) :]
    )
    if _PARTICIPANT_PILL_URL not in updated or "disabled" in active:
        raise SystemExit(f"Production lock: participant pill was not left enabled in {rel}")
    return updated


def _append_css_once(text: str, marker: str, addition: str) -> str:
    if marker in text:
        return text
    sep = "\r\n" if "\r\n" in text else "\n"
    body = addition.strip("\r\n").replace("\n", sep)
    if text and not text.endswith(("\n", "\r")):
        text += sep
    return text + sep + body + sep


def lock_production_forum_registration(deploy_root: Path) -> list[str]:
    """Mute the Forum 2026 Register submenu inside a deployment tree.

    The participant pill stays an active link to the external forum form.
    Does not touch source.
    """
    changed: list[str] = []

    nav_path = deploy_root / "i18n" / "nav.json"
    nav_orig = nav_path.read_text(encoding="utf-8")
    nav_updated = _lock_nav_json(nav_orig)
    if _write_if_changed(nav_path, nav_orig, nav_updated):
        changed.append("i18n/nav.json")

    nav_js = deploy_root / "js" / "daab-primary-nav.js"
    js_orig = nav_js.read_text(encoding="utf-8")
    js_updated = _lock_primary_nav_js(js_orig)
    if _write_if_changed(nav_js, js_orig, js_updated):
        changed.append("js/daab-primary-nav.js")

    common_css = deploy_root / "css" / "daab-common.css"
    common_orig = common_css.read_text(encoding="utf-8")
    common_updated = _append_css_once(common_orig, "nav-dropdown-link--disabled", _NAV_DISABLED_CSS)
    if _write_if_changed(common_css, common_orig, common_updated):
        changed.append("css/daab-common.css")

    for rel in _FORUM_REGISTER_HTML:
        path = deploy_root / rel
        original = path.read_text(encoding="utf-8")
        updated = _lock_forum_html(original, rel)
        if _write_if_changed(path, original, updated):
            changed.append(rel)

    return changed


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Build production Deployment/ package.")
    p.add_argument(
        "--include-images",
        action="store_true",
        help="Accepted for older commands. images/ and Books/ are always copied.",
    )
    return p.parse_args()


def main() -> int:
    parse_args()

    copyright_line = footer_copyright_line()
    import _paths

    _paths.FOOTER_COPYRIGHT_AZ = copyright_line
    _paths.FOOTER_COPYRIGHT_EN = copyright_line
    stamped = stamp_footer_copyrights(copyright_line)

    print("DAAB deployment package builder\n")
    print(f"  Source: {ROOT}")
    print(f"  Output: {DEPLOY_DIR}")
    print(f"  Footer: {copyright_line}")
    print(f"  Footer files updated: {stamped}")
    print("  Images and Books: copy from repo\n")

    # Preflight on source
    print("→ Validating source site…")
    pre = __import__("subprocess").run(
        [sys.executable, str(ROOT / "helpers" / "_validate_site.py")],
        cwd=ROOT,
    )
    if pre.returncode != 0:
        print("Source validation failed — fix errors before building Deployment/.")
        return 1

    included, skipped = collect_deploy_files()

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

    print("→ Muting Forum 2026 Register menu item for production…")
    for rel in lock_production_forum_registration(DEPLOY_STAGING):
        print(f"  locked {rel}")

    # Repo-root .htaccess is the source of truth (copied above with the site).
    # Do not overlay the previous Deployment/.htaccess or cache rules never ship.

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
    required.append("images/daab-logo.webp")
    required.append("images/daab-favicon.webp")
    required.append("favicon.ico")
    required.append("Books/DAAB_DK/forum-book-2026.pdf")
    missing_roots = [p for p in required if not (DEPLOY_STAGING / p).is_file()]
    if missing_roots:
        print("ERROR — deployment package missing required files:")
        for p in missing_roots:
            print(f"  ✗ {p}")
        return 1

    print("→ Validating staging link integrity…")
    if validate_deployment_tree(DEPLOY_STAGING) != 0:
        print("\nDeployment package validation FAILED.")
        return 1

    print("→ Publishing to Deployment/ …")
    replace_deploy_dir(DEPLOY_STAGING, DEPLOY_DIR, preserve_names=PRESERVE_DEPLOY_DIRS)

    forbidden_live = validate_forbidden_assets(DEPLOY_DIR)
    if forbidden_live:
        print("ERROR — forbidden assets remain in Deployment/:")
        for rel in forbidden_live[:20]:
            print(f"  ✗ {rel}")
        return 1

    img_n = sum(1 for p in (DEPLOY_DIR / "images").rglob("*") if p.is_file()) if (DEPLOY_DIR / "images").is_dir() else 0
    books_n = sum(1 for p in (DEPLOY_DIR / "Books").rglob("*") if p.is_file()) if (DEPLOY_DIR / "Books").is_dir() else 0
    print(f"  images/: {img_n} files")
    print(f"  Books/: {books_n} files")

    print(f"\nOK — Deployment/ is ready ({copied} files).")
    print("Upload everything inside Deployment/ to your production web root.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
