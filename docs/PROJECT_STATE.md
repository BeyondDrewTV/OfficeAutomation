# Copperline Project State

Last Updated: 2026-03-17

## Copperline Version
v0.2

## Current Phase
Lead Acquisition Engine

## Current Focus
Scheduling Clarity + Queue Timeline UX

## Copperline Positioning
Copperline = Service Business Operations

We identify where service businesses are losing work - missed calls, cold estimates, follow-ups that never happen - and install simple systems to fix it.

Automation is the implementation layer, not the headline.
Missed-call texting is one downstream solution, not the primary pitch.
Outreach goal: start a conversation about operational problems, not sell a product.

## Last Completed Pass
Pass 35 - Scheduling Clarity + Queue Timeline UX

- Added a queue timeline explainer bar under the outreach filters so operators can tell how `Actionable`, `Approved`, `Scheduled`, and `All` relate to future send windows.
- Added clearer status-cell messaging for outreach rows, distinguishing `Approved` and ready-now work from future `Scheduled` rows and schedule-window-reached rows.
- Added exact plus relative schedule timing helpers in the dashboard UI so scheduled rows show both when they are due and whether they are still waiting or already eligible to send now.
- Upgraded the review panel schedule block so it explains whether a row is waiting for a future morning window, already ready from a reached schedule, or simply approved and ready to send immediately.
- Tightened schedule/unschedule feedback copy across review/table/discovery bridge actions so the UI clearly says whether a row is waiting for later or back in a ready-now queue.
- Verified dashboard load, queue status clarity, scheduled vs ready-now distinction, panel schedule explanations, schedule/unschedule actions, and basic Pass 29-34 control availability with a focused live headless smoke pass using a synthetic queue subset and stubbed API writes.

Commit: `COMMIT_PENDING`

## Previous Completed Pass
Pass 34 - Outreach Review Throughput + Queue Control

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
2. System generates outreach drafts
3. Operator reviews, approves, or schedules for tomorrow morning
4. Scheduled queue sorted by send time - open it in the morning, send in order
5. Emails sent manually via Gmail
6. Follow-ups tracked automatically
7. Clients onboarded to missed-call texting service
