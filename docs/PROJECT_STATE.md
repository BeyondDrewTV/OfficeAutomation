# Copperline Project State

Last Updated: 2026-04-10 (mail config hardening)
Version: v0.4

## What Copperline Is

Copperline is the live contractor-outreach system inside OfficeAutomation. It discovers local businesses, builds first-touch drafts, lets the operator repair and approve queue work, schedules eligible rows, and keeps send/reply state in sync.

It is also a prelaunch hardening OS: the Delivery surface tracks real kit readiness, build status, and launch eligibility for every public offer. Nothing goes live until the underlying delivery kit is real and delivery-proven.

## Current Repo Truth

- Outbound email uses Google Workspace SMTP through the centralized config in `lead_engine/send/mail_config.py`. The official sender identity is `Drew @ Copperline <drewyomantas@copperlineops.com>`, reply-to defaults to the same address, and live sending is blocked unless `COPPERLINE_LIVE_SEND_ENABLED=true`.
- Delivery now has an **Offer Evidence Ledger + Promotion-Readiness Visibility** layer: offer-level evidence summaries are derived read-only from Delivery Run data and exposed in Hardening Command. Each offer can now show total runs, closeout captured count, review-ready count, reviewed-complete / reviewed-insufficient counts, proof coverage, blocker presence, and the last run that produced evidence. This is advisory visibility only; no offer is promoted automatically.
- Deploy Activation Step 3/Step 6 now supports **Recommendation + Simple Proposal Handoff**: editable simple options built from Quick Wins and the recommended stack, stored as `proposal_options`, then included in the copy-ready leave-behind. Quick Wins and proposal options are normalized through `/api/deploy_activation`. This is manual copy/paste only; no PDF, contract, invoice, or auto-send.
- Deploy Activation now supports **Accepted Option -> Activation Kickoff**: an operator can mark one proposal option as draft/leaning/accepted, carry acceptance notes/scope/assumptions, create an activation-ready delivery stack from the included real offer keys, and open the client-bound Delivery Run manually. Delivery Board rows show accepted option/scope when present. This is not a contract, payment, CRM, project automation, or verification promotion.
- Delivery Run now supports **Closeout Packet + Manual Verification Review**: each run can produce a copy-ready owner closeout packet, store run-level manual review state/notes, and appear in the Delivery Manual Review queue. This is evidence/review plumbing only; catalog `build_status`, `launch_eligible`, and offer verification truth do not move automatically.

- Queue/pipeline work is complete and stable — repair, approve, schedule, sent, and follow-up are all operational (passes 172–189)
- Command Center is the default landing tab
- Operations Theater surface is in active development — map-driven command center
- LOSI Theater visual prototype (standalone, pass 17 in Downloads) — not yet integrated
- Manual send discipline applies everywhere — no auto-send
- Deploy Activation is now a **6-step guided wizard** with a persistent summary panel (Step 1: Snapshot, Step 2: Discovery, Step 3: Recommend, Step 4: Confirm, Step 5: Packet, Step 6: Action)
- **All 11 public offers now have real kit files on disk** — every atomic offer has 5 files; bundles have 2–4 files. All at `hardening`, none delivery-proven yet.
- **Quick-Win Review** integrated into Deploy Activation Step 2 — operator captures 3–5 structured quick wins (category, what noticed, why it matters, quick win, priority, mapped offer) during a consultation. 11 starter templates. Leave-Behind output in Step 6 generates a copy-ready client summary from all wizard steps.
- **Delivery Run** page — client-bound execution flow: select client (from deployment pipeline) + offer → run checklist → capture before/after proof → closeout. `run_key = lead_key|offer_key` — runs are per-client, not global.
- **Missed Call Recovery** has a real 3-section operator checklist (Setup 5 + Testing 5 + Handoff 3 = 13 items). First offer ready to run against a real client.
- **Presence Refresh** checklist: 11 GBP + 10 Facebook = 21 items including before-state capture steps.
- **Verification-readiness rail** explicitly requires real closeout + proof before any offer can advance to verification. No auto-promotion.
- Only `Missed Call Recovery` is `ready` / `launch_eligible = true`
- Public catalog: 1 ready, 10 hardening, 0 verification, 0 planned
- Delivery execution state persisted to `data/delivery_execution_log.json`

## Current Baseline Commits

- Evidence ledger + delivery review queue: `HEAD` (this session)
- Mail config hardening: `830bd0e`
- Workspace sender identity + MCR checklist: `4b94f0b`
- Operations theater map-driven redesign: `95a6c01`
- Queue surface stable baseline: `bc0ef15`
- Queue pipeline completion (passes 172–189): `b6a54f5`

## Main Operator Surfaces

- Command Center: territory map, discovery, queue rail
- Pipeline / Queue: repair, approve, schedule, review
- Conversations: reply handling and commercial stack selection
- Delivery: downstream post-yes handoff board

## Queue Truth That Matters

- invalid drafts are not ready to send
- invalid or no-email rows cannot be approved into a sendable state
- scheduled-for-future rows are not send-ready right now
- send modal counts should only reflect rows that are truly `send_ready`
- operator-facing mail status should show the active Workspace sender and whether live send is enabled before any send run

## Known Open Risks

- LOSI Theater prototype not yet integrated into repo — integration will require a dedicated pass once prototype matures
- Live queue data contains historical edge cases — UI truth and API truth must be checked together before any queue-adjacent change
- All hardened kits (Lead & Contact Setup, Presence Refresh, Starter Website) are not yet delivery-proven — no kit advances to `verification` until a real closeout exists

## Where To Look Next

- `docs/CURRENT_BUILD.md` for current pass scope
- `docs/COPPERLINE_DELIVERY_KITS.md` for kit status and promotion criteria
- `docs/PROTECTED_SYSTEMS.md` for blast-radius rules
- `docs/CHANGELOG_AI.md` for pass history
