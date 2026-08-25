# Lucky Penny Kitties — Site Change Log

Maintained starting 2026-08-01, from the point the volunteer application form link was provided. Earlier work (sponsor page fixes, event system, donate page rebuild, Venmo/PayPal/GivingGrid additions, nav cleanup, etc.) predates this log and isn't included.

Each entry: what changed, why, and which theme/resource it landed on.

---

## 2026-08-01

### Added volunteer application link to "Apply to Volunteer" button
- **What:** The "Apply to Volunteer" button on the Volunteer page (`templates/page.volunteer.json`) was a placeholder linking to `#`. Updated it to the real Google Form: `https://docs.google.com/forms/d/e/1FAIpQLSeJC6Ismy7TbKn_jYmzsJmkWO5jvNfHYeZBmqaPZh234FWKAA/viewform`.
- **Why:** The button existed as scaffolding from an earlier page build but had never been wired to an actual application form. This was the first real submission channel for volunteers.
- **Scope check:** Confirmed no other "Volunteer" buttons/links on the site needed the same treatment — the main nav item and the homepage "Volunteer With Us" button both intentionally point to the Volunteer page itself (navigation), not the form, so they were left as-is.
- **Where:** Since the live theme ("Lucky Penny Pink Redo - Venmo edit") can't be edited directly (writes to the published theme are blocked as a safety measure), the change was made on a new duplicate theme, **"Lucky Penny Pink Redo - Volunteer link"**. User reviewed the preview and approved it.

### Theme cleanup requested
- **What:** User asked to delete the now-stale themes left over from prior work: **"Lucky Penny Pink Redo"** (the original theme, superseded once "Venmo edit" was published live) and **"Copy of Lucky Penny Pink Redo"** (a duplicate of that same superseded theme).
- **Why:** Reduce clutter in the theme library now that both are fully superseded by the live theme.
- **Outcome:** Theme deletion is blocked for me as a safety measure (same category as publishing — anything that could affect the live storefront requires manual action in Shopify Admin). Instructed the user to delete both themes themselves via **Admin → Online Store → Themes → Actions → Delete**. Not yet confirmed done.

### Started this change log
- **What:** Created this file at the user's request to track future site changes with reasoning, starting from the volunteer form link change above.
- **Why:** User wants a durable record of what's been changed and why, going forward.

