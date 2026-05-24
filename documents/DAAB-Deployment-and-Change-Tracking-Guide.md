# DAAB — deployment and change tracking

This guide explains how to **identify which files changed** after UI/UX, CSS, JavaScript, and HTML updates, and how to **deploy only what is needed** to production with minimal risk.

It complements:

- [DAAB-Site-Stability-and-Deployment-Guide.md](DAAB-Site-Stability-and-Deployment-Guide.md) — local preview, validation, cache busting, hosting pitfalls  
- [HOW-TO-USE-THE-BILINGUAL-SITE.md](HOW-TO-USE-THE-BILINGUAL-SITE.md) — AZ/EN structure and URLs  
- [DAAB-Launch-Checklist.md](DAAB-Launch-Checklist.md) — pre-launch checks  

---

## 1. What goes to production

The live site is **static HTML + assets**. Deploy only these from the repository root:

| Type | Paths | Notes |
|------|--------|--------|
| HTML | `*.html`, `index.html`, `index-gateway.html`, `404.html`, `az/**/*.html`, `en/**/*.html` | Lowercase filenames only |
| Styles | `css/*.css` | Never `CSS/` or root-level `.css` |
| Scripts | `js/*.js` | Never `JS/` or root-level `.js` |
| Images | `images/**` | Includes `images/qr/` if profile QR codes are used |
| Search index | `i18n/search-index.json` | Required if global search is enabled |
| CV pages | `cv/**` | Only if you host standalone CV HTML |

**Do not deploy** (not required for the public site):

- `helpers/` — Python maintenance and generators  
- `documents/` — internal documentation (this folder)  
- `sources/` — source copies for builds  
- `.cursor/`, `.vscode/`, `__pycache__/`, `.git/`  
- `_pdf_extract.txt`, test fixtures, local-only scripts  

Production **never runs Python**. Run helpers locally, commit the generated HTML/CSS/JS, then upload those files.

---

## 2. Track changes automatically with Git

Git is the primary source of truth for “what changed since last deploy.”

### See all local changes

From the repository root:

```powershell
cd "C:\Users\BSira\Documents\GitHub\DAAB-WAAS web site"
git status
```

| Symbol | Meaning |
|--------|---------|
| `M` | Modified |
| `??` | New (untracked) |
| `D` | Deleted |

### List paths only (deploy manifest draft)

```powershell
git status --porcelain
```

Modified and deleted vs last commit:

```powershell
git diff --name-only HEAD
```

New untracked files (respects `.gitignore`):

```powershell
git ls-files --others --exclude-standard
```

### See scope of changes

```powershell
git diff --stat HEAD
```

### Compare against last production deploy

**Best practice:** tag each production release, then diff by tag.

```powershell
git tag deploy-2026-05-23
git push origin deploy-2026-05-23
```

Later:

```powershell
git diff --name-only deploy-2026-05-23..HEAD
```

Or compare to remote `main`:

```powershell
git fetch origin
git diff --name-only origin/main
```

On **GitHub**, open a **Pull Request** — the **Files changed** tab is a human-readable deploy list with review comments.

---

## 3. Compare current files against previous versions

| Goal | Command |
|------|---------|
| All uncommitted edits | `git diff` |
| One file | `git diff az/index.html` |
| One file vs last commit (read old version) | `git show HEAD:az/index.html` |
| Only HTML | `git diff --name-only HEAD -- "*.html" "az/" "en/"` |
| Only CSS | `git diff --name-only HEAD -- "css/"` |
| Only JS | `git diff --name-only HEAD -- "js/"` |
| Only images | `git diff --name-only HEAD -- "images/"` |

**Rule:** If you only care about ship-worthy assets, filter the list mentally (or with a script) to drop `helpers/`, `documents/`, etc.

---

## 4. Feature bundles (what usually changes together)

When several features land in one branch, group files by **feature** so you can deploy a subset or understand blast radius.

### A. Responsive navigation (header)

