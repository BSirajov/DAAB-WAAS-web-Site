# DAAB / WAAS Website — Business Requirements Document (BRD)

Reverse-engineered from the current bilingual static website (May 2026).

**Document version:** 1.0  
**Date:** 30 May 2026  
**Status:** As-built requirements baseline for stakeholders, designers, and developers

---

## 1. Purpose of the website

The **Dünya Azərbaycanlı Alimlər Birliyi (DAAB)** / **World Association of Azerbaijani Scientists (WAAS)** official website is a bilingual, static web presence that serves the global community of Azerbaijani scientists and the broader public.

### 1.1 Institutional mission (as reflected on the site)

- Present the Association's **founding story**, **mission**, **governance**, and **charter**.
- Publish **news and activities**, with a dedicated **Forum 2024** microsite.
- Maintain a **directory and profile catalogue** of Azerbaijani scientists abroad.
- Explain **membership benefits and terms**, provide an **online application**, and support **invitation/sharing** via a printable flyer.
- Offer **AZ** and **EN** parity for international and diaspora audiences.

### 1.2 Target audience

| Audience | Primary needs met by the site |
|----------|------------------------------|
| General public & diaspora | Learn about DAAB/WAAS, Forum 2024, and activities |
| Potential members | Understand benefits, terms, apply online, receive invitations |
| Current members | Reference charter, board, news |
| Scientists listed in catalogue | Discoverable profiles, QR/deep links |
| Partner institutions | Forum cooperation, official addresses, roadmap |
| Press & researchers | Speeches, programme, presentations, galleries |
| Site maintainers | Predictable structure, i18n JSON, helper scripts |

### 1.3 Language and branding

- **Default language:** Azerbaijani (`az/`).
- **English mirror:** `en/` with WAAS branding in titles.
- **Configuration:** `i18n/routes.json`, `i18n/ui.json`, `i18n/nav.json`.

## 2. Website scope

### 2.1 Delivered site structure

| Area | AZ path prefix | EN path prefix | Page count (per locale) |
|------|----------------|----------------|-------------------------|
| Language gateway | `index.html` | `index.html` | 1 (shared) |
| Site core | `az/*.html` | `en/*.html` | 10 |
| Scientists | `az/scientists/` | `en/scientists/` | 2 |
| Forum 2024 | `az/forum/2024/` | `en/forum/2024/` | 12 |
| Embeds | `az/application/` | `en/application/` | 2 |

**Total mirrored content pages:** 26 × 2 locales = **52**, plus gateway and embed variants.

### 2.2 Technology scope

- Static HTML, CSS, JavaScript — no server-side application runtime in production.
- Client-side interactivity: search index, scientists filters, galleries, forms, PDF export.
- Content maintenance via HTML editing and Python helpers in `helpers/` (not deployed).

### 2.3 Out of scope (current implementation)

- Authenticated member portal or CMS admin UI.
- Server-side storage of membership applications (see storage strategy doc for future options).
- Automated machine translation; all copy is hand-maintained in AZ/EN pairs.

## 3. Stakeholders and user groups

| Stakeholder / user group | Role | Site expectations |
|--------------------------|------|-------------------|
| Visitor | Anonymous reader | Clear navigation, readable content, mobile access |
| Potential member | Prospective applicant | Benefits, terms, application, flyer share/print |
| Member scientist | Listed in catalogue | Accurate profile, QR/deep link, list + card views |
| Executive board | Governance visibility | Board page with photos and roles |
| Partner / institution | Forum cooperation | Official texts, roadmap, galleries |
| Content editor | Staff updating HTML/JSON | Consistent templates, rebuild scripts, validation |
| Web administrator | Deploy & cache | Ship az/, en/, css/, js/, images/, i18n/ only |
| Developer | Maintenance | Central tokens, route map, version bumps, validators |

## 4. Page-by-page requirements

Each row describes one logical page (AZ and EN mirrors share requirements). Paths are relative to the locale folder.

