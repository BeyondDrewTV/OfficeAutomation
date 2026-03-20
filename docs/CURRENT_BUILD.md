# Current Build Pass

## Active System
Pass 56 -- First-Touch Naturalness + Owner Readability

## Status
Pass 56 complete. Repo is ready for the next product pass.

---

## Completed: Pass 56 -- First-Touch Naturalness + Owner Readability

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

Observation-led first-touch drafts had already moved onto the right business
positioning, but they still had some assembled wording:
awkward site observation openers, clunky "what goes wrong" lines, and CTA
phrases that did not sound like a real person finishing the thought naturally.

### What was added

**`lead_engine/outreach/email_draft_agent.py`**

- Bumped `DRAFT_VERSION` from `v10` to `v11`.
- Kept the same deterministic structure and angle model, but rewrote the
  generated wording around:
  more natural site-observation openers, plainer owner-readable consequence
  language, cleaner offer lines, and complete soft CTAs.
- Added observation-clause cleanup for common machine-y phrases from saved
  observations like:
  `site is pretty explicit about ...`,
  `they are pushing ...`, and similar site-summary wording.
- Tightened the vague-phrase blocklist to reject awkward old phrasing like
  `the mess shows up`, `if that is a live issue there`, and unfinished
  `where i'd start` style closes.
- Expanded the concrete-signal validation list so plain-English bottleneck
  language like `missed calls`, `slow follow-up`, `new requests`, and
  `response side` still passes without needing internal tool labels.

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
  - 10 first-touch examples across after-hours, estimate, inquiry, service
    request, and general owner-workflow observations
  - missing observation still blocks
  - generic observation still blocks
  - hype language still blocks
  - vague positioning still blocks
  - before/after comparison against the previous committed Pass 55 draft agent
    shows more natural opener, consequence, offer, and CTA phrasing

---

## Previous Completed: Pass 55 -- First-Touch Service Positioning Hardening

- Added deterministic first-touch service-positioning angles so outreach could
  describe Drew's real offer more concretely without generic consulting copy.
