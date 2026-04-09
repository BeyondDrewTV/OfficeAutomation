# Current Build

Last Updated: 2026-04-09

## Active Focus

Operations Theater — map-driven command center redesign and LOSI Theater visual prototype.

The queue/pipeline work is complete (passes 172–189). The current build focus is the Operations Theater: a map-driven command center surface that gives the operator spatial awareness over territory, leads, and pipeline state from a single view.

## Current Baseline

- Operations theater map-driven redesign: `95a6c01`
- Command center operations theater prototype: `710bf2a`
- Queue surface stable baseline: `bc0ef15`

## LOSI Theater Prototype (External)

The LOSI Theater visual prototype lives in Downloads as a standalone HTML file, separate from the repo.

- Current state: pass 17 (`losi_prototype_v2_pass17.html`)
- Completed: SVG glyph hierarchy (T1–T4 nodes), hub compass-rose, Loop nucleus, ownership badges, capital seat rotating diamond, zone fills, sector vocabulary
- Next gap: lead-count pip labels on node glyphs (node.leads text rendered at z=6.5+, below the glyph)
- Integration: not yet merged to repo — pending prototype maturity

## Do Not Widen Into

- Email sender or queue schema rewrites
- Protected system changes (see `docs/PROTECTED_SYSTEMS.md`)
- Auto-send or scheduling logic changes
- Broad dashboard rewrites outside the operations theater surface

## Verification Standard

- Frontend-only changes: check locally in the browser, confirm no console errors
- Queue truth, send truth, schedule truth: require live verification before sign-off
- No real email sends during verification
- If a pass touches `dashboard_server.py` or `email_sender_agent.py`, verify real queue behavior before sign-off

## Historical Baseline

Queue pipeline completion baseline (passes 172–189): `b6a54f53334e28bf74398b71b0c0cef9ade8cafa`
Pass history: `docs/CHANGELOG_AI.md`
