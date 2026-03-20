# Current Build Pass

## Active System
Pass 59 -- First-Touch Subject Semantic Precision

## Status
Pass 59 complete. Repo is ready for the next product pass.

---

## Completed: Pass 59 -- First-Touch Subject Semantic Precision

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

First-touch subjects were better distributed after Pass 58, but some could
still feel broader or less exact than the underlying observation/body angle.
"call handling" led the callback pool, "question about X" appeared in multiple
angle families, and the owner_workflow fallback always returned the same generic
trio regardless of what the observation actually said.

### What was added

**`lead_engine/outreach/email_draft_agent.py`**

- Bumped `DRAFT_VERSION` from `v13` to `v14`.
- Rewrote `_subject_options_for_angle` to be observation-aware within each
  angle family. Subject pool options are now filtered/ordered toward the actual
  observation emphasis before the deterministic pick runs.
- `after_hours_response`: three sub-pools — emergency-first, weekend-first,
  general after-hours. No longer always offers "question about emergency calls".
- `estimate_follow_up`: quote-heavy observations now lead with "quote requests";
  estimate-heavy observations lead with "estimate follow-up". Dropped
  "estimate follow-up question" phrasing.
- `service_requests`: appointment/booking observations now lead with
  "appointment requests"; scheduling observations lead with "scheduling follow-up".
  Dead-code duplicate branch removed.
- `inquiry_routing`: contact-form observations get form-specific pool; text/chat
  observations get message-specific pool; general gets inquiry pool.
- `callback_recovery`: now leads with "missed calls" instead of "call handling".
  Voicemail/dispatch observations get voicemail-specific pool.
- `owner_workflow` fallback: routes by observation signal (phone/callback ?
  missed-calls pool; estimate/quote ? estimate pool; form/inquiry ? inquiry pool;
  true no-signal ? `["missed calls", "new inquiries", "follow-up timing"]`).
  "call handling" fully removed from all pools.

### What remains intentionally out of scope

- Observation generation or evidence refresh logic
- Queue/send/scheduler changes
- `run_lead_engine.py` changes
- Follow-up drafting
- Discovery/map work

### Verification

- AST parse clean, all public functions present, DRAFT_VERSION=v14
- 25 first-touch outputs across callback, after-hours (emergency/weekend/general),
  estimate, quote, contact-form, scheduling/appointment, voicemail, text/chat,
  and fallback observations — 23/25 generated; 2 fired expected pre-existing
  validation blocks (banned phrases in observation text)
- 8/8 before/after subject comparisons showed tighter semantic fit
- All blocking rules still hold (missing obs, short obs, generic obs,
  missing business_name)
- "call handling" confirmed absent from all subject pools

---

## Previous Completed: Pass 58 -- First-Touch Batch Variation Distribution

- Split first-touch variation selection across subject, opener, consequence,
  offer, and CTA components so batches feel less templated.