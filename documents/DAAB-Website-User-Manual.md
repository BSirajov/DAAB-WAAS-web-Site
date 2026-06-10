# DAAB / WAAS Website — User Manual

**Audience:** Visitors, members, and staff using the public website  
**Languages:** Azerbaijani (AZ) and English (EN)  
**Organization:** Dünya Azərbaycanlı Alimlər Birliyi (DAAB) / World Association of Azerbaijani Scientists (WAAS)  
**Document version:** 1.0 — May 2026

This manual describes how to use the official bilingual website: what you see on screen, how navigation works, and how to complete common tasks. It is written for end users, not developers.

---

## 1. About the website

The site is a **static, bilingual** web presence. All main content exists in parallel:

| Language | URL path | Brand name |
|----------|----------|------------|
| Azerbaijani (default) | `/az/…` | Dünya Azərbaycanlı Alimlər Birliyi (DAAB) |
| English | `/en/…` | World Association of Azerbaijani Scientists (WAAS) |

The site introduces the Association, publishes news and Forum 2024 materials, lists scientists who participated in the 2024 forum, explains membership, and provides an online membership application form.

---

## 2. Look and feel

### 2.1 Visual identity

- **Colours:** Deep blues (`#005a9a` family), white and light blue surfaces, gold accents on headings and card headers.
- **Typography:**  
  - **Playfair Display** — page titles and major headings (serif, formal tone).  
  - **Inter** — body text, navigation, forms, and tables (sans-serif, readable at small sizes).
- **Imagery:** DAAB logo, partner logos on Forum pages, scientist portraits, photo/video galleries, and occasional news images on Activities.

### 2.2 Layout patterns

Most pages follow a consistent structure:

1. **Top navigation bar** — fixed strip with logo, menu, language switcher, and search.
2. **Hero band** — large title, optional subtitle, and often a summary panel on the right (desktop).
3. **Breadcrumbs** (on many inner pages) — path such as `Home › Activities › Forum 2024`.
4. **Main content** — articles, cards, tables, or forms.
5. **Back-to-top control** — appears after you scroll down (floating button, bottom-right).

**Hub pages** (Home, Forum 2024 hub) use a **card grid**: each card has an icon, title, short description, and “Read more” style link.

**Long reading pages** (Activities, Forum official texts, Presentations, Charter) use **content cards** with blue gradient headers and white body areas.

**Scientists list** uses a **data table** with filters; **Scientists profiles** uses a **card grid** with photos and QR codes.

### 2.3 Responsive behaviour

- **Desktop:** Full horizontal menu, two-column hero, sidebars where provided (e.g. presentations menu).
- **Tablet / phone:** Hamburger menu (☰), stacked hero, collapsible filter panels, and collapsible sidebar widgets. Touch targets are enlarged on mobile.

---

## 3. Getting started

### 3.1 Opening the site

1. Open the site root URL in a browser (e.g. `https://yoursite.example/`).
2. You are usually sent automatically to **`/az/index.html`** (Azerbaijani home), unless you previously chose English (stored in the browser).
3. To choose language explicitly, use the **gateway page**: open `index.html?choose=1` and pick **Azərbaycan dilində davam et** or **Continue in English**.

### 3.2 Choosing your language

On every main page, the **language switcher** appears in the top navigation (AZ / EN flags or codes).

| Action | Result |
|--------|--------|
| Click **AZ** | Opens the Azerbaijani version of the **same page** (when a translation exists). |
| Click **EN** | Opens the English version. |

Your choice is remembered for future visits. On some long pages (e.g. Activities, Charter), the site tries to keep you at the **same section** after switching language.

### 3.3 Skip link (accessibility)

The first focusable control on many pages is **“Skip to content”** / **“Məzmuna keç”**. Press **Tab** once after loading the page, then **Enter**, to jump past the navigation to the main content.

---

## 4. Global user interface elements

### 4.1 Top navigation bar

