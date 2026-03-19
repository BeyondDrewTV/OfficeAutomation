# Copperline AI Entry Point

If you are an AI assistant joining this repository, start here.

## Fast AI Startup

Read these 4 files before writing any code:

1. `AI_CONTROL_PANEL.md` - single-file project snapshot
2. `PROJECT_STATE.md` - current phase, version, last/next pass
3. `CURRENT_BUILD.md` - approved scope for this session
4. `PROTECTED_SYSTEMS.md` - what must not be touched

These four files contain the complete project state under ~1,000 tokens.
Do not start implementing until you have read all four.

## Full Context (if needed)

- `COPPERLINE_OVERVIEW.md` - full system description and repo layout
- `DISCOVERY_MAP_VISION.md` - map strategy and design philosophy
- `CLAUDE_BUILD_RULES.md` - implementation discipline and pass report format
- `CHANGELOG_AI.md` - complete development history

## What this project is

Copperline is an internal platform for discovering local service businesses,
sending cold outreach, and converting them into clients for a missed-call
texting automation service.

The primary development focus is the lead acquisition system, specifically the
dashboard-driven discovery map and outreach pipeline.

Observation-led drafting remains required. Observations may now be either:
- operator-authored observation text
- system-generated observation candidates grounded in real available lead context

During hardening, generated observations remain operator-reviewed by default
before drafting or send workflows proceed.

## Rules before you write any code

- Do not implement features outside the scope defined in `CURRENT_BUILD.md`.
- Do not modify protected systems listed in `PROTECTED_SYSTEMS.md`.
- Prefer additive changes over rewrites.
- After completing a pass, update `CHANGELOG_AI.md`, `PROJECT_STATE.md`, and `AI_CONTROL_PANEL.md`.
- Do not assume hidden bulk observation generation, auto-accept, or auto-send
  exists unless the repo explicitly shows it.

## How to scope a pass

Each pass delivers **one operator outcome** end-to-end.

- Multiple tightly related sub-changes are allowed in one pass
- All sub-changes must serve the same workflow goal
- Unrelated systems must not be bundled together
- The pass must be testable when complete

Good scope example - Discovery Coverage Expansion:
- Grid search tiles + multi-industry sweep + dedupe + history summary + cancel support
- All sub-changes serve one outcome: systematic neighborhood-level discovery

Bad scope example:
- Discovery + scheduler UX + message quality + email extraction in one pass
- These are unrelated systems; they must be separate passes

Passes typically touch 1-6 files. No hard maximum, but larger passes require
stronger cohesion. A pass that is hard to describe as one outcome is too broad.

## Quick orientation

| File | Purpose |
|---|---|
| `lead_engine/run_lead_engine.py` | Core engine - **protected** |
| `lead_engine/dashboard_static/index.html` | Entire frontend dashboard |
| `lead_engine/dashboard_server.py` | Flask API server |
| `lead_engine/data/prospects.csv` | Prospect records |
| `lead_engine/queue/pending_emails.csv` | Email draft queue |
| `docs/CHANGELOG_AI.md` | AI development history |
