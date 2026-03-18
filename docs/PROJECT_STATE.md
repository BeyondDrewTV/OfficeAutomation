# Copperline Project State

Last Updated: 2026-03-17

## Copperline Version
v0.2

## Current Phase
Lead Acquisition Engine

## Current Focus
V2 Stage 2 — Unified Lead Workspace Backbone

## Copperline Positioning
Copperline = Service Business Operations

We identify where service businesses are losing work - missed calls, cold estimates, follow-ups that never happen - and install simple systems to fix it.

Automation is the implementation layer, not the headline.
Missed-call texting is one downstream solution, not the primary pitch.
Outreach goal: start a conversation about operational problems, not sell a product.

## Last Completed Pass
Pass 43 - V2 Stage 2F — Next-Action-Driven Controls + History Visibility

- Added shared next-action and history UI helpers so operator guidance now comes from `_leadRecord` semantics instead of scattered inline checks.
- Strengthened the shared workspace header with a clearer `Next Step` callout plus visible history chips for approved, scheduled, sent, replied, stale, and observation-present states.
- Discovery and Pipeline status rendering now lean more consistently on `_leadStatusMeta(_leadRecord(...))`, including clearer blocked/sent/replied tones.
- Review-panel footer controls and flow guidance now align with the lead's actual state, including stale-refresh-first and scheduled/unschedule contexts.
- Queue status cells now surface shared history chips where operators make send/review decisions.
- `_leadRecord.nextAction` now prioritizes stale or observation-missing refresh work before send-oriented actions.
- Zero backend changes. No queue schema changes. No protected systems touched.

Commit: `5a09991`


## Queue State Management Note — Pass 38
**Date:** 2026-03-17
**Operation:** Bulk unschedule of 56 pre-Pass-36 (v7 draft) scheduled rows.

All 56 rows were scheduled for 2026-03-18 morning windows but carry old-style
pre-observation drafts that should not auto-send. `send_after` was cleared on
each. No rows deleted. No other fields altered. 50 sent rows untouched.
Total row count unchanged at 180.

Backup: `_backups/pending_emails_pre_p38_20260317_182909.csv`

**Queue state after:**
- total rows: 180
- sent rows: 50
- scheduled+unsent: 0
- unscheduled+unsent: 130

## Previous Completed Pass
Pass 42 - V2 Stage 2E — Qualification + Status Derivation Unification

## Next Pass
TBD

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
