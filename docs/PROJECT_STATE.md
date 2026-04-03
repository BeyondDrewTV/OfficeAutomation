# Copperline Project State

Last Updated: 2026-04-02 (Pass 100–102)

## Copperline Version
v0.3

## Current Phase
Lead Acquisition + Conversion Delivery Engine

## Current Focus
Pass 103–105 in progress — Bulk-First Pipeline + Exception Queue

## Copperline Positioning
Copperline = One-on-one workflow consulting for small service business owners

## Last Completed Pass
Pass 100–102 -- Discovery Workflow Cohesion + Run Feedback: history always refreshes after discover; _shRerun race fixed; CC button async with loading state; grid sweep progress bar; exhaustive scan indeterminate animation; Cancel Sweep button; inline post-run results panel (_cdrShow); territory overlay dash patterns

## Recent Passes
Pass 100–102 milestone -- Discovery Workflow Cohesion + Run Feedback (frontend only)
Pass 97–99 milestone -- Discovery Throughput + History-to-Action Loop (frontend only)
Pass 94–96 milestone -- Discovery History recovery (DOM fix only)
Pass 93 -- Command Center UI/UX hierarchy polish (CSS only)
Pass 90–92 milestone -- Truth sync + Delivery nav fix + legacy DOM cleanup
Pass 89a -- CC blocking bug fix: discovery nav blank-page, mc-wrap layout compression, boot map init
Pass 88 -- Voice rules embedded + em dash enforcement (v20)
Pass 87 -- First-touch tightening: fixer/operator line enforcement, expanded bans, problem-labeled subjects, v19 draft version
Pass 86 -- Delivery Board: delivery_board endpoint, update_delivery_profile_by_key endpoint, board page with 3-column kanban (won/deployment_pending/live), readiness checklist per card, stage selector, auto-load on tab switch
Pass 85 -- Conversations: offer package menu, best-fit recommendation, lifecycle stage lane (discovered->live), deployment readiness checklist, durable save via lead_memory
Pass 84 -- Territory-to-queue scope: map selection scopes queue rail; scoped summary strip; ccCmdApproveScoped / ccCmdRegenScoped; bndSelectBoundary + bndClearBoundary hooks
Pass 83 -- CC layout QA: page containment fixed, map height/fill improved, panel narrowing, cmd bar density, queue rail copper hierarchy
Pass 82 -- Pipeline merged into Command Center: map-dominant layout, right queue rail, bottom command bar, CC default tab
Pass 81 -- Add Obs button now shows for fallback drafts; schedule block shows add obs CTA
Pass 80 -- lead_quality_score added to schema; CARTO voyager tiles; region outline-only w/ hover dash
Pass 76 -- Email search in pipeline + Ctrl+K global lead finder
Pass 75 -- Command Center: map + territory combined split-pane view
Pass 74 -- MX validation before send (prevents scrape-error bounces)
Pass 73 -- Follow-up voice rewrite (Drew tone, industry fallback path)
Pass 72 -- Territory button fix, stale warning suppressed for fallback drafts
Pass 71 -- Industry fallback drafts (17 trades mapped, no obs = no block)
Pass 70 -- Bulk regenerate: /api/bulk_regenerate + Regen Stale button
Pass 69 -- v18 voice: proper grammar, direct consequence, confident close
Pass 68 -- Auto-regen on panel open, panel layout overhaul, 22 industries

Protected systems are listed in `PROTECTED_SYSTEMS.md`. Do not duplicate that list here.

## Core Operator Workflow

1. Open Discovery -> Command Center
   - Left: map -- click county -> copper boundary, Search Territory runs tiled discovery
   - Right: territory panel -- city cards with per-industry status
   - Map click auto-selects city in territory panel + scopes queue rail to matching leads (Pass 84)
   - Territory run auto-refreshes map coverage overlay
   - Ctrl+K find-lead works from any tab

2. Pipeline -> Outreach
   - Search by name, email, phone, city in search box
   - Ctrl+K from anywhere for instant lead lookup by email
   - Stale leads auto-regen on panel open (obs -> draft silently)
   - No obs available -> industry fallback draft (22 trades)
   - Regen Stale button mass-refreshes all stale drafts

3. Review + Send
   - Panel: email body first, details collapsed below
   - Approve / Schedule / Send via Gmail
   - MX check blocks sends to scrape-error domains

