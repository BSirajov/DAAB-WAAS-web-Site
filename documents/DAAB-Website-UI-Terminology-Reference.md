# DAAB / WAAS Website — UI Terminology Reference

Shared vocabulary for the bilingual static site (`az/` and `en/`). Use the **official name** in prompts, tickets, and reviews. CSS classes and IDs are included so developers can locate elements quickly.

**Live preview:** run `START-SITE.bat` or `python -m http.server 8010 --bind 127.0.0.1`, then open `http://localhost:8010/index.html`.

---

## 1. How to use this guide

| Do | Don't |
| --- | --- |
| “Increase padding in the **hero summary panel** (`.hero-panel` / `.panel-card`).” | “Fix the box on the right under the title.” |
| “Move the **Forum breadcrumbs bar** above the hero on mobile.” | “Fix the grey strip under the menu on forum pages.” |
| “Add a link to the **Activities timeline sidebar widget**.” | “Put it in the left menu on the news page.” |

When referring to language-specific labels, give **both** AZ and EN if the instruction is about visible text; otherwise refer to the **official element name** (language-neutral).

---

## 2. Page layout overview

Most inner pages follow this vertical stack (home and hub pages omit breadcrumbs; some pages add a left column):

```
┌─────────────────────────────────────────────────────────────┐
│  SKIP LINK (keyboard only, off-screen until focused)        │
├─────────────────────────────────────────────────────────────┤
│  TOP CHROME (#daab-top-chrome) — fixed while scrolling      │
│    • Primary navigation bar (.nav-strip)                    │
│    • Breadcrumbs bar (.daab-breadcrumbs / .forum-breadcrumbs)│
├─────────────────────────────────────────────────────────────┤
│  CHROME SPACER (#daab-chrome-spacer) — reserves layout space│
├─────────────────────────────────────────────────────────────┤
│  HERO / PAGE HERO (.hero / .page-hero)                      │
│    • Page title (h1) + page hero subtitle                   │
│    • Hero summary panel (.hero-panel / .hero-summary-panel) │
├─────────────────────────────────────────────────────────────┤
│  OPTIONAL: Section navigation strip (.daab-section-nav)     │
├─────────────────────────────────────────────────────────────┤
│  MAIN CONTENT (#content)                                    │
│    • Single column, or content-wrap (sidebar + main)        │
├─────────────────────────────────────────────────────────────┤
│  SITE FOOTER (.footer-pro)                                  │
├─────────────────────────────────────────────────────────────┤
│  FLOATING: Back-to-top button (.daab-back-to-top)           │
│  OVERLAY: Site search modal (#search-overlay)               │
└─────────────────────────────────────────────────────────────┘
```

**Content width:** most blocks sit inside `.shell` (max-width container).

---

## 3. Global chrome (every page)

