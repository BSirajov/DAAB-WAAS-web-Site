# DAAB / WAAS Virtual Platform — Technical Specification

**Source document:** *Bəxtiyar Siracov, DAAB-ın virtual məkanda fəaliyyəti* (presentation at the 1st Forum of Azerbaijani Scientists Living Abroad, 9–11 September 2024, Baku, Khankendi, Shusha)

**Derived from:** Business vision in the Siracov presentation, the as-built bilingual static site (May–June 2026), and existing architecture documents in `documents/`.

**Document version:** 1.0  
**Date:** 5 June 2026  
**Status:** Specification for design, development, QA, and phased delivery  
**Audience:** Software developers, UI/UX designers, QA engineers, content editors, project stakeholders

---

## Table of contents

1. [Executive summary](#1-executive-summary)
2. [Business requirements elaboration](#2-business-requirements-elaboration)
3. [Scope, phases, and assumptions](#3-scope-phases-and-assumptions)
4. [Stakeholders and user personas](#4-stakeholders-and-user-personas)
5. [Information architecture](#5-information-architecture)
6. [Navigation structure](#6-navigation-structure)
7. [Functional requirements](#7-functional-requirements)
8. [Non-functional requirements](#8-non-functional-requirements)
9. [UI/UX standards](#9-uiux-standards)
10. [Multilingual support](#10-multilingual-support)
11. [Responsive design rules](#11-responsive-design-rules)
12. [Accessibility requirements](#12-accessibility-requirements)
13. [Performance expectations](#13-performance-expectations)
14. [Security considerations](#14-security-considerations)
15. [Integration points](#15-integration-points)
16. [Content management needs](#16-content-management-needs)
17. [Testing criteria](#17-testing-criteria)
18. [Acceptance criteria by major feature](#18-acceptance-criteria-by-major-feature)
19. [Appendices](#19-appendices)

---

## 1. Executive summary

### 1.1 Organizational goal

The **Dünya Azərbaycanlı Alimlər Birliyi (DAAB)** / **World Association of Azerbaijani Scientists (WAAS)** aims to unite Azerbaijani scientists worldwide, facilitate knowledge exchange, apply modern teaching approaches, and strengthen Azerbaijan’s scientific potential. The Siracov presentation defines a **virtual platform** that goes beyond a brochure website: it should become a communication hub, scholar directory, teaching environment, multimedia science channel, and collaboration enabler.

### 1.2 Technical vision

The platform should be:

- **Institutional** — credible, bilingual, accessible, and aligned with academic norms.
- **Discoverable** — structured IA, search, filters, deep links, and SEO.
- **Scalable** — start with a proven static core; add dynamic services (forms, LMS, media, competitions) in controlled phases.
- **Maintainable** — centralized i18n, design tokens, validation scripts, and documented deployment.

### 1.3 Delivery strategy

| Phase | Focus | Technology posture |
|-------|--------|-------------------|
| **Phase 1 (delivered)** | Institutional site, scientists catalogue, membership funnel, Forum 2024 microsite, Encyclopedia hub | Static HTML/CSS/JS; `i18n/*.json`; Python helpers (not deployed) |
| **Phase 2 (near term)** | Server-backed membership applications, enhanced scholar profiles, social links, newsletter | Form backend (Formspree / Apps Script / Supabase); optional auth for admins |
| **Phase 3 (medium term)** | Virtual teaching hubs, resource library, field-of-science portals | Headless CMS or LMS integration; video hosting |
| **Phase 4 (long term)** | Virtual labs, competitions, medical hubs, e-commerce for textbooks | Dedicated subsystems; third-party platform integration |

This specification describes **all phases** so teams can plan incrementally while Phase 1 acceptance criteria remain testable today.

---

## 2. Business requirements elaboration

The following table translates each theme from the Siracov presentation into elaborated business intent and the corresponding technical capability.

### 2.1 Website as communication and information hub

| Business intent | Elaboration | Technical capability |
|-----------------|-------------|----------------------|
| Present mission, vision, values | DAAB/WAAS must communicate purpose, governance, and credibility to diaspora scientists, partners, and the public | About section (Foundation, Mission, Board, Charter); hero summaries; bilingual copy in `i18n/` |
| Publish events and projects | Forum outcomes, news, cooperation, roadmap must remain findable after the event | Activities timeline; Forum 2024 microsite (12 subpages); future event templates |
| Share online resources | Articles, video tutorials, and useful materials should be catalogued and searchable | Resource library module (Phase 3); interim: inline links, video gallery, presentations TOC |
| Central communication | Site is the primary digital front door before social channels | Canonical URLs, `sitemap.xml`, `robots.txt`, Open Graph meta, consistent footer contact |

### 2.2 Scholars data bank (“Ziyalılarımızın data bankı”)

| Data category (business) | Elaboration | Technical fields / views |
|--------------------------|-------------|--------------------------|
| Personal information | Name, contact, address for collaboration outreach | `name`, `contactEmail`, `location`, `photo`, `slug` |
| Education | Degrees, institutions, academic achievements | `degrees[]`, `institutions[]`, `honors[]` |
| Work experience | Roles, employers, accomplishments | `positions[]`, `affiliations[]`, `publications[]` |
| Skills | Technical, language, leadership | `skills[]`, `languages[]`, `tags[]` |
| Achievements & certificates | Credentials supporting credibility | `certifications[]`, `awards[]` |
| Public activities | Volunteering, organizational roles | `service[]`, `memberships[]` |
| Hobbies & interests | Humanize profiles; optional for public display | `interests[]` (optional, privacy-controlled) |
| Internet resources | Papers, books, lectures | `publications[]`, `externalLinks[]`, DOI/ORCID |

**Current implementation:** Scientists list (~83 records) and card-based CV profiles with filters, QR codes, TTS, and deep linking.  
**Gap vs. vision:** Full structured data bank with contact fields, skills, hobbies, and admin CRUD — requires Phase 2 backend and privacy model.

### 2.3 Online teaching hubs (virtual university)

| Business intent | Elaboration | Technical capability |
|-----------------|-------------|----------------------|
| Courses and lectures by faculty | Professors deliver structured learning online | LMS integration (Moodle, Canvas, or custom) or embedded video course pages |
| Faculties and departments | Organizational structure mirrors academic units | IA section: `/learn/faculties/{slug}/` with department landing pages |
| Experimental laboratories | Students observe or simulate lab work | Video lab series + optional interactive simulations (Phase 4); iframe/embed to external lab platforms |
| Lecture auditoriums | Synchronous or async lecture spaces | Live stream embed (YouTube Live, Zoom webinar) + archived recordings |
| International platform links | Connect to global MOOC providers | Curated link directory with metadata; deep links to Coursera, edX, etc. |

### 2.4 Teaching programs and textbooks

| Business intent | Elaboration | Technical capability |
|-----------------|-------------|----------------------|
| Multi-disciplinary programs | Structured curricula across fields | Program catalogue with modules, prerequisites, credit metadata |
| Azerbaijani and foreign-language editions | Bilingual and translated materials | Locale-specific content variants; `lang` attribute per resource |
| Print, e-book, and audio distribution | Materials reach global audience | Metadata for format (PDF, EPUB, MP3); Phase 4: Amazon/e-commerce API or affiliate links |

### 2.5 Science field hubs (“Elm sahələri üzrə ocaqlar”)

| Category | Examples (business) | Technical structure |
|----------|-------------------|---------------------|
| Traditional sciences | Mathematics, physics, chemistry, biology, medicine | Hub landing page per field: overview, featured scholars, resources, events |
| Modern sciences | Nanotech, quantum physics, biomed, AI, cybersecurity | Same hub pattern; tag/filter taxonomy in search index |
| Interdisciplinary | Systems biology, materials science, space science | Cross-cutting hub pages with multi-tag filters |

**Relation to Encyclopedia:** Prominent Figures catalogue (`encyclopedia.html` + 200+ profile pages) partially fulfills “scientist biography dissemination”; field hubs extend this with living scholars, courses, and active research.

### 2.6 Multimedia hubs

| Format | Purpose | Technical delivery |
|--------|---------|-------------------|
| Podcasts | Popularize science | RSS feed + on-site player; podcast index page |
| Video lectures | Reach broad audience | YouTube/Vimeo embed gallery (pattern: Forum video gallery) |
| Animations / cartoons | Engage youth | Hosted video or Lottie animations; age-rated content tags |
| Scientist biographies | Inspire and educate | Encyclopedia profiles (delivered) + short-form video bios (Phase 3) |

### 2.7 Competitions and contests

| Type | Examples | Technical capability |
|------|----------|---------------------|
| Technical | Programming, cybersecurity, data science | Registration form + submission portal + judging workflow (Phase 4) |
| Creative | Music, visual arts | File upload + gallery of entries |
| Intellectual games | Quiz bowls, problem-solving | Timed quiz engine or third-party platform embed |

### 2.8 Medical hubs

| Focus | Content | Technical capability |
|-------|---------|---------------------|
| Healthy lifestyle | Prevention, wellness | Article hub + expert video series |
| Popular medical knowledge | Public health literacy | FAQ-style content; medically reviewed workflow |
| Modern medical research | Highlight DAAB scholar research | Research highlights linked to scholar profiles |

### 2.9 Social media presence

| Platform | Role | Integration |
|----------|------|-------------|
| Instagram | Visual outreach, events | Footer/header icon links; optional oEmbed feed widget |
| LinkedIn | Professional network | Organization page link; share buttons on news |
| Facebook | Community engagement | Page link; event cross-post |
| YouTube | Lectures, forum video | Channel link; embedded players on site |

---

## 3. Scope, phases, and assumptions

### 3.1 In scope (this specification)

- Full functional and non-functional requirements for the DAAB/WAAS web platform.
- IA and navigation for current and planned modules.
- Acceptance criteria for Phase 1 features (testable now).
- Forward-looking requirements for Phases 2–4 (design-ready, not yet implemented).

### 3.2 Out of scope (unless separately commissioned)

- Native mobile apps (responsive web is the mobile strategy).
- Custom video CDN or live streaming infrastructure (use YouTube/Vimeo).
- Full LMS replacement for universities.
- Automated machine translation of user-generated content.

### 3.3 Assumptions

- Primary hosting remains static-friendly (GitHub Pages, Netlify, or equivalent) for Phase 1.
- Azerbaijani (`az`) is the default locale; English (`en`) maintains structural parity.
- Content editors can run Python helpers locally; production ships HTML/CSS/JS/images/i18n only.
- PII (membership applications, contact details) never stored in the public Git repository.

### 3.4 Constraints

- Lowercase HTML filenames only.
- Assets live under `css/`, `js/`, `images/`, `cv/` — not repository root.
- Shared styles extend `css/daab-common.css` and `css/daab-tokens.css`.
- After path or shared asset changes: run `python helpers/_validate_site.py` and bump `?v=` cache busting.

---

## 4. Stakeholders and user personas

| Persona | Goals | Primary features |
|---------|-------|------------------|
| **General visitor** | Learn about DAAB/WAAS | Home, About, Activities |
| **Diaspora scientist** | Find peers, join network | Scientists catalogue, Encyclopedia, Membership |
| **Prospective member** | Understand benefits and apply | Membership funnel, application form, flyer |
| **Listed scientist** | Be discoverable with accurate profile | Profile card, QR, deep link |
| **Student / learner** | Access courses and materials | Teaching hubs (Phase 3), multimedia |
| **Partner institution** | Cooperation, forum materials | Forum microsite, cooperation page |
| **Content editor** | Update pages safely | HTML templates, i18n JSON, helper scripts |
| **Site administrator** | Deploy, monitor, validate | Deploy checklist, validators, analytics |
| **Board / leadership** | Governance visibility | Executive board, charter, official addresses |

---

## 5. Information architecture

### 5.1 Top-level domains of content

```text
DAAB / WAAS Platform
├── Gateway (language selection)
├── Institutional core (About, Activities, Membership)
├── Scientists & scholars (directory, profiles, encyclopedia)
├── Events & forums (Forum 2024; future forums as siblings)
├── Learning & resources (Phase 3+)
│   ├── Virtual university / teaching hubs
│   ├── Field-of-science portals
│   ├── Multimedia centre
│   └── Medical hubs
├── Engagement (Phase 4+)
│   ├── Competitions
│   └── Community / social
└── Utilities (search, language switch, embeds)
```

### 5.2 URL and folder conventions

| Pattern | Example | Rule |
|---------|---------|------|
| Locale prefix | `az/`, `en/` | All public pages under locale folder |
| Section nesting | `az/forum/2024/program.html` | Max 3 levels preferred for breadcrumbs |
| Scientists | `az/scientists/list.html`, `profiles.html` | Subfolder per major feature |
| Encyclopedia | `az/encyclopedia.html`, `az/prominent_figures/{group}/{slug}.html` | Hub + profile tree |
| Assets | `css/`, `js/`, `images/` | Relative from locale depth (`../` or `../../`) |
| i18n config | `i18n/routes.json` | Single source of truth for page IDs and AZ/EN paths |

### 5.3 Page inventory (Phase 1 — delivered)

| Area | AZ path | EN path | Count (per locale) |
|------|---------|---------|-------------------|
| Core pages | `az/*.html` | `en/*.html` | 10+ |
| Scientists | `az/scientists/` | `en/scientists/` | 2 |
| Forum 2024 | `az/forum/2024/` | `en/forum/2024/` | 12 |
| Encyclopedia hub | `az/encyclopedia.html` | `en/encyclopedia.html` | 1 |
| Prominent figure profiles | `az/prominent_figures/` | `en/prominent_figures/` | 200+ |
| Gateway | `index.html` | — | 1 (shared) |

### 5.4 Planned IA additions (Phases 2–4)

| Module | Proposed path | Nav placement |
|--------|---------------|---------------|
| Resource library | `az/resources/` | Activities → Resources |
| Teaching hubs | `az/learn/` | New top-level: **Təhsil / Learning** |
| Field portals | `az/fields/{slug}/` | Under Learning or Encyclopedia |
| Multimedia centre | `az/media/` | Activities or Learning |
| Competitions | `az/competitions/` | Activities |
| Medical hub | `az/health/` | Learning |

---

## 6. Navigation structure

### 6.1 Primary navigation (current — implemented)

| Order | AZ | EN | Type | Config source |
|-------|----|----|------|---------------|
| 1 | Ana səhifə | Home | Page | `nav.json` |
| 2 | Ensiklopediya | Encyclopedia | Page | `nav.json` |
| 3 | Fəaliyyətimiz | Activities | Group | `nav.json` |
| 4 | Alimlərimiz | Scientists | Group (dropdown) | `nav.json` |
| 5 | Haqqımızda | About us | Group (mega-menu) | `nav.json` |
| 6 | Üzvlük | Membership | Group (dropdown) | `nav.json` |

### 6.2 Secondary navigation

| Mechanism | Script / style | When shown |
|-----------|----------------|------------|
| Breadcrumbs | `daab-breadcrumbs.js` | All pages except gateway |
| Section siblings | Primary nav mega-menu (`daab-primary-nav.js`, `i18n/nav.json`) | About, Scientists, Membership, Forum groups |
| Hub cards | `daab-hub-cards.css` | Home, Forum index |
| Sidebar TOC / timeline | `daab-sidebar-widget.css`, `daab-sidebar-timeline.js` | Charter, presentations, activities, stories |
| In-page anchors | HTML `id` attributes | Long articles, speeches |
| Footer links | Static in `FOOTER` partial / HTML | Contact, leadership, legal |

### 6.3 Navigation requirements (all phases)

| ID | Requirement |
|----|-------------|
| NAV-01 | Primary nav MUST be driven from `i18n/nav.json` and rendered by `daab-primary-nav.js` when `data-daab-nav-mount="1"`. |
| NAV-02 | Active page MUST expose `aria-current="page"`; parent groups MUST show `has-active-child` when a child is active. |
| NAV-03 | Mobile nav MUST use hamburger pattern with focus trap and `scroll-lock` on `body`. |
| NAV-04 | Maximum 7±2 top-level items; deeper pages use section nav, not additional top-level links. |
| NAV-05 | Every nav label MUST exist in both `ui.json` → `nav.az` and `nav.en`. |
| NAV-06 | Legacy URLs MUST redirect via `routes.json page pairs` in `routes.json`. |
| NAV-07 | Forum and future event microsites MUST use section nav, not top-level proliferation. |

### 6.4 Proposed navigation (Phase 3)

Add **Təhsil / Learning** as a top-level group:

```text
Təhsil / Learning
├── Virtual university overview
├── Courses & programs
├── Field-of-science hubs
├── Multimedia centre
└── Medical hub
```

---

## 7. Functional requirements

Requirements use prefixes: **FR** (functional), **FR-P1** (Phase 1 delivered), **FR-P2+** (planned).

### 7.1 Institutional and communication (Phase 1)

| ID | Feature | Requirement | Implementation |
|----|---------|-------------|----------------|
| FR-P1-01 | Language gateway | Redirect to `az/` or `en/` based on `localStorage`; `?choose=1` forces chooser; `?lang=` overrides | `index.html`, `daab-i18n.js` |
| FR-P1-02 | Home hub | Section discovery cards route to major areas | `az/index.html`, `daab-hub-cards.css` |
| FR-P1-03 | About pages | Foundation, Mission, Board, Charter with shared hero pattern | Content pages + section nav |
| FR-P1-04 | Activities | News/timeline with sidebar jumps | `activities.html`, `daab-sidebar-timeline.js` |
| FR-P1-05 | Site search | Ctrl/Cmd+K overlay; AZ character normalization | `daab-search.js`, `search-index.json` |
| FR-P1-06 | Language switch | Open paired page from `routes.json`; persist preference | `daab-i18n.js`, `daab-lang-position.js` |

### 7.2 Scientists data bank (Phase 1 + extensions)

| ID | Feature | Requirement | Phase |
|----|---------|-------------|-------|
| FR-P1-10 | List view | Sortable table; country/field filters; hover preview | P1 |
| FR-P1-11 | Profile cards | Multi-filter, pagination, badge sync | P1 |
| FR-P1-12 | Deep linking | `#slug` opens matching profile card | P1 |
| FR-P1-13 | QR codes | Per-profile QR linking to canonical URL | P1 |
| FR-P1-14 | TTS | Read profile text via Web Speech API | P1 |
| FR-P2-10 | Extended schema | Education, skills, publications, ORCID fields in data model | P2 |
| FR-P2-11 | Contact opt-in | Scientist controls public email visibility | P2 |
| FR-P2-12 | Admin intake | Secure form for scholars to submit profile updates | P2 |
| FR-P2-13 | Export | CSV/JSON export for internal collaboration matching | P2 |

**Data sync rule:** `js/scientists-catalog-data.js` and inline `DATA` in list view MUST stay synchronized when records change.

### 7.3 Encyclopedia / prominent figures (Phase 1)

| ID | Feature | Requirement |
|----|---------|-------------|
| FR-P1-20 | Hub page | Filter and sort by period, field, country, group (Azerbaijani & Turkic / World) |
| FR-P1-21 | Profile pages | Biography sections: Life, Scholarly work, Contribution; sidebar metadata |
| FR-P1-22 | Bilingual profiles | AZ source in `az/prominent_figures/`; EN mirror in `en/prominent_figures/` |
| FR-P1-23 | Internal linking | Prev/next profile navigation within group |
| FR-P1-24 | Catalogue data | `prominent-figures-catalog-data.js` (+ EN variant) powers hub filters |

### 7.4 Membership funnel (Phase 1 + Phase 2 backend)

| ID | Feature | Requirement | Phase |
|----|---------|-------------|-------|
| FR-P1-30 | Value proposition | Benefits page with CTA to application | P1 |
| FR-P1-31 | Terms | Categories, fees, rights, obligations | P1 |
| FR-P1-32 | Application wizard | 4-step form with client validation UI | P1 |
| FR-P1-33 | Flyer | Print/PDF (jsPDF) and Share (Web Share API) | P1 |
| FR-P2-30 | Server submit | POST application JSON to approved backend | P2 |
| FR-P2-31 | Draft save | Optional `sessionStorage` draft on same device | P2 |
| FR-P2-32 | Admin notification | Email to board on new submission | P2 |
| FR-P2-33 | Status workflow | Submitted → Under review → Accepted/Rejected | P2 |

### 7.5 Forum and events (Phase 1)

| ID | Feature | Requirement |
|----|---------|-------------|
| FR-P1-40 | Forum hub | Card grid to 11 subpages |
| FR-P1-41 | Photo gallery | Categories, lazy load, lightbox, keyboard nav |
| FR-P1-42 | Video gallery | YouTube links; external tab |
| FR-P1-43 | Presentations TOC | Sidebar jump navigation |
| FR-P1-44 | Event template | Reusable pattern for Forum 2025+ (copy `forum/2024/` structure) |

### 7.6 Virtual university & teaching (Phase 3)

| ID | Feature | Requirement |
|----|---------|-------------|
| FR-P3-01 | Course catalogue | List courses with title, instructor, language, level, format |
| FR-P3-02 | Course detail | Syllabus, modules, prerequisites, enrollment CTA |
| FR-P3-03 | Faculty structure | Faculty → department → course hierarchy |
| FR-P3-04 | Lecture embed | YouTube/Vimeo player with transcript link |
| FR-P3-05 | Live sessions | Embed scheduled stream; calendar integration (ICS download) |
| FR-P3-06 | External MOOC links | Curated directory with platform badge |
| FR-P3-07 | Progress tracking | Requires authenticated learner account (LMS or SSO) |

### 7.7 Teaching programs & textbooks (Phase 3–4)

| ID | Feature | Requirement |
|----|---------|-------------|
| FR-P3-10 | Program registry | Multi-module programs with AZ/EN metadata |
| FR-P3-11 | Downloadable materials | PDF/EPUB links with license label |
| FR-P4-10 | Audio books | MP3/stream links |
| FR-P4-11 | Commerce links | Amazon/affiliate URLs for print and e-book formats |

### 7.8 Science field hubs (Phase 3)

| ID | Feature | Requirement |
|----|---------|-------------|
| FR-P3-20 | Field landing | Overview, featured scholars, resources, related courses |
| FR-P3-21 | Taxonomy | Traditional / modern / interdisciplinary tags in search index |
| FR-P3-22 | Cross-link | Field hub ↔ Encyclopedia profiles ↔ Scientists catalogue |

### 7.9 Multimedia centre (Phase 3)

| ID | Feature | Requirement |
|----|---------|-------------|
| FR-P3-30 | Video library | Reuse gallery pattern; categories: lectures, labs, biographies |
| FR-P3-31 | Podcast index | RSS feed link; episode list with duration and date |
| FR-P3-32 | Animation series | Youth content tag; parental guidance label where needed |

### 7.10 Competitions (Phase 4)

| ID | Feature | Requirement |
|----|---------|-------------|
| FR-P4-20 | Competition listing | Status: upcoming / open / closed / results |
| FR-P4-21 | Registration | Authenticated or email-verified registration |
| FR-P4-22 | Submission | File/code upload with virus scan and size limits |
| FR-P4-23 | Judging | Role-based reviewer access; scoring rubric |
| FR-P4-24 | Results | Public leaderboard or winner gallery |

### 7.11 Medical hubs (Phase 3–4)

| ID | Feature | Requirement |
|----|---------|-------------|
| FR-P3-40 | Content sections | Lifestyle, popular medicine, research highlights |
| FR-P3-41 | Medical review | Content workflow: draft → medical reviewer → published |
| FR-P3-42 | Disclaimer | Prominent non-diagnostic disclaimer on all health content |

### 7.12 Social media integration (Phase 1–2)

| ID | Feature | Requirement |
|----|---------|-------------|
| FR-P1-50 | Footer social icons | Instagram, LinkedIn, Facebook, YouTube with `rel="noopener"` |
| FR-P2-50 | Share buttons | Share on news/activity items (Web Share API + fallback) |
| FR-P2-51 | Optional feed embed | Config-driven oEmbed or static “latest posts” curation |

---

## 8. Non-functional requirements

### 8.1 Reliability and availability

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-01 | Static pages served without application server dependency | 99.9% uptime (hosting SLA) |
| NFR-02 | No single point of failure for read-only content | CDN or dual hosting optional |
| NFR-03 | Graceful degradation if search index fails to load | Nav and links remain usable |

### 8.2 Maintainability

| ID | Requirement |
|----|-------------|
| NFR-10 | All page IDs registered in `i18n/routes.json` |
| NFR-11 | Validators run before release: `_validate_site.py`, `_validate_bilingual.py` |
| NFR-12 | Design tokens in `css/daab-tokens.css`; no new root-level CSS/JS |
| NFR-13 | Helper scripts in `helpers/` only; not deployed to production |

### 8.3 Compatibility

| ID | Requirement |
|----|-------------|
| NFR-20 | Support latest two versions of Chrome, Firefox, Safari, Edge |
| NFR-21 | iOS Safari and Android Chrome for mobile |
| NFR-22 | ES5-compatible bundles not required; modern evergreen browsers assumed |

### 8.4 Privacy and compliance

| ID | Requirement |
|----|-------------|
| NFR-30 | Cookie/consent banner if analytics or third-party embeds track users |
| NFR-31 | Privacy policy page linked from footer (Phase 2) |
| NFR-32 | GDPR-style data subject rights for stored applications and profiles (Phase 2+) |

### 8.5 Operability

| ID | Requirement |
|----|-------------|
| NFR-40 | Documented deploy checklist (`DAAB-Deploy-Checklist.md`) |
| NFR-41 | Version cache bust on shared CSS/JS changes |
| NFR-42 | Rollback via Git revert + redeploy |

---

## 9. UI/UX standards

### 9.1 Design system reference

| Layer | Location | Purpose |
|-------|----------|---------|
| Tokens | `css/daab-tokens.css` | Colors, typography, spacing, radii, shadows, z-index |
| Global | `css/daab-common.css` | Reset, nav, buttons, footer, forms base |
| Mobile | `css/daab-mobile.css` | Touch targets, safe-area, compact nav |
| Feature modules | `css/daab-*.css` | Page-specific layouts |
| JS tokens | `i18n/design-system.json`, `daab-design-tokens.js` | Breakpoints for nav/sidebar |
| Copy | `i18n/ui.json` | Nav, breadcrumbs, search, buttons |

### 9.2 Typography

| Use | Font | Fallback |
|-----|------|----------|
| Headings / hero | Playfair Display | Georgia, serif |
| Body / UI | Inter | system-ui, sans-serif |
| Minimum body size | 16px (1rem) on mobile | — |
| Line height (prose) | 1.6–1.75 | — |

### 9.3 Color and brand

- Primary institutional blue from `--blue-700` token family.
- Gold accent for hero tags and highlights (`--gold` / hero-tag gold variant).
- Semantic surfaces: `--soft`, `--color-surface-toolbar` for toolbars and cards.
- Do not introduce one-off hex colors in page CSS; extend tokens.

### 9.4 Layout

| Element | Rule |
|---------|------|
| Content shell | Max width via `.shell`; horizontal padding `--shell-padding-x` |
| Hero | Shared `daab-content-hero.css` / `daab-hero-summary.css` patterns |
| Cards | Consistent radius `--radius`, shadow `--shadow` |
| Sticky chrome | Nav + breadcrumbs; offset via `--daab-sticky-top-stack` |

### 9.5 Components (required patterns)

| Component | Standard |
|-----------|----------|
| Buttons | `.btn`, `.btn-primary`, `.btn-secondary`; min touch 44×44px |
| Forms | Visible labels; error states; `aria-invalid`, `aria-describedby` |
| Tables | Scientists list: resizable columns, sort indicators, hover preview |
| Cards | Profile cards: photo, name, fields, QR, action row |
| Modals / lightbox | Focus trap; Esc to close; `aria-modal="true"` |
| Empty states | Clear message when filters return zero results |

### 9.6 Motion

- Respect `prefers-reduced-motion`: disable non-essential transitions.
- Standard transition: `--transition-fast` (150–200ms).
- No autoplay video with sound.

### 9.7 Content tone

- Institutional, academic, respectful.
- AZ: formal Azerbaijani; EN: polished international English (WAAS branding).
- Avoid emoji in primary navigation labels (optional in body content only).

---

## 10. Multilingual support

### 10.1 Locale model

| Property | Value |
|----------|-------|
| Default locale | `az` |
| Supported locales | `az`, `en` |
| URL strategy | Path prefix (`/az/`, `/en/`) |
| Config | `i18n/routes.json`, `ui.json`, `nav.json`, `page-subtitles.json` |
| HTML | `lang="az"` or `lang="en"`; `data-daab-lang` on `<html>` |
| Page pairing | Each `page.id` maps `az` and `en` paths |

### 10.2 Translation workflow

1. Author content in AZ (primary).
2. Create EN mirror with equivalent structure (not machine-translated for institutional prose).
3. Register both paths in `routes.json`.
4. Add UI strings to `ui.json` under `az` and `en` keys.
5. Run `_validate_bilingual.py` before release.

### 10.3 Language switcher behavior

| Rule | Detail |
|------|--------|
| Persistence | `localStorage.daab-lang` |
| Scroll preservation | `daab-lang-position.js` stores section anchor |
| Missing pair | Fall back to locale home; log in validator |
| Gateway | Root `index.html` redirects; `?choose=1` shows explicit chooser |

### 10.4 Future locales

Architecture supports additional locales by extending `routes.json` → `languages[]` and adding `tr`, `ru`, etc. paths. Not in current scope.

---

## 11. Responsive design rules

### 11.1 Breakpoints (authoritative)

| Name | Width | Behavior |
|------|-------|----------|
| Mobile | &lt; 768px | Single column; hamburger nav; stacked heroes |
| Tablet | 768–1179px | Two-column where appropriate; condensed nav |
| Desktop | ≥ 1180px | Full nav (`navCompact` breakpoint); mega-menu |
| Sidebar stack | &lt; 1060px | Sidebar widgets move below main content |

Source: `i18n/design-system.json`, `daab-design-tokens.js`.

### 11.2 Mobile-specific rules

| Rule | Implementation |
|------|----------------|
| Viewport meta | `width=device-width, initial-scale=1.0, viewport-fit=cover` on all pages |
| Touch targets | Minimum 44×44px (`--daab-touch-min`) |
| Safe areas | `env(safe-area-inset-*)` for notched devices |
| Tables | Scientists list: horizontal scroll or card fallback on narrow screens |
| Filters | Collapsible drawer for scientists and encyclopedia toolbars |
| Sticky toolbars | Profile/catalogue toolbars stick below nav stack |

### 11.3 Images and media

- Responsive images: `max-width: 100%`; explicit `width`/`height` where possible to reduce CLS.
- Gallery thumbnails: lazy-load via `loading="lazy"`.
- Flyer/PDF: fixed A4 aspect for print; screen scales down.

### 11.4 Testing viewports (QA)

| Device class | Width × height |
|--------------|----------------|
| Mobile S | 375 × 667 |
| Mobile L | 414 × 896 |
| Tablet | 768 × 1024 |
| Laptop | 1280 × 800 |
| Desktop | 1920 × 1080 |

---

## 12. Accessibility requirements

Target: **WCAG 2.1 Level AA** for all public pages.

| ID | Requirement | Verification |
|----|-------------|--------------|
| A11Y-01 | Skip to content link as first focusable element | Keyboard test |
| A11Y-02 | Logical heading hierarchy (one `h1` per page) | axe / manual |
| A11Y-03 | All images have meaningful `alt` (decorative: `alt=""`) | HTML audit |
| A11Y-04 | Color contrast ≥ 4.5:1 body text, ≥ 3:1 large text | Contrast checker |
| A11Y-05 | Focus visible on all interactive elements | Keyboard walkthrough |
| A11Y-06 | `aria-current="page"` on active nav item | DOM inspection |
| A11Y-07 | Mobile menu: focus trap, Esc closes, return focus to toggle | Manual test |
| A11Y-08 | Form fields: associated `<label>`; errors announced | Screen reader |
| A11Y-09 | Lightbox: `aria-modal`, focus management, Esc closes | Manual test |
| A11Y-10 | TTS: optional enhancement; must not be only access path | Policy |
| A11Y-11 | `prefers-reduced-motion` honored | CSS check |
| A11Y-12 | Language declared: `<html lang="...">` | Validator |

---

## 13. Performance expectations

| Metric | Target (Phase 1 static) | Measurement |
|--------|-------------------------|-------------|
| LCP (Largest Contentful Paint) | &lt; 2.5s on 4G | Lighthouse mobile |
| INP (Interaction to Next Paint) | &lt; 200ms | Lighthouse |
| CLS (Cumulative Layout Shift) | &lt; 0.1 | Lighthouse |
| Total page weight (HTML+CSS+JS, no images) | &lt; 500 KB | Network tab |
| Search index load | Async; non-blocking | Script `defer` |
| Photo gallery | Lazy-load thumbs; manifest-driven | Custom audit |
| Time to interactive (home) | &lt; 3s mid-tier mobile | WebPageTest |

### 13.1 Optimization rules

- All scripts use `defer` unless inline bootstrapping required (gateway redirect).
- Shared CSS bundled per page type; avoid loading unused forum CSS on membership pages.
- Cache bust via `?v=` on `css/` and `js/` when content changes.
- Images: WebP/AVIF where conversion pipeline exists; SVG for logos/icons.
- Minimize third-party scripts; flyer PDF libs loaded only on flyer page.

---

## 14. Security considerations

| ID | Threat | Mitigation |
|----|--------|------------|
| SEC-01 | XSS via injected HTML | Static content only; sanitize if CMS/user input added (Phase 2+) |
| SEC-02 | PII in Git repo | Never commit applications; use backend store |
| SEC-03 | Form spam | CAPTCHA/honeypot on server-backed forms (Phase 2) |
| SEC-04 | MITM | HTTPS only in production; HSTS at hosting layer |
| SEC-05 | Dependency supply chain | Pin CDN versions; prefer self-hosted for critical libs |
| SEC-06 | Admin access | IAM for review portal; MFA for board tools (Phase 2+) |
| SEC-07 | File upload abuse | Type/size limits; virus scan; isolated storage (Phase 4) |
| SEC-08 | Embedding attacks | `rel="noopener noreferrer"` on external links; CSP headers at host |
| SEC-09 | Search index leakage | Never index private or draft content in `search-index.json` |

---

## 15. Integration points

### 15.1 Current and planned integrations

| System | Purpose | Phase | Protocol |
|--------|---------|-------|----------|
| YouTube | Forum and lecture video | P1 | External links / embed iframe |
| Google Fonts | Inter, Playfair Display | P1 | CSS `@import` / link |
| jsPDF + html2canvas | Flyer PDF export | P1 | Client-side CDN |
| Web Share API | Flyer share | P1 | Browser API |
| Web Speech API | Profile TTS | P1 | Browser API |
| Formspree / Apps Script / Supabase | Membership applications | P2 | HTTPS POST JSON |
| Google Analytics / Plausible | Usage analytics | P2 | Script tag + consent |
| ORCID API | Scholar identifier lookup | P2 | OAuth / public API |
| Amazon Associates | Textbook links | P4 | Affiliate URLs |
| LMS (Moodle/Canvas) | Course delivery | P3 | LTI or SSO |
| Zoom / YouTube Live | Live lectures | P3 | Embed + calendar |
| Instagram / LinkedIn / Facebook | Social presence | P1–P2 | Outbound links; optional oEmbed |
| GitHub Pages / static host | Production deploy | P1 | Git push / CI |

### 15.2 API design guidelines (Phase 2+)

- REST or serverless functions over HTTPS.
- JSON request/response; UTF-8.
- Version prefix: `/api/v1/`.
- Rate limiting on public endpoints.
- No API keys in client-side static JS.

---

## 16. Content management needs

### 16.1 Current model (Phase 1)

| Content type | Authoring | Build / validate |
|--------------|-----------|------------------|
| HTML pages | Edit `az/` and `en/` mirrors | `_validate_site.py` |
| Nav / routes | `i18n/nav.json`, `routes.json` | `_validate_bilingual.py` |
| Scientists data | `scientists-catalog-data.js`, list inline DATA | `_validate_cv_cards.py`, `_check_name_order.py` |
| Encyclopedia | Profile HTML + catalog JS | `_build_prominent_figures_catalog.py` |
| Search index | `i18n/search-index.json` | `_build_search_index.py` |
| Photos gallery | Manifest JSON + images | `_build_photos_gallery_manifest.py` |

### 16.2 Editor requirements

| ID | Requirement |
|----|-------------|
| CMS-01 | Templates for new pages: include viewport, CSS list, JS list, `data-daab-page-id` |
| CMS-02 | Checklist before publish: validators, cache bump, spot-check nav |
| CMS-03 | Image guidelines: max dimensions, alt text, `_thumbs/` for galleries |
| CMS-04 | AZ/EN parity checklist per page |

### 16.3 Future CMS (Phase 2–3)

Recommended: headless CMS (Sanity, Contentful, or Decap CMS for Git-based workflow) for:

- News / activities posts
- Course catalogue
- Resource library metadata
- Competition announcements

Static site generators or CI webhooks regenerate `az/` and `en/` HTML on publish.

---

## 17. Testing criteria

### 17.1 Automated checks (release gate)

| Script | Purpose | Must pass |
|--------|---------|-----------|
| `helpers/_validate_site.py` | Broken links, asset paths, HTML structure | Yes |
| `helpers/_validate_bilingual.py` | AZ/EN route parity | Yes |
| `helpers/_validate_section_anchors.py` | In-page anchor integrity | Yes |
| `helpers/_validate_cv_cards.py` | Scientists profile data | When scientists change |
| `helpers/_check_name_order.py` | Alphabetical order | When scientists change |

### 17.2 Manual test matrix

| Area | Tests |
|------|-------|
| Gateway | AZ default; EN persist; `?choose=1`; query preserved |
| Nav | All top-level and dropdown links; mobile hamburger; active states |
| Language switch | Every page type; scroll position on long pages |
| Search | AZ diacritics; EN terms; keyboard shortcut |
| Scientists | Sort, filter, preview, pagination, deep link, TTS |
| Encyclopedia | Filters, profile navigation, AZ/EN content parity |
| Membership | Form steps, validation messages, flyer PDF |
| Forum | Gallery lightbox; video external links; sidebar TOC |
| Accessibility | Keyboard-only pass on 5 representative pages |
| Responsive | 5 viewports on home, scientists, encyclopedia, application |
| Performance | Lighthouse on home + heaviest gallery page |
| Print | Charter and flyer print layouts |

### 17.3 Regression triggers

Full manual matrix required when changing:

- `daab-nav.js`, `daab-primary-nav.js`, `daab-i18n.js`
- `i18n/routes.json`, `nav.json`
- `css/daab-common.css`, `daab-tokens.css`
- Scientists or encyclopedia data pipelines

### 17.4 Phase 2+ additional tests

| Feature | Tests |
|---------|-------|
| Form backend | Submit success/failure; spam rejection; email notification |
| Auth admin | Login, role access, logout, session timeout |
| LMS embed | Course embed loads; SSO redirect |
| Competitions | Upload limits; deadline enforcement |

---

## 18. Acceptance criteria by major feature

Each feature lists **given / when / then** criteria testable by QA.

### 18.1 Language gateway

| # | Criterion |
|---|-----------|
| AC-GW-01 | **Given** a first-time visitor, **when** opening `/index.html`, **then** browser redirects to `az/index.html` within 1s. |
| AC-GW-02 | **Given** `localStorage.daab-lang = "en"`, **when** opening `/index.html`, **then** redirect goes to `en/index.html`. |
| AC-GW-03 | **Given** `?choose=1`, **when** page loads, **then** gateway card shows AZ and EN buttons without auto-redirect. |

### 18.2 Primary navigation

| # | Criterion |
|---|-----------|
| AC-NAV-01 | **Given** any content page, **when** viewing desktop width ≥1180px, **then** all top-level nav items are visible without horizontal scroll. |
| AC-NAV-02 | **Given** mobile width &lt;768px, **when** opening menu, **then** focus is trapped until menu closes. |
| AC-NAV-03 | **Given** current page is `mission.html`, **then** About group shows active child and `aria-current` is set. |

### 18.3 Site search

| # | Criterion |
|---|-----------|
| AC-SRCH-01 | **Given** any page with search, **when** pressing Ctrl+K, **then** search overlay opens and input is focused. |
| AC-SRCH-02 | **Given** query with AZ characters (ə, ş, ı), **when** searching, **then** relevant AZ pages appear. |
| AC-SRCH-03 | **Given** a result click, **when** navigating, **then** correct locale page opens. |

### 18.4 Scientists directory (list)

| # | Criterion |
|---|-----------|
| AC-SCI-L-01 | **Given** list page, **when** sorting by name, **then** order follows locale collation rules. |
| AC-SCI-L-02 | **Given** country filter applied, **when** viewing table, **then** only matching rows display. |
| AC-SCI-L-03 | **Given** row hover, **when** pointer rests 300ms, **then** preview popover shows photo and summary. |

### 18.5 Scientists profiles (cards)

| # | Criterion |
|---|-----------|
| AC-SCI-P-01 | **Given** profiles page, **when** applying field filter, **then** card count and badges update synchronously. |
| AC-SCI-P-02 | **Given** URL `profiles.html#slug`, **when** page loads, **then** matching card expands or scrolls into view. |
| AC-SCI-P-03 | **Given** TTS button, **when** activated, **then** profile text is spoken in page language. |
| AC-SCI-P-04 | **Given** QR on card, **when** scanned, **then** device opens correct profile URL. |

### 18.6 Encyclopedia

| # | Criterion |
|---|-----------|
| AC-ENC-01 | **Given** encyclopedia hub, **when** filtering by group “World scientists”, **then** only world figures display. |
| AC-ENC-02 | **Given** profile page, **when** switching language, **then** EN profile opens with equivalent structure. |
| AC-ENC-03 | **Given** profile prev/next nav, **when** clicking next, **then** adjacent profile in catalogue order loads. |
| AC-ENC-04 | **Given** AZ profile prose, **when** viewing EN mirror, **then** biographical content is in English (not placeholder template text). |

### 18.7 Membership funnel

| # | Criterion |
|---|-----------|
| AC-MEM-01 | **Given** value page, **when** clicking join CTA, **then** user reaches application wizard. |
| AC-MEM-02 | **Given** application step 1, **when** required fields empty and user continues, **then** inline validation messages appear. |
| AC-MEM-03 | **Given** completed wizard (Phase 1), **when** submitting, **then** success screen displays and instructions mention email for CV. |
| AC-MEM-04 | **Given** flyer page, **when** Print/PDF clicked, **then** single A4 PDF downloads with branding intact. |
| AC-MEM-05 | **Given** Phase 2 backend live, **when** submitting valid form, **then** HTTP 2xx and confirmation email sent. |

### 18.8 Forum 2024 microsite

| # | Criterion |
|---|-----------|
| AC-FOR-01 | **Given** forum hub, **when** loading, **then** all 11 section cards link to valid pages. |
| AC-FOR-02 | **Given** photo gallery, **when** thumbnail clicked, **then** lightbox opens with keyboard prev/next. |
| AC-FOR-03 | **Given** video gallery, **when** play clicked, **then** YouTube opens in new tab with `noopener`. |

### 18.9 About and governance

| # | Criterion |
|---|-----------|
| AC-ABT-01 | **Given** charter page, **when** sidebar TOC link clicked, **then** page scrolls to correct article anchor. |
| AC-ABT-02 | **Given** executive board, **when** viewing mobile, **then** member cards stack in single column without overlap. |

### 18.10 Virtual university (Phase 3 — forward)

| # | Criterion |
|---|-----------|
| AC-LRN-01 | **Given** course catalogue, **when** filtering by language AZ, **then** only AZ-tagged courses show. |
| AC-LRN-02 | **Given** course detail, **when** enrollment CTA clicked, **then** user reaches LMS or contact flow. |
| AC-LRN-03 | **Given** live lecture scheduled, **when** within 15 min of start, **then** embed shows live stream or waiting state. |

### 18.11 Competitions (Phase 4 — forward)

| # | Criterion |
|---|-----------|
| AC-CMP-01 | **Given** open competition, **when** deadline passed, **then** registration form is disabled. |
| AC-CMP-02 | **Given** file submission, **when** file exceeds size limit, **then** clear error without server crash. |

### 18.12 Cross-cutting release criteria

| # | Criterion |
|---|-----------|
| AC-REL-01 | All automated validators pass with zero errors. |
| AC-REL-02 | No broken internal links on sampled 20 pages per locale. |
| AC-REL-03 | Lighthouse accessibility score ≥ 90 on home page. |
| AC-REL-04 | `sitemap.xml` includes all public routes except `sitemap: false` entries. |
| AC-REL-05 | Production deploy excludes `helpers/`, `documents/`, `__pycache__/`. |

---

## 19. Appendices

### Appendix A — Traceability matrix (business → technical)

| Siracov theme | Phase | Primary FR IDs | Primary AC IDs |
|---------------|-------|----------------|----------------|
| Website as hub | P1 | FR-P1-01–06 | AC-GW, AC-NAV, AC-ABT |
| Scholars data bank | P1–P2 | FR-P1-10–14, FR-P2-10–13 | AC-SCI-L, AC-SCI-P |
| Virtual university | P3 | FR-P3-01–07 | AC-LRN |
| Programs & textbooks | P3–P4 | FR-P3-10–11, FR-P4-10–11 | AC-LRN |
| Science field hubs | P3 | FR-P3-20–22 | AC-ENC, AC-LRN |
| Multimedia | P3 | FR-P3-30–32 | AC-FOR (video pattern) |
| Competitions | P4 | FR-P4-20–24 | AC-CMP |
| Medical hubs | P3–P4 | FR-P3-40–42 | AC-LRN |
| Social media | P1–P2 | FR-P1-50, FR-P2-50–51 | AC-NAV (footer links) |

### Appendix B — Key repository paths

| Path | Role |
|------|------|
| `az/`, `en/` | Locale content roots |
| `i18n/` | Routes, nav, UI strings, search index |
| `css/daab-tokens.css` | Design tokens |
| `js/daab-i18n.js` | Language and routing |
| `js/daab-primary-nav.js` | Navigation rendering |
| `helpers/_validate_site.py` | Release validation |
| `documents/DAAB-Site-Stability-and-Deployment-Guide.md` | Deploy rules |

### Appendix C — Related documents

| Document | Topic |
|----------|-------|
| `DAAB-Website-Business-Requirements.md` | As-built BRD |
| `DAAB-Navigation-and-Information-Architecture-Strategy.md` | IA strategy |
| `DAAB-Design-System-Architecture.md` | Design tokens |
| `DAAB-Bilingual-Website-Strategy.md` | i18n strategy |
| `DAAB-Membership-Application-Storage-Strategy.md` | Form backend |
| `DAAB-Site-Stability-and-Deployment-Guide.md` | Hosting and validation |

### Appendix D — Glossary

| Term | Definition |
|------|------------|
| DAAB | Dünya Azərbaycanlı Alimlər Birliyi |
| WAAS | World Association of Azerbaijani Scientists (English branding) |
| Gateway | Root `index.html` language router |
| Hub page | Card-grid landing linking to section subpages |
| Mega-menu section | Primary nav dropdown listing sibling pages in a site group (About, Scientists, Membership, Forum) |
| Profile deep link | URL hash identifying one scientist card |
| Phase | Delivery tranche (P1 delivered, P2–P4 planned) |

---

*End of technical specification.*