| Page | Paths (AZ / EN) | Nav group | Purpose | Main content blocks | Navigation elements | Interactive elements | Media | Functional reqs | Design reqs |
|------|-----------------|-----------|---------|---------------------|---------------------|----------------------|-------|-----------------|-------------|
| **Language gateway** | `index.html` | — | Entry point; redirect to AZ or EN home; optional explicit language choice | Brand logo; association title; AZ/EN action buttons; explanatory note | No primary nav; links to az/index.html and en/index.html | Auto-redirect via localStorage; ?choose=1 forces chooser; ?lang=az|en override | DAAB logo SVG | Must preserve query string on redirect; default language AZ | Centered card on site background; gateway gradient overlay |
| **Home** | `index.html` / `index.html` | — | Introduce DAAB/WAAS; route visitors to major sections via hub cards | Hero with title, subtitle, summary panel; intro strip; section card grid; join banner | Full top nav; breadcrumbs omitted; cards link to About, Scientists, Activities, Membership, Forum | Site search; language switcher; mobile hamburger menu; back-to-top | Brand logo; optional partner imagery in cards; diaspora body background | data-daab-page-id=home; JSON-driven nav when data-daab-nav-mount=1 | Hub card layout (daab-hub-cards.css); hero summary panel; Playfair + Inter typography |
| **Foundation of the Association** | `foundation.html` / `foundation.html` | about | Document founding history and Istanbul establishment narrative | Hero; page subtitle; long-form article sections; historical images | About dropdown; section nav (Foundation, Mission, Board, Charter); breadcrumbs | Language switch with scroll preservation; search | Historical photos (Şuşa congress, Istanbul founding, etc.) | Shared content-hero pattern; justified prose | Content hero + foundation-page.css; white content cards on patterned background |
| **News and activities** | `activities.html` / `activities.html` | activities | Publish association news, events, and activity timeline | Hero; timeline or news cards; dated entries; sidebar timeline widget | Activities dropdown; breadcrumbs; links to Forum 2024 hub | Sidebar timeline jumps (daab-sidebar-timeline.js); search | News thumbnails where present | Long scroll page; sticky chrome offsets | Activities layout CSS; card headers with blue gradient |
| **Scientists directory (list view)** | `scientists/list.html` / `scientists/list.html` | scientists | Tabular catalogue of Azerbaijani scientists abroad with sort/filter | Hero; toolbar (search, filters); sortable data table; row hover preview | Scientists dropdown; section nav (List, Profiles); breadcrumbs | Column sort; country/field filters; resizable columns; hover preview popover; mobile filter drawer | Scientist thumbnails in preview popover | scientists-catalog-data.js (~83 records); AZ/EN data files; collation for AZ alphabet | Catalogue toolbar; table layout; scientists-list-page.css |
| **Why become a member** | `membership_value.html` / `membership_value.html` | membership | Explain membership benefits and value proposition | Hero; benefit sections; CTA to application and terms | Membership dropdown landing; section nav (4 membership pages); breadcrumbs | CTA buttons; language switch | Iconography in benefit blocks | Membership funnel entry page | daab-membership-value.css; hero summary panel |
| **Mission, vision and values** | `mission.html` / `mission.html` | about | State organizational mission, vision, and core academic values | Hero; subtitle; mission/vision/value panels or sections | About dropdown landing; section nav; breadcrumbs | Language switch; search | Optional illustrative imagery in hero | About section landing page in nav.json | daab-content-hero.css + daab-mission-page.css |
| **Forum 2024 hub** | `forum/2024/index.html` / `forum/2024/index.html` | forum | Overview and entry point for all Forum 2024 materials | Hero; partner logos (DİDK, ETN); hub card grid to 11 subpages | Activities dropdown; forum section nav (12 pills); breadcrumbs | Card navigation; search | Partner logos; forum branding | Forum microsite root; not in top-level bar as separate item | Hub cards + forum section nav icons from ui.json navIcons |
| **Academic profiles catalogue** | `scientists/profiles.html` / `scientists/profiles.html` | scientists | Card-based CV profiles with search, filters, TTS, and deep linking | Hero; sticky filter toolbar; profile cards (photo, bio, fields, QR); pagination | Scientists dropdown; section nav; breadcrumbs; #slug deep links | Multi-filter search; sort; pagination; TTS read-aloud; QR codes; URL hash opens card | Portrait photos; QR per profile | scientists-cv-filters.js; daab-profile-tts.js; daab-profile-deep-link.js; sticky toolbar | Card grid; sticky toolbar on desktop; collapsible filters on mobile |
| **Membership terms** | `membership.html` / `membership.html` | membership | Define membership categories, fees, rights, and obligations | Hero; terms sections; fee tables; procedural text | Membership dropdown; section nav; breadcrumbs | Links to application and flyer | Minimal | Legal/informational reference for applicants | daab-membership-page.css + content hero |
| **Presentations and papers** | `forum/2024/presentations.html` / `forum/2024/presentations.html` | forum | Table of contents for forum presentations and paper titles | Hero; TOC sidebar; presentation entries with authors | Forum section nav; sidebar TOC jumps; breadcrumbs | Sidebar widget navigation | Minimal text TOC | Academic reference listing | daab-presentations-toc.css; sidebar widget |
| **Executive board** | `executive-board.html` / `executive-board.html` | about | Present leadership and board member profiles | Hero; board member cards with photos, roles, affiliations; QR codes on cards | About dropdown; section nav; breadcrumbs | QR scan opens profile or contact context (where configured) | Portrait photos; QR code images | Uses scientists-profile-qr.css patterns | Executive board grid; responsive card stack on mobile |
| **Membership application** | `application.html` / `application.html` | membership | Collect membership applications via multi-step online form | Hero; 4-step wizard (personal, academic, documents, review); progress indicator | Membership dropdown; section nav; breadcrumbs | Step navigation; field validation UI; progress bar (client-side) | Form UI only | daab-membership-application.js; embed variant at application/application.html for Google Sites | daab-membership-application.css; accessible form controls |
| **Official addresses** | `forum/2024/official.html` / `forum/2024/official.html` | forum | Publish formal opening addresses and official forum statements | Hero; speech/article cards; long-form justified text | Forum section nav; breadcrumbs; presentations-style TOC where used | In-page anchors; search | Speaker photos in speech layout | Long-form reading; print-friendly | daab-forum-content.css; daab-presentations-toc.css |
| **Charter (bylaws)** | `charter.html` / `charter.html` | about | Publish official charter articles for legal/governance reference | Hero; table-of-contents sidebar widget; numbered articles; annexes | About dropdown; section nav; in-page TOC links; breadcrumbs | Sidebar TOC jump links; language switch preserves section where possible | Minimal; text-focused legal document styling | Print-friendly article layout; anchor links per article | Legal document typography; daab-charter-page.css; sidebar widget |
| **Membership invitation flyer** | `membership_flyer.html` / `membership_flyer.html` | membership | Printable/shareable invitation for potential members | A4 flyer sheet (brand, pillars, benefits, youth, CTA, QR); page controls toolbar | Membership dropdown; section nav; standard site chrome above flyer | Print/PDF (single-page jsPDF export); Share (Web Share API or download + mailto); controls hidden from export | Logos; QR code; decorative flyer layout | html2canvas + jsPDF CDN; off-screen A4 clone; generatePdfBlob pipeline | daab-membership-flyer.css; A4 print/PDF fidelity requirements |
| **University rectors' speeches** | `forum/2024/rector_speeches.html` / `forum/2024/rector_speeches.html` | forum | Present rectors' forum contributions | Hero; speech sections with photos and attributed text | Forum section nav; breadcrumbs | Anchor navigation within speeches | Rector portrait photos (daab-speech-photos.css) | Static content page | Speech photo + text layout |
| **ANAS leadership speeches** | `forum/2024/anas_leadership_speeches.html` / `forum/2024/anas_leadership_speeches.html` | forum | Present ANAS leadership forum addresses | Hero; speech sections with photos | Forum section nav; breadcrumbs | Anchor links | Leadership photos | Static content page | Speech layout CSS |
| **Forum programme** | `forum/2024/program.html` / `forum/2024/program.html` | forum | Publish schedule and session structure of Forum 2024 | Hero; programme tables/sections by day or track | Forum section nav; breadcrumbs | Search; optional sidebar | Minimal | Reference schedule for participants and press | Forum content cards; tables where applicable |
| **Forum impressions** | `forum/2024/impressions.html` / `forum/2024/impressions.html` | forum | Share participant impressions and reflective essays | Hero; impression articles; photo-text layouts | Forum section nav; breadcrumbs | Search | Impression photos (daab-impressions-photos.css) | Static editorial content | Photo + prose layout |
| **Photo gallery** | `forum/2024/photos_gallery.html` / `forum/2024/photos_gallery.html` | forum | Browse categorized Forum 2024 photographs with lightbox | Hero; category sections; thumbnail grids; lightbox overlay | Forum section nav; breadcrumbs | Category expand; lazy-loaded thumbnails; lightbox prev/next; keyboard navigation | Hundreds of JPGs in images/photos-gallery/ with _thumbs variants | daab-photos-gallery.js; photos-gallery-manifest.json; thumbs manifest | daab-photos-gallery.css; responsive grid |
| **Video gallery** | `forum/2024/video_gallery.html` / `forum/2024/video_gallery.html` | forum | Link to Forum 2024 video recordings (YouTube) | Hero; video cards with titles and external links | Forum section nav; breadcrumbs | External YouTube links open in new tab | YouTube thumbnails / embed links | Static HTML; maintenance via helpers and video-gallery-data.json (build-time) | daab-video-gallery.css |
| **Strategic roadmap** | `forum/2024/roadmap.html` / `forum/2024/roadmap.html` | forum | Present post-forum strategic priorities and roadmap | Hero; roadmap cards; sidebar widget | Forum section nav; breadcrumbs | Sidebar jumps | Icons in roadmap cards | Policy/strategy communication | Forum content + sidebar widget |
| **Forum stories** | `forum/2024/stories.html` / `forum/2024/stories.html` | forum | Narrative stories related to Forum 2024 | Hero; story articles; timeline sidebar | Forum section nav; daab-sidebar-timeline.js; breadcrumbs | Timeline sidebar navigation; story TTS script exists but not wired on live page | Story imagery inline | Long-form narrative content | Forum content + timeline sidebar |
| **Contributions and cooperation** | `forum/2024/cooperation.html` / `forum/2024/cooperation.html` | forum | Document institutional contributions and cooperation outcomes | Hero; cooperation sections; justified long-form text | Forum section nav; breadcrumbs | Search | Optional inline images | Static content | Forum content cards |
| **Application embed (standalone)** | `application/application.html` / `application/application.html` | — | Embed membership form in external hosts (e.g. Google Sites) without full site chrome | Form wizard only | None (no site nav) | Same 4-step form logic as main application page | None | daab-application-embed-az.css / -en.css; relative asset paths for iframe | Minimal embed styling |
| **Membership value embed** | `application/membership_value.html` / `application/membership_value.html` | — | Embed membership value content externally | Benefit content without full shell | None | Minimal | Inline icons | daab-application-membership-value-embed.css | Embed-optimized typography |