| Official name | CSS / HTML | Purpose | Where | Example instruction |
| --- | --- | --- | --- | --- |
| **Skip link** | `a.skip` → `#content` | Keyboard shortcut to main content; first focusable control. | All main pages | “Ensure the **skip link** remains the first tab stop on `charter.html`.” |
| **Top chrome shell** | `#daab-top-chrome` | Fixed wrapper for nav + breadcrumbs; mounted by `daab-sticky-chrome.js`. | All pages except language gateway | “Reduce **top chrome** height on mobile when breadcrumbs are hidden.” |
| **Chrome spacer** | `#daab-chrome-spacer` | In-flow placeholder matching fixed chrome height. | Same as top chrome | “Verify **chrome spacer** height matches nav + breadcrumbs after font change.” |
| **Primary navigation bar** | `nav.nav-strip` | Site-wide top menu: logo, brand text, section links, search, language switcher. | All main pages | “Highlight the active item in the **primary navigation bar** on Forum pages.” |
| **Navigation inner row** | `.nav-inner` | Flex row holding logo, brand, menu, utilities. | Inside `.nav-strip` | “Align **nav inner row** items vertically on tablet.” |
| **Brand logo link** | `.page-logo` → `.nav-brand-logo` | Clickable DAAB/WAAS logo returning to home. | Nav bar left | “Set **brand logo** max height to 52px on mobile.” |
| **Brand text link** | `.nav-brand` → `.nav-brand-text` | Organization name beside logo (wraps on small screens). | Nav bar | “Shorten **brand text** line break on EN home only.” |
| **Primary nav menu** | `#primaryNavMenu.nav-menu` | Container for top-level links and dropdowns; rebuilt from `i18n/nav.json`. | Nav bar | “Add a new item to the **primary nav menu** under Activities.” |
| **Nav link** | `a.nav-link` | Top-level menu item (Home, or dropdown toggle). | Nav menu | “Set **nav link** ‘Home’ as active on `index.html`.” |
| **Nav dropdown** | `.nav-dropdown` | Flyout group (Activities, Scientists, About, Membership). | Nav menu | “Keep **nav dropdown** open on hover for desktop.” |
| **Nav dropdown toggle** | `.nav-dropdown-toggle` | Button that opens a dropdown panel. | Each dropdown | “Increase touch target on **nav dropdown toggle**.” |
| **Nav dropdown panel** | `.nav-dropdown-panel` | Mega-menu panel with titled links. | Below toggle | “Add Forum 2024 link description in **nav dropdown panel**.” |
| **Nav dropdown link** | `.nav-dropdown-link` | Individual destination inside a dropdown (title + desc). | Dropdown panel | “Reorder **nav dropdown links** under Scientists.” |
| **Nav divider** | `.nav-divider` | Visual separator before first nav link. | Start of `#primaryNavMenu` | “Hide **nav divider** on mobile drawer.” |
| **Mobile menu toggle (hamburger)** | `.mobile-menu-toggle` | Opens/closes full-screen mobile nav drawer (`#primaryNavMenu`). | Nav bar; visible ≤1180px | “Fix **hamburger menu** so it closes after link tap.” |
| **Mobile nav drawer** | `#primaryNavMenu` (open state) | Stacked nav links when hamburger is expanded—not a separate DOM tree. | Mobile / narrow viewport | “Scroll **mobile nav drawer** independently when menu is long.” |
| **Site search button** | `#nav-search-btn.nav-search-btn` | Opens global search overlay; injected by `daab-search.js`. | Nav bar right area | “Move **site search button** left of language switcher.” |
| **Language switcher** | `.daab-lang-switch` | AZ / EN flag toggle; links to mirrored page in other language. | Nav bar | “Ensure **language switcher** keeps current page path when switching.” |
| **Language flag link** | `.daab-lang-link` + `.daab-lang-flag` | Individual language option (screen-reader code in `.daab-lang-code`). | Inside switcher | “Highlight active **language flag link** with stronger border.” |

---

## 4. Breadcrumbs

| Official name | CSS / HTML | Purpose | Where | Example instruction |
| --- | --- | --- | --- | --- |
| **Breadcrumbs bar** | `#daab-breadcrumbs` or `nav.daab-breadcrumbs` | Dynamic trail: Home › section › current page; built by `daab-breadcrumbs.js`. | Most inner pages (not home) | “Hide **breadcrumbs bar** on membership application step 2.” |
| **Forum breadcrumbs bar** | `.breadcrumbs.forum-breadcrumbs` | Static or enhanced trail including Activities › Forum 2024 › subpage. | All `forum/2024/*` pages | “Update **Forum breadcrumbs bar** label for Photos gallery (EN).” |
| **Breadcrumb current page** | `.forum-breadcrumbs-current` | Non-link label for active page. | Last segment of forum breadcrumbs | “Shorten **breadcrumb current page** text on mobile.” |

**Distinction — breadcrumbs vs section nav vs sidebar:** The **breadcrumbs bar** shows *where you are in the site hierarchy* (top, under nav). The **section navigation strip** (`.daab-section-nav`) shows *sibling pages within one section* (e.g. Membership). The **sidebar widget** (`.sidebar` / `.sidebar-widget`) is a *left column tool* (timeline, forum links, photo categories)—not site hierarchy.

---

## 5. Hero area

