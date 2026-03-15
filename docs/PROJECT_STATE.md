# Copperline Project State

Last Updated: 2026-03-15

## Current Phase
Lead Acquisition Engine

## Current Focus
Discovery Map System

## Last Completed Pass
Step 2 — Marker Clustering on Discovery Map

- Loaded `Leaflet.markercluster` v1.5.3 via CDN
- Added `_mapClusterGroup` variable and initialized in `_mapInit()`
- Result markers now route through `MarkerClusterGroup` instead of directly to map
- `_mapClearResultMarkers()` updated to use `clearLayers()`
- Drag handle and circle markers unchanged

Commit: `38da7c3`

## Previous Pass
Step 1 — Dashboard Navigation Restructure

Reduced nav from 13 tabs to 5 parent sections with sub-tabs.

Sections: Pipeline | Discovery | Clients | Health | Tools

Commit: `1dc811a`

## Next Pass
Results Side Panel — show discovered business list alongside the map

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