### 4.1 Language/version requirements (all pages)

- Every public content page MUST exist in **both** AZ and EN with equivalent structure.
- `<html lang>` and `data-daab-lang` MUST match the folder (`az` or `en`).
- `data-daab-page-id` MUST match `i18n/routes.json` page id for i18n, breadcrumbs, and language pairing.
- Language switcher MUST open the alternate locale URL from `routes.json`.
- Legacy filenames MUST redirect via `legacyRedirects` in routes.json.

## 5. Navigation and information architecture

### 5.1 Top-level primary navigation

| Order | AZ label | EN label | Type | Landing / notes |
|-------|----------|----------|------|-----------------|
| — | Ana səhifə | Home | page | Landing: `home` |
| — | Fəaliyyətimiz | Activities | group | Landing: `activities` |
| ↳ | Yeniliklər | News | child | `activities` |
| ↳ | Forum 2024 | Forum 2024 | child | `forum-2024` |
| — | Alimlərimiz | Scientists | group | Landing: `scientists-list` |
| ↳ | scientists-list | scientists-list | child | `scientists-list` |
| ↳ | scientists-profiles | scientists-profiles | child | `scientists-profiles` |
| — | Haqqımızda | About us | group | Landing: `mission` |
| ↳ | Birliyin təsisi | Foundation | child | `foundation` |
| ↳ | Missiya və dəyərlər | Mission & values | child | `mission` |
| ↳ | executive-board | executive-board | child | `executive-board` |
| ↳ | Nizamnamə | Charter | child | `charter` |
| — | Üzvlük | Membership | group | Landing: `membership-value` |
| ↳ | Niyə üzv olmalı | Why become a member | child | `membership-value` |
| ↳ | Üzvlük şərtləri | Membership terms | child | `membership` |
| ↳ | Bizə qoşulun | Join us | child | `membership-application` |
| ↳ | Dəvət göndərin | Send invite | child | `membership-flyer` |