| Element | Appearance | What it does |
|---------|----------------|--------------|
| **Logo** | DAAB emblem, left | Returns to home (`/az/` or `/en/`). |
| **Site name** | Two-line title next to logo | Also links to home. |
| **Menu items** | Text links; some with ▼ caret | Opens pages or dropdown panels. |
| **Hamburger (mobile)** | Three lines, top-left | Opens/closes the full menu. |
| **Language switcher** | AZ / EN | Switches site language (see §3.2). |
| **Search** | Magnifying glass or search field in nav | Opens site-wide search (see §4.2). |

**Main menu structure** (labels differ slightly in EN):

| Top item | Sub-items |
|----------|-----------|
| **Home** | — |
| **Activities** | News · Forum 2024 |
| **Scientists** | Directory (list) · Profiles |
| **About us** | Foundation · Mission & values · Board of Directors · Charter |
| **Membership** | Why become a member · Membership terms · Join us (application) |

Dropdown panels show a **title** and a **one-line description** for each link. The current section is highlighted.

**How to use dropdowns (desktop):** Click the parent label (e.g. “Scientists”) or hover (depending on device); click a row in the panel to go to that page.

**How to use the menu (mobile):** Tap ☰ → tap a section → tap a sub-link. Tap outside or the toggle again to close.

### 4.2 Site-wide search

Search finds pages and in-page sections across the current language.

| How to open | |
|-------------|---|
| Click the **search control** in the navigation bar | |
| Keyboard shortcut | **Ctrl+K** (Windows/Linux) or **Cmd+K** (Mac) |

**Search overlay:**

- A panel opens over the page with a text field.
- Type at least one word; results appear in a list (page titles and snippets).
- **Click** a result or use **↑ / ↓** and **Enter** to open it.
- Press **Escape** or click outside to close.

Search understands Azerbaijani characters in a flexible way (e.g. typing without special letters may still match ə, ş, etc.).

### 4.3 Breadcrumbs

Below the navigation on many pages, a trail such as:

`Ana səhifə › Fəaliyyətimiz › Forum 2024 › Məruzələr`

- Each segment except the last is a **link**.
- The last segment is the **current page** (not linked).
- Use breadcrumbs to move up one level without using the browser Back button.

### 4.4 Section navigation (pills)

Some long pages (Membership application, Charter, and similar) show a **horizontal row of pills** under the hero:

- Each pill jumps to a section on the same page.
- The active pill updates as you scroll (on supported pages).
- On narrow screens, pills may scroll horizontally.

### 4.5 Back to top

After scrolling down, a **back-to-top** button appears (typically bottom-right). Click it to scroll smoothly to the top of the page.

### 4.6 Hero area and subtitles

- **Main heading (H1):** Large serif title; key words may be emphasised in colour.
- **Subtitle:** Italic line under the title (loaded from site configuration); summarises the page purpose.
- **Summary panel:** Light card on the right (desktop) with a short explanation — read this for context before diving into content.

---

## 5. Home page

**Path:** `/az/index.html` or `/en/index.html`

### What you see

- Hero with welcome message and two primary buttons: **Meet our scientists** and **Join the Association** (wording varies by language).
- Introductory text and a **search box** labelled “Search sections…” — filters the **cards below** on the home page only (not the whole site).
- **Card grid** linking to major sections: Mission, Activities, Scientists, Board, Charter, Membership, etc.

### Common actions

| Goal | Steps |
|------|--------|
| Browse all main topics | Scroll the card grid; click any card. |
| Find a home-page section quickly | Type in the home search box; non-matching cards hide. |
| Go to scientists | Click **Meet our scientists** or the Scientists card. |
| Apply for membership | Click **Join** / membership card → follow links to terms and application. |

---

## 6. About us

### 6.1 Foundation

Story of how the Association was established: narrative sections in card layout, readable body text.

### 6.2 Mission, vision and values

Explains purpose, strategic direction, and core values — same card/hero pattern as other About pages.

### 6.3 Board of Directors (Executive board)

- **Member cards** in a grid: photo (portrait frame), role, name, country.
- **QR code** on each card links to that person’s entry on the Scientists profiles page.
- Click the card area to open the full profile (where linked).

### 6.4 Charter

Long legal/governance document, often with:

- **Sidebar table of contents** (desktop) listing articles.
- Click an article in the sidebar to jump to that section.
- On mobile, the sidebar may collapse into a **menu button** — tap to open the list of articles.

