# Copperline Project State

Last Updated: 2026-03-15

## Copperline Version
v0.2

## Current Phase
Lead Acquisition Engine

## Current Focus
Discovery Map System

## Last Completed Pass
Step 4 — Map Result Usability Polish

- Added sort select (default / Name A–Z / City A–Z) and email-only filter checkbox to results panel
- `_mapRenderPanel()` applies filter+sort from control state; `_mapResultItems[]` never mutated
- Count updates to show `(N of M)` when filter is active
- `_mapClearResultMarkers()` resets sort and filter controls on clear

Commit: `a19bc16`

## Previous Pass
Step 3 — Results Side Panel

Commit: `c0caa17`

## Next Pass
Step 5 — Search Visible Area (scope to be defined before implementation)

## Upcoming Passes
- Search Visible Area button
- Tiled discovery backend (neighborhood-level grid search)
- Territory heatmap overlay
- Industry saturation view

## Protected Systems
- `run_lead_engine.py`
- Queue schema
- `pending_emails.csv` pipeline
- Email sender
- Follow-up scheduler
- Exception router
- `safe_autopilot_eligible` logic

## Core Operator Workflow

1. Discover businesses via map
2. System generates outreach drafts
3. Operator reviews and approves
4. Emails sent manually via Gmail
5. Follow-ups tracked automatically
6. Clients onboarded to missed-call texting service
