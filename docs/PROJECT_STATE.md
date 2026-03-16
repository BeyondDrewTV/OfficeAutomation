# Copperline Project State

Last Updated: 2026-03-16

## Copperline Version
v0.2

## Current Phase
Lead Acquisition Engine

## Current Focus
Outreach Positioning Correction

## Copperline Positioning
Copperline = Service Business Operations

We identify where service businesses are losing work — missed calls, cold estimates, follow-ups that never happen — and install simple systems to fix it.

Automation is the implementation layer, not the headline.
Missed-call texting is one downstream solution, not the primary pitch.
Outreach goal: start a conversation about operational problems, not sell a product.

## Last Completed Pass
Pass 15b — Outreach Tone Correction: Operational Problem-First Messaging

- Corrected Pass 15a automation-agency drift
- `_OPENING_QUESTIONS` rewritten to lead with concrete loss scenarios
- `_BODY_FIXED` rewritten to lead with what the business is currently losing
- `cvSendQuick` templates updated to match operational framing
- `DRAFT_VERSION` bumped to `v6`
- No logic, routing, schema, or protected system changes

Commit: `fix: Pass 15b — correct outreach tone, lead with operational problems not automation framing`

## Previous Completed Pass
Pass 15a — Outreach Positioning: Remove Missed-Call-First Framing

## Next Pass
Pass 16 — TBD (territory heatmap, saturation view, tiled backend improvements, or outreach doc updates)

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
4. Scheduled queue sorted by send time — open it in the morning, send in order
5. Emails sent manually via Gmail
6. Follow-ups tracked automatically
7. Clients onboarded to missed-call texting service
