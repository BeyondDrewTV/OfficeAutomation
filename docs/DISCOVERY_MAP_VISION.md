# Discovery Map Vision

## Purpose

The discovery map is the primary tool for finding new outreach targets.
The operator draws a circle on a map, selects an industry, and the system
queries the Google Places API to surface businesses within that area.

The map is intentionally manual and operator-driven — it does not run
automatically on zoom or pan. Every search is an explicit action.

---

## Current Behavior: Search This Area

The operator clicks to place a circle, sets a radius and industry, then
clicks "Search This Area." The backend calls `/api/discover_area`, which
queries Google Places and returns matching businesses. Discovered businesses
are written to `prospects.csv` as new leads, drafts are generated, and
markers are placed on the map at their coordinates.

This model works well for targeted searches. The operator controls exactly
where to look and how large an area to cover.

---

## The Radius Problem

Google Places returns results ranked by prominence. When a search radius is
large (e.g., 15–20 miles), the API surfaces only the most well-known
businesses in that region — franchises, chains, and highly-reviewed
establishments with strong Google profiles.

Smaller, independent local service businesses — the primary target for
Copperline — tend to have thin Google profiles and get buried in large-radius
searches. They only appear reliably when the search area is small and focused.

**Implication:** To discover the best outreach targets, the operator needs to
search at the neighborhood or zip-code level, not the metro level.

---

## Marker Clustering

When a discovery run returns 40–80 markers in a dense area, individual pins
overlap and become unreadable. Marker clustering solves this by grouping
nearby markers into cluster bubbles that display a count.

Zooming in splits clusters into smaller groups. Zooming in far enough reveals
individual business markers. Zooming back out regroups them.

Clustering does not trigger new searches — it only reorganizes markers already
loaded from the last discovery run.

---

## Planned: Search Visible Area

A "Search Visible Area" button will tile the current map viewport into a grid
of small-radius cells and run sequential discovery searches across each cell.
This systematically covers an area at the neighborhood level without requiring
the operator to manually reposition the circle for each block.

The tiled search approach is designed specifically to surface smaller
businesses that large-radius searches miss.

---

## Metro → Neighborhood Drilldown Strategy

The operator workflow is designed to work at increasing levels of granularity:

1. **Metro-level pass** — large radius, finds prominent businesses, fast
2. **City-level pass** — medium radius, narrower industry focus
3. **Neighborhood-level pass** — small radius (500m–1km), finds independent operators

The neighborhood level is where the most valuable undiscovered prospects live.
Search Visible Area automates the neighborhood-level grid systematically.

---

## Future: Territory Exploration

A longer-term goal is a territory system where the operator can designate
geographic zones (by zip code, city, or drawn polygon), track which zones
have been searched, and see a saturation view showing which industries are
already covered vs. underexplored in a given area.

This is not in scope for current development but informs the architecture
decisions being made now — specifically why cluster groups, marker arrays,
and search boundaries are being built as distinct, composable layers.
