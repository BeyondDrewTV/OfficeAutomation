# Current Build Pass

## Active System
Pass 77 -- Command Center polish: real city names, industry lead drill-down, map init fix

## Status
Pass 77 complete.

---

## Completed: Pass 77 -- Command Center Polish

**Files:** `dashboard_static/index.html`, `city_planner.py`, `dashboard_server.py`

### Real city names for Map Area entries
`CityPlanner._display_name()` — reverse-geocodes coordinate entries via Nominatim
once, caches result in `city_planner.json`. AREA entries now show real place names.
`_tpCityDisplay(c)` updated to accept full city object and use `display_name`.

### Industry lead drill-down
Click any industry row in the territory panel → expands inline lead list:
- Lead name, email, status badge (Replied/Sent/Approved/Draft)
- Summary counts: X replied, X sent, X approved, X draft
- Click any lead row → opens panel directly via `qlfJump(gi)`
- Up to 20 leads shown, overflow count displayed
- Click again to collapse. Arrow indicator ▸/▾ per row.
Backend: `/api/territory/leads` — matches by city+state (exact) or lat/lng
proximity for AREA entries.

### Map init fix (first-load blank)
`_runPageHooks` now fires 5x `invalidateSize` at 30/100/300/700/1200ms after
`requestAnimationFrame`. Leaflet now renders correctly on first Discovery click.

### Nav renamed
Top nav: "🔍 Discovery" → "🗺 Command Center"
Sub-tab: "⚡ Command Center" → "🗺 Map + Territory"

### Territory panel bottom cutoff fixed
`.cc-tp-body` padding-bottom 14px → 60px. Last card no longer clipped.

### event.stopPropagation on Run/Skip/X buttons
Industry row click triggers lead list. Run/Skip/X buttons stop propagation
so they don't accidentally toggle the lead list.

---

## Pass 76 -- Email/Lead Search + Global Lead Finder (Ctrl+K)
## Pass 75 -- Command Center split-pane (map + territory combined)
## Pass 74 -- MX validation before send
## Pass 73 -- Follow-up voice rewrite
