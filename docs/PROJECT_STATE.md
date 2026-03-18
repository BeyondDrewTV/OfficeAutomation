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

We identify where service businesses are losing work - missed calls, cold estimates, follow-ups that never happen - and install simple systems to fix it.

Automation is the implementation layer, not the headline.
Missed-call texting is one downstream solution, not the primary pitch.
Outreach goal: start a conversation about operational problems, not sell a product.

## Last Completed Pass
Pass 47 -- Lead Timeline / Lifecycle Event Spine

- Extended lead_memory.py with a second entry type: 'event' entries that append
  to history[] without changing current_state. EVT_* constants for drafted,
  observation_added, draft_regenerated, replied, note_added, followup_sent.
- record_event() and get_timeline() added. get_timeline() back-fills type/label
  for pre-Pass-47 entries and returns history sorted oldest-first.
- Four lifecycle hooks in dashboard_server.py: api_update_observation (obs added),
  api_regenerate_draft (draft regenerated), api_update_conversation (note added),
  api_log_contact result=replied (replied). All try/except wrapped.
- New POST /api/lead_timeline route: returns full timeline by lead identity.
- Panel workspace: async timeline strip below Business Info, last 6 events
  with hover tooltips, non-blocking (fires after panel renders).
- Lead Memory tab: event count is now a clickable expand button; full timeline
  shown inline with icon, label, timestamp, detail per entry. Lazy-loaded.
- No protected systems touched. No queue schema changes. 6/6 checks passed.

Commit: `4a4a04b`

## Previous Completed Pass
Pass 46 -- Contacted Memory Seeding + Safer Contact Recording

Commit: `65d113e`

## Queue State Management Note -- Pass 38
**Date:** 2026-03-17
**Operation:** Bulk unschedule of 56 pre-Pass-36 (v7 draft) scheduled rows.

Backup: `_backups/pending_emails_pre_p38_20260317_182909.csv`

**Queue state after:**
- total rows: 180
- sent rows: 50
- scheduled+unsent: 0
- unscheduled+unsent: 130

## Next Pass
TBD (candidates: Pass 48 Contact Path Recommendation, Pass 49 Observation Model Expansion)

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
