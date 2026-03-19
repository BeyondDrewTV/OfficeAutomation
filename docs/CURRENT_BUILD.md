# Current Build Pass

## Active System
Pass 50 -- Follow-Up System Rebuild

## Status
Pass 50 complete.

---

## Completed: Pass 50 -- Follow-Up System Rebuild -- `4ab7bd5`

Product changes across four files:
- `lead_engine/outreach/followup_draft_agent.py` (new)
- `lead_engine/outreach/followup_scheduler.py`
- `lead_engine/dashboard_server.py`
- `lead_engine/dashboard_static/index.html`

Docs updated in:
- `docs/PROJECT_STATE.md`
- `docs/CURRENT_BUILD.md`
- `docs/CHANGELOG_AI.md`
- `docs/AI_CONTROL_PANEL.md`

No queue schema reorder/rename changes. No `run_lead_engine.py` changes.
No email sender core changes. No scheduler timing changes.

### Problem addressed

Follow-up copy had split entry points and still leaned on generic sequence-style
language. The scheduler path and direct-send path did not share the same
grounding rules, and weak-context rows could still drift toward swappable,
agency-flavored copy instead of a real continuation tied to the lead record.

### What was added

**`lead_engine/outreach/followup_draft_agent.py`** (new)

New deterministic follow-up planner:
- `build_followup_plan(row, touch_num)` returns `{ subject, body, angle_family,
  angle_label, context }` or raises `FollowupBlockedError`.
- Uses only safe current lead context:
  current observation, obs history, timeline event detail, conversation notes,
  conversation next step, send timing, contact history, and email-path gating.
- Explicit angle families:
  - `observation_continuation`
  - `operational_nudge`
  - `note_reframe`
  - `timeline_reframe`
  - `low_pressure_closeout`
- Validation blocks:
  - banned buzzwords / automation / agency language
  - hard CTA language
  - first-touch/opening drift
  - missing lead-context overlap
  - swappable generic copy
  - overlong follow-up bodies
- Structured blocked reasons:
  `insufficient_context`, `generic_context`,
  `invalid_banned_language`, `invalid_hard_cta`,
  `invalid_generic_copy`, `invalid_missing_context_overlap`,
  `invalid_not_continuation`, `invalid_too_long`,
  `contact_path_not_email`

**`lead_engine/outreach/followup_scheduler.py`**

- Kept the scheduler's timing/eligibility mechanics intact.
- Replaced inline follow-up copy generation with `build_followup_plan(...)`.
- Rows with weak context now increment `blocked` / `blocked_reasons` and are skipped.
- Dry run output now includes angle family when a row is actually ready.

**`lead_engine/dashboard_server.py`**

- `POST /api/run_followups_dry_run` now returns both ready previews and blocked previews.
- `GET /api/followup_queue` now annotates rows with:
  `followup_copy_ready`, `followup_angle_family`, `followup_angle_label`,
  `followup_context_source`, `followup_blocked_reason`,
  `followup_blocked_message`.
- `POST /api/send_followup` now uses the shared planner and returns
  structured blocked errors instead of sending generic copy.
- Successful direct sends now record `EVT_FOLLOWUP_SENT`.

**`lead_engine/dashboard_static/index.html`**

- Follow-Up run toast now reports blocked rows when nothing queues.
- Dry-run console preview now prints both ready rows and blocked rows.
- Follow-Up cards now show angle/source metadata when copy is ready.
- Follow-Up cards now show grounded-context blocker text when copy is not ready.
- Auto-send button is hidden for rows that are not due or do not have safe
  follow-up copy ready; manual workflow remains available.

### What remains intentionally out of scope

- Scheduler timing model and due-date math
- Existing `compute_followup_status()` timing behavior
- Queue schema redesign
- Generic nurture / sequence automation
- Protected send-path rewrites

### Verification

- `python` import check: `outreach.followup_draft_agent`,
  `outreach.followup_scheduler`, and `dashboard_server` all import clean.
- Dashboard JS extracted and `new vm.Script(...)` parses clean.
- Flask test client:
  - `POST /api/run_followups_dry_run` -> `200`, current local queue returns `count=0`
    and `blocked_count=0` under the existing scheduler timing gates.
  - `GET /api/followup_queue` -> `200`, current local queue returns `total=50`.
  - Real blocked send check: `POST /api/send_followup` for current due row
    `Lars Plumbing` returns `422` with `blocked_reason=insufficient_context`
    before any email send attempt.
- Deterministic sample follow-up planning verified for:
  - step 1 `operational_nudge`
  - step 2 `timeline_reframe`

---

## Previous Completed: Pass 49 -- Observation Model Expansion -- `pending`

- Added observation grading, obs history, why-this-lead-now, and contact-path recommendation.
