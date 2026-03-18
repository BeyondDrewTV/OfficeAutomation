# Copperline Project State

Last Updated: 2026-03-18

## Copperline Version
v0.2

## Current Phase
Lead Acquisition Engine

## Current Focus
V2 Stage 2 — Unified Lead Workspace Backbone

## Copperline Positioning
Copperline = Service Business Operations

## Last Completed Pass
Pass 48 -- Lifecycle Coverage Expansion

- Added EVT_APPROVED, EVT_UNAPPROVED, EVT_SCHEDULED, EVT_UNSCHEDULED to
  lead_memory.py constants, _ALL_EVENT_TYPES, and _EVENT_LABELS.
- api_approve_row -> EVT_APPROVED; api_unapprove_row -> EVT_UNAPPROVED;
  api_schedule_email -> EVT_SCHEDULED (with send_after detail) or EVT_UNSCHEDULED.
- All hooks try/except wrapped.
- _TL_ICON and _TL_COLOR in index.html extended for the 4 new types.
- Existing state transitions (contacted, suppressed, deleted_intentionally,
  do_not_contact, hold, revived) already in timeline via record_suppression() --
  no new code needed for those.
- discovered event intentionally skipped: post-pipeline row attribution too
  risky without touching protected code.
- EVT_DRAFTED and EVT_FOLLOWUP_SENT deferred to Pass 50.
- 6/6 verification checks passed. 3 files changed, 28 insertions.

Commit: `e8d8312`

## Previous Completed Pass
Pass 47 -- Lead Timeline / Lifecycle Event Spine

Commit: `4a4a04b`

## Queue State Management Note -- Pass 38
**Date:** 2026-03-17

Backup: `_backups/pending_emails_pre_p38_20260317_182909.csv`

Queue state after: 180 rows / 50 sent / 0 scheduled+unsent / 130 unscheduled+unsent.

## Next Pass
TBD (candidates: Pass 49 Observation Model Expansion, Pass 50 Follow-Up System Rebuild)

## Protected Systems
- `run_lead_engine.py`
- Queue schema (column order and naming)
- `pending_emails.csv` pipeline
- Email sender
- Follow-up scheduler
- `safe_autopilot_eligible` logic

## Core Operator Workflow

1. Discover businesses via map
2. Add a business_specific_observation for each strong lead
3. System generates observation-led outreach drafts
4. Operator reviews, approves, or schedules for tomorrow morning
5. Scheduled queue sorted by send time - open it in the morning, send in order
6. Emails sent manually via Gmail
7. Follow-ups tracked automatically
8. Clients onboarded to missed-call texting service
