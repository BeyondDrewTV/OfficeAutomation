# Copperline Project State

Last Updated: 2026-03-19

## Copperline Version
v0.2

## Current Phase
Lead Acquisition Engine

## Current Focus
V2 Stage 2 - Unified Lead Workspace Backbone

## Copperline Positioning
Copperline = Service Business Operations

## Last Completed Pass
Pass 56 -- First-Touch Naturalness + Owner Readability

- Kept the deterministic observation-led structure from Pass 55, but rewrote
  the first-touch language to read more like a real owner-facing cold email and
  less like assembled system copy.
- Openers now use more natural site-reference phrasing and normalize some
  machine-y observation text into plain owner-facing language.
- Consequence sentences now stay probabilistic and owner-readable:
  missed calls, slow follow-up, inquiries slipping through, and estimate
  requests sitting too long once the day gets busy.
- Offer and CTA lines now stay concrete without drifting into product-feature
  dumping, jargon, or unfinished phrasing.
- Validation still blocks missing observation, generic observation, hype, and
  vague positioning.

## Previous Completed Pass
Pass 55 -- First-Touch Service Positioning Hardening

## Next Pass
UNKNOWN / TBD

## Protected Systems
- `run_lead_engine.py`
- Queue schema (column order and naming)
- `pending_emails.csv` pipeline
- Email sender
- Follow-up scheduler timing/core
- `safe_autopilot_eligible` logic

## Core Operator Workflow

1. Review the discovery map for coarse territory coverage, industry saturation,
   lead clustering, and underworked versus duplicate-heavy cells
2. Load a territory cell into the working circle or place the circle manually,
   compare industry saturation in that area, then fine-tune radius and run
   deliberate area discovery
3. System can generate a grounded observation candidate when real lead evidence
   is strong enough
4. If the saved evidence is weak, the operator can trigger a single-lead
   evidence refresh from the review panel to re-check live website/contact
   signals and retry candidate generation
5. Operator reviews, uses, or edits the observation candidate, then saves the
   final observation to the lead row
6. Observation-led first-touch drafting still blocks when there is no valid
   saved observation
7. System generates observation-led first-touch drafts from the approved/saved
   observation, framing the message around a believable owner/operator offer
   instead of generic consulting language
8. Operator reviews, approves, or schedules for tomorrow morning
9. Emails are sent manually via Gmail
10. Follow-up drafting only proceeds when the lead record has grounded
   continuation context
11. Weak or generic follow-ups block instead of auto-queuing generic nurture copy
12. Clients onboard to missed-call texting service