| Deploy | Do not deploy |
|--------|----------------|
| `css/daab-common.css` | `helpers/_sync_primary_nav.py` |
| `css/daab-lang.css` | |
| `css/daab-mobile.css` | |
| `css/daab-nav-mega.css` | |
| `js/daab-nav.js` | |
| `js/daab-shell.js` | |
| `js/daab-primary-nav.js` | |
| All `az/*.html`, `en/*.html` that reference bumped `?v=` | |

### B. Global site search

| Deploy | Do not deploy |
|--------|----------------|
| `css/daab-search.css` | `helpers/_build_search_index.py` |
| `js/daab-search.js` | `helpers/_inject_global_search.py` |
| `js/daab-i18n.js` | |
| `i18n/search-index.json` | |
| `i18n/ui.json` (if search strings changed) | |
| `index.html`, `az/**`, `en/**` (injected search assets) | |

### C. Scientists catalogue (list + profiles)

| Deploy | Do not deploy |
|--------|----------------|
| `css/scientists-catalog-toolbar.css` | `helpers/_inject_scientists_toolbar_mobile.py` |
| `js/daab-scientists-toolbar-mobile.js` | `helpers/scientists_profiles_core.py` |
| `js/scientists-cv-filters.js` | `helpers/_build_scientists_profiles.py` |
| `js/scientists-catalog-data.js` or `scientists-catalog-data-en.js` | |
| `az/scientists/list.html`, `en/scientists/list.html` | |
| `az/scientists/profiles.html`, `en/scientists/profiles.html` | |
| `css/scientists-profile-deep-link.css`, `css/scientists-profile-qr.css` | |
| `js/daab-profile-deep-link.js` | |
| `images/qr/**` | |

### D. Home / membership copy

| Deploy | Do not deploy |
|--------|----------------|
| `az/index.html`, `en/index.html` | `helpers/i18n_home_en.py` |
| `az/membership.html`, `en/membership.html` | `helpers/i18n_membership_en.py` |
| `sources/home_az.html` (optional; not served live) | |

### Minimal deploy example (filters + nav only)

If you only need the latest scientist filter toolbar alignment:

```
css/daab-common.css
css/daab-lang.css
css/daab-mobile.css
css/scientists-catalog-toolbar.css
js/daab-nav.js
js/daab-shell.js
js/daab-scientists-toolbar-mobile.js
js/scientists-cv-filters.js
az/scientists/list.html
az/scientists/profiles.html
en/scientists/list.html
en/scientists/profiles.html
```

Add profile QR/deep-link assets only if that feature is live.

---

## 5. Shared components and indirect dependencies

DAAB does not use server-side includes. Navigation, footer, and many `<link>` / `<script>` tags are **duplicated in each HTML file**, but behaviour and styling come from **shared assets**.

If you change any row below, treat dependent HTML as potentially stale until redeployed or cache-busted.

| Shared asset | Role | If changed, also deploy |
|--------------|------|-------------------------|
| `css/daab-common.css` | Global layout, nav strip, buttons | All HTML linking to it (or bump `?v=` everywhere) |
| `css/daab-mobile.css` | Touch, safe areas, mobile nav | Same |
| `css/daab-lang.css` | Language switcher | Same |
| `css/daab-nav-mega.css` | Breadcrumbs, section nav | Pages that include it |
| `js/daab-nav.js` | Menu, dropdowns, mobile drawer | Pages that load it |
| `js/daab-primary-nav.js` | Nav from `i18n/nav.json` | Same + consider `i18n/nav.json` |
| `js/daab-shell.js` | Language switcher placement | Same |
| `js/daab-i18n.js` | Routes, UI strings, search index | Same + `i18n/*.json` if needed |
| `i18n/nav.json`, `i18n/routes.json`, `i18n/ui.json` | Client-side i18n data | Pages using `daab-i18n.js` |

### Cache busting (`?v=`)

Shared assets are referenced with a version query:

```html
<link href="../css/daab-common.css?v=21" rel="stylesheet"/>
<script src="../js/daab-nav.js?v=8" defer></script>
```

When you change `daab-common.css` but only upload the CSS file (not HTML), browsers may keep an **old cached** copy if HTML still points at `?v=18`.

**Options:**

