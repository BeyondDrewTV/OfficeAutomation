# Current Build

Last Updated: 2026-04-10

## Active Focus

Outbound email sender identity is being migrated to the official Google Workspace sender `drewyomantas@copperlineops.com`, with SMTP config centralized and live sends gated by explicit operator env setup.

The selected send path is Google Workspace SMTP, not Gmail API, because current repo truth already sends through Gmail SMTP/IMAP and has no OAuth provider abstraction. Live send requires `COPPERLINE_LIVE_SEND_ENABLED=true`; safe verification starts with the dashboard **More -> Preview Send** dry run.

Delivery now bridges run-level evidence back into offer-level hardening truth through an offer evidence ledger and promotion-readiness visibility layer.

The current milestone adds a read-only offer evidence summary derived from Delivery Run data, hardening-card evidence visibility, and advisory promotion-readiness readouts. No offer status is promoted automatically.

Prelaunch hardening OS — public delivery-kit coverage is now complete for all atomic offers.

The queue/pipeline work is complete (passes 172–189). All public offers now have real kit files on disk. No offer is delivery-proven yet.

## Completed This Session

### Workspace Sender Migration (this pass)
- Centralized Copperline outbound sender identity in `lead_engine/send/mail_config.py`: from email, display name, reply-to, provider, SMTP login, and live-send mode.
- Kept the current repo-truth SMTP architecture and migrated it to Google Workspace SMTP rather than introducing OAuth/Gmail API without an existing integration layer.
- First-touch sends, scheduled sends, follow-up sends, reply checking, and sent reconciliation now use the same mail config.
- Dashboard status now shows active sender identity and live/test mode; live sends are blocked until `COPPERLINE_LIVE_SEND_ENABLED=true`.
- `.env.example`, README, and operator docs now list the Workspace SMTP variables and safe dry-run verification path.
- No real outbound email was sent during verification.

### Offer Evidence Ledger + Promotion-Readiness Visibility (this pass)
- Added a read-only **offer evidence aggregation layer** derived from `lead_engine/data/delivery_execution_log.json`: total runs, closeout captured count, review-ready count, reviewed-complete count, reviewed-insufficient count, proof coverage, blocker presence, last run, last evidence run, and last reviewed run.
- Added `/api/delivery_offer_evidence` plus catalog enrichment in `/api/delivery_catalog`, so Hardening Command can read offer-level evidence truth without adding a new persistence layer.
- Hardening Command cards now show an **Offer evidence ledger** block: reviewed-complete runs, closeout-captured runs, review-ready runs, proof coverage, last evidence/reviewed run, and advisory promotion readiness.
- Promotion readiness is now operator-visible only: `No reviewed runs yet`, `Evidence captured, waiting for manual review`, `Reviewed evidence exists, but proof incomplete`, `Reviewed evidence exists, criteria partially supported`, or `Ready for human verification decision`.
- Hardening evidence links back to the actual run and the Manual Review queue. No offer is auto-promoted to `verification`, `ready`, or `launch_eligible = true`.
- No sender, scheduler, queue schema, follow-up automation, CRM/project system, invoicing, auto-send, fake verification automation, or automatic catalog promotion changes.

### Closeout Packet + Manual Verification Review (this pass)
- Delivery Run now generates a copy-ready **Owner Closeout Packet** from the selected client run: business, offer, delivery/closeout dates, completed checklist items, proof refs, artifact refs, owner acknowledgment state, remaining recommendations, blockers, and Drew/Copperline footer.
- Delivery Run now stores run-level manual review state: `not_ready`, `ready_for_manual_review`, `reviewed_insufficient`, and `reviewed_complete`, plus manual review notes.
- Delivery now has a **Manual Review** subtab that lists delivery runs with closeout status, proof presence, artifact refs, blocker state, owner acknowledgment, review status, and an Open Run action.
- `/api/delivery_review_queue` reads the delivery execution log and returns run-level review candidates without changing catalog-level `build_status`, `launch_eligible`, or verification state.
- No sender, scheduler, queue, PDF, invoice, contract, payment, auto-send, automatic project creation, or automatic offer promotion changes.