### 5.2 Forum 2024 section navigation

Forum subpages (12) are NOT separate top-level menu items. They appear in the **In this section** pill strip (`daab-section-nav`) and breadcrumbs when browsing `forum/2024/`.

| Page ID | AZ label | EN label |
|---------|----------|----------|
| `forum-2024` | Forum 2024 | Forum 2024 |
| `forum-official` | Rəsmi müraciətlər | Official addresses |
| `forum-rector-speeches` | Rektorlar | Rectors |
| `forum-anas-leadership-speeches` | AMEA rəhbərliyi | ANAS Leadership |
| `forum-program` | Proqram | Programme |
| `forum-2024-presentations` | Məruzələr | Presentations |
| `forum-impressions` | Təəssüratlar | Impressions |
| `forum-photos-gallery` | Foto qalereya | Photo gallery |
| `forum-video-gallery` | Video qalereya | Video gallery |
| `forum-roadmap` | Strateji yol xəritəsi | Strategic roadmap |
| `forum-bagli-hekayeler` | Hekayələr | Stories |
| `forum-cooperation` | Töhfələr | Contributions |

### 5.3 Other navigation mechanisms

| Mechanism | Implementation | Requirement |
|-----------|----------------|-------------|
| Breadcrumbs | `js/daab-breadcrumbs.js` | Show path from Home to current page |
| Section nav | `js/daab-section-nav.js` | Horizontal pills for About, Scientists, Membership, Forum |
| Hub cards | `daab-hub-cards.css` | Home and Forum hub discovery grids |
| Sidebar widgets | `daab-sidebar-widget.css` | TOC/timeline on charter, presentations, stories, activities |
| Skip link | First focusable control | Keyboard users skip to `#content` |
| Back to top | `daab-back-to-top.js` | Appears after scroll on long pages |
| Sticky chrome | `daab-sticky-chrome.js` | Nav + breadcrumbs stack; height CSS variables |
| Search | `daab-search.js` | Ctrl/Cmd+K overlay; `i18n/search-index.json` |