1. **Preferred:** Bump `?v=` in HTML and deploy **CSS/JS + all affected HTML** together.  
2. Run an inject helper (e.g. `helpers/_inject_global_search.py`) locally, commit HTML, deploy the batch.  
3. Ask testers to hard-refresh once after deploy (`Ctrl+Shift+R`).

---

## 6. Avoid unnecessary deployment

| Situation | Action |
|-----------|--------|
| Only `helpers/*.py` changed | Do not deploy; run helper, commit HTML output, deploy HTML |
| Only `documents/*.md` changed | Do not deploy |
| Local test edits reverted | Nothing to deploy |
| One typo on one page | Deploy that HTML file only (if `?v=` unchanged) |
| Shared CSS changed | Deploy CSS **and** every HTML with old `?v=` |

### Filter ship list from Git

Example: only assets under public trees:

```powershell
git diff --name-only HEAD -- css js az en index.html index-gateway.html 404.html i18n/search-index.json
```

Remove any path you intentionally exclude (e.g. `forum_2024/` until ready).

Save to a file for FTP/rsync:

```powershell
git diff --name-only origin/main | Where-Object { $_ -notmatch '^(helpers|documents|sources|\.cursor)/' } | Set-Content deploy-list.txt
```

---

## 7. Pre-deploy checklist

Run from repository root.

### 1. Identify changes

```powershell
git status
git diff --name-only HEAD
```

### 2. Build deploy list

- Include all **shared** CSS/JS you changed.  
- Include all HTML that reference **bumped** `?v=` values.  
- Include `i18n/search-index.json` if search changed.  
- Include `images/qr/` if profiles QR changed.  
- Exclude `helpers/`, `documents/`, `sources/`.

### 3. Validate

```powershell
python helpers/_validate_site.py
```

If scientists catalogue changed:

```powershell
python helpers/_validate_cv_cards.py
python helpers/_check_name_order.py
```

**Do not deploy if `_validate_site.py` reports errors.**

### 4. Local smoke test

Start server (`START-SITE.bat` or `python -m http.server 8010 --bind 127.0.0.1`), then open:

- http://localhost:8010/az/index.html  
- http://localhost:8010/en/index.html  
- http://localhost:8010/az/scientists/list.html  
- http://localhost:8010/az/scientists/profiles.html  

Check:

- Navigation at desktop, tablet, and mobile widths  
- Mobile menu open/close and dropdowns  
- Scientist filter toggle (expand/collapse, filters still apply when collapsed)  
- Global search (`Ctrl+K`) if deployed  
- Hard refresh after CSS/JS changes  

### 5. Upload to server

Preserve directory structure (`css/`, `js/`, `az/scientists/`, etc.).

### 6. Verify production

Repeat smoke test on `https://daab-waas.com/` (or your host). Test one AZ and one EN page on a phone.

---

## 8. Deployment methods

### Method A — Git tag + full public tree (safest)

1. Commit and merge to `main`.  
2. Tag: `git tag deploy-YYYY-MM-DD`.  
3. Upload **entire** ship set: `*.html`, `az/`, `en/`, `css/`, `js/`, `images/`, required `i18n/`.  
4. Omit `helpers/`, `documents/`, `sources/`.

Low risk of missing a dependent HTML file; slightly larger upload.

### Method B — Selective upload from diff

1. `git diff --name-only deploy-LAST..HEAD > deploy-list.txt`  
2. Edit list: remove non-ship paths.  
3. Add any **missing** shared dependencies (see §5).  
4. Upload only listed files.

Efficient; requires discipline on shared assets and `?v=`.

### Method C — CI / Git-connected host

GitHub Pages, Netlify, or similar: deploy from `main` branch root. Change tracking = git history; production always matches `main`.

### rsync example (SSH host)

```bash
rsync -av --files-from=deploy-list.txt ./ user@host:/var/www/daab-waas/
```

---

## 9. Git and GitHub best practices