### Accepted Option -> Activation Kickoff (prior pass)
- Deploy Activation Step 3 now has **Accepted Option** controls: selected proposal option, draft/leaning/accepted status, acceptance date, acceptance note, accepted scope note, and owner constraints / assumptions.
- `Create Activation Scope` turns the accepted option's real Copperline offer keys into the active delivery stack: core offer, bundle, selected modules, price note when blank, offer notes, packet status, next step, and `stage = won`.
- Step 4, Step 5, and Step 6 now show accepted-option context so the chosen scope carries through confirm, packet, and action surfaces.
- Step 6 adds manual kickoff actions for using accepted scope and opening the client-bound Delivery Run for the accepted offer.
- Delivery Board rows now show the accepted option label and accepted scope note when present.
- `accepted_option_*`, `accepted_scope_note`, and `accepted_assumptions` now normalize through `/api/deploy_activation` on the delivery profile.
- No sender, scheduler, queue, PDF, invoice, contract, payment, auto-send, or fake verification changes. No offer status promoted.

### Recommendation + Simple Proposal Handoff (prior pass)
- Deploy Activation Step 3 now has **Simple Options**: editable option cards with option label, included real Copperline offer keys, price note, scope note, recommended toggle, and assumptions.
- Added `Build From Recommendation` to turn the current recommendation + Quick Wins into a recommended option, smaller first step, and optional add-on/stretch placeholder for manual follow-up.
- Step 6 Consultation Leave-Behind now includes the simple options section, price notes, and next-step CTA.
- `proposal_options` now saves through `/api/deploy_activation` on the delivery profile.
- Fixed Quick-Win persistence truth: `consult_builder.quick_wins` is now preserved by the server normalizer instead of being stripped on save/load.
- No sender, scheduler, queue, PDF, invoice, contract, or delivery verification changes. No offer status promoted.

### Quick-Win Review System + Consultation Leave-Behind (prior pass)
- **Quick Wins capture** added to Deploy Activation Step 2 (Discovery) — structured 6-field cards: category, what I noticed, why it matters, quick win, priority (Now/Soon/Later), mapped offer, easy-fix flag
- **11 starter templates** seeded in `QW_TEMPLATES` covering: Presence Refresh (GBP hours, description, FB photo, review responses), Website (missing site, no phone CTA), Missed Call Recovery, Lead & Contact Setup, Review Request System, Estimate & Job Status Communication, Follow-Up & Reminder Setup — all tied to real Copperline offers
- **Leave-Behind output** added to Step 6 (Action) — "📄 Preview Leave-Behind" / "📋 Copy" buttons generate a plain-text consultation summary: business name + date header, numbered quick wins with all fields, recommended next steps from Step 3, quoted price if entered
- **State integration**: `quick_wins` is now preserved through `/api/deploy_activation`; this pass fixed the server normalizer so Step 2 Quick Wins are durable.
- Re-render is comparison-gated — auto-save does not destroy textarea focus while operator is typing

### Client-bound Delivery Run — execution identity + MCR checklist (prior pass)
- **Missed Call Recovery** now has a real 3-section delivery checklist in `DR_CHECKLISTS`: Setup (5 items), Testing (5 items), Handoff (3 items) — 13 items total. MCR is the only `launch_eligible=true` offer; it now has a runnable operator checklist.
- **Presence Refresh** checklist updated: added "Before-state captured" as first item in each section (GBP + Facebook), ensuring proof capture is part of the checklist flow. Now 11 GBP + 10 Facebook = **21 items total**.
- `delivery_execution_log.json` migrated from old bare-key format (`"presence_refresh"`) to `run_key` format (`"practice|presence_refresh"`) with explicit `lead_key` + `offer_key` fields.

