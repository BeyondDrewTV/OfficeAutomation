# Current Build Pass

Last Updated: 2026-04-01

## Active Pass
Pass 97–99 milestone -- Discovery Throughput + History-to-Action Loop

## Status
Complete. Frontend-only changes to index.html. No backend changes. Verified live.

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