## 6. Content requirements

### 6.1 Text content

- Formal institutional tone; AZ primary, EN professional translation.
- Hero **page subtitle** from `i18n/page-subtitles.json` via `daab-page-subtitle.js`.
- Hero **summary panel** text from `i18n/page-panel-summaries.json` where configured.
- Long-form forum and charter text: justified prose, accessible heading hierarchy.
- Scientists data: names, affiliations, fields — synchronized between list and profiles.

### 6.2 Media content

| Content type | Location | Requirements |
|--------------|----------|--------------|
| Brand logos | `images/daab-logo.svg` | Consistent header/footer usage |
| Partner logos | Forum hub | DİDK, ETN SVG logos |
| Scientist portraits | `images/` scientist paths | Used in list preview and profile cards |
| Forum photos | `images/photos-gallery/` | Categorized; thumbnails in `_thumbs/` |
| Forum videos | YouTube URLs in HTML | Open externally; maintain titles AZ/EN |
| Site background | `images/diaspor-body-top-bg.png` | Top-faded pattern on all page bodies |
| QR codes | Profile/board cards | Link to profile deep URLs |

### 6.3 Downloadable / shareable materials

- Membership flyer: single-page PDF via Print/PDF and Share actions.
- Charter and long articles: browser print; print CSS hides chrome.
- No generic document library UI; PDFs linked inline where present.

## 7. Functional requirements

