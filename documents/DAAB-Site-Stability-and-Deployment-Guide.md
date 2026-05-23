# DAAB site — stability, deployment, and long-term maintenance

This guide explains why the site sometimes shows **“This page isn’t working”** (Chrome/Edge) or similar errors, and how to keep the project reliable as files are renamed, refactored, or embedded in Google Sites.

---

## 1. What “This page isn’t working” usually means

That browser message is **not** a normal “broken CSS” or “404 image” problem. It almost always means the **browser could not load the page at all** from the URL you opened.

| Symptom | Typical cause |
|--------|----------------|
| Chrome: “This page isn’t working” / `ERR_CONNECTION_REFUSED` | Local server not running on port 8010 |
| Same error with server “running” in terminal | On Windows, default `http.server` may listen on IPv6 only — use `--bind 127.0.0.1` and open **http://localhost:8010/** (not a dead `127.0.0.1` if IPv4 is not bound) |
| `ERR_EMPTY_RESPONSE` / `ERR_CONNECTION_RESET` | Server crashed, wrong port, firewall, or preview tool stopped |
| Blank page after deploy | Wrong hosting root (files not at site root), or deploy failed |
| Works on PC, fails on phone | Cached old HTML pointing to deleted filenames |
| Worked yesterday, broken today | Renamed HTML without updating links; or embed URL still points to old path |
| Google Sites embed broken | iframe URL wrong, http/https mix, or host blocking embed |

**Important:** Editing HTML/CSS/JS in the repo does **not** by itself cause this error unless you also break **how the site is served** (server down, wrong URL, or hosting misconfiguration).

---

## 2. Root causes seen in this project

### 2.1 Local preview without a web server

- **VS Code/Cursor** `launch.json` opens `http://127.0.0.1:8010/index.html`.
- If no server is running on port **8010**, Chrome shows **“This page isn’t working”**.
- Opening `index.html` via **file://** avoids that error but can cause other issues (relative paths, CORS, some scripts).

**Fix:** Always start the static server before using the debugger or that URL (see §5).

### 2.2 Filename and path churn (renames)

The site went through several naming schemes (`Scientists_AZ.html` → `scientists_az.html` → `scientists_list_view_az.html`). Any of these leave breakage if:

- Navigation `href`s were not updated everywhere
- Bookmarks or Google Sites embeds still use old URLs
- Git on Windows hid case-only renames (works locally, fails on Linux hosting)

### 2.3 Case-sensitive paths (Linux hosting)

Hosted on **GitHub Pages**, **Netlify**, or Linux VPS:

- `js/daab-nav.js` ≠ `JS/daab-nav.js`
- `cv/page.html` ≠ `CV/page.html`
- `images/Scientists_Photos/` ≠ `images/scientists-photos/`

Windows often treats these as the same folder; **production does not**.

### 2.4 Duplicate or misplaced assets

Avoid:

- Second copies of `daab-common.css` or `daab-nav.js` at repo root (deleted in the past but easy to reintroduce)
- Editing files in a wrong folder (e.g. `JS/` vs `js/` on a case-sensitive clone)
- Python helpers writing HTML with old paths after a rename

### 2.5 Very large HTML pages

`scientists_card_view_az.html` is thousands of lines. That rarely causes “This page isn’t working”, but it can cause **slow load** or browser tab freeze. Prefer regenerating via `helpers/_rebuild_cv_catalog.py` instead of hand-editing huge blocks.

### 2.6 Google Sites embedding

If the public site is an **iframe** to `https://daab-waas.com/...` or GitHub Pages:

- Embed URL must be **exact** (including filename and lowercase)
- **HTTPS** embed target required for HTTPS Sites
- Some hosts send `X-Frame-Options: DENY` — page works when opened directly but not in iframe
- Google Sites cannot host this repo’s files locally; it only **links/embeds** a real URL

### 2.7 Cache

Browsers cache HTML/CSS/JS. After renames, users may still request old assets → 404s (usually partial breakage, not “isn’t working”). Use **cache-busting** query strings (`?v=6`) on shared CSS/JS when you change them.

### 2.8 Deploying the wrong folder

Only deploy the **site root** contents:

- `*.html`, `css/`, `js/`, `images/`, `cv/` (if public)

Do **not** require `helpers/`, `documents/`, `_pdf_extract.txt` for the live site.

---

## 3. Recommended project structure (stable layout)

