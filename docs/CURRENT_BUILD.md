# Current Build Pass

Last Updated: 2026-04-03

## Active Pass
Pass 130–135 — Queue Session Throughput + Batch Recovery Discipline

## Status
Pass 130–135 complete.

## What Pass 130–135 Changed

**Goal:** Queue becomes a disciplined working session surface. Cohort/session work is deliberate, progress is visible at table level, and exception cleanup has clear start/progress/complete states.

**Changes (frontend only — `lead_engine/dashboard_static/index.html`):**

- **Pass 130 — Queue session banner (CSS + DOM):** `#queue-session-banner` div inserted after mode bar, before stats strip. Shows session label, row N of M, remaining count, Resume and End buttons. Copper accent in active state; green accent in done state. CSS classes: `.qsb-label`, `.qsb-meta`, `.qsb-actions`, `.qsb-btn`, `.qsb-resume`, `.qsb-end`, `.qsb-next`.

- **Pass 131 — Session-current row highlight:** `renderTable()` computes `_sessionCurrentKey` (the row key at current session position). Matching row gets `.session-current` CSS class — subtle copper left-rail accent on the checkbox cell. Gives the operator a visual bookmark in the table when the drawer is closed.

- **Pass 132 — End-of-session signal:** `navigatePanel(dir)` now calls `_qsMarkDone()` when advancing past the last row in a scoped session. Banner transitions to green "✓ [Label] complete" state with next-cohort suggestion and Close button. Previously: silent failure at boundary.

- **Pass 133 — Cohort session labels with live counts:** `_cohortStartSession()` now generates labels like `"Obs Review (7)"`, `"Stale Review (3)"`, `"No-Email Review (5)"` instead of generic `"Review"`. Count reflects live row count at session start.

- **Pass 134 — Queue session persistence across close:** `closePanel()` saves `panelIdx` into `_queueSession.pos` before clearing panel state. `navigatePanel()` keeps `_queueSession.pos` in sync on every advance. Resume picks up where the operator left off.

- **Pass 135 — Session lifecycle API:** New global `_queueSession` (null when inactive). New functions: `_qsStart(cohortKey, rows, label)`, `_qsUpdatePos(pos)`, `_qsMarkDone()`, `_qsEnd()`, `_qsResume()`, `_renderQueueSessionBanner()`. `renderTable()` calls `_renderQueueSessionBanner()` on every render. Banner next-cohort suggestion picks the highest-priority cohort (needs_obs → stale → no_email) with live rows.

**Files changed:** `lead_engine/dashboard_static/index.html`, docs

**Protected-system status:** unchanged.

## What Pass 124–129 Changed

**Goal:** Queue becomes disciplined — every cohort row gets a consistent action pattern, blocker explanation, and next-step treatment. Drawer narrowed to deep review and manual recovery only.

**Changes (frontend only — `lead_engine/dashboard_static/index.html`):**
- Row action block replaced with cohort-aware `_rowActionHtml` switch:
  - `no_email` (Pass 124): Approve + Edit removed; `📲 Social →` as primary (calls `_setWorkbenchMode('social')`); dim `Review` opens drawer for inspection
  - `needs_obs` (Pass 125): generic Edit removed; obs-focused `openPanelForRefresh` button IS the drawer entry
  - `stale` (Pass 126): generic Edit removed; if obs exists → `↻ Regen` calls `_rowDirectRegen(gi)` directly; if no obs → `Add Obs` opens drawer focused; dim `Review` secondary
  - `bulk_safe` (Pass 127): `Edit` renamed to `Review` (dimmed, 10px) to signal depth not requirement; Approve remains primary
- Blocker banners upgraded (Pass 128): stale banner adds `↻ Regen now` button (calls `panelRegenerateDraft()`); no_email banner adds `📲 Social DMs →` button (calls `_setWorkbenchMode('social')` + `closePanel()`)
- New `_rowDirectRegen(gi)` function (Pass 129): fetches obs from row, calls `/api/regenerate_draft`, updates `row.subject/body/draft_version/dm_draft` in memory, calls `renderTable()` — no drawer required

