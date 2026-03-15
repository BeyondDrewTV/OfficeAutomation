# Copperline Project State

Last Updated: 2026-03-15

## Copperline Version
v0.2

## Current Phase
Lead Acquisition Engine

## Current Focus
Discovery Map System

## Last Completed Pass
Step 5 — Discovery Coverage Memory

- Added `_mapCoverageCircles[]` session array
- Added `_mapClearCoverage()` function
- On successful search, snapshots `_mapCenter` + `_mapRadiusM` as faint blue dashed `L.circle` overlay (`interactive:false`)
- `Clear Coverage` button added to toolbar, hidden until first search
- Active circle and all existing behavior unchanged

Commit: `f27a472`

## Previous Pass
Step 4 — Map Result Usability Polish

Commit: `a19bc16`

## Next Pass
Step 6 — Search Visible Area (scope questions still open in CURRENT_BUILD.md)

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