---

## 7. Scientists

### 7.1 Directory (list view)

**Path:** `/az/scientists/list.html` or `/en/scientists/list.html`

**Purpose:** Searchable table of scientists who participated in the 2024 forum.

| UI element | Look and feel | Use |
|------------|---------------|-----|
| **Search field** | Wide box with magnifier icon | Type name, country, field, degree, email, etc. Table filters as you type. |
| **Filters button** | Funnel icon + “Filters” | On mobile/small screens, opens the filter panel. |
| **Country / Field / Degree dropdowns** | Select boxes with emoji labels | Narrow the list; **×** beside each clears that filter. |
| **Results table** | Columns: photo, name, country, field, degree, email, … | Click column headers to sort where supported. |
| **Row click** | Highlights row | Opens or focuses the scientist (depending on configuration — often links to profiles with hash). |
| **Pagination** | Page numbers at bottom | Move through large result sets. |

**Typical workflow:** Open Filters → choose country → type part of a name → click a row to view profile.

### 7.2 Profiles (card view)

**Path:** `/az/scientists/profiles.html` or `/en/scientists/profiles.html`

**Purpose:** Richer **profile cards** with photo, affiliation, email, field, and a **QR code** for sharing a direct link to that profile.

| Action | How |
|--------|-----|
| Find someone | Scroll, or use browser **Find** (Ctrl+F), or open a link with `#scientist-id` in the URL. |
| Share a profile | Scan or copy link via QR / address bar (`…/profiles.html#slug`). |
| Email a scientist | Click the email link on their card (opens your mail app). |

Profile cards use a rounded photo frame and structured metadata rows (label + value).

---

## 8. Activities and Forum 2024

### 8.1 Activities (News)

**Path:** `/az/activities.html` or `/en/activities.html`

- **Layout:** Left **timeline sidebar** (“News” / events list) + **main column** of news cards.
- **Sidebar:** Lists news items by date/title; click an item to scroll the main column to that article.
- **News cards:** Blue header (title/date), body text, images, external source links where present.
- On mobile, the sidebar may open via a **menu toggle** on the widget header.

### 8.2 Forum 2024 hub

**Path:** `/az/forum/2024/index.html` or `/en/forum/2024/index.html`

- Hero shows Forum title and **partner logos** (DAAB, DİDK, Ministry).
- Card grid links to all Forum sub-sections (see table below).
- Home-style **search box** filters Forum cards by title.

| Card (EN examples) | Content |
|--------------------|---------|
| Official addresses | Speeches and official texts |
| Forum programme | Schedule tables |
| Presentations | Scientific presentations (sidebar + long articles) |
| Impressions | Participant reflections |
| Strategic roadmap | Policy/roadmap document |
| Stories of the forum | Narrative stories |
| Contributions and cooperation | Cooperation chapter |
| Photo gallery | Browse forum photos by category |
| Video gallery | Embedded video reports |

### 8.3 Presentations page

**Path:** `/az/forum/2024/presentations.html` or `/en/forum/2024/presentations.html`

**Layout:**

| Area | Description |
|------|-------------|
| **Left sidebar** | List of all presentations: small **photo**, **speaker name**, **presentation title**. |
| **Right column** | Full text of each presentation in separate cards. |

**Actions:**

| Goal | Steps |
|------|--------|
| Jump to a talk | Click an item in the left sidebar → page scrolls to that presentation. |
| Read | Scroll the main column; body text is **justified**; bullet lists use compact spacing. |
| Know who is speaking | Blue header shows name; lead row shows photo + presentation title. |

On mobile, open the sidebar with the **☰ control** on the “Presentations” widget.

### 8.4 Photo gallery

- Sections/group headings with thumbnail grids.
- Click a thumbnail to view the larger image (lightbox-style behaviour where implemented).
- Thumbnails load from organised folders per event segment.

### 8.5 Video gallery

- Grid of video entries (thumbnails and titles).
- Click to play or open the linked video content (external or embedded players as configured per item).

### 8.6 Other Forum pages (official, programme, impressions, etc.)

Shared patterns:

