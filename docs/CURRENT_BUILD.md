# Current Build Pass

## Active System
Discovery Map — Frontend Improvements

## Status
Step 6 complete. Step 7 not yet scoped.

---

## Completed: Step 2 — Marker Clustering — `38da7c3`
## Completed: Step 3 — Results Side Panel — `c0caa17`
## Completed: Step 4 — Map Result Usability Polish — `a19bc16`
## Completed: Step 5 — Discovery Coverage Memory — `f27a472`

---

## Completed: Step 6 — Discovery History List

Session-only history of successful searches, rendered below the map.
Each entry stores `{lat, lng, radiusM, found}`. Max 10 entries, newest-first.
Clicking a row sets `_mapRadiusM`, calls `_mapDrawCircle()`, and recenters
the map view. `_mapClearHistory()` resets. Coverage overlays unaffected.

Commit: `6d79c64`

---

## Next: Step 7 — Search Visible Area Button

Scope to be fully defined before implementation begins.

Direction: button tiles the current viewport into a grid of small-radius
cells and runs sequential `/api/discover_area` calls across each cell.

### Open scope questions
- Reuse `/api/discover_area` or new backend endpoint?
- How to handle rate limiting / delays between tile calls?
- What UI feedback during multi-tile search?
- How do accumulated markers from multiple tiles interact with clustering?
- Coverage memory (Step 5) + history (Step 6) would both auto-populate per tile — confirm desired behavior.

### Out of Scope
- Territory heatmaps, saturation metrics, deployment, Stripe

---

## Upcoming Passes (not yet active)

| Pass | Description |
|---|---|
| Step 4 | Search Visible Area button |
| Step 5 | Tiled discovery backend |
| Step 6 | Territory exploration heatmap |
