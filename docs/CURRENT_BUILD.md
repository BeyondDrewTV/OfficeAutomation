# Current Build Pass

## Active System
Discovery Map — Frontend Improvements

## Status
Step 8 complete.

---

## Completed: Step 2 — Marker Clustering — `38da7c3`
## Completed: Step 3 — Results Side Panel — `c0caa17`
## Completed: Step 4 — Map Result Usability Polish — `a19bc16`
## Completed: Step 5 — Discovery Coverage Memory — `f27a472`
## Completed: Step 6 — Discovery History List — `6d79c64`
## Completed: Step 7 — Human-Readable Discovery Labels — `3f86767`

---

## Completed: Step 8 — Search Visible Area Button — `32ff2bf`

Tiles the current map viewport into a grid of 1000m-radius cells and runs
sequential `/api/discover_area` calls across each cell.

**New HTML:**
- `#btnSearchVisible` — `.btn-secondary`, triggers `mapSearchVisible()`
- `#btnCancelVisible` — `.btn-ghost`, hidden by default, triggers `_mapCancelVisible()`
- Both inserted in map toolbar after `#btnMapSearch`, before Clear button
- `#map-industry` gains `onchange` handler to keep `#btnSearchVisible` in sync

**New JS module variables:**
- `let _mapVisibleSearchActive = false` — loop guard
- `let _mapVisibleSeenKeys = new Set()` — cross-tile dedup

**`_mapRenderHistory()` fix:**
- `radiusM: null` entries render as "tiled" instead of "NaN mi"
- Click handler now guards: `if (entry.radiusM != null) _mapRadiusM = entry.radiusM`

**New functions:**
- `_mapAppendResultMarkers(markers)` — appends to cluster group, result arrays, renders panel; never clears
- `_mapVisibleTiles()` — reads `_mapInstance.getBounds()`, builds lat/lng grid at 2000m step, returns `{ tiles, tooLarge }`, rejects > 30 tiles
- `mapSearchVisible()` — requires industry, rejects duplicate run, iterates tiles sequentially, 1200ms inter-tile delay, deduplicates via `_mapVisibleSeenKeys`, adds coverage circle per productive tile, writes one history entry with `radiusM: null` on completion
- `_mapCancelVisible()` — sets `_mapVisibleSearchActive = false`, updates status text

**Industry/circle enable wiring:**
- `_mapDrawCircle` enables `#btnSearchVisible` only if industry is already selected
- `mapClearCircle` disables `#btnSearchVisible`
- `#map-industry` onchange disables `#btnSearchVisible` if no industry or no circle

**Unchanged:**
- `mapSearch()` single-circle flow
- All protected systems
- All prior steps

---

## Next: Step 9 — TBD

Candidates:
- Territory heatmap overlay
- Tiled backend improvements (rate-limit handling, pagination)
- Zoom-to-fit after tiled search completes

Define scope before starting.

### Out of Scope
- Territory heatmaps, saturation metrics, deployment, Stripe