### Added clean short URL redirects for social posts
- **What:** Created 7 URL redirects so the site's most-shared pages have short, clean addresses for posting online, instead of the default Shopify `/pages/<handle>` paths:
  - `/donate` → `/pages/donate`
  - `/volunteer` → `/pages/volunteer`
  - `/foster` → `/pages/foster`
  - `/events` → `/pages/upcoming-events`
  - `/adopt` → `/pages/adoptable-lpk-kitties-🐾` (this page's real handle has an emoji in it, so the redirect is especially useful here)
  - `/sponsors` → `/pages/our-incredible-sponsors`
  - `/surrender` → `/pages/surrender`
- **Why:** User explained they post these page addresses in social posts and want them as clean as possible. Shopify enforces `/pages/`, `/products/`, `/collections/`, etc. prefixes for all non-homepage content — there's no way to actually serve a Page at a bare root path like `/donate`. Redirects are the standard workaround: the short URL works when clicked/typed, though the browser's address bar will still show the longer real URL once it lands (this was called out to the user as a caveat).
- **Where:** URL redirects are a store-level (not theme-level) resource, so this took effect immediately — no theme publish needed.

### Built a dedicated "Contact Us" page (email-only, no phone)
- **What:**
  - Created a new **"Contact Us"** page (`/pages/contact`, plus a clean `/contact` redirect) with an intro explaining the org is volunteer-run with no staffed phone line, followed by Shopify's built-in contact form (Name, Email, Message).
  - **Removed the phone number field** from the shared `sections/contact-form.liquid` theme section, since this section wasn't enabled/live on any existing page (confirmed by checking every template) — safe to edit without affecting anything else, and it wasn't being shown to visitors, so it was safe to edit for the sole page that now uses it.
  - Added **"Contact Us"** to the main nav (live immediately — menus aren't theme-gated).
  - Form submissions route through Shopify's native contact form handler, which emails the shop's contact address (`meow@luckypennykitties.org`) automatically — no additional app or integration required.
- **Why:** User wants to move away from phone calls for inquiries and have people reach out by email/form instead.
- **Where:** Page content/nav/redirect are live immediately (store-level resources). The actual page layout (intro + form) lives in a new template, `templates/page.contact-us.json`, on a new duplicate theme, **"Lucky Penny Pink Redo - Contact Us page"** — not yet published. Until it's published, `/pages/contact` will render as a blank/generic page rather than the intended form, since the live theme doesn't have this template.

## 2026-08-25

### Diagnosed and fixed adoptable-cat age confusion
- **What it was doing:** The "Adoptable Kitties" cat gallery (`cat_gallery` custom-liquid block, in `templates/page.actual-contact-page.json`) computes each cat's displayed age from `date_of_birth` whenever it's set, and only ever falls back to the manually-typed `age_months` field when `date_of_birth` is blank. Practically every cat has a birth date on file, so `age_months` was almost always dead — editing it in Admin had zero visible effect on the site.
- **User's report:** "the adoptable cat table is causing issues for the other users, I think the age is confusing them." Diagnosis: this is a data-entry confusion, not a display bug — volunteers editing `age_months` in Admin, seeing no change on the live page, and assuming something's broken.
- **Changes made (user approved a/b, declined c for now):**
  1. **(a) Backfilled `age_months` for every cat** so it matches what `date_of_birth` computes to as of today, fixing 8 cats that had drifted out of sync (Jack, Sandy, Maple, Draxie, Sig, Angel, Fitz, Kristi).
  2. **(a) Set up a daily automated sync** (Routine `trig_012kPFcsuqj8VZwjFGVWrJwu`, 09:00 UTC) that recomputes `age_months` from `date_of_birth` for every cat and corrects any drift, so this doesn't need to be caught manually again. Cats with no `date_of_birth` are left alone (age_months is their only source of truth). Bound to this ongoing session rather than a fresh session per fire, since this Shopify org doesn't currently support granting MCP connector access to fresh-session Routines.
  3. **(b) Changed the age display format:** ages 24+ months now show as `"2.5 years old"` (one decimal, computed exactly) instead of the old `"~3 years old"` (rounded to a whole number with a `~`), which could look flatly wrong to anyone who knew the cat's real age. Under 24 months still shows `"X months old"` — unchanged.
  4. **(c) Left alone, per user's instruction:** a genuine data duplicate was found while investigating — two metaobject entries (`sig` and `luna` handles) both currently named "Luna," sharing the same cat ID (`26-035`) and birth date, apparently from a rename that created a new record instead of updating the existing one. Not merged or deleted; flagged for the user to decide later.
- **Where:** The display-format fix (b) is on the same pending duplicate theme as the Contact Us page, **"Lucky Penny Pink Redo - Contact Us page"** — not yet published. The `age_months` backfill (a) and the daily sync Routine are metaobject/store-level, so they're already live and running regardless of theme publish state.

### Added quick-apply buttons to the Contact Us page
- **What:** Added a row of 4 shortcut buttons between the intro and the general contact form: "Looking to Adopt?", "Looking to Foster?", "Looking to Volunteer?", "Need to Surrender a Cat?" — each linking straight to the same application forms already used elsewhere on the site (adoption/foster/volunteer/surrender Google Forms). Relabeled the general form's heading to "Or Send Us a General Message" so it reads as the catch-all option after the shortcuts.
- **Why:** User's idea — most people landing on a contact page already know why they're there, so let them skip straight to the right application instead of writing a general message that just gets redirected manually.
- **Where:** Same pending duplicate theme, **"Lucky Penny Pink Redo - Contact Us page"** — not yet published.

### Audited the site for phone numbers
- **What:** At the user's request ("make sure there is no phone number anywhere"), checked every page's content, every custom section, header/footer, both nav menus, shop legal policy pages, SEO/structured data (Organization schema), and the contact form itself.
- **Finding:** No phone number is displayed anywhere on the storefront. The only phone number that exists at all is one field in Shopify's back-end business/billing info (Admin → Settings) — it's never referenced by any theme file or shown to visitors, purely internal Shopify account info.
- **Follow-up:** User asked to also strip the now-unused phone input field from the shared `sections/contact-form.liquid` on the **live** theme (it was already removed on the pending "Contact Us page" duplicate when that page was built). Confirmed this needs no new action — it's already part of the pending duplicate theme and will go live automatically once that theme is published.
- **Where:** No changes made this entry — informational audit + confirmation only. Nothing pending beyond publishing the existing duplicate theme.
