# Copperline — AI Project Context

Read this file first when joining a new session on this repository.
Then read `docs/AI_START_HERE.md` for the full entry protocol.

---

## What This Project Is

Copperline is a private outbound acquisition engine for a one-person
automation consultancy. The product being sold is a missed-call texting
service for local service businesses (plumbers, HVAC, electricians, roofers,
landscapers).

The system discovers businesses, generates cold outreach, manages follow-ups,
and tracks the pipeline to close.

---

## Current Development Focus

The discovery map system — a Leaflet.js map embedded in the dashboard that
lets the operator draw a search circle, select an industry, and surface local
businesses via the Google Places API.

Active improvements: marker clustering, results panel, search-visible-area,
tiled neighborhood-level discovery.

---

## Tech Stack

- Backend: Python / Flask
- Frontend: Single HTML file, no build step, CDN dependencies only
- Map: Leaflet.js + Leaflet.markercluster
- Data: CSV files (no database)
- Email: Gmail, manual send

---

## Repository Layout (key paths)

```
lead_engine/run_lead_engine.py          ← core engine (protected)
lead_engine/dashboard_server.py         ← Flask API
lead_engine/dashboard_static/index.html ← entire frontend
lead_engine/data/prospects.csv          ← prospect records
lead_engine/queue/pending_emails.csv    ← email draft queue
docs/                                   ← AI control panel (start here)
```

---

## Critical Constraints

- `run_lead_engine.py`, the queue schema, and the email pipeline are protected.
  A prior repair script caused data loss. Do not touch these without explicit
  operator approval.
- All frontend work happens in a single HTML file. No build tools. CDN only.
- Email sending is manual. Auto-send is not enabled.
- Every pass must be scoped, committed, and documented before starting the next.

---

## Where to Find Current Status

| Question | File |
|---|---|
| What are we building right now? | `docs/CURRENT_BUILD.md` |
| What was last completed? | `docs/PROJECT_STATE.md` |
| What must not be touched? | `docs/PROTECTED_SYSTEMS.md` |
| What is the full system design? | `docs/COPPERLINE_OVERVIEW.md` |
| What has been built so far? | `docs/CHANGELOG_AI.md` |
| What are the build rules? | `docs/CLAUDE_BUILD_RULES.md` |