```
DAAB-WAAS web site/
├── index.html                    # Site entry (lowercase names only)
├── *_az.html                     # Other public pages at repo root
├── css/
│   ├── daab-common.css           # Global design system
│   ├── daab-mobile.css           # Mobile/touch layer
│   └── scientists-catalog-toolbar.css
├── js/
│   ├── daab-nav.js
│   ├── daab-mobile.js
│   ├── scientists-catalog-data.js
│   └── scientists-cv-filters.js
├── images/                       # Web paths: images/...
├── cv/                           # Optional standalone CV HTML (lowercase)
├── helpers/                      # Python — NOT deployed
├── documents/                    # Internal docs — NOT deployed
└── scripts/                      # serve.ps1, optional tooling
```

**Rules:**

| Type | Location |
|------|----------|
| `.css` | `css/` only |
| `.js` | `js/` only (never `JS/` on git/Linux) |
| Maintenance `.py` | `helpers/` |
| Public `.html` | Repository root, **lowercase** filenames |
| Photos for site | `images/` with stable lowercase path segments where possible |

---

## 4. Best practices for HTML, CSS, JS, and assets

### HTML

- One **canonical** shared nav/footer pattern; same asset links on every page:
  - `css/daab-common.css?v=N`
  - `css/daab-mobile.css?v=N`
  - `js/daab-nav.js?v=N`
  - `js/daab-mobile.js?v=N`
- Use **relative** paths from site root: `css/...`, `js/...`, `images/...` (not absolute `C:\...`).
- Internal links: `href="scientists_list_view_az.html"` (no leading `/` unless you always host at domain root and understand subpaths).
- After renames, run **`python helpers/_validate_site.py`**.

### CSS

- Shared rules in `daab-common.css`; mobile in `daab-mobile.css`; avoid duplicating nav CSS in every page.
- `url(../images/...)` from `css/` is correct; do not move CSS without fixing those URLs.
- Bump `?v=` when changing shared CSS so caches refresh.

### JavaScript

- Load order on CV page: `scientists-catalog-data.js` **before** `scientists-cv-filters.js` (data file without `defer` if filters run on DOMContentLoaded).
- No build step required today; keep scripts small and in `js/`.
- Do not fork duplicates into inline `<script>` unless necessary.

### Images

- Prefer **lowercase** filenames and folders for new assets (`images/scientists-photos/`).
- Avoid spaces in paths when possible (encode as `%20` if unavoidable).
- Large photos: reasonable dimensions for web (performance).

---

## 5. Local development and testing workflow

### Start the server (required for `localhost:8010`)

From repository root:

```powershell
# PowerShell
.\scripts\serve.ps1
```

or:

```bash
python -m http.server 8010
```

Then open:

- http://127.0.0.1:8010/index.html  
- http://127.0.0.1:8010/scientists_list_view_az.html  
- http://127.0.0.1:8010/scientists_card_view_az.html  

**Do not** rely on double-clicking HTML files for final testing.

### VS Code / Cursor

Use task **“Start DAAB static server”** before **“Launch Chrome against localhost”** (see `.vscode/tasks.json`).

### Quick manual smoke test (after every change)

1. Home → nav → each main section opens (no 404)
2. Scientists dropdown: list + card views
3. Mobile width (DevTools): menu, search overlay, filters
4. Hard refresh: `Ctrl+Shift+R` (Windows) / `Cmd+Shift+R` (Mac)

---

## 6. Validate changes before deployment

Run from repo root:

```bash
python helpers/_validate_site.py
python helpers/_validate_cv_cards.py
python helpers/_check_name_order.py
```

`_validate_site.py` checks:

- Local HTML links and asset references exist
- Required shared CSS/JS on main pages
- Risky path casing (`CV/`, `JS/`)
- Links to obsolete filenames (common old names)

**Gate:** Do not deploy if `_validate_site.py` exits with errors.

Optional later upgrades:

- **html-validate** or **lychee** link checker in CI
- **GitHub Action** that runs validators on every push
- **Playwright** smoke test (open index + scientists pages)

---

## 7. Browser cache and hosting

### Cache busting

When you change shared assets, increment version query:

```html
<link href="css/daab-common.css?v=7" rel="stylesheet"/>
<script src="js/daab-nav.js?v=4" defer></script>
```

Tell editors to hard-refresh after deploy.

### GitHub Pages

- Publish from **`main`** branch, folder **`/` (root)** or `/docs` if you move site there — pick one and keep consistent.
- Repo name with spaces becomes awkward URLs; custom domain `daab-waas.com` is fine if DNS points correctly.
- **Case-sensitive paths** — test on Linux CI.

