# Current Build Pass

## Active System
Pass 57 -- First-Touch Subject Fit + Variation

## Status
Pass 57 complete. Repo is ready for the next product pass.

---

## Completed: Pass 57 -- First-Touch Subject Fit + Variation

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

Observation-led first-touch drafts were in a better place after Pass 56, but
the subject lines were still too repetitive, too dependent on generic
`question` patterns, and not always well matched to the actual body angle.

### What was added

**`lead_engine/outreach/email_draft_agent.py`**

- Bumped `DRAFT_VERSION` from `v11` to `v12`.
- Replaced the old one-subject-per-angle approach with bounded deterministic
  subject families tied to the actual first-touch angle.
- Added subject variation across after-hours, estimate follow-up, service
  requests, inquiries/contact-form follow-up, call handling, and fallback
  owner-workflow cases.
- Added explicit subject validation so first-touch subjects stay short,
  non-salesy, and owner-readable while blocking hype, clickbait, and generic
  spam wording.
- Kept the existing observation-led body generation intact; this pass was
  limited to subject quality and subject/body fit.

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
  - 12 subject/body pairs across after-hours, estimate, inquiry, service
    request, callback, and fallback owner-workflow observations
  - missing observation still blocks
  - generic observation still blocks
  - hype language still blocks
  - vague positioning still blocks
  - subject/body comparison against the previous committed Pass 56 draft agent
    shows cleaner subject fit and less repetitive `question` usage

---

## Previous Completed: Pass 56 -- First-Touch Naturalness + Owner Readability

- Kept the deterministic observation-led body structure, but rewrote first-touch
  wording so the outreach sounded more human and owner-readable.
