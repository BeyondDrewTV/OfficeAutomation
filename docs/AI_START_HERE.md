# Copperline AI Entry Point

If you are an AI assistant joining this repository, start here.

## Fast AI Startup

If you are a new AI session, read these 4 files:

1. `AI_CONTROL_PANEL.md` — single-file project snapshot
2. `docs/PROJECT_STATE.md` — current phase, version, last/next pass
3. `docs/CURRENT_BUILD.md` — approved scope for this session
4. `docs/PROTECTED_SYSTEMS.md` — what must not be touched

These four files contain the complete project state under ~1,000 tokens.
Do not start implementing until you have read all four.

## Full Context (if needed)

For deeper understanding, also read:

- `docs/COPPERLINE_OVERVIEW.md` — full system description and repo layout
- `docs/DISCOVERY_MAP_VISION.md` — map strategy and design philosophy
- `docs/CLAUDE_BUILD_RULES.md` — implementation discipline and pass report format
- `docs/CHANGELOG_AI.md` — complete development history

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
