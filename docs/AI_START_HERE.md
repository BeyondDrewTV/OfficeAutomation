# Copperline AI Entry Point

If you are an AI assistant joining this repository, start here.

## Read these files in order

1. `docs/PROJECT_STATE.md` — current phase, last commit, next pass
2. `docs/CURRENT_BUILD.md` — what is approved to build right now
3. `docs/PROTECTED_SYSTEMS.md` — what must not be touched
4. `docs/COPPERLINE_OVERVIEW.md` — full system understanding

## What this project is

Copperline is an internal platform for discovering local service businesses,
sending cold outreach, and converting them into clients for a missed-call
texting automation service.

The primary development focus is the lead acquisition system — specifically the
dashboard-driven discovery map and outreach pipeline.

## Rules before you write any code

- Do not implement features outside the scope defined in `CURRENT_BUILD.md`.
- Do not modify protected systems listed in `PROTECTED_SYSTEMS.md`.
- Prefer additive changes over rewrites.
- Read `CLAUDE_BUILD_RULES.md` before starting any implementation pass.
- After completing a pass, update `CHANGELOG_AI.md` and `PROJECT_STATE.md`.

## Quick orientation

| File | Purpose |
|---|---|
| `lead_engine/run_lead_engine.py` | Core engine — **protected** |
| `lead_engine/dashboard_static/index.html` | Entire frontend dashboard |
| `lead_engine/dashboard_server.py` | Flask API server |
| `lead_engine/data/prospects.csv` | Prospect records |
| `lead_engine/queue/pending_emails.csv` | Email draft queue |
| `docs/CHANGELOG_AI.md` | AI development history |