| Official name | CSS / HTML | Purpose | Where | Example instruction |
| --- | --- | --- | --- | --- |
| **Hero region (standard)** | `header.hero` + `.hero-wrap.shell` | Top banner: page title, subtitle, summary panel. | Mission, charter, executive board, home, etc. | “Reduce **hero region** bottom margin on `mission.html`.” |
| **Page hero region** | `header.page-hero` | Variant used on Activities and some forum pages. | `activities.html`, some forum pages | “Match **page hero region** typography to standard hero.” |
| **Hero copy column** | `.hero-copy` | Left column: `h1` + subtitle. | Inside hero | “Left-align **hero copy column** on mobile.” |
| **Page title** | `h1` in hero | Main page heading (Playfair Display). | Hero left column | “Change **page title** on EN charter to ‘Charter’.” |
| **Page hero subtitle** | `.page-hero-subtitle` `#page-hero-subtitle` | One-line summary under title; text from `i18n/page-subtitles.json`. | Most pages with hero | “Update **page hero subtitle** for scientists profiles (AZ).” |
| **Hero actions row** | `.hero-actions` | Primary/secondary CTA buttons below subtitle. | Home page only | “Add third button to **hero actions row** on home.” |
| **Hero summary panel** | `.hero-panel` + `.panel-card` | Right-side info card with panel title + prose summary. | Most content pages | “Shorten **hero summary panel** lead text on Forum hub.” |
| **Hero summary panel (profiles variant)** | `.hero-summary-panel` + `.hero-summary-card` | Same role; used on scientists profiles layout. | `scientists/profiles.html` | “Align **hero summary panel** width with catalog toolbar.” |
| **Activities summary panel** | `.activities-summary-panel` + `.activities-summary-card` | Page-specific summary card on Activities. | `activities.html` | “Update **Activities summary panel** title copy.” |
| **Panel title** | `.panel-title` or `.activities-summary-title` | Heading inside summary card. | Summary panels | “Set **panel title** to sentence case in EN.” |
| **Panel copy lead** | `.panel-copy-lead` / `.hero-text` | Justified prose paragraph in summary card. | Summary panels | “Justify **panel copy lead** on all hub pages.” |

**Distinction — hero summary panel vs intro card vs hub card:** The **hero summary panel** is a *context blurb in the hero* (one per page). The **intro card** (`.intro-card`) on home is a *welcome + site search* block in main content. **Hub cards** (`.page-card`) are *navigation tiles* to other pages.

---

## 6. Buttons and links

| Official name | CSS / HTML | Purpose | Where | Example instruction |
| --- | --- | --- | --- | --- |
| **Primary button** | `a.btn.btn-primary` or `button.btn.btn-primary` | Main call-to-action (filled blue). | Home hero, CTAs | “Style **primary button** with gold hover on home.” |
| **Secondary button** | `.btn.btn-secondary` | Secondary action (outline). | Home, membership CTAs | “Swap order of **secondary button** and primary on home.” |
| **Link button / text link styled as button** | `.btn` on `<a>` | Navigates like a link, looks like a button. | Various | “Use **link button** not raw `<button>` for external URLs.” |
| **Card source link** | `.card-source` | External “read full article” link with icon. | Activities news cards | “Open **card source link** in same tab for internal URLs.” |
| **Card arrow affordance** | `.card-arrow` | Visual “go” indicator on hub cards. | `.page-card` footer | “Hide **card arrow** on mobile hub grid.” |

---

## 7. Home and hub pages

| Official name | CSS / HTML | Purpose | Where | Example instruction |
| --- | --- | --- | --- | --- |
| **Hub page body class** | `html/body.daab-hub-page` | Layout tweaks for card grid pages. | Home, Forum 2024 index | “Reduce top padding on **hub page** main area.” |
| **Intro card** | `.intro-card` | Welcome text + hub card search on home. | `index.html` | “Move **intro card** below hub card grid.” |
| **Hub card search box** | `.intro-card .search-box` / `#cardSearch` | Filters `.page-card` tiles on home and Forum hub. | Home, `forum/2024/index.html` | “Fix **hub card search** placeholder (EN).” |
| **Hub cards grid** | `.cards-grid` `#cardsGrid` | Responsive grid of navigation tiles. | Home, Forum hub | “Add ninth tile to **hub cards grid**.” |
| **Hub card / page card** | `a.page-card` | Clickable tile: icon, title, description, tag, arrow. | Hub grids | “Update **hub card** description for Mission (AZ).” |
| **Hub card icon** | `.card-icon-wrap` | Emoji or icon circle at top of card. | Hub cards | “Change **hub card icon** for Scientists list.” |
| **Hub card tag** | `.card-tag` | Small category label in card footer. | Hub cards | “Rename **hub card tag** ‘About’ to ‘Organisation’.” |
| **Hub search empty state** | `#cardSearchEmpty.search-empty` | Message when hub filter matches nothing. | Hub pages with search | “Translate **hub search empty state** to AZ.” |
| **Forum partner logos row** | `.forum-partner-logos` | DAAB + DİDK + ETN logos under Forum hero. | `forum/2024/index.html` | “Resize **Forum partner logos row** on mobile.” |
| **Forum partner item** | `.forum-partner-item` | Single logo + institution name. | Forum hub | “Update **Forum partner item** caption for ETN.” |

