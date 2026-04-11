# Copperline — Claude Code Instructions

## ⚠️ LIVE PRODUCTION SYSTEM
This pipeline sends real outbound emails to real leads. 100+ emails sent, live replies active as of March 2026.

**Before running ANY command that triggers the pipeline:**
- Confirm you intend to run against production
- Never use production lead lists for testing
- Changes to email generation, send scheduling, or suppression logic require explicit review before execution

## Startup Read Order
Before writing any code, read in this order:
1. `docs/CLAUDE.md` — operating contract and blast-radius rules
2. `docs/PROJECT_STATE.md` — implementation truth
3. `docs/CURRENT_BUILD.md` — approved scope for this session
4. `docs/PROTECTED_SYSTEMS.md` — what must not be touched

## What This Is
Copperline — a 7-agent AI pipeline for outbound contractor lead acquisition.
Agents: prospecting → website scanning → opportunity scoring → AI draft generation → send scheduling → reply detection → suppression management.

## Tech Stack
- Backend: Python/Flask (`lead_engine/dashboard_server.py`)
- Frontend: single-file HTML/JS/CSS (`lead_engine/dashboard_static/index.html`)
- Map: Leaflet.js
- Email: Google Workspace SMTP via `lead_engine/send/mail_config.py`
- AI pipeline: 7 agents in `lead_engine/`

## Critical Files
| File/Folder | Notes |
|---|---|
| `.env` | **Never commit. Contains API keys and SMTP credentials.** |
| `lead_engine/dashboard_server.py` | Flask app — all API routes |
| `lead_engine/dashboard_static/index.html` | Entire frontend — 18k+ lines |
| `lead_engine/send/mail_config.py` | Centralized mail config boundary |
| `lead_engine/data/` | Live CSVs and JSON — queue, delivery log, suppression |
| `missed_call_product/` | MCR product module (imported by dashboard_server) |
| `missed_call_service/` | Standalone MCR webhook service |

## Commands
```bash
# Activate venv first
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # macOS/Linux

# Run the dashboard
flask run
# or
python lead_engine/dashboard_server.py
```

## Safety Rules
1. `.env` must never be staged or committed
2. Never trigger a send loop during debugging — `COPPERLINE_LIVE_SEND_ENABLED` must be `true` explicitly
3. If you're not sure whether a command will send real emails, stop and ask
4. The suppression list (`lead_engine/data/`) is critical — do not truncate or overwrite it

## Git
- Remote: `origin → https://github.com/DrewYomantas/Copperline.git`
- Branch: main

## Repo-Level Claude Settings
`.claude/settings.json` — production guard hook fires before `flask run`, pipeline commands, and `git add/commit`.
