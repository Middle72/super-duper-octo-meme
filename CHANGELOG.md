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