---

## 8. Section navigation strip

| Official name | CSS / HTML | Purpose | Where | Example instruction |
| --- | --- | --- | --- | --- |
| **Section navigation strip** | `nav.daab-section-nav` `#daab-section-nav` | Horizontal sibling links within a site section. | Membership pages (`membership*.html`, `application.html`) | “Add active state to **section navigation strip** on application page.” |
| **Section nav title** | `.daab-section-nav-title` | Group label (e.g. “Membership” / “Üzvlük”). | Section nav | “Rename **section nav title** in EN.” |
| **Section nav list** | `.daab-section-nav-list` | List of section subpages with icons. | Section nav | “Reorder **section nav list** to put Application first.” |
| **Section nav link** | `.daab-section-nav-list a` + `.daab-section-nav-label` | Individual subpage tab; `.active` = current. | Section nav | “Fix **section nav link** icon for ‘Send invite’.” |

**Distinction — section nav vs primary nav:** **Primary navigation bar** covers the whole site. **Section navigation strip** appears *below the hero* and only links between related pages in one area (Membership suite).

---

## 9. Sidebar and widgets (Activities, Forum, Charter, Gallery)

| Official name | CSS / HTML | Purpose | Where | Example instruction |
| --- | --- | --- | --- | --- |
| **Content wrap (two-column)** | `.content-wrap` | Flex/grid: sidebar + main column. | Activities, Forum subpages, charter, photos gallery | “Stack **content wrap** to single column below 900px.” |
| **Left sidebar column** | `aside.sidebar` | Left column container for widgets. | Two-column layouts | “Fix **left sidebar** sticky offset under breadcrumbs.” |
| **Sidebar widget** | `.sidebar-widget` | Bordered panel with head + body. | Sidebar | “Add padding to **sidebar widget** on charter page.” |
| **Widget head** | `.widget-head` | Title row; may include mobile toggle. | Sidebar widgets | “Change **widget head** icon on Activities timeline.” |
| **Widget body** | `.widget-body` | Scrollable list area. | Sidebar widgets | “Limit **widget body** max-height on desktop.” |
| **Sidebar mobile toggle** | `.events-menu-toggle` | Hamburger to collapse widget list on mobile. | Widget heads | “Ensure **sidebar mobile toggle** aria-controls matches list id.” |
| **Timeline list** | `.timeline-list` | Date + link list (news chronology or charter articles). | Activities sidebar, charter TOC, gallery categories | “Add new item to **timeline list** for April 2026 news.” |
| **Timeline date label** | `.tl-date` | Date or article code prefix in list. | Timeline items | “Format **timeline date label** as MM.YYYY on Activities.” |
| **Charter table-of-contents sidebar** | `.toc-card.charter-sidebar` | Charter-specific TOC widget (same widget pattern). | `charter.html` | “Jump link in **charter TOC sidebar** to article 26.” |

**Distinction — left sidebar vs section nav:** **Section nav** is a horizontal tab bar for Membership. **Left sidebar** is a vertical auxiliary panel (news timeline, forum section links, photo categories, charter articles).

---

## 10. Activities page content

| Official name | CSS / HTML | Purpose | Where | Example instruction |
| --- | --- | --- | --- | --- |
| **News feed main column** | `main.news-feed` `#content` | Scrollable list of news articles. | `activities.html` | “Add anchor offset for **news feed** when jumping from timeline.” |
| **News card** | `article.news-card` | Single news story block with id anchor. | Activities feed | “Insert new **news card** above Ankara story.” |
| **News card header** | `.card-header` + `.card-date` + `.card-title` | Date and headline. | News cards | “Use h2 in **news card header** consistently.” |
| **News card body** | `.card-body` + `.card-text` | Article paragraphs. | News cards | “Justify **news card body** text.” |
| **News card lead** | `.card-text.act-card-lead` | Uppercase or emphasized opening line. | Some news cards | “Remove all-caps from **news card lead**.” |
| **News card gallery** | `.card-gallery` | Inline photo row (`.act-row-thumb`). | News cards | “Show two columns in **news card gallery** on mobile.” |
| **News card source link** | `.card-source` | External article link. | News cards | “Track clicks on **news card source link** (future analytics).” |

