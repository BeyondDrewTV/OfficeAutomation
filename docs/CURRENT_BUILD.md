# Current Build Pass

## Active System
Discovery Map — Frontend Improvements

## Status
Step 7 complete. Step 8 not yet scoped.

---

## Completed: Step 2 — Marker Clustering — `38da7c3`
## Completed: Step 3 — Results Side Panel — `c0caa17`
## Completed: Step 4 — Map Result Usability Polish — `a19bc16`
## Completed: Step 5 — Discovery Coverage Memory — `f27a472`
## Completed: Step 6 — Discovery History List — `6d79c64`

---

## Completed: Step 7 — Human-Readable Discovery Labels

`_mapAreaLabel(markers)` frequency-counts `biz.city` across result set and
returns the most common city name, or null if no city data exists. Label
stored in history entry as `label` field. `_mapRenderHistory()` uses it as
primary text with `lat/lng` fallback; secondary line shows radius + found
count; exact coords available as `title` tooltip on the label span.

Commit: `3f86767`

---

## Next: Step 8 — Search Visible Area Button

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
