# DAAB / WAAS website

Static website for **Dünya Azərbaycanlı Alimlər Birliyi** (World Association of Azerbaijani Scientists).

## Bilingual site (Azerbaijani + English)

| Language | Address (local) | Address (live) |
|----------|-----------------|----------------|
| Azerbaijani | http://localhost:8010/az/ | https://daab-waas.org/az/ |
| English | http://localhost:8010/en/ | https://daab-waas.org/en/ |

Use **AZ | EN** in the top menu to switch language.  
Plain guide: [`documents/HOW-TO-USE-THE-BILINGUAL-SITE.md`](documents/HOW-TO-USE-THE-BILINGUAL-SITE.md)

## Open the site locally (fix for “This page isn’t working”)

**Double-click:** [`START-SITE.bat`](START-SITE.bat) in this folder.

That starts the web server and opens the site.  
Keep the black **“DAAB Server”** window open while you browse.

If you see **“This page isn’t working”**: the server is not running, or an old server is still on port 8010 — close it, then run `START-SITE.bat` again. Do not double-click HTML files (`file://`).

## Project structure

```
DAAB-WAAS web site/
├── css/                 Stylesheets (linked as css/… from HTML)
├── js/                  Client-side scripts (linked as js/… from HTML)
├── images/              Logos, photos, backgrounds
├── helpers/             Python maintenance tools (not deployed)
├── documents/           Internal documentation
├── cv/                  Individual CV HTML pages
├── *.html               Public site pages at repo root (lowercase names)
└── _pdf_extract.txt     Optional book text extract (helpers only)
```

## Conventions for new files

| File type | Place in |
|-----------|----------|
| `.css` | `css/` |
| `.js` | `js/` |
| Maintenance `.py` | `helpers/` (use `helpers/_paths.py` for `ROOT`) |
| `.html` (site pages) | Repository root; **lowercase** only (e.g. `activities_az.html`) |

See `css/README.md`, `js/README.md`, and `helpers/README.md` for details.

## Local preview

**Important:** If Chrome shows **“This page isn’t working”** for `http://127.0.0.1:8010`, the local server is not running.

```powershell
.\scripts\serve.ps1
# or: python -m http.server 8010
```

Then open http://127.0.0.1:8010/index.html (do not use `file://` for final testing).

In VS Code/Cursor: run task **“Start DAAB static server”** before **“Launch Chrome against localhost”**.

## Validate before deploy

```bash
python helpers/_build_bilingual_tree.py
python helpers/_publish_en_pages.py all
python helpers/_validate_bilingual.py
python helpers/_validate_site.py
python helpers/_validate_cv_cards.py
```

## Maintenance

```bash
python helpers/_rebuild_cv_catalog.py
```

- Tooling: `documents/DAAB-Site-Python-and-JavaScript-Files.md`
- Stability & deployment: `documents/DAAB-Site-Stability-and-Deployment-Guide.md`
