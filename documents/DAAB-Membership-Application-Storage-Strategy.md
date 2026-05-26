# DAAB / WAAS — Membership application storage strategy

This document describes how to **store and manage membership application submissions** for the bilingual application forms (`az/application.html`, `en/application.html`). It is tailored to the current stack: **static HTML** on GitHub Pages / `daab-waas.com`, client script `js/daab-membership-application.js`, and deployment rules in `documents/DAAB-Site-Stability-and-Deployment-Guide.md`.

---

## 1. Current behaviour (as of 2026)

| Item | Detail |
|------|--------|
| **Pages** | `az/application.html`, `en/application.html` (built from `az/application/application.html`, `en/application/application.html` via `helpers/_build_az_application_page.py`, `helpers/_build_en_application_page.py`) |
| **Submit handler** | `daabApplicationSubmit()` in `js/daab-membership-application.js` |
| **What happens on submit** | Success screen is shown in the browser only; **no data is sent to a server or database** |
| **CV / photo** | Applicants are asked to email `bilik.birlik@gmail.com` after submitting the form |
| **Hosting constraint** | The public site ships `*.html`, `css/`, `js/`, `images/` only — **not** `helpers/` or server-side code |

**Implication:** The association does not automatically receive a structured record of each application. Any “keeping” of applications for review must be added deliberately.

---

## 2. Two different needs

| Goal | What it means | Where it lives |
|------|----------------|----------------|
| **Applicant convenience** | “Don’t lose my progress if I close the tab” | Browser only (draft) |
| **Organization record** | “We have every submission, searchable, for board review” | Server-side store (required for official records) |

**Recommendation:** Support both layers — optional **draft** in the browser for UX, and a **mandatory server-side store** on submit.

---

## 3. What not to use as the primary solution

| Approach | Why it is insufficient alone |
|----------|------------------------------|
| **Success screen only** (current) | No record for DAAB/WAAS; applicant may think data was received by the board |
| **Email-only** (`mailto:` or manual copy-paste) | Unreliable delivery, no structured export, hard to audit |
| **`localStorage` / `sessionStorage` only** | Data stays on one device/browser; cleared with cache; not visible to admins |
| **Files in the Git repo** | PII must not be committed; repo is public or widely cloned |
| **Search index** (`i18n/search-index.json`) | Public content only; never index form submissions |

CV and photo files should continue to use **email** (or a dedicated upload service later), not the static site repository.

---

## 4. Recommended architecture

```
Applicant browser                    Your backend / store              Admins
─────────────────                    ───────────────────              ──────
az/application.html  ──POST JSON──►  Formspree / Apps Script /       Review in
en/application.html                  Supabase + serverless            Sheet or DB
       │                                      │
       │ optional draft                       ├── email notification
       ▼                                      └── export / status workflow
 sessionStorage / localStorage
 (same device only)
```

### 4.1 Layer A — Official submissions (required)

On successful validation, `daabApplicationSubmit()` should **POST** form data to a backend endpoint. Store at minimum:

- `submitted_at` (ISO timestamp)
- `locale` (`az` | `en`)
- All required form fields (email, name, affiliation, science selections, etc.)
- Optional: `user_agent` or IP only if disclosed in privacy text

**Do not** embed database passwords or private API keys in public `js/` files. Use:

- A **public** form endpoint ID (Formspree-style), or
- A **serverless function** that holds secrets and writes to a database/Sheet.

### 4.2 Layer B — Draft save (optional, UX)

Use **`sessionStorage`** (same tab/session) or **`localStorage`** (persists across visits on the same browser):

- Keys such as `daab-application-draft-az` and `daab-application-draft-en`
- Save on step change or debounced `input` events
- On load: offer “Continue previous application?” if draft exists
- **Clear draft** after successful server submit

Show a short notice: *Drafts are stored only on this device and are not sent to DAAB until you submit.*

### 4.3 Layer C — CV and photo (unchanged for phase 1)

Keep post-submit instructions to send CV and photo to **`bilik.birlik@gmail.com`** with a subject line such as `WAAS Membership — [Full Name]`.

A later phase may add **file upload** (object storage + virus scanning + size limits). That is separate from text-field storage.

---

## 5. Backend options (static-site compatible)

Ranked for DAAB/WAAS today: low operational burden first.

### 5.1 Form service (Formspree, Getform, Basin, etc.)

| Pros | Cons |
|------|------|
| Works with GitHub Pages; minimal code change | Monthly limits; vendor lock-in |
| Email notifications + dashboard/export | Check EU/data residency if required |
| No server to maintain | Less control over schema and workflow |

**Fit:** Fastest path to “every submission is kept” without running infrastructure.

### 5.2 Google Apps Script + Google Sheet

