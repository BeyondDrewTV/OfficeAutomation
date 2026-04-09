# Copperline Project State

Last Updated: 2026-04-09
Version: v0.3

## What Copperline Is

Copperline is the live contractor-outreach system inside OfficeAutomation. It discovers local businesses, builds first-touch drafts, lets the operator repair and approve queue work, schedules eligible rows, and keeps send/reply state in sync.

## Current Repo Truth

- Queue/pipeline work is complete and stable — repair, approve, schedule, sent, and follow-up are all operational (passes 172–189)
- Command Center is the default landing tab
- Operations Theater surface is in active development — map-driven command center giving the operator spatial awareness over territory, leads, and pipeline state
- LOSI Theater visual prototype (standalone, pass 17 in Downloads) drives art direction for the map surface; not yet integrated into the repo
- Manual send discipline applies everywhere — no auto-send

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

## Where To Look Next

- `docs/CURRENT_BUILD.md` for current pass scope
- `docs/PROTECTED_SYSTEMS.md` for blast-radius rules
- `docs/CHANGELOG_AI.md` for pass history
