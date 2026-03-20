# Current Build Pass

## Active System
Pass 62 -- Voice Rewrite, Consultation Positioning

## Status
Pass 62 complete.

---

## Completed: Pass 62 -- Voice Rewrite, Consultation Positioning

- `lead_engine/outreach/email_draft_agent.py` (v16 -> v17)

### What changed

Completely rewrote body generation to match Drew's actual writing voice and
reposition the offer away from product-feature language toward one-on-one
personalized consultation.

Structure changed from one run-on paragraph to 4 short paragraphs with line
breaks between each:
- P1: "My name is Drew. Saw [observation]." — direct, present tense, no "I noticed that"
- P2: Consequence — hedged with "probably", natural trailing thought, observation-specific
- P3: Offer — "I work one on one with owners to find where things like that are slipping
  and put something together specific to how they run things." No product pitch, no feature
  list. Sells the person and the process.
- P4: Real close question — "Worth a quick call?" Not "happy to", not "worth a look"

Killed permanently: "happy to", "worth a look", "i help owners [verb] the [noun] side",
"the fix is usually", "doesn't have to be complicated", "came across your site",
"i was checking out your site", em-dash transitions, run-on sentences.

Added `_build_observation_opener`, `_build_consequence_sentence`, `_build_offer_sentence`,
`_build_close_sentence` — all voice-matched to Drew's actual writing patterns.

### Verification
- 10/10 drafts clean across all angle types
- All blocking rules holding
- Reads like a person, not a system

---

## Previous: Pass 61 -- Fully Reactive Offer, Close, Opener Variety