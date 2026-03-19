# Copperline Project State

Last Updated: 2026-03-18

## Copperline Version
v0.2

## Current Phase
Lead Acquisition Engine

## Current Focus
V2 Stage 2 - Unified Lead Workspace Backbone

## Copperline Positioning
Copperline = Service Business Operations

## Last Completed Pass
Pass 50 -- Follow-Up System Rebuild

- Added `lead_engine/outreach/followup_draft_agent.py`: deterministic follow-up
  planner with five explicit angle families:
  `observation_continuation`, `operational_nudge`, `note_reframe`,
  `timeline_reframe`, `low_pressure_closeout`.
- Follow-up planning now consumes safe lead context when present:
  current observation, observation history, timeline event detail,
  conversation notes / next step, send timing, contact history, and email-path gating.
- Generic or weak follow-ups now block with structured reasons instead of falling
  back to reusable sequence copy (`insufficient_context`, `generic_context`,
  invalid copy reasons).
- `outreach/followup_scheduler.py` keeps its timing/eligibility flow but now
  calls the shared planner, counts blocked rows separately, and queues nothing
  when grounded continuation context is missing.
- `dashboard_server.py` routes now share the same planner:
  `/api/run_followups_dry_run`, `/api/followup_queue`, and `/api/send_followup`.
  `api_send_followup` now records `EVT_FOLLOWUP_SENT` on success.
- `index.html` Follow-Up tab now shows angle/source metadata when copy is ready,
  shows grounded-context blockers when it is not, and removes auto-send for rows
  that are not due or do not have safe follow-up copy ready.
- No queue schema reorder/rename changes. No `run_lead_engine.py` changes.
  No email sender core changes. No scheduler timing changes.

Commit: pending

## Previous Completed Pass
Pass 49 -- Observation Model Expansion

Commit: pending

## Next Pass
Territory heatmap overlay

## Protected Systems
- `run_lead_engine.py`
- Queue schema (column order and naming)
- `pending_emails.csv` pipeline
- Email sender
- Follow-up scheduler timing/core
- `safe_autopilot_eligible` logic

## Core Operator Workflow

1. Discover businesses via map
2. Add a business-specific observation for each strong lead
3. System generates observation-led first-touch drafts
4. Operator reviews, approves, or schedules for tomorrow morning
5. Emails are sent manually via Gmail
6. Follow-up drafting only proceeds when the lead record has grounded continuation context
7. Weak or generic follow-ups block instead of auto-queuing generic nurture copy
8. Clients onboard to missed-call texting service
