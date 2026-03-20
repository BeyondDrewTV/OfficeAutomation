# Current Build Pass

## Active System
Pass 58 -- First-Touch Batch Variation Distribution

## Status
Pass 58 complete. Repo is ready for the next product pass.

---

## Completed: Pass 58 -- First-Touch Batch Variation Distribution

Product changes in:
- `lead_engine/outreach/email_draft_agent.py`

Docs updated in:
- `docs/PROJECT_STATE.md`
- `docs/CURRENT_BUILD.md`
- `docs/CHANGELOG_AI.md`
- `docs/AI_CONTROL_PANEL.md`

No queue schema reorder/rename changes. No `run_lead_engine.py` changes.
No email sender core changes. No scheduler timing/core changes.
No send-path changes. No follow-up system changes.

### Problem addressed

Observation-led first-touch drafts were stronger after Pass 57, but batches of
drafts could still feel templated because one shared deterministic variant
choice was driving subject, opener, consequence, offer, and CTA phrasing in
lockstep.

### What was added

**`lead_engine/outreach/email_draft_agent.py`**

- Bumped `DRAFT_VERSION` from `v12` to `v13`.
- Added per-component deterministic variation selection for subject, opener,
  consequence, offer, and CTA phrasing.
- Replaced the old single-variant lockstep pattern with context-hashed
  component picks based on lead/business fields plus the actual observation and
  angle.
- Kept the existing angle model and validation rules intact while reducing
  repeated sentence skeletons across a batch.
- Added a bounded body-fit fallback so longer combinations keep the CTA instead
  of trimming off the fourth sentence.

### What remains intentionally out of scope

- Observation generation or evidence refresh logic
- Queue/send/scheduler changes
- `run_lead_engine.py` changes
- Follow-up drafting
- Discovery/map work
- Hidden bulk regeneration or auto-send behavior

### Verification

- Python compile check:
  - `lead_engine/outreach/email_draft_agent.py`
- Direct draft-agent verification:
  - 20 first-touch outputs across after-hours, estimate, inquiry, service
    request, callback, and fallback owner-workflow observations
  - missing observation still blocks
  - generic observation still blocks
  - hype language still blocks
  - vague positioning still blocks
  - comparison against the previous committed Pass 57 draft agent shows more
    even subject distribution, more even opener spread, and less repeated
    consequence/offer/CTA phrasing across the same batch

---

## Previous Completed: Pass 57 -- First-Touch Subject Fit + Variation

- Kept first-touch subjects short and angle-matched while improving subject/body
  fit and reducing overuse of generic `question` constructions.