**Files changed:** `lead_engine/dashboard_static/index.html`, docs

**Protected-system status:** unchanged.

## What Pass 118–123 Changed

**Goal:** All cohort exception paths Queue-native. Legacy surfaces visually demoted.

**Changes:**
- Stale CTA: dual buttons — bulk regen + scoped `→ Review Stale` session
- No-email CTA: dual buttons — scoped `→ Review No-Email` session + `📲 Social DMs →` mode switch
- Mode bar: `<span class="wb-mode-sep">` separator inserted between Email Queue and secondary tools; Social DMs + Focus Mode get `.wb-mode-tool` (0.7 opacity, 10px font) — demotion without deletion
- CSS: `.wb-mode-sep`, `.wb-mode-tool`, `.wb-mode-tool.active`, `.wb-mode-tool:hover`

**Files changed:** `lead_engine/dashboard_static/index.html`, docs

**Protected-system status:** unchanged.

## What Pass 112–117 Changed

**Goal:** Make Queue the real operating system — exception rows self-explanatory inline, needs_obs cohort actionable without drawer.

**Changes:**
- CSS: `.cohort-pill`, `.cp-needs-obs`, `.cp-stale`, `.cp-no-email` — per-row state badge styles
- `needs_obs` cohort CTA replaced: dim "open each row" text → `→ Start Obs Review (N)` button wired to `_cohortStartSession('needs_obs')`
- New `_cohortStartSession(cohortKey)`: filters `filteredRows` to the cohort, sets `panelOpenIntent='refresh'` for needs_obs, opens a scoped panel session via `openPanel(0, rows, label)`
- Per-row cohort pill computed in `renderTable`: `_rowCohort = !row.sent_at ? _pipelineCohort(row) : 'bulk_safe'`; injected into `td-biz` next to business name — visible in ALL filter views (active, pending, all, stale, etc.)
- Active filter timeline note updated: now explains cohort structure instead of generic "work you can handle right now"

**Files changed:** `lead_engine/dashboard_static/index.html`, docs

**Protected-system status:** unchanged.

## What Pass 106–111 Changed

**Goal:** Unify Social/Sprint/Outreach into one workbench surface; make the drawer exception-aware.

**Changes:**
- Social and Sprint nav tabs hidden (`display:none`); Outreach tab renamed to "Queue"
- Mode bar at top of page-outreach: Email Queue / Social DMs / Focus Mode buttons
- `_setWorkbenchMode(mode)`: switches sub-page via `switchSubPage()`, toggles active button
- "← Back to Queue" button on page-social and page-sprint
- `#panel-blocker` div in drawer: shows cohort-specific blocker banner for exception rows
- Blocker logic in `fillPanel()`: `needs_obs` → amber "Missing observation" + auto-sets panelOpenIntent; `stale` → blue "Stale draft"; `no_email` → dim "No email path"; `bulk_safe` → hidden
- CSS: `.wb-mode-bar`, `.wb-mode-btn`, `.panel-blocker`, `.wb-back-btn`

**Files changed:** `lead_engine/dashboard_static/index.html`, docs

**Protected-system status:** unchanged.

## What Pass 103–105 Changed

**Goal:** Make Actionable view bulk-first with cohort-based grouping.

**Changes:**
- `_pipelineCohort(row)`: classifies each actionable row into bulk_safe | needs_obs | stale | no_email
- `_cohortHeaderHtml(key, count)`: renders section header with count + scoped CTA per cohort
- `_cohortBulkApprove()`: approves all bulk_safe rows in one pass (no drawer required)
- `renderTable()`: when filter is 'active', stable-sorts filteredRows by cohort order then injects cohort header rows between groups
- CSS: `.cohort-hdr` row styling
- Shipped cohorts: Ready to Approve (✓ Approve All Ready), Needs Observation, Stale Draft (↻ Regen All Stale), No Email Path (→ Social Queue)
- All other filters, bulk actions, drawer, and send gates unchanged

**Files changed:** `lead_engine/dashboard_static/index.html`, docs

**Protected-system status:** unchanged.

## What Pass 97–99 Changed

