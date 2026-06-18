# Stylesheets

Shared and page-specific CSS for the DAAB static site.

## Core (include on most pages)

| File | Purpose |
|------|---------|
| `daab-common.css` | Global design system (inlined bundles: tokens, site background, sticky chrome, etc.). |
| `daab-mobile.css` | Mobile/touch layer: safe areas, scroll lock, hamburger, landscape. |
| `daab-site-background.css` | **Source** for site-wide `body::before` background (`images/diaspor-body-top-bg.png`). Content is synced into `daab-common.css`; edit here first, then re-inline or bump `daab-common.css`. |

**HTML reference (from `az/` or `en/`):**

```html
<link href="../css/daab-common.css?v=72" rel="stylesheet"/>
<link href="../css/daab-mobile.css?v=13" rel="stylesheet"/>
```

Image URLs inside `daab-common.css` use `../images/` (relative to `css/`).

## Page-specific (linked from matching HTML only)

Examples: `daab-scientists-profiles-page.css`, `daab-forum-content.css`, `daab-membership-application.css`, `daab-work-done-report.css`.

## Build-only / not linked from live HTML

These are kept for future pages or legacy layouts; safe to omit from deploy unless a page links them:

- `daab-encyclopedia-page.css`
- `daab-forum-book.css`
- `daab-membership-page.css` (legacy membership layout; `membership.html` redirects to `membership_value.html`)
- `daab-prominent-figure-profile.css`

**Related:** client scripts in `../js/`; maintenance tools in `../helpers/`. Deploy exclusions: see `../.deployignore` and `helpers/_deploy_assets.py`.
