# Copperline Project State

Last Updated: 2026-04-01 (Pass 89a)

## Copperline Version
v0.3

## Current Phase
Lead Acquisition + Conversion Delivery Engine

## Current Focus
First-touch drafting tightened — service-first fixer/operator positioning, earlier value prop, DRAFT_VERSION v19

## Copperline Positioning
Copperline = One-on-one workflow consulting for small service business owners

## Last Completed Pass
Pass 93 -- Command Center UI/UX Hierarchy Polish: 14 CSS/HTML changes to index.html — copper top-border on territory panel header, brighter panel titles, denser pipeline stat strip, larger queue rail stats, stronger zone borders, delivery column accents, active tab tint, copper cmd-bar accent

## Recent Passes
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
