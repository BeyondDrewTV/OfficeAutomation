# Copperline AI Entry Point

If you are an AI assistant joining this repository, start here.
Then read `docs/CLAUDE.md` for the concise startup contract.

---

## Mandatory Read Order

Read these before writing any code:

1. `docs/CLAUDE.md` -- startup contract, blast-radius rules, verification expectations
2. `docs/AI_CONTROL_PANEL.md` -- active guardrails, current pass state, key constraints
3. `docs/PROJECT_STATE.md` -- live implementation truth, current workflow reality
4. `docs/CURRENT_BUILD.md` -- approved scope for this session
5. `docs/PROTECTED_SYSTEMS.md` -- what must not be touched

These five files contain the complete project context needed to operate safely.
Do not start implementing until you have read all five.

---

## File Roles (one responsibility each)

| File | Sole responsibility |
|---|---|
| `CLAUDE.md` | Startup contract / operating rules for AI sessions |
| `AI_CONTROL_PANEL.md` | Active guardrails / current state snapshot |
| `PROJECT_STATE.md` | Live implementation truth / current reality |
| `CURRENT_BUILD.md` | Active build focus / near-term handoff state |
| `PROTECTED_SYSTEMS.md` | High-caution system boundaries |
| `AI_DEV_STANDARDS.md` | Durable engineering rules / pass scoping / recommendation format |
| `CHANGELOG_AI.md` | Append-only pass history (not current-state authority) |

**When file roles conflict:** `PROJECT_STATE.md` is the authority on current reality.
`PROTECTED_SYSTEMS.md` is the authority on what not to touch.
`CURRENT_BUILD.md` is the authority on approved scope.

---

## What This Project Is

Copperline is an internal platform for discovering local service businesses,
sending cold outreach, and converting them into clients for a missed-call
texting automation service.

Current focus: Command Center as unified discovery + outreach operational surface.
Map drives territory selection. Queue rail shows actionable leads. Command bar runs bulk actions.

---

## Pass Scoping

Pass scoping rules are in `AI_DEV_STANDARDS.md`. Do not duplicate them here.
The short version: one goal per pass, all sub-changes must serve that goal, testable when complete.

---

## Rules Before Writing Any Code

- Do not implement features outside the scope defined in `CURRENT_BUILD.md`
- Do not modify protected systems listed in `PROTECTED_SYSTEMS.md`
- Prefer additive changes over rewrites
- Inspect the relevant file before claiming any repo behavior
- After completing a pass: update `PROJECT_STATE.md`, `CURRENT_BUILD.md`, `AI_CONTROL_PANEL.md`, append to `CHANGELOG_AI.md`

---

## Quick File Reference

| File | Purpose |
|---|---|
| `lead_engine/run_lead_engine.py` | Core engine -- **protected** |
| `lead_engine/dashboard_static/index.html` | Entire frontend dashboard |
| `lead_engine/dashboard_server.py` | Flask API server |
| `lead_engine/data/prospects.csv` | Prospect records |
| `lead_engine/queue/pending_emails.csv` | Email draft queue -- **protected** |

---

## Additional Context (if needed)

- `docs/COPPERLINE_OVERVIEW.md` -- full system description and repo layout
- `docs/DISCOVERY_MAP_VISION.md` -- map strategy and design philosophy
- `docs/CLAUDE_BUILD_RULES.md` -- pass report format reference (see also AI_DEV_STANDARDS.md)
- `docs/CHANGELOG_AI.md` -- complete development history