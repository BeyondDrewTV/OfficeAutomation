# Current Build

Last Updated: 2026-04-10

## Active Focus

Prelaunch hardening OS — public delivery-kit coverage is now complete for all atomic offers.

The queue/pipeline work is complete (passes 172–189). All public offers now have real kit files on disk. No offer is delivery-proven yet.

## Completed This Session

### Delivery execution layer (this pass)
- Added **📋 Delivery Run** sub-tab and page to the Delivery section
- Operator can select any hardening offer, work through a per-offer checklist, check off items, capture proof links, add work notes, record blockers, set closeout status, and write closeout notes
- **Presence Refresh** gets a detailed 2-section checklist: GBP (12 items) + Facebook (11 items)
- All other offers fall back to their `qa_checks` from the catalog
- **Verification-readiness rail** shows: kit files on disk → delivery in progress/complete → closeout captured → verification (explicitly requires real proof on file — no fake promotion)
- **"▶ Run" button** on kit-complete Hardening Command cards — navigates directly to Delivery Run for that offer
- State persisted to `data/delivery_execution_log.json` via two new API routes (`GET/POST /api/delivery_run`)
- Server restart required to serve new routes

### Full public delivery-kit coverage milestone
- **Follow-Up & Reminder Setup**: cadence worksheet, message template pack, access checklist, test sequence, handoff closeout — 5 files, `hardening`
- **Review Request System**: review setup worksheet, review copy library, access checklist, QA checklist, handoff closeout — 5 files, `hardening`
- **Basic Cleanup** (bundle): scope matrix, activation checklist, closeout template — 3 files, advanced `planned` → `hardening`
- **Presence + Website** (bundle): intake worksheet, dependency checklist, combined go-live checklist, bundle closeout template — 4 files, advanced `planned` → `hardening`
- **Full Starter Package** (bundle): master intake worksheet, dependency sequencing checklist — 2 files, advanced `planned` → `hardening` (missing_qa and missing_closeout intentionally kept until bundle is delivery-proven)
- `delivery_kits.py` updated for all 5: `artifact_files`, `promotion_criteria`, cleared `missing_*` where real files now exist

### Previously hardened (prior passes)
- **Lead & Contact Setup**: 5 files, `hardening`
- **Presence Refresh**: 5 files, `hardening`
- **Starter Website**: 5 files, `hardening`
- **Estimate & Job Status Communication**: 5 files, `hardening`
- **Client Approval / Estimate Portal**: 5 files, `hardening`

### Deploy Activation — 6-step wizard (prior pass)
- Replaced long-scroll Deploy Activation page with a guided 6-step wizard
- Steps: Snapshot → Discovery → Recommend → Confirm → Packet → Action
- Persistent summary panel (right column / below on mobile)
- Progress bar is clickable; Back/Next navigation on each step

## Public Catalog State

| Status | Count |
|---|---|
| Ready | 1 (Missed Call Recovery only) |
| Hardening | 10 |
| Verification | 0 |
| Planned | 0 |

## Current Baseline

- Operations theater map-driven redesign: `95a6c01`
- Command center operations theater prototype: `710bf2a`
- Queue surface stable baseline: `bc0ef15`

## LOSI Theater Prototype (External)

- Current state: pass 17 (`losi_prototype_v2_pass17.html`)
- Completed: SVG glyph hierarchy, hub compass-rose, Loop nucleus, zone fills
- Next gap: lead-count pip labels on node glyphs
- Integration: not yet merged — pending prototype maturity

## Do Not Widen Into

- Email sender or queue schema rewrites
- Protected system changes (see `docs/PROTECTED_SYSTEMS.md`)
- Auto-send or scheduling logic changes
- Promoting any kit to `ready` or `launch_eligible = true` without a real delivered closeout on file
- Building "real" approval portal web apps or CRM systems — the approval portal is link/form based only

## Verification Standard

- Frontend-only changes: check locally in the browser, confirm no console errors
- Queue truth, send truth, schedule truth: require live verification before sign-off
- No real email sends during verification
- If a pass touches `dashboard_server.py` or `email_sender_agent.py`, verify real queue behavior before sign-off

## Historical Baseline

Queue pipeline completion baseline (passes 172–189): `b6a54f53334e28bf74398b71b0c0cef9ade8cafa`
Pass history: `docs/CHANGELOG_AI.md`
