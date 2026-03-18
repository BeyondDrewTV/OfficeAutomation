# Copperline AI Control Panel

Last Updated: 2026-03-18
Repository Version: v0.2

---

## Project Phase
Lead Acquisition Engine

## Current Focus
V2 Stage 2 — Unified Lead Workspace Backbone

## Current Build Pass
Pass 48 -- Lifecycle Coverage Expansion (complete)

## Last Completed Pass
Pass 48 -- Lifecycle Coverage Expansion

Commit: `e8d8312`

## Next Pass
TBD

## Upcoming Passes
- Pass 49 -- Observation Model Expansion
- Pass 50 -- Follow-Up System Rebuild
- Territory heatmap overlay
- Industry saturation view

---

## Execution Model

Bounded cohesive passes. Each pass delivers one operator outcome end-to-end.
Unrelated systems must not be bundled. No protected-system drift without explicit approval.

---

## Core Product

Copperline: discover local service businesses, draft outreach, send manually,
track replies, convert to clients, deploy missed-call texting.

---

## Key Systems

| System | Location |
|---|---|
| Lead discovery engine | `lead_engine/discovery/` |
| Outreach drafting | `lead_engine/outreach/` |
| Email queue | `lead_engine/queue/pending_emails.csv` |
| Follow-up automation | `lead_engine/run_lead_engine.py` |
| Map discovery interface | `lead_engine/dashboard_static/index.html` |
| Dashboard API | `lead_engine/dashboard_server.py` |
| Durable lead memory + timeline | `lead_engine/lead_memory.py` + `lead_engine/data/lead_memory.json` |
| Memory seed script | `lead_engine/scripts/seed_contacted_memory.py` |

## Protected Systems

- `run_lead_engine.py`
- Queue schema (column order and naming)
- `pending_emails.csv` pipeline
- Email sender
- Follow-up scheduler
- `safe_autopilot_eligible` logic

## Active Constraints

- Discovery must be intentional — no auto-search on pan or zoom
- No build steps — frontend is a single HTML file with CDN dependencies only
- Email sending is manual — auto-send is not enabled
- Suppressed/contacted leads filtered from all discovery entry points by default

---

## Complete Lifecycle Event Registry (as of Pass 48)

| Constant | Event | Hook point | Status |
|---|---|---|---|
| EVT_DRAFTED | Draft created | run_pipeline (protected) | Deferred |
| EVT_OBSERVATION_ADDED | Observation saved | api_update_observation | Live |
| EVT_DRAFT_REGENERATED | Draft regenerated | api_regenerate_draft | Live |
| EVT_REPLIED | Replied | api_log_contact result=replied | Live |
| EVT_NOTE_ADDED | Note added | api_update_conversation | Live |
| EVT_FOLLOWUP_SENT | Follow-up sent | send_followup (Pass 50) | Deferred |
| EVT_APPROVED | Approved | api_approve_row | Live |
| EVT_UNAPPROVED | Approval removed | api_unapprove_row | Live |
| EVT_SCHEDULED | Scheduled | api_schedule_email (set) | Live |
| EVT_UNSCHEDULED | Unscheduled | api_schedule_email (clear) | Live |

## Suppression State Registry (as of Pass 44-46)

| State | Hook point |
|---|---|
| contacted | api_log_contact, seed script, Mark Contacted btn |
| suppressed | /api/suppress_lead |
| deleted_intentionally | api_delete_row |
| do_not_contact | api_opt_out_row |
| hold | Panel Hold button |
| revived | /api/revive_lead, Memory tab Revive btn |

## Repo Quick Reference

| Question | File |
|---|---|
| What is being built now? | `docs/CURRENT_BUILD.md` |
| What is the project state? | `docs/PROJECT_STATE.md` |
| What must not be touched? | `docs/PROTECTED_SYSTEMS.md` |
| Dev history | `docs/CHANGELOG_AI.md` |
