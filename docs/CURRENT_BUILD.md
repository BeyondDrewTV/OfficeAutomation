# Current Build Pass

## Active System
Discovery Map — Frontend Improvements

## Status
Step 5 complete. Step 6 not yet scoped.

---

## Completed: Step 2 — Marker Clustering
Commit: `38da7c3`

---

## Completed: Step 3 — Results Side Panel
Commit: `c0caa17`

---

## Completed: Step 4 — Map Result Usability Polish
Commit: `a19bc16`

---

## Completed: Step 5 — Discovery Coverage Memory

After a successful search, the searched area is snapshotted as a faint blue
dashed `L.circle` overlay (`interactive:false`, `fillOpacity:0.04`). Overlays
accumulate per session. A `Clear Coverage` button appears in the toolbar after
the first search and calls `_mapClearCoverage()` to remove all overlays.
Active circle and all existing behavior unchanged. No localStorage, no backend.

Commit: `f27a472`

---

## Next: Step 6 — Search Visible Area Button

Scope to be fully defined before implementation begins.

Direction: button that tiles the current viewport into a grid of small-radius
cells and runs sequential `/api/discover_area` calls across each cell.

### Known scope questions
- Reuse existing `/api/discover_area` endpoint or require new backend endpoint?
- How to handle rate limiting / delays between tile calls?
- What UI feedback during a multi-tile search?
- How do accumulated markers from multiple tiles interact with clustering?
- Coverage memory (Step 5) means tiled searches would auto-populate overlays — confirm desired behavior.

### Out of Scope for this pass
- Territory heatmaps
- Industry saturation metrics
- Deployment changes
- Stripe billing

---

## Upcoming Passes (not yet active)

| Pass | Description |
|---|---|
| Step 4 | Search Visible Area button |
| Step 5 | Tiled discovery backend |
| Step 6 | Territory exploration heatmap |
