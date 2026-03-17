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
Pass 18b — Human Draft Enforcement Layer

- Added `enforce_human_style()` post-processing function to `email_draft_agent.py`
- Applied between body assembly and sign-off append in `draft_email()`
- Strips formal opener phrases, lowercases `Hey` openers, trims at 65 words
- Does not sentence-split across paragraph breaks (preserves existing structure)
- 5-draft sample verified: 54–65 words, 2–3 sentences, no formal phrases
- No schema changes, no DRAFT_VERSION bump, no protected systems touched

Commit: `ff7564d`

## Previous Completed Pass
Pass 18a — Discovery State Reset (Phase 2)

## Next Pass
Pass 19 — TBD (territory heatmap, saturation view, tiled backend improvements, or outreach doc updates)

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
