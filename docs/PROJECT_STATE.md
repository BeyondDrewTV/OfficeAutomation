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
Pass 54 -- On-Demand Observation Evidence Refresh

- Added an operator-triggered single-lead evidence refresh path from the review
  panel.
- The system can now re-check website/contact evidence for one lead, update the
  stored lead insight/contact fields, and immediately retry observation
  candidate generation.
- Fresh site evidence is stored on the lead via existing insight/contact
  fields; the observation itself is still not auto-saved or auto-accepted.
- Refresh stays bounded and truthful:
  if no retrievable source exists, fetch fails, only generic template language
  is found, or no concrete business-specific signal appears, the panel stays
  blocked with a specific reason instead of fabricating evidence.
- Identity-sensitive lead keys remain stable during refresh:
  fallback websites may be used for the scan, but they are not silently written
  back to lead identity fields in this pass.

Commit: `e643def`

## Previous Completed Pass
Pass 53 -- Industry Saturation View

Commit: `f2ac842`

## Next Pass
TBD

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
   observation
8. Operator reviews, approves, or schedules for tomorrow morning
9. Emails are sent manually via Gmail
10. Follow-up drafting only proceeds when the lead record has grounded
   continuation context
11. Weak or generic follow-ups block instead of auto-queuing generic nurture copy
12. Clients onboard to missed-call texting service
