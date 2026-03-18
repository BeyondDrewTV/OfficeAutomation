# Copperline AI Control Panel

Last Updated: 2026-03-18
Repository Version: v0.2

---

## Project Phase
Lead Acquisition Engine

## Current Focus
V2 Stage 2 — Unified Lead Workspace Backbone

## Current Build Pass
Pass 47 -- Lead Timeline / Lifecycle Event Spine (complete)

## Last Completed Pass
Pass 47 -- Lead Timeline / Lifecycle Event Spine

Commit: `4a4a04b`

## Next Pass
TBD

## Upcoming Passes
- Pass 48 -- Contact Path Recommendation
- Pass 49 -- Observation Model Expansion
- Pass 50 -- Follow-Up System Rebuild
- Territory heatmap overlay
- Industry saturation view

---

## Execution Model

Passes use bounded cohesive blocks, not artificially tiny micro-changes.

- A pass may include 3-6 tightly related changes if they all improve one operator workflow
- Scope is defined by workflow cohesion: all sub-changes must serve the same outcome
- Unrelated systems must not be bundled in a single pass
- Passes must be testable end-to-end when complete
- No redesigns or protected-system drift without explicit operator approval

---

## Core Product

Copperline is an internal platform used to:

- Discover local service businesses
- Generate cold outreach drafts
- Send outreach manually via Gmail
- Track replies and follow-ups
- Convert prospects into clients
- Deploy missed-call texting automation

## Target Industries

- Plumbers
- HVAC companies
- Electricians
- Locksmiths
- Garage door companies
- Restoration contractors

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

- Discovery must be intentional - no auto-search on pan or zoom
- No build steps - frontend is a single HTML file with CDN dependencies only
- Email sending is manual - auto-send is not enabled
- Suppressed/contacted leads filtered from all discovery entry points by default

## Lifecycle Event Types (as of Pass 47)

| Constant | Event | Recorded by |
|---|---|---|
| EVT_DRAFTED | Draft created | (future: run_pipeline hook) |
| EVT_OBSERVATION_ADDED | Observation saved | api_update_observation |
| EVT_DRAFT_REGENERATED | Draft regenerated | api_regenerate_draft |
| EVT_REPLIED | Lead replied | api_log_contact result=replied |
| EVT_NOTE_ADDED | Conversation note added | api_update_conversation |
| EVT_FOLLOWUP_SENT | Follow-up sent | (future: send_followup hook) |

## Suppression States (as of Pass 44-46)

| State | Meaning | Recorded by |
|---|---|---|
| contacted | Outreach confirmed sent | api_log_contact, seed script, Mark Contacted btn |
| suppressed | General operator suppression | /api/suppress_lead |
| deleted_intentionally | Removed from queue | api_delete_row |
| do_not_contact | Opt-out / explicit block | api_opt_out_row |
| hold | Not now, revisit later | Panel Hold button |
| revived | Un-suppressed by operator | /api/revive_lead, Memory tab Revive btn |

## Repo Quick Reference

| Question | File |
|---|---|
| What is being built now? | `docs/CURRENT_BUILD.md` |
| What is the project state? | `docs/PROJECT_STATE.md` |
| What must not be touched? | `docs/PROTECTED_SYSTEMS.md` |
| Full system overview | `docs/COPPERLINE_OVERVIEW.md` |
| Dev history | `docs/CHANGELOG_AI.md` |
