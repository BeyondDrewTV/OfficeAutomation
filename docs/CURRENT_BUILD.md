# Current Build Pass

## Active System
Discovery Map — Frontend Improvements

## Status
Step 4 complete. Step 5 not yet scoped.

---

## Completed: Step 2 — Marker Clustering
Commit: `38da7c3`

---

## Completed: Step 3 — Results Side Panel
Commit: `c0caa17`

---

## Completed: Step 4 — Map Result Usability Polish

Added sort and filter controls to the results panel. Sort select (default /
Name A–Z / City A–Z) and email-only checkbox filter. `_mapRenderPanel()`
applies filter+sort at render time from control state; `_mapResultItems[]`
is never mutated. Count shows `(N of M)` when filter active. Controls reset
on clear.

Commit: `a19bc16`

---

## Next: Step 5 — Search Visible Area Button

Scope to be fully defined before implementation begins.

Direction: button that tiles the current viewport into a grid of small-radius
cells and runs sequential `/api/discover_area` calls across each cell.

### Known scope questions
- Reuse existing `/api/discover_area` endpoint or require new backend endpoint?
- How to handle rate limiting / delays between tile calls?
- What UI feedback during a multi-tile search?
- How do accumulated markers from multiple tiles interact with clustering?

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
