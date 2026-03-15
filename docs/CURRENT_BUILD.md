# Current Build Pass

## Active System
Discovery Map — Frontend Improvements

## Status
Step 2 complete. Step 3 not yet started.

---

## Completed: Step 2 — Marker Clustering

Markers returned from `/api/discover_area` now cluster automatically via
`Leaflet.markercluster`. Zoom splits clusters; zoom out regroups them.
Commit: `38da7c3`

---

## Next: Step 3 — Results Side Panel

After a discovery search completes, display a scrollable list of discovered
businesses in a panel alongside the map.

### Scope
- Frontend only
- `dashboard_static/index.html` only

### Direction
- Panel appears on the right side of the map view after search completes
- Lists each discovered business: name, city, email presence indicator
- Clicking a list item opens the marker popup on the map
- Panel is cleared when a new search area is drawn

### Out of Scope
- Backend changes
- Search tiling or grid discovery
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