---

## 11. Forum 2024 subpages

| Official name | CSS / HTML | Purpose | Where | Example instruction |
| --- | --- | --- | --- | --- |
| **Forum sidebar navigation widget** | `.sidebar-widget` in Forum layout | Links to Programme, Photos, Stories, etc. | Forum subpages (not hub) | “Add Video gallery to **Forum sidebar navigation widget**.” |
| **Forum story lead** | `.forum-story-lead` | Intro block on Stories page. | `forum/2024/stories.html` | “Edit **Forum story lead** paragraph for rectors story.” |

---

## 12. Photos gallery

| Official name | CSS / HTML | Purpose | Where | Example instruction |
| --- | --- | --- | --- | --- |
| **Photos gallery main panel** | `#photos-gallery-panel.photos-gallery-main` | Right column: title, count, grid. | `photos_gallery.html` | “Show skeleton in **photos gallery main panel** while loading.” |
| **Photos gallery head** | `.photos-gallery-head` | Category title area. | Gallery main | “Sync **photos gallery head** with sidebar selection.” |
| **Photos gallery meta** | `#photosGalleryCount.photos-gallery-meta` | Photo count line. | Gallery main | “Update **photos gallery meta** format (EN).” |
| **Photos gallery grid** | `#photosGalleryGrid.photos-gallery-grid` | Thumbnail grid. | Gallery main | “Increase **photos gallery grid** column count on wide screens.” |
| **Photo lightbox** | `#photosGalleryLightbox.lightbox` | Full-screen image viewer dialog. | Gallery page | “Trap focus inside **photo lightbox** when open.” |
| **Lightbox close control** | `.lightbox-close` | Closes lightbox. | Lightbox | “Enlarge **lightbox close control** touch target.” |
| **Lightbox caption** | `#photosGalleryLightboxCaption.lightbox-caption` | Image caption under enlarged photo. | Lightbox | “Show filename in **lightbox caption** for admins only.” |

---

## 13. Scientists catalog and profiles

| Official name | CSS / HTML | Purpose | Where | Example instruction |
| --- | --- | --- | --- | --- |
| **Catalog toolbar** | `.catalog-toolbar` | Search + filter controls above scientist list/cards. | `scientists/list.html`, `scientists/profiles.html` | “Pin **catalog toolbar** below breadcrumbs on scroll.” |
| **Catalog search field** | `#searchInput` in `.search-wrap` | Inline filter (not global site search). | Catalog pages | “Expand **catalog search field** placeholder (AZ).” |
| **Catalog filters toggle** | `.catalog-toolbar__toggle` | Opens filter panel on mobile/narrow layouts. | Catalog toolbar | “Show badge on **catalog filters toggle** when filters active.” |
| **Catalog filters panel** | `#catalogFilterPanel.catalog-toolbar__panel` | Country, field, degree filters. | Below toolbar | “Add ‘Honorary’ to **catalog filters panel**.” |
| **Catalog section** | `#scientists-catalog.catalog-section` | Grid/list of scientist entries. | Profiles page | “Lazy-load images in **catalog section**.” |
| **Scientist profile card** | `.profile-card` (card layout in profiles HTML) | Photo, name, bio, metadata for one scientist. | Profiles page | “Reduce gap in **scientist profile card** header.” |
| **Profile card photo** | `.card-photo` / `.photo-wrap` | Portrait image (also on executive board). | Profiles, executive board | “Use placeholder when **profile card photo** missing.” |
| **Profile card bio** | `.card-bio` | Justified biography text. | Profiles | “Limit **profile card bio** to 120 words with expand.” |
| **Profile QR link** | `.card-qr-link` + `.card-qr` | QR code linking to profile anchor URL. | Profile cards | “Move **profile QR link** 10px left on all cards.” |
| **Scientists list view** | Table/list layout on `list.html` | Compact directory (distinct from card profiles). | `scientists/list.html` | “Add sort column to **scientists list view**.” |

**Distinction — catalog search vs site search:** **Site search** (`#search-overlay`) searches the whole site from the nav bar. **Catalog search field** filters only the scientists list on that page.

---

## 14. Executive board

| Official name | CSS / HTML | Purpose | Where | Example instruction |
| --- | --- | --- | --- | --- |
| **Board member card** | `.board-card` / member blocks in grid | Photo + name + role for each director. | `executive-board.html` | “Update **board member card** title for co-chair.” |
| **Board photo wrap** | `.photo-wrap` | Circular or framed portrait container. | Executive board | “Fix **board photo wrap** aspect ratio on mobile.” |