| ID | Feature | Requirement | Primary implementation |
|----|---------|-------------|------------------------|
| FR-01 | Site search | Overlay search with debounce; AZ character normalization | `daab-search.js`, `search-index.json` |
| FR-02 | Language switch | Pair pages via routes.json; persist preference | `daab-i18n.js`, `daab-shell.js` |
| FR-03 | Scroll preservation | Maintain section on language switch | `daab-lang-position.js` |
| FR-04 | Primary nav | JSON-driven menu with dropdowns | `daab-primary-nav.js`, `nav.json` |
| FR-05 | Mobile nav | Hamburger, scroll lock, tap dropdowns | `daab-nav.js`, `daab-mobile.js` |
| FR-06 | Scientists list filters | Sort, filter, preview, resize columns | `scientists-list-preview.js`, catalog data JS |
| FR-07 | Scientists profile filters | Multi-filter, pagination, badge sync | `scientists-cv-filters.js` |
| FR-08 | Profile deep link | URL `#slug` opens matching card | `daab-profile-deep-link.js` |
| FR-09 | Profile TTS | Read profile text via Web Speech API | `daab-profile-tts.js` |
| FR-10 | Photo gallery | Categories, lazy load, lightbox | `daab-photos-gallery.js` + manifests |
| FR-11 | Video gallery | Curated YouTube links | Static HTML |
| FR-12 | Membership form | 4-step wizard, client validation UI | `daab-membership-application.js` |
| FR-13 | Flyer PDF | Single-page A4 PDF, layout preserved | `daab-membership-flyer-email.js` |
| FR-14 | Flyer share | Web Share API or download + mailto fallback | Same module |
| FR-15 | Sidebar timeline | Section jumps on activities/stories | `daab-sidebar-timeline.js` |
| FR-16 | Legacy redirects | Old root filenames → az/ paths | Hosting / routes.json map |
| FR-17 | Path validation | CI/local check for broken refs | `helpers/_validate_site.py` |

## 8. UI/UX requirements

### 8.1 Design system

- **Tokens:** `css/daab-tokens.css` (colors, typography, spacing, shadows, z-index).
- **Fonts:** Playfair Display (headings), Inter (body/UI) via Google Fonts.
- **Colors:** Blue palette (`--blue-700` primary), white/light blue surfaces, gold accents.
- **Background:** Diaspora pattern + soft scrim on all bodies (`daab-site-background.css`).

### 8.2 Layout patterns

| Pattern | Usage | Key CSS |
|---------|-------|---------|
| Standard shell | Most pages | `daab-common.css`, sticky chrome |
| Content hero | About, membership | `daab-content-hero.css` |
| Hub cards | Home, Forum hub | `daab-hub-cards.css` |
| Forum article | Forum inner pages | `daab-forum-content.css` |
| Data table | Scientists list | `daab-scientists-list-page.css` |
| Profile cards | Scientists profiles | `daab-scientists-profiles-page.css` |
| Flyer sheet | Membership flyer | `daab-membership-flyer.css` |

### 8.3 Accessibility requirements

- Skip-to-content link on main pages.
- `aria-current`, `aria-expanded`, and keyboard-operable nav dropdowns.
- Visible focus rings on interactive controls.
- Sufficient color contrast on body text; hero scrim preserves readability over background.
- `prefers-reduced-transparency`: simplified background gradient.
- Form labels and step indicators on membership application.

## 9. Responsive and browser compatibility requirements

- **Viewport:** `width=device-width, initial-scale=1.0, viewport-fit=cover` on all pages.
- **Breakpoints:** Nav compact ~1180px; sidebar stack ~1060px (`design-system.json`).
- **Mobile:** Hamburger menu, collapsible filters, stacked heroes, touch-friendly targets (`daab-mobile.css`).
- **Tablets:** Section nav horizontal scroll; scientists sticky toolbar behavior.
- **Browsers:** Chrome, Edge, Firefox, Safari (desktop and mobile) — static HTML/CSS/ES5+ compatible scripts.
- **PDF/print:** Flyer export tested via jsPDF; browser print as fallback with print-specific CSS.

## 10. Non-functional requirements

