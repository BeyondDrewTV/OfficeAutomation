# Copperline Project State

Last Updated: 2026-03-17

## Copperline Version
v0.2

## Current Phase
Lead Acquisition Engine

## Current Focus
Discovery Triage + Lead Qualification Controls

## Copperline Positioning
Copperline = Service Business Operations

We identify where service businesses are losing work - missed calls, cold estimates, follow-ups that never happen - and install simple systems to fix it.

Automation is the implementation layer, not the headline.
Missed-call texting is one downstream solution, not the primary pitch.
Outreach goal: start a conversation about operational problems, not sell a product.

## Last Completed Pass
Pass 32 - Discovery Triage + Lead Qualification Controls

- Added a frontend-only qualification layer to the discovery results rail so leads are classified at a glance as `Ready now`, `Maybe later`, `Needs contact info`, `Weak / skip`, or `Sent / closed`.
- Added compact triage chips with live counts so operators can instantly narrow large result sets to ready leads, weak leads, no-email leads, or contact-info gaps without manually scanning a flat list.
- Added a `Group: Qualification` mode and per-result qualification badges/reason chips so large discovery sweeps are easier to sort into work-now vs later buckets.
- Preserved Pass 30 edit stability by keeping the visible review context tied to the current narrowed result set and verifying overlay clicks still do not dismiss the review panel.
- Verified the dashboard still loads, triage chips/grouping render correctly, item clicks still drive marker popups, review opening remains stable, and Pass 29 discovery controls still load.
- Reconfirmed no protected systems were touched; the pass stayed in `lead_engine/dashboard_static/index.html`.

Commit: `8868847`

## Previous Completed Pass
Pass 31 - Contact Quality Upgrade

## Next Pass
TBD

## Protected Systems
- `run_lead_engine.py`
- Queue schema (column order and naming)
- `pending_emails.csv` pipeline
- Email sender
- Follow-up scheduler
- `safe_autopilot_eligible` logic

## Core Operator Workflow

1. Discover businesses via map
2. System generates outreach drafts
3. Operator reviews, approves, or schedules for tomorrow morning
4. Scheduled queue sorted by send time - open it in the morning, send in order
5. Emails sent manually via Gmail
6. Follow-ups tracked automatically
7. Clients onboarded to missed-call texting service
