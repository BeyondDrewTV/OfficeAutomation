# Current Build Pass

## Active System
Discovery Map — Frontend Improvements

## Status
Step 3 complete. Step 4 not yet started.

---

## Completed: Step 2 — Marker Clustering
Commit: `38da7c3`

---

## Completed: Step 3 — Results Side Panel

After discovery, a scrollable panel appears to the right of the map listing
each discovered business with name, city, and email indicator. Clicking a
row calls `zoomToShowLayer` + `openPopup` to surface the marker through
any active cluster.

Commit: `c0caa17`

---

## Next: Step 4 — Search Visible Area Button

Add a button that tiles the current map viewport into a grid of small-radius
cells and runs sequential `/api/discover_area` calls across each cell.

### Scope
- Frontend: button, progress UI, tiling logic
- Backend: may require a new endpoint or reuse existing `/api/discover_area`
- To be fully scoped before implementation begins

### Out of Scope
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