---

## 15. Charter (long-form document)

| Official name | CSS / HTML | Purpose | Where | Example instruction |
| --- | --- | --- | --- | --- |
| **Charter layout** | `.charter-layout` | Sidebar TOC + main charter text. | `charter.html` | “Widen **charter layout** main column on desktop.” |
| **Charter article section** | `section` with `#section-NN` | Numbered charter article block. | Charter main | “Fix anchor scroll for **charter article section** 12.” |
| **Charter sidebar (TOC)** | `.toc-card` | Article jump list (uses timeline-list pattern). | Charter left column | “Highlight current **charter sidebar** article on scroll.” |

---

## 16. Membership and application

| Official name | CSS / HTML | Purpose | Where | Example instruction |
| --- | --- | --- | --- | --- |
| **Membership value section** | `.mv-section` + `.mv-card` | Benefit blocks on membership value page. | `membership_value.html` | “Add fifth **membership value section** card.” |
| **Membership terms card** | `.lang-card` | Highlight card on membership terms page. | `membership.html` | “Update **membership terms card** heading.” |
| **Application progress bar** | `.app-progress-bar` | Step indicator (1–4) for multi-step form. | `application.html` | “Mark step 3 active in **application progress bar**.” |
| **Application form section** | `.form-section` `#sec-N` | One step of the membership application. | Application page | “Validate email in **application form section** 1.” |
| **Form field group** | `.field-group` + `.field-label` | Label + input row. | Application form | “Add tooltip to **form field group** ‘Phone’.” |
| **Application button row** | `.app-btn-row` | Next / back buttons per step. | Application form | “Disable Next in **application button row** until valid.” |

---

## 17. Site footer

| Official name | CSS / HTML | Purpose | Where | Example instruction |
| --- | --- | --- | --- | --- |
| **Site footer** | `footer.footer-pro` | Contact, address, leadership, copyright. | All main pages | “Add LinkedIn to **site footer** contact column.” |
| **Footer inner** | `.footer-inner` | Padded container for footer content. | Footer | “Center **footer inner** on mobile.” |
| **Footer brand block** | `.footer-brand` | Organization name heading. | Footer top | “Use WAAS acronym in **footer brand block** (EN).” |
| **Footer grid** | `.footer-grid` | Three-column contact / address / leadership. | Footer | “Stack **footer grid** columns on tablet.” |
| **Footer column** | `.footer-col` | One column of footer links/text. | Footer grid | “Merge phone and email in one **footer column**.” |
| **Footer column title** | `.footer-title` | Column heading (Contact, Address, …). | Footer columns | “Translate **footer column title** ‘Leadership’ (AZ).” |
| **Footer bottom bar** | `.footer-bottom` | Copyright line. | Footer base | “Update year in **footer bottom bar**.” |

---

## 18. Overlays and utilities

| Official name | CSS / HTML | Purpose | Where | Example instruction |
| --- | --- | --- | --- | --- |
| **Site search overlay** | `#search-overlay` | Full-screen site-wide search dialog. | Injected on pages with `daab-search.js` | “Close **site search overlay** on route change.” |
| **Search modal panel** | `.search-modal` | Inner layout of search overlay. | Search overlay | “Increase **search modal** top padding on iOS.” |
| **Search input row** | `.search-input-row` `#search-input` | Query field in overlay. | Search overlay | “Debounce **search input row** to 200ms.” |
| **Search results list** | `#search-results.search-results` | Live result list. | Search overlay | “Show section name in **search results list**.” |
| **Search keyboard hints** | `.search-hint` | ↑↓ / Enter / Esc legend. | Search overlay | “Hide **search keyboard hints** on touch devices.” |
| **Back-to-top button** | `.daab-back-to-top` | Floating scroll-to-top control. | Long pages | “Show **back-to-top button** after 400px scroll.” |
| **Language gateway page** | `.daab-gateway-page` | Root language chooser (not main chrome). | Site entry / gateway HTML | “Redesign **language gateway page** cards.” |

---

## 19. Similar elements — quick reference