4. Follow-Up
   - Touch 1: operational nudge (references specific observation)
   - Touch 2: timeline reframe (acknowledges time passed)
   - Touch 3: low-pressure closeout
   - Industry fallback path: no obs = industry-specific anchor phrase

5. Conversation -> Delivery Handoff (Pass 85)
   - Replied leads open in Conversations with operator notes + next step
   - Operator assigns one standard offer package (or uses best-fit recommendation)
   - Operator sets lifecycle stage (discovered -> drafted -> contacted -> replied -> call booked -> proposal ready -> won -> deployment pending -> live)
   - Operator tracks deployment checklist (intake, access, copy, routing, testing, live)
   - Metadata persists in durable lead_memory (no queue schema changes)

6. Delivery Board (Pass 86)
   - Dedicated Delivery tab in top nav
   - 3-column board: Won / Deployment Pending / Live
   - Each card shows: business name, city, package, readiness progress bar, per-item checklist
   - Readiness items: intake complete, vendor access, copy approved, routing logic, testing, live
   - Operator can tick checklist items inline (persists via update_delivery_profile_by_key)
   - Operator can move stage via dropdown on each card
   - Top stats strip: won / pending / live / fully ready counts
   - Board auto-loads when Delivery tab is clicked; manual Refresh button

## DRAFT_VERSION
Current: v20

## Industry List (22 total)
plumbing, hvac, electrical, roofing, construction, landscaping, painting,
tree_service, cleaning, auto, flooring, concrete, towing, appliance_repair,
pressure_washing, moving, drywall, welding, pool_service, pest_control,
locksmith, garage_door

## Territory Industries (15, priority order)
plumbing, hvac, electrical, roofing, construction, landscaping, painting,
tree_service, cleaning, auto, flooring, concrete, towing, appliance_repair,
pressure_washing

[2026-04-02] Session: Pass 100-102 — Discovery Workflow Cohesion + Run Feedback. History always refreshes after discover runs; _shRerun race fixed with polling check; last-updated timestamp added. CC Discover button async with loading state; grid sweep wired to progress bar; exhaustive scan gets indeterminate animation; visible Cancel Sweep button; map-status styled during active runs. Post-run drilldown panel (_cdrShow) appears inline after CC discover with lead summary. Territory overlay dash patterns; searched circle opacity reduced; legend labels legible. Next: commit Pass 100-102, then start Pass 103-105 (Bulk-First Pipeline + Exception Queue).

---
**Pass 100–102 — 2026-04-02 — Discovery workflow cohesion + run feedback**

What was done:
- `discoverLeads()`: removed conditional history refresh — `loadSearchHistory()` now always fires after any discover run regardless of active tab
- `_shRerun()`: replaced fixed 200ms setTimeout with a polling readiness check (`_attempt`, up to 650ms) that verifies CC form values are populated before firing `ccCmdDiscover()`
- Added `_shLastRefreshTime` + `_shRenderTimestamp()`: "Updated just now / Xs ago" timestamp in History header, auto-increments via `setInterval` every 10s
- `ccCmdDiscover()`: refactored to `async` with CC button loading state (`.loading` class + `disabled`) via try/finally
- Grid sweep: wired `_cmdProgressSet()` at each `callsDone++` for real progress bar fill; reset in finally
- Exhaustive scan: indeterminate animated progress bar via `#cmd-progress-fill.indeterminate` keyframe; `.running` class on `#map-status`; cleared in finally
- Added `#btnCancelGridVisible` (✕ Cancel Sweep) adjacent to `#map-status`; toggled by `_mapSetGridRunUi()`
- Added `_cdrShow()` + `#cc-discover-results`: lightweight inline post-run summary panel (business, website, status, score — max 20 rows, dismissible, no actions)
- Territory rect dash patterns: `worked` (4 3), `saturated` (6 3), `quiet` (3 5); `next` cells weight 2.5 solid
- Coverage circle `searched`: opacity 0.45→0.3, dashArray `4 4`
- Legend labels: `var(--text)`, dot 9px→11px with border-radius

Files touched: `lead_engine/dashboard_static/index.html`, `docs/PROJECT_STATE.md`

State after this pass: History updates immediately after every discover run; CC button shows loading state; grid sweeps show real progress fill; exhaustive scans show indeterminate animation; Cancel Sweep always visible during sweeps; lightweight results panel appears inline after CC discover; territory overlay cells differentiated by dash pattern.

Next: Pass 103–105 — Bulk-First Pipeline + Exception Queue