**Goal:** Turn Search History into a real action surface. Fix re-run destination. Add load-without-rerun. Reduce column scan noise.

**Root cause fixed:** `_shRerun()` navigated to Outreach — wrong surface since CC became canonical in Pass 82.

**Changes:**
- Added `_shLoadCC(city, state, industry)`: fills CC command bar inputs, navigates to `command-center`. No search fires.
- Rewrote `_shRerun()`: calls `_shLoadCC()` then `ccCmdDiscover()` after 200ms delay. Lands on CC, not Outreach.
- Added "→ Load" button on each history row (calls `_shLoadCC`).
- Merged City + ST columns into "Location" (6 cols). Updated thead and all 4 colspan instances.

**Files changed:**
- `lead_engine/dashboard_static/index.html`
- `docs/PROJECT_STATE.md`, `docs/CURRENT_BUILD.md`, `docs/AI_CONTROL_PANEL.md`, `docs/CHANGELOG_AI.md`

**Protected-system status:** unchanged.

## Verification Completed
Pending live server verification — see live check below.

## Next Pass
TBD

---

## What Pass 94–96 Changed

**Goal:** Fix Discovery History blank sub-tab. Smallest correct structural fix only.

**Root cause:** `page-searches` was nested inside `page-command-center`. Activating the searches page removed `.active` from `page-command-center`, making it `display:none` and hiding its child regardless.

**Fix:**
- Moved `page-searches` DOM block to after `</div><!-- /page-command-center -->`
- No JS changes. No nav logic changes.
- Div balance verified: 767/767

**Files changed:**
- `lead_engine/dashboard_static/index.html`
- `docs/PROJECT_STATE.md`, `docs/CURRENT_BUILD.md`, `docs/AI_CONTROL_PANEL.md`, `docs/CHANGELOG_AI.md`

**Protected-system status:** unchanged.

## Verification Completed (Pass 94–96)
1. Server restarted; hard-refreshed
2. Command Center boots, map, territory panel, queue rail ✓
3. History tab: Search History renders (437 searches) ✓
4. Map+Territory returns after History ✓
5. Pipeline intact ✓
6. Zero JS console errors ✓

---

## What Pass 93 Changed

**Goal:** Improve Command Center UI/UX hierarchy — stronger panel zone framing, denser information layout, clearer operator command surface. No new features.

**Changes (frontend only — `lead_engine/dashboard_static/index.html`):**
- Copper divider bar: `2px / opacity:.7` → `3px / opacity:.85`
- `.nav-tab.active`: + copper background tint (`rgba(200,136,74,.06)`)
- `.cc-tp-header`: + `border-top:2px solid var(--copper)` — territory panel zone authority
- `.cc-tp-title`: `10px / muted` → `11px / var(--text)` — panel header legible
- `.cc-tp-stat strong`: `600` → `700 / 12px / mono` — territory stats numbers dominant
- `.cc-tp-pane` border-left: `var(--border)` → `var(--border-hi)` — clearer zone separation
- `.cc-qr-stat-n`: `16px` → `18px`; `.cc-qr-stat-l`: `8px` → `9px`
- `.stat` pipeline padding: `16px 24px` → `12px 20px` — denser stat strip
- `.tp-progress-bar`: `80px / 6px` → `88px / 7px`
- `.ftab.active`: + inset shadow for depth
- `.cc-cmd-bar` border-top: copper tint (`rgba(184,115,51,.2)`)
- `.db-stat-n`: `22px / 600` → `24px / 700`
- Delivery board column top accents: `#db-col-won` amber, `#db-col-deployment_pending` blue, `#db-col-live` green

**Files changed:**
- `lead_engine/dashboard_static/index.html`
- `docs/PROJECT_STATE.md`, `docs/CURRENT_BUILD.md`, `docs/AI_CONTROL_PANEL.md`, `docs/CHANGELOG_AI.md`

**Protected-system status:** unchanged. No backend, queue, scheduler, send-path, or autopilot changes.

