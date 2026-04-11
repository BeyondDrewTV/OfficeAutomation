# Copperline — Outbound Lead Acquisition System

**A 7-agent AI pipeline that handles the full outbound acquisition workflow — from prospecting to live reply.**

Built by [Andrew Yomantas](https://www.linkedin.com/in/andrew-yomantas-94a7383b0) | AI Product & Operations Builder

---

## What It Does

Most outbound tools are email sequencers with a fancier UI. Copperline is a designed workflow system — every stage has logic, every transition has a gate.

The pipeline:
- **Google Places discovery** — finds and scores local businesses as prospecting targets
- **Website scanning** — crawls each target and extracts context for personalization
- **Opportunity scoring (0–100)** — deterministic scoring model ranks leads before any outreach
- **AI draft generation** — produces personalized outbound emails scoped to each target's context
- **Send-window scheduling** — time-of-day and rate limiting enforced at the send layer
- **Gmail reply detection** — monitors the inbox and flags live responses automatically
- **Suppression state management** — SHA-256 deduplication ensures no target is contacted twice

**Production result: 100+ emails sent, live replies received.**

---

## What This Proves

- **End-to-end workflow design** — not a script, a system. Every stage is designed with edge cases, failure modes, and transitions in mind
- **Anti-spam enforcement** — deterministic send guards, rate limiting, and deduplication baked into the architecture, not bolted on
- **AI-directed execution at production scope** — the system runs, sends real email, and receives real replies
- **GTM and growth operations fluency** — the domain (outbound lead acquisition) is revenue-critical. The design reflects that

---

## Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python + Flask |
| Frontend | Leaflet.js (interactive lead map) |
| Email Integration | Google Workspace SMTP |
| Prospecting | Google Places API |
| Deduplication | SHA-256 hashing |
| Scheduling | Time-of-day + rate limiting logic |
| Dashboard | HTML/CSS ops interface |

---

## Architecture Highlights

**7-agent pipeline** — each agent owns a discrete stage: discovery → scan → score → draft → schedule → send → detect. Agents don't overlap. Failures in one stage don't cascade.

**Deterministic scoring** — opportunity scores are rule-based, not AI-generated. Consistent, auditable, and tunable without model changes.

**Anti-spam enforcement at the draft layer** — send guards run before any email leaves the system. Rate limiting (45s between sends), time-of-day windows (8am–6pm), and SHA-256 deduplication all enforced independently.

**Reply detection loop** — Gmail inbox is monitored for responses. When a live reply arrives, the lead state updates automatically and suppression kicks in.

---

## Status

Active / production. April 2026. 100+ emails sent, live replies in production. Dashboard includes delivery execution, deploy activation wizard, and offer hardening pipeline.

---

## Contact

[LinkedIn](https://www.linkedin.com/in/andrew-yomantas-94a7383b0) | drewyomantas@gmail.com
