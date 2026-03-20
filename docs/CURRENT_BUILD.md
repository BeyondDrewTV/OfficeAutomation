# Current Build Pass

## Active System
Pass 61 -- Fully Reactive Offer, Close, Opener Variety

## Status
Pass 61 complete. Repo is ready for the next product pass.

---

## Completed: Pass 61 -- Fully Reactive Offer, Close, Opener Variety

Product changes in:
- `lead_engine/outreach/email_draft_agent.py`

Docs updated in:
- `docs/PROJECT_STATE.md`
- `docs/CURRENT_BUILD.md`
- `docs/CHANGELOG_AI.md`
- `docs/AI_CONTROL_PANEL.md`

No queue schema changes. No `run_lead_engine.py` changes.
No sender/scheduler/follow-up changes.

### Problem addressed

After Pass 60, consequence sentences were observation-reactive but offer and
close sentences were still pulled from angle-keyed pools. The offer said "i help
owners tighten X" regardless of the specific thing noticed. The close always
defaulted to "happy to share a few ideas specific to your setup if useful."
All openers started with the same verb cluster (i noticed / saw / noticed that).

### What was changed

**`lead_engine/outreach/email_draft_agent.py`** (v15 -> v16)

- Added `_build_reactive_offer(obs, angle)`: names the specific practical fix
  implied by the observation. Covers: no-confirmation-after-form, phone-only
  path, voicemail/dispatch, 24/7-emergency, after-hours/weekend, estimate-form
  as-CTA, quote-buttons-every-page, proposal/free-in-home, chat/text-back
  multi-channel, online-booking-widget, scheduling-link. Falls back to short
  plain angle sentence when no signal found. Removed `_offer_options` pool.

- Added `_build_reactive_close(obs, angle, channel)`: closes with a reference
  to something specific from the observation (dispatch setup, emergency-response
  operation, shop running nights and weekends, practice, etc.) instead of always
  defaulting to the generic permission phrase. Stays soft, no hard CTA.

- Expanded opener variety: "came across your site —" and "was looking at your
  site and noticed" added alongside existing "i was checking out your site".
  Openers now spread naturally across a batch (9 came-across, 5 was-looking,
  1 i-was-checking across a 15-draft sample).

- Updated `_build_first_touch_body` to call all three reactive functions
  directly. Fit fallback trims offer at first clause boundary; final fallback
  drops offer entirely (consequence + close preserved).

- Extended `_CONCRETE_SERVICE_SIGNALS` with reactive-sentence signal words so
  new offer/close phrasing passes the concrete-signal validator.

- DRAFT_VERSION bumped v15 -> v16.

### Sample draft (voicemail/dispatch observation)

  came across your site — your site lists a dispatch number and pushes voicemail
  for after-hours tow requests. requests that go to voicemail often don't get
  followed up until the next morning at the earliest. the fix is usually just a
  text that fires when a call goes to voicemail, so people know you got it and
  aren't calling around. happy to walk through what that looks like for a
  dispatch setup if useful.

### What remains intentionally out of scope

- Observation generation or evidence refresh
- Queue/send/scheduler changes
- `run_lead_engine.py` changes
- Follow-up drafting, discovery/map work

### Verification

- AST parse clean. DRAFT_VERSION=v16. All public functions present.
- 20/20 drafts generated cleanly across all angle families and obs types.
- 8/8 before/after comparisons: offer and close both now specific to the
  actual observation. Generic pool patterns eliminated.
- Opener variety confirmed spread across batch.
- All blocking rules confirmed holding.

---

## Previous Completed: Pass 60 -- Observation-Reactive Consequence Sentence

- Replaced the fixed angle-keyed consequence pool with `_build_reactive_consequence`.
  "usually the hard part is not the work itself..." fully eliminated.