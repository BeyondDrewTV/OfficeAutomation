# Copperline Project State

Last Updated: 2026-03-15

## Copperline Version
v0.2

## Current Phase
Lead Acquisition Engine

## Current Focus
Discovery Map System

## Last Completed Pass
Step 3 — Results Side Panel

- Added `#map-layout` flex wrapper around map and panel
- Added `#map-results-panel` (260px, hidden until results exist)
- Added `_mapResultItems[]` array storing `{biz, marker}` pairs
- Added `_mapRenderPanel()` — builds list DOM, binds click to `zoomToShowLayer` + `openPopup`
- Extended `_mapClearResultMarkers()` to clear panel
- Extended `_mapPlaceResultMarkers()` to populate items and call render

Commit: `c0caa17`

## Previous Pass
Step 2 — Marker Clustering on Discovery Map

Commit: `38da7c3`

## Next Pass
Step 4 — Search Visible Area button

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
