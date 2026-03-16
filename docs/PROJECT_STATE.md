# Copperline Project State

Last Updated: 2026-03-16

## Copperline Version
v0.2

## Current Phase
Lead Acquisition Engine

## Current Focus
Outreach Queue Safety + Scheduled Send Foundations

## Last Completed Pass
Pass 9a — Queue Visual Safety

- `statusBadge()` extended: `send_after && !sent_at` → `🕐 Scheduled` badge (amber, between stale and approved)
- `🕐 Scheduled` filter tab added to outreach toolbar (filters `send_after` set + unsent)
- `applyFiltersAndSort()` handles `currentFilter === 'scheduled'`
- `renderTable()` adds `row-scheduled` class to `<tr>` when `send_after` set + unsent
- `tbody tr.row-scheduled td:first-child` gets amber left border
- `panelFieldChanged()` extended: body edits show `Saving…` / `Saved ✓` / `Error saving` via `#panel-save-state` span
- CSS added: `.badge-scheduled`, `.row-scheduled`, `.panel-save-state` + state variants
- No backend changes. No protected systems touched.

Commit: `f712909`

## Previous Completed Pass
Step 8a — Decouple Search Visible Area button from manual circle state

Commit: `651df94`

## Previous Pass
Step 8 — Search Visible Area

Commit: `32ff2bf`

## Next Pass
Pass 9b — Schedule Action (requires operator approval to add `send_after` to `PENDING_COLUMNS` in `run_lead_engine.py`)

## Blocked: Pass 9b
`_write_pending_rows()` in `run_lead_engine.py` rewrites the CSV using only
`PENDING_COLUMNS`. Any `send_after` field written by a new route will be
silently stripped on next engine run. Adding `send_after` to `PENDING_COLUMNS`
requires a deliberate protected-system change. Needs operator sign-off.

## Protected Systems
- `run_lead_engine.py`
- Queue schema (`PENDING_COLUMNS` list)
- `pending_emails.csv` pipeline
- Email sender
- Follow-up scheduler
- Exception router
- `safe_autopilot_eligible` logic

## Core Operator Workflow

1. Discover businesses via map
2. System generates outreach drafts
3. Operator reviews and approves
4. Emails sent manually via Gmail
5. Follow-ups tracked automatically
6. Clients onboarded to missed-call texting service
