# Current Build Pass

## Active System
Pass 65 -- US Sales Regions + Visual Makeover

## Status
Pass 65 complete.

---

## Completed: Pass 65 -- US Sales Regions + Visual Makeover

Files: `lead_engine/dashboard_server.py`, `lead_engine/dashboard_static/index.html`

### US Sales Regions
- Map now starts at full US view (lat 39.5, lng -98.35, zoom 4)
- `US_SALES_REGIONS` — 6 baked-in regions (Northeast, Southeast, Midwest,
  South Central, Mountain West, Pacific West) as colored clickable rectangles
- `_mapShowRegions()` renders at zoom =5 with colored labels
- `_mapSelectRegion()` zooms into region, enables county-level clicking
- `_mapHandleZoomRegions()` auto-shows/hides on zoom events
- Map click guard at zoom =5 lets region polygons handle their own clicks
- `/api/reverse_boundary` backend endpoint added for click-to-county

### Visual Makeover
- Deeper dark background: `--bg:#080a0f` (was `#0e0f12`)
- Gradient header with copper-branded Copperline title (webkit gradient text)
- Gradient buttons with drop shadows (`--btn-shadow`, `--card-shadow`)
- Cards use subtle top-to-bottom gradients
- Nav bars use layered gradient backgrounds
- Map container taller: 560px (was 500px)
- Results panel wider: 340px (was 320px)
- Deeper panel shadow on review panel
- Map instructions styled as blue-tinted info card
- Territory and grid toolbars use darker gradient backgrounds

---

## Previous: Pass 64 -- Click-to-Boundary, Reverse Geocoding, Zoom Drill-Down