- Breadcrumbs: `Home › Activities › Forum 2024 › [page]`.
- Long content in **stacked cards** with section headings (`program-subhead` style).
- Some pages include **tables** (programme schedule) — scroll horizontally on small screens if needed.

---

## 9. Membership

### 9.1 Why become a member

Benefits and value proposition — informational cards and text; links onward to terms and application.

### 9.2 Membership terms

Fees, rules, payment/bank details, and procedures. Read before applying.

### 9.3 Online application (“Join us”)

**Path:** `/az/application.html` or `/en/application.html`

**Look and feel:**

- Multi-section **form** with clear steps (personal data, academic fields, documents, etc.).
- **Section nav pills** jump between form parts.
- Required fields are marked; validation messages appear if you leave required items empty.
- Instructions explain emailing CV/photo to the Association address where uploads are not done in-browser.

**How to apply:**

1. Read **Membership terms**.
2. Open **Join us** / **Bizə qoşulun**.
3. Use the primary navigation menu (Membership) or in-page links to complete each part of the form.
4. Submit according to on-page instructions (and send attachments by email if requested).
5. Keep a copy of any confirmation message or email you receive.

---

## 10. Tips for efficient use

| Tip | Detail |
|-----|--------|
| Prefer navigation + breadcrumbs | More reliable than only the browser Back button on deep Forum pages. |
| Use site search for unknown location | Ctrl/Cmd+K, then type topic keywords. |
| Switch language from the header | Avoids manually editing `/az/` vs `/en/` in the URL. |
| Scientists: combine filters + search | Faster than scrolling the full table. |
| Presentations: use left sidebar | Long page — sidebar is the fastest table of contents. |
| Hard refresh after updates | If layout looks wrong, try Ctrl+F5 (Windows) or Cmd+Shift+R (Mac). |

---

## 11. Accessibility features

- **Skip to content** link for keyboard users.
- **ARIA labels** on navigation, menus, and many controls (screen reader friendly).
- **Keyboard:** Tab through links and form fields; Escape closes search overlay and some menus.
- **Contrast:** Dark blue on white/light backgrounds for main text; white on blue in card headers.
- **Responsive text:** Headings scale with viewport (`clamp` sizing on key titles).

---

## 12. Troubleshooting

| Problem | What to try |
|---------|-------------|
| “This page isn’t working” / blank connection error | Site server may be down, or wrong URL — use the address provided by your host; for local preview, start the site server and open `http://localhost:8010/`. |
| Page looks unstyled (plain HTML) | Wait for network; hard refresh; check you opened `http://` not `file://` for full features. |
| Wrong language | Use AZ/EN switcher in header. |
| Old content after an update | Hard refresh (Ctrl+F5) to clear cached CSS/JS. |
| Search shows no results | Try simpler keywords or the other language version. |
| Link goes nowhere | Report to site maintainers — may be outdated bookmark. |
| Form will not submit | Fill required fields; check error messages in red/near fields. |

---

## 13. Quick reference — main URLs

| Section | Azerbaijani | English |
|---------|-------------|---------|
| Home | `/az/index.html` | `/en/index.html` |
| Scientists list | `/az/scientists/list.html` | `/en/scientists/list.html` |
| Scientists profiles | `/az/scientists/profiles.html` | `/en/scientists/profiles.html` |
| Activities | `/az/activities.html` | `/en/activities.html` |
| Forum 2024 | `/az/forum/2024/index.html` | `/en/forum/2024/index.html` |
| Presentations | `/az/forum/2024/presentations.html` | `/en/forum/2024/presentations.html` |
| Membership application | `/az/application.html` | `/en/application.html` |

---

## 14. Document maintenance

This manual reflects the site structure as of **May 2026**. When navigation labels, page URLs, or major layouts change, update this file alongside `i18n/routes.json` and `i18n/ui.json`.

**Related internal docs (for staff):**

- `documents/DAAB-Navigation-and-Information-Architecture-Strategy.md`
- `documents/DAAB-Site-Stability-and-Deployment-Guide.md`
- `documents/DAAB-Bilingual-Website-Strategy.md` (if present)

---

*End of user manual*
