# DAAB — one-page deploy checklist

**Site:** static HTML at repo root · **Production:** `https://daab-waas.com/`  
**Tools:** `.deployignore` · `scripts/deploy-rsync.sh` · `scripts/deploy-rsync.ps1` · `scripts/deploy-ftp.lftp`

---

## Before upload

| Step | Action | Pass? |
|------|--------|:-----:|
| 1 | `git status` — know what changed; tag release if needed (`deploy-YYYY-MM-DD`) | ☐ |
| 2 | `python helpers/_deploy_preflight.py` — **must be OK** (links, sitemap, scientists, artifacts) | ☐ |
| 3 | If `i18n/nav.json` changed: `python helpers/_build_search_index.py` then spot-check nav (runtime menu from JSON) | ☐ |
| 4 | If scientists changed: `_validate_cv_cards.py` + `_check_name_order.py` | ☐ |
| 5 | If shared CSS/JS changed: bump `?v=` on affected HTML and include **both** in upload | ☐ |
| 6 | Local smoke test: `START-SITE.bat` → `http://localhost:8010/az/index.html` + one EN page | ☐ |

---

## Ship these paths

| Include | Notes |
|---------|--------|
| `index.html` | Language gateway |
| `az/**/*.html` | All locale pages |
| `en/**/*.html` | All locale pages |
| `css/` | Full folder recommended |
| `js/` | Full folder + gallery JSON manifests |
| `images/` | Full tree (~1500 files) |
| `i18n/` | All JSON (nav, routes, ui, search, subtitles, design-system, profiles) |
| `sitemap.xml`, `robots.txt`, `404.html` | SEO + branded errors |
| `forum_2024/*.pdf` | Book download only |

---

## Do not upload

`helpers/` · `documents/` · `sources/` · `_archive/` · `node_modules/` · `scripts/` · `forum_2024/*.docx` · `.git/` · `.cursor/`

---

## Upload

| Method | Command |
|--------|---------|
| **rsync (Linux / WSL / Git Bash)** | Copy `scripts/deploy.env.example` → `scripts/deploy.env`, edit, then `./scripts/deploy-rsync.sh` |
| **rsync (Windows PowerShell)** | `.\scripts\deploy-rsync.ps1` |
| **FTP (lftp)** | Copy `scripts/deploy.env.example` → `scripts/deploy.env`, set `FTP_*` vars, then `./scripts/deploy-ftp.sh` |

Optional selective upload: `git diff --name-only deploy-TAG..HEAD` → filter with `.deployignore` rules → upload listed files only.

---

## After upload

| Step | Action | Pass? |
|------|--------|:-----:|
| 6 | Hard refresh production (`Ctrl+F5`) — clears stale CSS/JS cache | ☐ |
| 7 | Open `/az/index.html` and `/en/index.html` — nav, language switch | ☐ |
| 8 | Spot-check: scientists list + profiles, one forum page, membership application | ☐ |
| 9 | Phone/tablet: mobile menu + one inner page | ☐ |
| 10 | Forum book link on `/az/forum/2024/index.html` downloads PDF | ☐ |

---

## Rollback

Restore files from last good tag or backup, then re-upload:

```powershell
git checkout deploy-YYYY-MM-DD -- css/ js/ az/index.html
```

---

*May 2026 — see `documents/DAAB-Deployment-and-Change-Tracking-Guide.md` for full detail.*
