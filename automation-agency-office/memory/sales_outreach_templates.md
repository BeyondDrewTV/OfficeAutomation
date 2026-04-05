# DEPRECATED — sales_outreach_templates.md

> **This file is stale and must not be used as outreach guidance.**
>
> Last updated: 2026-04-05
> Deprecated in commit: `docs: deprecate stale outreach templates`

---

## Why this file is deprecated

This file was written for an older product positioning: a missed-call text-back
service sold at a fixed setup + monthly rate ($750 setup / $150/month).

That framing no longer reflects how Copperline operates or how outreach is
positioned. The copy here contains banned patterns (fake warmth, hard CTAs,
pricing, product-first pitch) that conflict with current voice rules.

Do not use these templates. Do not reference them in new drafts.

---

## Where live outreach truth lives

All first-touch and follow-up copy is generated deterministically at runtime by:

- `lead_engine/outreach/email_draft_agent.py` — first-touch email + DM drafts (v24 as of 2026-04-05)
- `lead_engine/outreach/followup_draft_agent.py` — follow-up sequence

Voice rules that govern all outreach:
- `docs/VOICE_RULES.md` — authoritative

Positioning guardrails:
- `automation-agency-office/memory/positioning_guardrails.md`

---

## For agents

If you are an agent reading this file as a listed input: **stop here**.
Do not use any copy from this file. Treat this entire file as void.
Route to `docs/VOICE_RULES.md` and `memory/positioning_guardrails.md` instead.
