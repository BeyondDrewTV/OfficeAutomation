# Copperline Voice Rules

Last Updated: 2026-04-01
Applies to: first-touch drafts, fallback drafts, all email body generation

---

## Short Version

Write like a human. Keep it professional but conversational. Be clear, direct, and natural. Do not use em dashes. Do not use buzzwords like "streamlined," "optimized," "unlock," or "transform." Do not sound like a press release, a SaaS company, or an SDR. Sound like a practical operator who understands service businesses and can help fix a real workflow problem. Friendly is good. Vague, fluffy, or overly polished is bad.

---

## Full Rules

### Write like a real person, not a marketing system.

Keep it professional but conversational. Be clear, direct, and natural, like you're writing to a smart friend.

### Do:

- Use plain English
- Keep sentences fairly short
- Sound grounded and confident
- Sound like a human operator who understands the business
- Be friendly without being fluffy
- Be specific without sounding scripted
- Make the email feel one-to-one, not campaign-written
- Use owner-language: missed calls, callbacks, estimates, follow-up, scheduling, work slipping through the cracks

### Do not:

- Use em dashes
- Use buzzwords like "streamlined," "optimized," "unlock," "transform," "synergy," or similar
- Sound like a press release
- Sound like a SaaS company
- Sound like an SDR sequence
- Sound overly polished, corporate, or performative
- Use fake warmth like "hope this finds you well"
- Use filler like "just reaching out" or "wanted to introduce myself"

---

## Copperline-Specific Tone Guidance

- Sound like a practical fixer, not a consultant trying to impress someone
- Sound like someone who understands how service businesses actually run
- Speak in owner-language: missed calls, callbacks, estimates, follow-up, scheduling, work slipping through the cracks
- Get to the point faster
- Keep the value clear early
- Stay low-pressure, but do not hide what Drew helps fix

---

## Target Feel

The email should feel like one capable person reaching out to another about a real business issue they can help fix.

It should NOT feel like:

- A pitch deck in email form
- A networking intro
- An AI-generated cold email
- A software sales message
- A marketing agency pretending to sound personal

---

## Mechanical Enforcement (in email_draft_agent.py)

These rules are enforced by `enforce_human_style()` and `validate_draft()`:

- Em dashes (`—`) are automatically converted to commas or periods in post-processing
- "Hope this finds you well" and similar fake warmth phrases are banned via `_VAGUE_POSITIONING_PHRASES`
- "Just reaching out," "wanted to introduce myself," and similar fillers are banned
- Buzzwords (optimize, unlock, transform, synergy, etc.) are banned via `_BANNED_WORDS`
- Subject lines cannot use "quick question" style phrasing

---

## Implementation Note

Apply these rules where they make sense for Copperline. Do not make the drafts stiff, robotic, or over-controlled. Keep the voice natural. The goal is a real human, not a perfectly formatted machine.