| Pros | Cons |
|------|------|
| Low cost; familiar to small associations | Must secure endpoint (secret token, not an open URL) |
| Easy board review and export | Google account governance |
| Aligns with existing `@gmail.com` workflow | Not ideal for very high volume |

**Fit:** Strong default for a volunteer-run scientific association.

**Sheet columns (example):** `submitted_at`, `locale`, `email`, `first_name`, `last_name`, `country`, `affiliation`, `sci_fields` (JSON or comma-separated), `additional_info`, `cv_confirm`, `status` (`pending` / `reviewed` / `approved`).

### 5.3 Supabase (or Firebase) + serverless function

| Pros | Cons |
|------|------|
| Proper database, search, application status | More setup and maintenance |
| Row-level security possible | Requires Cloudflare Worker / Vercel / similar for secrets |
| Scales with growth | |

**Fit:** When you need statuses, search, many applications per year, or a future admin UI.

### 5.4 Self-hosted API + database

Only if DAAB has dedicated IT capacity. Usually **overkill** for current site size.

---

## 6. Suggested end-to-end workflow

1. User opens `az/application.html` or `en/application.html` (from `membership.html` “Join” button).
2. User completes the four steps (optional draft restored from browser storage).
3. Client validates required fields.
4. Client **POST**s JSON or `FormData` to the chosen backend.
5. Backend persists one row per submission and optionally sends confirmation email to applicant and notification to `bilik.birlik@gmail.com`.
6. Client shows success screen and clears local draft.
7. User sends CV/photo by email as instructed.
8. Board reviews rows in Sheet/DB; **no PII in Git**.

Route registration for language switching: `i18n/routes.json` → `membership-application` (`az/application.html`, `en/application.html`).

---

## 7. Implementation notes (when building)

### 7.1 Changes in this repo

| File | Change |
|------|--------|
| `js/daab-membership-application.js` | Collect form values; `fetch()` POST on submit; handle errors; clear draft |
| `az/application.html`, `en/application.html` | Ensure field `name` attributes are stable; add privacy notice if storing IP |
| `documents/DAAB-Membership-Application-Storage-Strategy.md` | This document; update when backend is chosen |

Rebuild application pages after form markup changes:

```bash
python helpers/_build_az_application_page.py
python helpers/_build_en_application_page.py
```

### 7.2 Configuration

- Store endpoint URL or public form ID in **one place** (e.g. a small `js/daab-application-config.js` or build-time constant), not scattered in HTML.
- Use **environment-specific** endpoints: test Sheet vs production Sheet.
- Never commit secrets; use serverless env vars or Formspree project settings.

### 7.3 Validation

After implementation:

1. Submit a test application in AZ and EN.
2. Confirm row appears in Sheet/DB and notification email arrives.
3. Confirm success UI only shows after server confirms (or show error if POST fails).
4. Run `python helpers/_validate_site.py` (unchanged asset paths).
5. Test on `http://127.0.0.1:8010/` per stability guide.

---

## 8. Privacy and compliance

Membership applications contain **personal data**. Minimum practices:

| Topic | Guidance |
|-------|----------|
| **Transparency** | State purpose, retention period, and who can access data (membership or charter-related page) |
| **Transport** | HTTPS only (production already) |
| **Access control** | Limit Sheet/DB to board or designated officers |
| **Retention** | Define how long applications are kept after decision |
| **Git** | Do not commit submissions, exports with PII, or API secrets |
| **Search** | Do not add application data to `i18n/search-index.json` |
| **Drafts** | Browser drafts are still personal data on the user’s device; mention in notice |

Consult local law (e.g. GDPR if EU applicants) before going live with storage.

---

## 9. Decision summary

| Layer | Role | Recommended technology |
|-------|------|-------------------------|
| **Draft (optional)** | UX — continue later on same device | `sessionStorage` / `localStorage` |
| **Official record (required)** | One row per submission | **Google Sheet + Apps Script** or **Formspree** to start |
| **Notifications** | Alert board + optional applicant ack | Email via backend |
| **Files** | CV, photo | Email now; upload service later if needed |
| **Upgrade path** | Status workflow, search, volume | **Supabase** + serverless function |

**Default recommendation for DAAB/WAAS:** implement **server-side POST on submit** first (Sheet or Formspree), add **optional browser draft** second, keep **CV/photo by email** until upload requirements are defined.

---

## 10. Related documents

- `documents/DAAB-Site-Stability-and-Deployment-Guide.md` — local preview, deploy scope, validation
- `documents/DAAB-Bilingual-Website-Strategy.md` — AZ/EN structure and routes
- `documents/DAAB-Launch-Checklist.md` — pre-launch checks
- `.cursor/rules/daab-file-organization.mdc` — where new JS/CSS may live

---

*Last updated: May 2026. Update this file when a backend is selected and `daab-membership-application.js` is wired to production.*
