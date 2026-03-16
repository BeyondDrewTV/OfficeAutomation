# Copperline Project State

Last Updated: 2026-03-16

## Copperline Version
v0.2

## Current Phase
Lead Acquisition Engine

## Current Focus
Discovery Map System

## Last Completed Pass
Step 8 — Search Visible Area

- `#btnSearchVisible` and `#btnCancelVisible` added to map toolbar
- `_mapVisibleSearchActive` and `_mapVisibleSeenKeys` module variables added
- `_mapRenderHistory()` guards `radiusM: null` — shows "tiled" instead of NaN
- Click handler in history list no longer overwrites `_mapRadiusM` with null
- `_mapAppendResultMarkers(markers)` added — additive, never calls `_mapClearResultMarkers`
- `_mapVisibleTiles()` added — tiles current viewport into 1000m-radius grid cells, rejects > 30 tiles
- `mapSearchVisible()` added — sequential tiled discovery with 1200ms delay, dedup via `_mapVisibleSeenKeys`, coverage circles per productive tile, single history entry per run
- `_mapCancelVisible()` added — sets cancel flag, stops loop after current tile
- `#btnSearchVisible` wired to industry + circle state: enabled only when both are set
- `mapSearch()` single-circle flow unchanged

Commit: `32ff2bf`

## Previous Completed Pass
Pass A — Operator Safety Fixes

Commit: `4a169dd`

## Previous Pass
Step 7 — Human-Readable Discovery Labels

Commit: `3f86767`

## Next Pass
Step 9 — TBD (territory heatmap or tiled backend improvements)

## Upcoming Passes
- Territory heatmap overlay
- Industry saturation view
- Tiled discovery backend improvements

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
