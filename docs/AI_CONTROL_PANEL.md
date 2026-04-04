# Copperline AI Control Panel

Last Updated: 2026-04-04 (Pass 142–147)
Repository Version: v0.3

> **Role:** Active operating contract + current AI guardrails.
> For live implementation truth, see `PROJECT_STATE.md`.
> For engineering rules, see `AI_DEV_STANDARDS.md`.
> For protected system boundaries, see `PROTECTED_SYSTEMS.md`.

---

## Current State

| Field | Value |
|---|---|
| Project Phase | Lead Acquisition + Conversion Delivery Engine |
| Current Focus | Pass 142–147 — Session Outcomes + Queue-Owned Recovery |
| Last Completed Pass | Pass 142–147 — Session Outcomes + Queue-Owned Recovery |
| Pass Before That | Pass 136–141 — Inline Exception Repair + Session Persistence |
| Next Pass | TBD |

---

## Core Product

Copperline: discover local service businesses -> draft outreach -> send manually -> track replies -> convert to clients -> deploy missed-call texting.

---

## Key Systems

| System | Location |
|---|---|
| Lead discovery engine | `lead_engine/discovery/` |
| Observation evidence refresh | `lead_engine/intelligence/observation_evidence_agent.py` |
| First-touch drafting | `lead_engine/outreach/email_draft_agent.py` |
| Observation candidate generation | `lead_engine/outreach/observation_candidate_agent.py` |
| Follow-up drafting | `lead_engine/outreach/followup_draft_agent.py` |
| Follow-up scheduler | `lead_engine/outreach/followup_scheduler.py` |
| Email queue | `lead_engine/queue/pending_emails.csv` |
| Map discovery interface | `lead_engine/dashboard_static/index.html` |
| Dashboard API | `lead_engine/dashboard_server.py` |
| Durable lead memory + timeline | `lead_engine/lead_memory.py` + `lead_engine/data/lead_memory.json` |

Protected systems are listed in `PROTECTED_SYSTEMS.md`. Do not duplicate that list here.

---

## Active Constraints

These constraints are enforced on all passes. Do not change product behavior that conflicts with these without explicit operator approval and an isolated commit.

- Discovery must be intentional -- no auto-search on pan or zoom
- No build steps -- frontend is a single HTML file with CDN dependencies only
- Territory overlay uses coarse stored data only -- no fake neighborhood precision
- Territory cells guide area selection; circle remains the working search geometry
- Email sending is manual/operator-reviewed -- auto-send must not drift into nurture behavior
- Observation-led drafting remains required for first-touch
- First-touch drafts must follow the 4-part structure: observation → loss/leak → fixer/operator line → reply-first CTA
- First-touch fixer/operator line must be visible by sentence 2–3 (validated structurally by `validate_draft()`)
- First-touch subjects must be problem-labeled (e.g. "missed calls", "estimate follow-up") — "quick question" style banned
- First-touch drafts must stay short, grounded in real service-business bottlenecks
- Generated observations are operator-reviewed by default during hardening
- Observation evidence refresh is operator-triggered, single-lead only
- No hidden bulk observation mutation or auto-accept behavior
- Suppressed/contacted leads filtered from all discovery entry points by default
- Discovery failures surface the real API error, not a generic label

---

## Governance Distinction

Protected delivery-core systems remain constrained. Operator-visible intelligence layers may evolve additively when changes are truthful, documented, reversible, and do not introduce hidden send-path or bulk-mutation behavior.

---

## Lifecycle Event Registry (as of Pass 58)

| Constant | Event | Hook point | Status |
|---|---|---|---|
| EVT_DRAFTED | Draft created | run_pipeline (protected) | Deferred |
| EVT_OBSERVATION_ADDED | Observation saved | api_update_observation | Live |
| EVT_DRAFT_REGENERATED | Draft regenerated | api_regenerate_draft | Live |
| EVT_REPLIED | Replied | api_log_contact result=replied | Live |
| EVT_NOTE_ADDED | Note added | api_update_conversation | Live |
| EVT_FOLLOWUP_SENT | Follow-up sent | api_send_followup | Live |
| EVT_APPROVED | Approved | api_approve_row | Live |
| EVT_UNAPPROVED | Approval removed | api_unapprove_row | Live |
| EVT_SCHEDULED | Scheduled | api_schedule_email (set) | Live |
| EVT_UNSCHEDULED | Unscheduled | api_schedule_email (clear) | Live |

---

## Repo Quick Reference

| Question | File |
|---|---|
| What are we building right now? | `docs/CURRENT_BUILD.md` |
| What is the project state? | `docs/PROJECT_STATE.md` |
| What must not be touched? | `docs/PROTECTED_SYSTEMS.md` |
| Engineering + scoping rules? | `docs/AI_DEV_STANDARDS.md` |
| Dev history? | `docs/CHANGELOG_AI.md` |
| Startup contract? | `docs/CLAUDE.md` |
| Email voice rules? | `docs/VOICE_RULES.md` |
| Audit report (Pass 90–92 context)? | See `docs/CHANGELOG_AI.md` |