### Delivery Run infrastructure (prior pass — confirmed operational)
- Added **📋 Delivery Run** sub-tab and page to the Delivery section
- Client selector (`#dr-client-select`) pulls from `/api/delivery_run_clients` — shows clients with a `delivery_profile.stage` set, grouped by stage
- Offer selector groups by client stack vs. all other offers
- `run_key = lead_key|offer_key` — different clients' runs do not overwrite each other
- `drOpenForClient(leadKey, offerKey)` — deep-link from Delivery Board or other surfaces
- Proof & Artifacts: before-proof, after-proof, artifact refs, work notes, blockers
- Closeout section: closeout status (open/in_progress/captured), owner ack, closeout notes, post-closeout notes
- **7-item verification-readiness rail**: kit files on disk → client bound → checklist progress → proof captured → closeout captured → blockers → manual review required
- Context chip shows business name, stage, offer label, run key
- Auto-save on input (800ms debounce); explicit Save button also available
- State persisted to `data/delivery_execution_log.json` via `GET/POST /api/delivery_run`

### Full public delivery-kit coverage milestone
- **Follow-Up & Reminder Setup**: cadence worksheet, message template pack, access checklist, test sequence, handoff closeout — 5 files, `hardening`
- **Review Request System**: review setup worksheet, review copy library, access checklist, QA checklist, handoff closeout — 5 files, `hardening`
- **Basic Cleanup** (bundle): scope matrix, activation checklist, closeout template — 3 files, advanced `planned` → `hardening`
- **Presence + Website** (bundle): intake worksheet, dependency checklist, combined go-live checklist, bundle closeout template — 4 files, advanced `planned` → `hardening`
- **Full Starter Package** (bundle): master intake worksheet, dependency sequencing checklist — 2 files, advanced `planned` → `hardening` (missing_qa and missing_closeout intentionally kept until bundle is delivery-proven)
- `delivery_kits.py` updated for all 5: `artifact_files`, `promotion_criteria`, cleared `missing_*` where real files now exist

### Previously hardened (prior passes)
- **Lead & Contact Setup**: 5 files, `hardening`
- **Presence Refresh**: 5 files, `hardening`
- **Starter Website**: 5 files, `hardening`
- **Estimate & Job Status Communication**: 5 files, `hardening`
- **Client Approval / Estimate Portal**: 5 files, `hardening`

### Deploy Activation — 6-step wizard (prior pass)
- Replaced long-scroll Deploy Activation page with a guided 6-step wizard
- Steps: Snapshot → Discovery → Recommend → Confirm → Packet → Action
- Persistent summary panel (right column / below on mobile)
- Progress bar is clickable; Back/Next navigation on each step

## Public Catalog State

| Status | Count |
|---|---|
| Ready | 1 (Missed Call Recovery only) |
| Hardening | 10 |
| Verification | 0 |
| Planned | 0 |

## Current Baseline

- Operations theater map-driven redesign: `95a6c01`
- Command center operations theater prototype: `710bf2a`
- Queue surface stable baseline: `bc0ef15`

## LOSI Theater Prototype (External)

- Current state: pass 17 (`losi_prototype_v2_pass17.html`)
- Completed: SVG glyph hierarchy, hub compass-rose, Loop nucleus, zone fills
- Next gap: lead-count pip labels on node glyphs
- Integration: not yet merged — pending prototype maturity

## Do Not Widen Into

- Email sender or queue schema rewrites
- Protected system changes (see `docs/PROTECTED_SYSTEMS.md`)
- Auto-send or scheduling logic changes
- Promoting any kit to `ready` or `launch_eligible = true` without a real delivered closeout on file
- Building "real" approval portal web apps or CRM systems — the approval portal is link/form based only

## Verification Standard

- Frontend-only changes: check locally in the browser, confirm no console errors
- Queue truth, send truth, schedule truth: require live verification before sign-off
- No real email sends during verification
- If a pass touches `dashboard_server.py` or `email_sender_agent.py`, verify real queue behavior before sign-off

## Historical Baseline

Queue pipeline completion baseline (passes 172–189): `b6a54f53334e28bf74398b71b0c0cef9ade8cafa`
Pass history: `docs/CHANGELOG_AI.md`