### Google Sites

- Prefer **link** (“Open in new tab”) to full site URL rather than iframe when possible.
- If embedding: use **HTTPS** URL to the real host; test iframe in incognito.
- After renames, update **every** embed/link in Google Sites manually.
- Google Sites cannot run this repo; it only points to your hosted copy.

---

## 8. Error logging and debugging

| Layer | What to do |
|-------|------------|
| Browser | F12 → **Network**: red 404/500 on `document` or `index.html` = wrong URL/server |
| Browser | **Console**: JS errors (broken page features, not always “isn’t working”) |
| Local | Confirm server: `curl -I http://127.0.0.1:8010/index.html` → `200 OK` |
| Hosting | Check host dashboard (GitHub Pages build failed, DNS, SSL) |
| Paths | Run `python helpers/_validate_site.py` |

There is no server-side log for pure static hosting unless you add analytics (Plausible, GA4) or a host with access logs.

---

## 9. Safe refactor and rename procedure

1. **Choose new lowercase name** (e.g. `scientists_list_view_az.html`).
2. **Rename file** (two-step on Windows git: `git mv old tmp && git mv tmp new`).
3. **Replace references** in all `*.html`, `js/`, `helpers/*.py`, `documents/`, `.cursor/rules/`.
4. Run **`python helpers/_validate_site.py`**.
5. Run scientists validators if catalogue touched.
6. **Bump `?v=`** on shared CSS/JS if behavior changed.
7. Test on **http://127.0.0.1:8010** (all nav links).
8. Deploy; update **Google Sites** / bookmarks / printed QR codes.
9. Optional: server **301 redirects** from old names (`.htaccess`, Netlify `_redirects`, Cloudflare rules).

---

## 10. Google Sites — minimize embedding issues

| Approach | Pros | Cons |
|----------|------|------|
| Link out to `https://daab-waas.com/...` | Most reliable | Leaves Google Sites chrome |
| iframe embed | Looks integrated | Blocked by headers, sizing, mobile scroll |
| Upload HTML to Sites | — | **Not supported** for this multi-file site |

**Recommendations:**

- Host the full site on **daab-waas.com** or GitHub Pages.
- On Google Sites, use prominent **buttons/links** to the real site.
- If using iframe: test on phone; set width 100%; avoid nested scroll fights.
- Never point embed at `localhost` or `file://`.
- Keep one **canonical** home URL and document it in Sites.

---

## 11. Modern practices and tools (roadmap)

Today the site is **static HTML + CSS + JS** (no bundler). That is fine if discipline is maintained.

**Short term (low cost, high value)**

- `helpers/_validate_site.py` before every deploy ✅
- `scripts/serve.ps1` + VS Code task ✅
- `.gitignore` for `__pycache__`, editor junk ✅
- Version query on shared assets ✅
- This guide + file-organization Cursor rule ✅

**Medium term**

- **GitHub Action**: run validators on push
- **`_redirects` / `.htaccess`** for old filenames
- Consolidate inline page CSS into shared files slowly
- **Single data source** for scientists (JSON → generate HTML/JS) to avoid sync bugs

**Long term (if the site grows)**

- **Eleventy (11ty)** or **Astro** — components, includes, one nav partial
- **npm scripts**: `npm run build`, `npm run validate`, `npm run preview`
- **Staging** subdomain (`staging.daab-waas.com`) for preview before production
- **CDN** for images; **responsive images** (`srcset`)

---

## 12. Deployment checklist (printable)

- [ ] `python helpers/_validate_site.py` — no errors  
- [ ] `python helpers/_validate_cv_cards.py` — 83 cards OK  
- [ ] Local server smoke test on port 8010  
- [ ] All nav links and scientists dropdown tested  
- [ ] Mobile menu + search tested  
- [ ] Shared CSS/JS `?v=` bumped if those files changed  
- [ ] No secrets in repo (emails public OK)  
- [ ] Deploy only: html, css, js, images, cv  
- [ ] Google Sites / DNS URLs updated after renames  
- [ ] Hard refresh or incognito check on live URL  

---

## Related files

- `README.md` — quick start  
- `documents/DAAB-Site-Python-and-JavaScript-Files.md` — scripts reference  
- `.cursor/rules/daab-file-organization.mdc` — where to put new files  
- `helpers/_validate_site.py` — automated link/path checks  