| If you mean… | Official name | Not this name |
| --- | --- | --- |
| Blue bar at very top with logo and menu | **Primary navigation bar** | “Header banner”, “top menu bar” |
| Grey trail Home › Activities › … | **Breadcrumbs bar** (or **Forum breadcrumbs bar**) | “Secondary menu”, “subnav” |
| Horizontal Membership tabs under hero | **Section navigation strip** | “Breadcrumbs”, “top nav” |
| Left column with dates / forum links | **Sidebar widget** / **timeline list** | “Section nav”, “breadcrumbs” |
| Right card in hero with paragraph summary | **Hero summary panel** | “Sidebar”, “info box”, “banner” |
| Clickable tiles on home to open pages | **Hub card** (`.page-card`) | “Content card”, “news card” |
| News story on Activities page | **News card** | “Hub card”, “page card” |
| Three-line button opening mobile menu | **Mobile menu toggle (hamburger)** | “Submenu”, “dropdown” (those are different) |
| Magnifying glass in nav opening full-screen search | **Site search overlay** | “Hub card search”, “catalog search field” |
| Filter box above scientist cards | **Catalog search field** | “Site search” |
| AZ / EN flags in nav | **Language switcher** | “Locale dropdown”, “country selector” |
| Contact block at bottom of every page | **Site footer** | “Footer menu” (there is no separate footer nav) |

---

## 20. Page-type matrix (where elements appear)

| Page type | Primary nav | Breadcrumbs | Hero summary | Section nav | Sidebar | Hub cards | Footer |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Home (`index.html`) | Yes | No | Yes | No | No | Yes | Yes |
| Standard content (mission, foundation, …) | Yes | Yes* | Yes | No | No | No | Yes |
| Activities | Yes | Yes* | Yes (activities variant) | No | Yes (timeline) | No | Yes |
| Forum 2024 hub | Yes | Forum bar | Yes | No | No | Yes | Yes |
| Forum 2024 subpage | Yes | Forum bar | Yes | No | Yes (forum links) | No | Yes |
| Membership suite | Yes | Yes* | Yes | Yes | No | No | Yes |
| Scientists list / profiles | Yes | Yes* | Yes | No | No | No | Yes |
| Charter | Yes | Yes* | Yes | No | Yes (TOC) | No | Yes |
| Application form | Yes | Yes* | Yes | Yes | No | No | Yes |

\*Breadcrumbs injected by JS except where static forum breadcrumbs exist in HTML.

---

## 21. Prompt examples (copy-ready)

**Content change**

> Update the **panel copy lead** in the **hero summary panel** on EN `mission.html` to the following text: “…”

**Layout / CSS**

> On mobile, collapse the **sidebar widget** body by default and expand only when the **sidebar mobile toggle** is pressed (Activities page).

**Navigation**

> Add “Video gallery” to the **Forum sidebar navigation widget** on all Forum 2024 subpages (AZ and EN), below Photos gallery.

**Scientists**

> In the **catalog filters panel**, add a filter for “Emeritus” and show active count on the **catalog filters toggle**.

**Do not confuse**

> ❌ “Change the left menu breadcrumbs on Activities.”  
> ✅ “Add a link to the **timeline list** in the **Activities sidebar widget**.”

---

## 22. Developer reference (key files)

| Concern | Primary files |
| --- | --- |
| Nav structure | `i18n/nav.json`, `js/daab-primary-nav.js`, `css/daab-nav-mega.css` |
| Breadcrumbs | `js/daab-breadcrumbs.js`, `css/daab-common.css` |
| Sticky chrome | `js/daab-sticky-chrome.js`, `css/daab-sticky-chrome.css` |
| Hero summaries | `i18n/page-panel-summaries.json`, `css/daab-hero-summary.css` |
| Hub cards | `css/daab-hub-cards.css` |
| Section nav | `js/daab-section-nav.js`, `css/daab-common.css` |
| Site search | `js/daab-search.js`, `css/daab-search.css` |
| Scientists catalog | `css/scientists-catalog-toolbar.css`, `js/scientists-catalog-data.js` |
| Footer | `css/daab-common.css` (`.footer-pro` block) |

---

## 23. Document maintenance

When new UI patterns are added to the site:

1. Choose a clear **official name** (noun phrase, not CSS-only jargon).
2. Record CSS classes / IDs and **where the element appears**.
3. Add a row to the appropriate section table and, if needed, to **Section 19 (Similar elements)**.
4. Regenerate the Word export: `python helpers/_export_ui_terminology_docx.py`.

*Generated from site source (AZ/EN HTML, CSS, JS). Element names reflect implementation as of May 2026.*
