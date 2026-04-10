# Copperline Project State

Last Updated: 2026-04-10
Version: v0.4

## What Copperline Is

Copperline is the live contractor-outreach system inside OfficeAutomation. It discovers local businesses, builds first-touch drafts, lets the operator repair and approve queue work, schedules eligible rows, and keeps send/reply state in sync.

It is also a prelaunch hardening OS: the Delivery surface tracks real kit readiness, build status, and launch eligibility for every public offer. Nothing goes live until the underlying delivery kit is real and delivery-proven.

## Current Repo Truth

- Queue/pipeline work is complete and stable — repair, approve, schedule, sent, and follow-up are all operational (passes 172–189)
- Command Center is the default landing tab
- Operations Theater surface is in active development — map-driven command center
- LOSI Theater visual prototype (standalone, pass 17 in Downloads) — not yet integrated
- Manual send discipline applies everywhere — no auto-send
- Deploy Activation is now a **6-step guided wizard** with a persistent summary panel (Step 1: Snapshot, Step 2: Discovery, Step 3: Recommend, Step 4: Confirm, Step 5: Packet, Step 6: Action)
- **All 11 public offers now have real kit files on disk** — every atomic offer has 5 files; bundles have 2–4 files. All at `hardening`, none delivery-proven yet.
- Only `Missed Call Recovery` is `ready` / `launch_eligible = true`
- Public catalog: 1 ready, 10 hardening, 0 planned

## Current Baseline Commits

- Operations theater map-driven redesign: `95a6c01`
- Command center operations theater prototype: `710bf2a`
- Queue surface stable baseline: `bc0ef15`
- Queue pipeline completion (passes 172–189): `b6a54f53334e28bf74398b71b0c0cef9ade8cafa`

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

## Known Open Risks

- LOSI Theater prototype not yet integrated into repo — integration will require a dedicated pass once prototype matures
- `lead_engine/scripts/reset_queue_from_gmail.py` remains a prevention-side cleanup gap from the stranded-drafted hotfix
- Live queue data contains historical edge cases — UI truth and API truth must be checked together before any queue-adjacent change

## Known Open Risks

- LOSI Theater prototype not yet integrated into repo
- `lead_engine/scripts/reset_queue_from_gmail.py` remains a prevention-side cleanup gap
- All three hardened kits (Lead & Contact Setup, Presence Refresh, Starter Website) are not yet delivery-proven — no kit advances to `verification` until a real closeout exists

## Where To Look Next

- `docs/CURRENT_BUILD.md` for current pass scope
- `docs/COPPERLINE_DELIVERY_KITS.md` for kit status and promotion criteria
- `docs/PROTECTED_SYSTEMS.md` for blast-radius rules
- `docs/CHANGELOG_AI.md` for pass history
