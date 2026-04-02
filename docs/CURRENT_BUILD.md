# Current Build Pass

Last Updated: 2026-04-01

## Active Pass
Pass 90–92 milestone -- Truth Sync + Delivery Recovery + Legacy DOM Cleanup

## Status
Complete. Docs synced to repo truth. Delivery nav blank-page fixed. Legacy DOM removed. No backend changes.

## What Pass 87 Builds

**Goal:** Tighten first-touch email generation so the value proposition (what Drew fixes) is visible by sentence 2–3. Keep the philosophy. Improve the execution.

**4-part structure now enforced as contract:**
1. Observation — specific detail about this business
2. Owner-readable loss / leak — what that probably costs them
3. Fixer/operator line — clearly states what Drew helps fix (required by validation)
4. Reply-first CTA — soft question, no hard close

**Changes:**
- `DRAFT_VERSION`: v18 → v19
- `_build_offer_sentence()`: Completely rewritten — angle-specific fixer/operator language replaces generic "I work one on one with owners..." across all 5 angles
- All 17 trade fallback bodies + generic fallbacks updated: sentence 2 now states what Drew fixes, not just "I work one on one"
- `_BANNED_WORDS` expanded: added "just reaching out", "wanted to introduce myself", "curious if", "would love to chat", "another set of eyes", "ai", "software", "dashboard", "transform", "unlock", "roi", "synergy", "workflow gap", "from the business side"
- `_SUBJECT_BANNED_PHRASES` expanded: added "quick question", "had a question", "wanted to ask", "just checking", "touching base", "following up"
- `_FALLBACK_SUBJECTS`: replaced "quick question" style with problem-labeled subjects: "missed calls", "callback backlog", "estimate follow-up", "after-hours leads", "contact form lag", "scheduling friction"
- `_VAGUE_POSITIONING_PHRASES` expanded: added soft intro phrases
- `validate_draft()` — three new checks added:
  - Fixer/operator line required (raises `DraftInvalidError` if missing)
  - Reply-first CTA required (raises `DraftInvalidError` if missing)
  - Complaint-risk linting: exclamation overuse, multiple CTAs flagged

**Files changed:**
- `lead_engine/outreach/email_draft_agent.py`
- `docs/PROJECT_STATE.md`
- `docs/CURRENT_BUILD.md`
- `docs/AI_CONTROL_PANEL.md`
- `docs/CHANGELOG_AI.md`

**Protected-system status:** unchanged. No edits to send path, queue schema, scheduler, Gmail workflow, delivery board, or conversation board.

## Verification Completed
1. All fallback bodies manually verified: fixer/operator line present by sentence 2
2. Banned word / subject lists reviewed against new first-touch contract
3. `validate_draft()` now enforces fixer line + CTA structurally — drafts without them will fail and regenerate
4. No protected systems touched

## What This Milestone Changed

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