| Practice | Why |
|----------|-----|
| One branch per feature | Smaller PRs, clearer deploy notes |
| Commit by area | e.g. `fix: align profiles filter toolbar with list` |
| PR description lists test URLs | Reviewers know what to verify |
| Tag every production deploy | `git diff tag..HEAD` = next upload list |
| Never deploy with failing `_validate_site.py` | Catches broken relative paths |
| Use lowercase `css/`, `js/` only | Linux hosting is case-sensitive |
| Do not commit secrets | No API keys in `js/` or HTML |

### Suggested release workflow

1. Develop on a feature branch.  
2. Run validators and local smoke test.  
3. Open PR → review **Files changed**.  
4. Merge to `main`.  
5. Tag `deploy-YYYY-MM-DD`.  
6. Upload to host (manual or CI).  
7. Note tag name in your deployment log (spreadsheet or GitHub Release).

---

## 10. Organizing shared DAAB components

| Concern | Location | Deploy? |
|---------|----------|---------|
| Design tokens, nav chrome | `css/daab-common.css`, `daab-mobile.css` | Yes |
| Navigation behaviour | `js/daab-nav.js`, `daab-primary-nav.js` | Yes |
| Nav structure / labels | `i18n/nav.json` | Yes (if used client-side) |
| Routes, UI strings | `i18n/routes.json`, `i18n/ui.json` | Yes |
| Page-specific CSS | `css/scientists-catalog-toolbar.css`, etc. | Yes |
| Maintenance | `helpers/_inject_*.py`, `_sync_primary_nav.py`, `_build_*.py` | No |

**Navigation and footer** are not a single reusable HTML file on the server today; they are repeated per page with shared CSS/JS. When updating nav:

1. Change shared CSS/JS and `i18n/nav.json` as needed.  
2. Run `python helpers/_sync_primary_nav.py` or embed helpers if you use static nav injection.  
3. Commit updated `az/` and `en/` HTML.  
4. Deploy HTML + assets together.

Long-term improvement: keep inject scripts idempotent and documented in [DAAB-Site-Python-and-JavaScript-Files.md](DAAB-Site-Python-and-JavaScript-Files.md).

---

## 11. Minimize production risk

| Risk | Mitigation |
|------|------------|
| Broken relative paths | `python helpers/_validate_site.py` before deploy |
| Stale browser cache | Bump `?v=` on changed CSS/JS; deploy matching HTML |
| Partial deploy (CSS only) | Deploy CSS + HTML together for shared assets |
| Wrong folder on server | Upload with paths intact; never flatten `az/` into root |
| Case mismatch (`JS/` vs `js/`) | Only lowercase `js/`, `css/` in repo and on server |
| Broken profiles HTML | Rebuild with `python helpers/_build_scientists_profiles.py`; validate structure |
| Rollback needed | Keep previous tag or zip of last good `css/`, `js/`, key HTML |

### Rollback

```powershell
git checkout deploy-2026-05-23 -- css/daab-common.css az/scientists/profiles.html
```

Then redeploy those files. Or restore entire tree from the tagged commit.

---

## 12. Quick reference commands

```powershell
cd "C:\Users\BSira\Documents\GitHub\DAAB-WAAS web site"

# What changed vs last commit
git status
git diff --name-only HEAD
git diff --stat HEAD

# What changed since last deploy tag
git diff --name-only deploy-2026-05-23..HEAD

# Ship-worthy paths only (example)
git diff --name-only HEAD -- css js az en index.html 404.html i18n/search-index.json

# Validate before upload
python helpers/_validate_site.py

# Local preview
.\START-SITE.bat
# Then: http://localhost:8010/az/index.html
```

---

## 13. Related maintenance commands

| Task | Command |
|------|---------|
| Rebuild scientist profiles | `python helpers/_build_scientists_profiles.py` |
| Inject collapsible catalogue toolbar | `python helpers/_inject_scientists_toolbar_mobile.py` |
| Rebuild search index | `python helpers/_build_search_index.py` |
| Inject global search on pages | `python helpers/_inject_global_search.py` |
| Sync primary nav | `python helpers/_sync_primary_nav.py` |

Always run `_validate_site.py` after generators change HTML or paths.

---

*Last updated: May 2026 — aligns with bilingual `az/` + `en/` layout and shared static asset pipeline.*
