# Copperline Project State

Last Updated: 2026-03-20

## Copperline Version
v0.2

## Current Phase
Lead Acquisition Engine

## Current Focus
V2 Stage 2 - Unified Lead Workspace Backbone

## Copperline Positioning
Copperline = Service Business Operations


    # Copperline Project State

Last Updated: 2026-03-20

## Copperline Version
v0.2

## Current Phase
Lead Acquisition Engine

## Current Focus
V2 Stage 2 - Unified Lead Workspace Backbone

## Copperline Positioning
Copperline = Service Business Operations

## Last Completed Pass
Pass 59 -- First-Touch Subject Semantic Precision (`7b0f5be`)

- Kept Pass 57's subject/body fit improvements, but split first-touch variation
  selection across subject, opener, consequence, offer, and CTA components so
  batches feel less templated.
- Variation stays deterministic by hashing real lead context per component
  instead of using one shared business-name-only variant across the whole draft.
- Added a bounded body-fit fallback so longer variation combinations keep the
  four-part structure intact instead of trimming away the CTA.
- Existing observation-required drafting, subject validation, and body
  validation remain intact.

## Previous Completed Pass
Pass 57 -- First-Touch Subject Fit + Variation

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
   observation, with subject lines and body copy both framed around a
   believable owner/operator offer instead of generic consulting language
8. Operator reviews, approves, or schedules for tomorrow morning
9. Emails are sent manually via Gmail
10. Follow-up drafting only proceeds when the lead record has grounded
   continuation context
11. Weak or generic follow-ups block instead of auto-queuing generic nurture copy
12. Clients onboard to missed-call texting service
.Value
 Previous Completed Pass
Pass 57 -- First-Touch Subject Fit + Variation

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
   observation, with subject lines and body copy both framed around a
   believable owner/operator offer instead of generic consulting language
8. Operator reviews, approves, or schedules for tomorrow morning
9. Emails are sent manually via Gmail
10. Follow-up drafting only proceeds when the lead record has grounded
   continuation context
11. Weak or generic follow-ups block instead of auto-queuing generic nurture copy
12. Clients onboard to missed-call texting service