| Category | Requirement |
|----------|-------------|
| Maintainability | Central i18n JSON, shared CSS modules, helper scripts for regeneration |
| Performance | Lazy-loaded gallery thumbs; cache-busting `?v=` on shared CSS/JS |
| Accessibility | WCAG-oriented patterns (skip link, ARIA, focus, reduced transparency) |
| SEO readiness | `<title>`, meta description, canonical where set, semantic headings |
| Code cleanliness | Lowercase paths; no duplicate root css/js; validators after changes |
| Naming consistency | Page IDs in routes.json; lowercase HTML filenames |
| Reusable styles | Tokens + common.css; page CSS extends rather than duplicates |
| Dead code avoidance | Audit before removal; documented unused assets (story TTS) |

## 11. Content management and maintenance requirements

### 11.1 Adding or updating content

| Content type | Recommended workflow |
|--------------|---------------------|
| New static page | Add AZ+EN HTML; register in `routes.json` and `nav.json`; add ui labels |
| Nav label change | Edit `i18n/ui.json` only (not duplicated in HTML) |
| Scientist record | Update catalog JS + regenerate profiles via `helpers/_rebuild_cv_catalog.py` |
| Forum speech/article | Edit HTML or rebuild from docx via `helpers/_build_*` |
| Photo gallery | Add images under `images/photos-gallery/`; update manifests; run thumb helper |
| Membership form fields | Edit HTML + `daab-membership-application.js` together |
| Shared design change | Edit tokens/common CSS; bump `?v=` via `_site_wide_cleanup.py` |

### 11.2 Quality gates before publish

```bash
python helpers/_validate_site.py
python helpers/_validate_cv_cards.py
python helpers/_check_name_order.py
python helpers/_audit_repo_health.py
```

## 12. Deployment requirements

### 12.1 Include in production bundle

| Path | Purpose |
|------|---------|
| `index.html` | Language gateway / redirect |
| `az/`, `en/` | All public HTML pages |
| `css/` | Stylesheets |
| `js/` | Client scripts and JSON manifests used at runtime |
| `images/` | Photos, logos, gallery assets |
| `i18n/` | routes, ui, nav, search index, subtitles |
| `cv/` | Standalone CV HTML if linked publicly |

### 12.2 Exclude from production

| Path | Reason |
|------|--------|
| `helpers/` | Python maintenance only |
| `documents/` | Internal documentation |
| `sources/`, `_archive/` | Prototypes and backups |
| `Deployment/`, `.deployment-staging/` | Local staging copies |
| `node_modules/`, `__pycache__/` | Dev artifacts |

### 12.3 Hosting rules

- Serve from site root with **case-sensitive** paths (Linux/GitHub Pages).
- Use HTTPS for production; required for embeds and modern APIs (Web Share).
- After deploy, hard-refresh or rely on bumped `?v=` to clear CSS/JS cache.

## 13. Open issues and recommendations

| # | Issue | Impact | Recommendation |
|---|-------|--------|----------------|
| 1 | `daab-story-tts.js` not linked on `stories.html` | Feature incomplete | Wire script or remove unused CSS/JS |
| 2 | `daab-forum-book.css` unused in live HTML | Dead asset | Keep for build pipeline or archive |
| 3 | Membership application has no server-side submit | Data not persisted | Implement backend or form service per storage strategy doc |
| 4 | Large scientists profiles HTML | Maintenance cost | Continue generator-based updates only |
| 5 | `Deployment/` folder may lag source versions | Stale preview | Deploy from repo root, not Deployment snapshot |
| 6 | Forum video data partly build-time | Manual sync risk | Document update steps in video gallery helper |
| 7 | Residual legacy URL bookmarks | 404 off-site | Maintain redirects; communicate new `/az/` `/en/` paths |
| 8 | Full unused CSS/JS audit deferred | Bundle size | Run `_audit_css_usage.py` per stylesheet |
| 9 | Manual QA checklist incomplete | Release risk | Complete keyboard/tablet QA from pre-release doc |
| 10 | Google Sites embed constraints | iframe/X-Frame-Options | Test embed URLs after each path change |

---

*End of document — generated from live site structure May 2026.*
