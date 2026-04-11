# Copperline AI Control Panel

Last Updated: 2026-04-09

This file holds pipeline-specific constraints and the high-risk file list.
It is not required startup reading. For current truth, read the 4-file contract:
`docs/CLAUDE.md` → `docs/PROJECT_STATE.md` → `docs/CURRENT_BUILD.md` → `docs/PROTECTED_SYSTEMS.md`

## Active Constraints

- manual send discipline stays intact — no auto-send
- first-touch remains observation-led — no hidden bulk mutation
- no queue/send truth changes without live verification
- frontend remains single-file `lead_engine/dashboard_static/index.html`
- discovery remains operator-triggered
- future-scheduled rows can be valid without being sendable now
- outbound mail sends through Google Workspace SMTP as `drewyomantas@copperlineops.com`; live sends require `COPPERLINE_LIVE_SEND_ENABLED=true`

## High-Risk Files

- `lead_engine/dashboard_static/index.html`
- `lead_engine/dashboard_server.py`
- `lead_engine/send/email_sender_agent.py`
- `lead_engine/send/mail_config.py`
- `lead_engine/run_lead_engine.py`
- `lead_engine/queue/pending_emails.csv`
