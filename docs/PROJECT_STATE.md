# Copperline Project State

Last Updated: 2026-03-16

## Copperline Version
v0.2

## Current Phase
Lead Acquisition Engine

## Current Focus
Outreach Queue Safety + Scheduled Send Foundations

## Last Completed Pass
Pass 9b — Scheduled Send Intent

Protected systems modified deliberately in this pass (schema extension only).
Scheduling is intent-only — no auto-send, no Gmail trigger, no background scheduler.

### Commit A — `24dc5b2`
- `"send_after"` appended to `PENDING_COLUMNS` in `run_lead_engine.py`
- `"send_after"` appended to `PENDING_COLUMNS` in `dashboard_server.py`
- `"send_after"` appended to `PENDING_EMAIL_COLUMNS` in `send/email_sender_agent.py`
- `"send_after"` appended to `PENDING_COLUMNS` in `outreach/followup_scheduler.py`
- `reply_checker.py` truncation bug fixed: 20-col list replaced with full 42-col schema including `send_after`

### Commit B — `52dd64a`
- `POST /api/schedule_email` added to `dashboard_server.py`
- Validates: index in bounds, business_name non-empty, send_after non-empty, index/name match
- Writes `send_after` only — no other field touched, no send triggered

### Commit C — `a5f09c5`
- `SEND_WINDOWS` const added to `index.html` (industry → local HH:MM send time)
- `panelScheduleTomorrow()` function added — computes tomorrow + window, POSTs to `/api/schedule_email`, updates row in memory, refreshes panel and table
- `🕐 Schedule for Tomorrow` button added to panel footer (`#panel-schedule-btn`)
- `fillPanel` extended to hide button when `row.sent_at` is set
- No auto-send, no Gmail launch, no background scheduler activation

## Previous Completed Pass
Pass 9a — Queue Visual Safety

Commit: `f712909`

## Next Pass
Pass 10 — TBD (territory heatmap, saturation view, or tiled backend improvements)

## Protected Systems Modified This Pass
- `run_lead_engine.py` — `PENDING_COLUMNS` extended (append only, no reorder)
- `send/email_sender_agent.py` — `PENDING_EMAIL_COLUMNS` extended (append only)
- `outreach/followup_scheduler.py` — `PENDING_COLUMNS` extended (append only)
- `outreach/reply_checker.py` — schema corrected to full 42-col list (was truncated to 20)
- `dashboard_server.py` — `PENDING_COLUMNS` extended + new route added

## Protected Systems Still Untouched
- Queue schema column ordering (unchanged — append only)
- `safe_autopilot_eligible` logic
- Email sender send logic
- Follow-up scheduler eligibility logic
- Gmail SMTP send path

## Core Operator Workflow

1. Discover businesses via map
2. System generates outreach drafts
3. Operator reviews and approves — or schedules for tomorrow morning
4. Emails sent manually via Gmail
5. Follow-ups tracked automatically
6. Clients onboarded to missed-call texting service
