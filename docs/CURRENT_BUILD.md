# Current Build Pass

## Active System
Pass 54 -- On-Demand Observation Evidence Refresh

## Status
Pass 54 complete. Repo is ready for the next product pass.

---

## Completed: Pass 54 -- On-Demand Observation Evidence Refresh -- `8ad0e99`

Product changes in:
- `lead_engine/dashboard_server.py`
- `lead_engine/dashboard_static/index.html`
- `lead_engine/intelligence/website_scan_agent.py`
- `lead_engine/intelligence/observation_evidence_agent.py`
- `lead_engine/outreach/observation_candidate_agent.py`

Docs updated in:
- `docs/PROJECT_STATE.md`
- `docs/CURRENT_BUILD.md`
- `docs/CHANGELOG_AI.md`
- `docs/AI_CONTROL_PANEL.md`

No queue schema reorder/rename changes. No `run_lead_engine.py` changes.
No email sender core changes. No scheduler timing changes. No send-path changes.

### Problem addressed

Observation-led drafting could still stall when the saved lead evidence was too
weak for a safe candidate, which forced manual human observation writing even
when the operator intent was simply to re-check the business site and contact
signals.

### What was added

**`lead_engine/dashboard_server.py`**

- Added `POST /api/refresh_observation_evidence` for a single lead.
- The route refreshes website/contact evidence, writes safe lead-side updates,
  then reruns observation candidate generation before responding.
- Refresh stays bounded:
  no observation auto-save, no auto-regenerate/send, no scheduler/send-path
  changes.

**`lead_engine/intelligence/observation_evidence_agent.py`**

- Added a deterministic single-lead evidence refresh helper that reuses the
  existing website fallback, contact extraction, and website scan paths.
- Added bounded site-signal extraction for concrete operational evidence such
  as specialty/service, emergency or same-day language, estimate/booking
  language, and explicit service-area coverage.
- Added specific blocked reasons for:
  `no_retrievable_source`, `fetch_failed`,
  `generic_template_language`, and `no_concrete_business_signal`.

**`lead_engine/intelligence/website_scan_agent.py`**

- Extended the bounded site scan to keep a capped text corpus so the refresh
  helper can derive deterministic observation evidence without a second fetch
  loop.

**`lead_engine/outreach/observation_candidate_agent.py`**

- Added support for fresh site evidence already saved on the lead.
- The normal candidate generator can now reuse refreshed insight fields after a
  successful refresh, not just the immediate refresh response.

**`lead_engine/dashboard_static/index.html`**

- Added a `Refresh Evidence` action in the review panel.
- Refresh now updates the lead insight section, candidate box, and operator
  status text in place.
- The panel now shows clean ready/blocked states after refresh instead of
  forcing manual observation entry first.

### What remains intentionally out of scope

- Bulk evidence refresh
- Hidden background evidence mutation
- Observation auto-save or auto-accept
- Queue/send/scheduler changes
- `run_lead_engine.py` changes
- Persisting fallback websites into lead identity fields during this pass

### Verification

- Python compile checks:
  - `lead_engine/intelligence/website_scan_agent.py`
  - `lead_engine/intelligence/observation_evidence_agent.py`
  - `lead_engine/outreach/observation_candidate_agent.py`
  - `lead_engine/dashboard_server.py`
- Dashboard JS parses clean via `new vm.Script(...)`.
- Flask test client against temporary fixtures built from real repo rows:
  - `POST /api/refresh_observation_evidence` for `Massie Heating and Air Conditioning` -> `200`
    with candidate:
    `site is pretty explicit about ductless mini-split work and emergency service.`
  - `POST /api/refresh_observation_evidence` for `Premier Auto Repairs` -> `200`
    with candidate:
    `site is pretty explicit about brake work and service scheduling.`
  - `POST /api/refresh_observation_evidence` for `Dunham Plumbing LLC` -> `200`
    with refresh blocked reason `no_retrievable_source`, while the route still
    returned the existing phone-only candidate path truthfully.
  - After refresh, a normal `POST /api/generate_observation_candidate` on the
    refreshed `Massie Heating and Air Conditioning` fixture reused the stored
    fresh insight sentence/signals and returned the same candidate.

---

## Previous Completed: Pass 53 -- Industry Saturation View -- `f2ac842`

- Added a truthful industry saturation layer to the territory overlay workflow
  without changing the discovery backend or replacing the working circle.
