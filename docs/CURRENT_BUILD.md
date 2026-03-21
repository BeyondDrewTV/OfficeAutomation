# Current Build Pass

## Active System
Pass 76 -- Email/Lead Search, Global Lead Finder (Ctrl+K)

## Status
Pass 76 complete.

---

## Completed: Pass 76 -- Email/Lead Search + Global Lead Finder

Files: `lead_engine/dashboard_static/index.html`

### Pipeline search now includes email + phone
The search box in Outreach previously only matched business name, city, subject.
Now matches: name, email address, city, phone, subject.
Placeholder updated: "Search name, email, city, phone…"

Use case: you see a bounce in Gmail for `tad@marksautoil.com`, type that into
the pipeline search and the lead surfaces instantly.

### Global Lead Finder — Ctrl+K
Floating quick-find overlay that works from ANY tab in the app.
- Press Ctrl+K anywhere (or click "🔍 Find Lead" in header)
- Type email, name, phone, or city — results appear instantly
- Copper highlight on matching text in results
- Status badges: Sent / Approved / Replied / Draft
- Arrow keys to navigate, Enter to open, ESC to close
- Clicking a result: switches to Pipeline → Outreach, opens review panel
  on that lead directly. If lead is filtered out, populates search box
  with email to surface it.

---

## Pass 75 -- Command Center (Map + Territory Combined)

Files: `lead_engine/dashboard_static/index.html`

Replaced two Discovery sub-tabs (Map Search + Territory) with single
"⚡ Command Center" tab — split-pane layout: map left 60%, territory right 40%.

Bidirectional wiring:
- Map boundary click → territory panel finds/adds city, opens card,
  scrolls to it, flashes copper border
- Territory Run/Run Remaining/Run Next → map coverage overlay refreshes

Pass 74 -- MX validation before send (catches scrape-error domains)
Pass 73 -- Follow-up voice rewrite (Drew tone, industry fallback, anchor cleaning)
Pass 72 -- Territory button fix (JSON.stringify quote bug), stale warning fix
Pass 71 -- Industry fallback drafts (17 trades, no obs = no problem)
Pass 70 -- Bulk regenerate endpoint + "Regen Stale" toolbar button
Pass 69 -- v18 voice rewrite (grammar, confident consequence + close)
Pass 68 -- Auto-regen on panel open, panel layout overhaul, 22 industries