## Verification Completed
1. Server restarted; hard-refreshed
2. CC boots, map loads, territory panel loads, queue rail loads ✓
3. Pipeline stat strip denser, table intact ✓
4. Delivery empty state correct, active tab tint visible ✓
5. Zero JS console errors ✓
6. DOM inspect: `cc-tp-header` border-top `2px solid copper` ✓; queue stat `18px/700/DM Mono` ✓

## Next Pass
TBD

---

## What This Milestone Changed (Pass 90–92)

**Goal:** Bring repo into truth alignment. Fix Delivery blank-page. Remove legacy DOM debt.

**Files changed:**
- `docs/AI_CONTROL_PANEL.md` — updated last completed pass, current focus
- `docs/PROJECT_STATE.md` — DRAFT_VERSION v18 → v20, last completed pass updated, Pass 88 added to recent passes
- `docs/CURRENT_BUILD.md` — active pass and status updated; stale "Next Pass: Pass 86" footer removed
- `docs/CHANGELOG_AI.md` — milestone entry appended
- `lead_engine/dashboard_static/index.html`:
  - `_parentDefaults` and `_parentLastPage`: added `delivery: 'delivery-board'`
  - Removed: empty `page-cities` stub (was "kept for JS compat" — verified not activated by any live nav path)
  - Removed: empty `page-map` stub (same; empty div, never activated)
  - Removed: hidden `mc-wrap` legacy territory planner block (tp-*, cp-* IDs duplicated live in CC right pane)
  - Removed: second hidden `page-map` block (all IDs duplicated in live CC — bnd-*, cmd-*, map-*, mrp-*, btn* etc.)

**Protected-system status:** unchanged. No backend, queue, scheduler, send-path, or autopilot changes.

## Next Pass
TBD

---

## What Pass 85 Builds
- Conversations panel now includes an operator-visible Offer + Deployment Readiness block
- Fixed package menu (5 standard Copperline offers):
  - Missed Call Recovery
  - Lead Intake + Routing
  - Follow-Up Reactivation
  - Review Request System
  - Estimate / Job Status Communication
- Deterministic best-fit recommendation (operator can accept or override)
- Lifecycle handoff stage selector:
  discovered -> drafted -> contacted -> replied -> call booked -> proposal ready -> won -> deployment pending -> live
- Deployment checklist:
  intake complete, phone/vendor access collected, copy approved, routing logic defined, testing complete, live
- New API endpoint: `POST /api/update_delivery_profile` (lead-memory only; no queue mutation)
- `GET /api/conversation_queue` now returns normalized `delivery_profile` for replied leads
- Durable storage in `lead_engine/data/lead_memory.json` via new `lead_memory` helper functions

**Files changed:**
- `lead_engine/dashboard_static/index.html`
- `lead_engine/dashboard_server.py`
- `lead_engine/lead_memory.py`

**Protected-system status:** unchanged. No edits to queue schema, sender core, scheduler core, or run orchestrator.

## Verification Completed
1. `python -m py_compile lead_engine/lead_memory.py lead_engine/dashboard_server.py`
2. JS parse check of `lead_engine/dashboard_static/index.html` script block via Node `vm.Script`
3. Flask test client check:
   - `GET /api/conversation_queue` returns 200
   - `POST /api/update_delivery_profile` accepts valid payload and returns normalized profile

---

## Pass 83 -- CC Layout QA (complete)
- Page containment: `#page-command-center.active` height-constrained
- `cc-wrap` height: `100%` (inherits constrained parent)
- Duplicate `#map-layout` rules consolidated
- `cc-map-pane` padding reduced; `min-width:500px` added
- Territory pane: 300px -> 260px; queue rail: 300px -> 280px
- cmd-bar CC override: padding tightened
- `map-page-wrap` made flex column in CC context
- Queue rail: stat numbers 13px -> 16px; copper top accent + title
- Row padding: 7px -> 6px; cc-qrow-bot margin 3px -> 2px

---

## Pass 82 -- Command Center unified layout (complete)
- CC is default landing tab
- Map-dominant layout, right queue rail, persistent bottom command bar
- ccQueueRender / ccQueueFilter / ccQueueUpdateStats / ccQueueOpenRow
- ccCmdDiscover wired to Pipeline discovery
- Full View button preserves Pipeline access

---

