# Copperline Project State

Last Updated: 2026-03-15

## Copperline Version
v0.2

## Current Phase
Lead Acquisition Engine

## Current Focus
Discovery Map System

## Last Completed Pass
Step 6 — Discovery History List

- Added `_mapSearchHistory[]` session array (max 10, newest-first)
- Added `_mapRenderHistory()` and `_mapClearHistory()`
- Each successful search appends `{lat, lng, radiusM, found}` entry
- History list renders below map, hidden until first search
- Click restores `_mapRadiusM`, calls `_mapDrawCircle()`, recenters view
- Coverage overlays and clustering unchanged

Commit: `6d79c64`

## Previous Pass
Step 5 — Discovery Coverage Memory

Commit: `f27a472`

## Next Pass
Step 7 — Search Visible Area (scope questions in CURRENT_BUILD.md)

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
