# Copperline Delivery Kits

Copperline is in explicit prelaunch hardening mode.

- `prelaunch_mode = true`
- public offers tracked by `build_status`
- `launch_eligible` is the launch gate
- internal items stay internal
- target state never overrides current truth

## Runtime Model

Each offer or module carries:

- `offer_type`: `public` or `internal`
- `build_status`: `planned`, `hardening`, `verification`, or `ready`
- `launch_eligible`: `true` only when the real kit is hardened and delivery-proven
- `current_truth_note`
- `target_truth_note`
- `artifact_files`: real files on disk (path keyed by artifact name)
- `promotion_criteria`: what must be true before advancing to next status
- `missing_artifacts` / `missing_qa` / `missing_closeout` / `missing_rollback`
- `next_hardening_step`

## Current Repo Truth

| Offer / Module | Offer Type | Build Status | Launch Eligible | Kit Files on Disk | Current Truth |
|---|---|---|---|---|---|
| Presence Refresh | public | hardening | false | 5 files | Asset request, access checklist, cleanup checklist, QA checklist, closeout snapshot — not yet delivery-proven. |
| Lead & Contact Setup | public | hardening | false | 5 files | Intake/routing worksheet, access checklist, notification template, routing test script, handoff closeout — not yet delivery-proven. |
| Starter Website | public | hardening | false | 5 files | Content intake, asset checklist, domain/hosting decision, publish checklist, handoff closeout — not yet delivery-proven. |
| Basic Cleanup | public | hardening | false | 3 files | Scope matrix, activation checklist, closeout template — bundle docs exist. Depends on Presence Refresh delivery-proven. |
| Presence + Website | public | hardening | false | 4 files | Bundle intake worksheet, dependency checklist, combined go-live checklist, bundle closeout template — component kits on disk, not delivery-proven. |
| Full Starter Package | public | hardening | false | 2 files | Master intake worksheet, dependency sequencing checklist — bundle partially hardened. Missing bundle QA sequence and handoff packet. |
| Missed Call Recovery | public | ready | true | (existing code + setup guide) | Real multi-client product with code, onboarding, pricing, and rollback path. Launch benchmark. |
| Follow-Up & Reminder Setup | public | hardening | false | 5 files | Cadence worksheet, message template pack, access checklist, test sequence, handoff closeout — client-service setup kit, not internal Copperline logic. Not yet delivery-proven. |
| Review Request System | public | hardening | false | 5 files | Review setup worksheet, copy library, access checklist, QA checklist, handoff closeout — not yet delivery-proven. |
| Estimate & Job Status Communication | public | hardening | false | 5 files | Status map worksheet, message template pack, access checklist, test sequence, handoff closeout — not yet delivery-proven. |
| Client Approval / Estimate Portal | public | hardening | false | 5 files | Approval flow worksheet, estimate page template, access checklist, QA checklist, closeout/rollback — not yet delivery-proven. |
| Mobile Admin / owner workflow helper | internal | hardening | false | 0 files | Internal-only operator tooling. Never a public sellable item. |

## Kit Files on Disk

### Lead & Contact Setup (`lead_engine/delivery_kits/lead_contact_setup/`)

| File | Purpose |
|---|---|
| `intake_routing_worksheet.md` | Intake/routing map, scope ceiling, and access confirmation — fill during or after consult |
| `access_checklist.md` | Every access item required before setup begins, by active channel |
| `notification_preference_template.md` | Owner notification settings capture and copy approval |
| `routing_test_script.md` | Step-by-step test of all active channels — must pass before handoff |
| `handoff_closeout.md` | Final deliverable to owner — what was set up, how to manage it, how to pause it |

### Presence Refresh (`lead_engine/delivery_kits/presence_refresh/`)

| File | Purpose |
|---|---|
| `asset_request_template.md` | Client asset request — send before starting; work begins only after required assets received |
| `access_checklist.md` | GBP and Facebook access confirmation before any platform edits |
| `presence_cleanup_checklist.md` | Step-by-step work checklist — GBP, Facebook, cross-platform consistency |
| `presence_qa_checklist.md` | Operator signoff QA — run after cleanup, before handoff |
| `closeout_snapshot_template.md` | Before/after audit trail — the delivery record for each engagement |

## Kit Files on Disk — Starter Website (`lead_engine/delivery_kits/starter_website/`)

| File | Purpose |
|---|---|
| `content_intake_form.md` | 7-section form for collecting all site content before building — must be complete before build starts |
| `asset_checklist.md` | Logo, photos, domain access, hosting access, contact form destination — gates the build |
| `domain_hosting_decision.md` | 4-decision worksheet (domain, hosting, contact route, DNS) — nothing deploys until all 4 resolved |
| `publish_checklist.md` | 4-stage sequential checklist from finished build to live site — pre-publish, DNS/HTTPS, post-launch, confirmation |
| `handoff_closeout.md` | Owner-facing closeout: what was built, how to manage it, revision boundary, support options, domain renewal |

## Promotion Criteria

### Presence Refresh (hardening → verification)
- Kit used on at least one real client delivery
- All checklist items completed without gaps
- Closeout snapshot on file for the delivery
- No open issues in the QA log

### Lead & Contact Setup (hardening → verification)
- Kit used on at least one real client delivery
- All routing test script channels passed
- Handoff closeout issued and on file
- No open issues in the test log

### Starter Website (hardening → verification)
- Kit used on at least one real client delivery
- Site published and live at client URL
- Contact CTA tested and working
- Publish checklist completed and on file
- Handoff closeout issued and owner acknowledged

### Estimate & Job Status Communication (hardening → verification)
- Kit used on at least one real client delivery
- All active status stages tested and passed
- Owner approved all message copy before go-live
- Handoff closeout issued and on file
- No open issues in the test log

### Client Approval / Estimate Portal (hardening → verification)
- Kit used on at least one real approval flow
- Client responded via the correct approval path
- Drew notification received correctly
- Deactivation/expiry path confirmed after approval
- Closeout log entry on file

### Follow-Up & Reminder Setup (hardening → verification)
- Kit used on at least one real client delivery
- Cadence and all active reminder triggers tested and passed
- Owner approved all message copy before go-live
- Handoff closeout issued and on file
- No open issues in the test log

### Review Request System (hardening → verification)
- Kit used on at least one real client delivery
- Test review request completed and delivered correctly
- Owner approved copy before go-live
- Handoff closeout issued and on file
- No open issues in the QA log

### Basic Cleanup (hardening → verification)
- Presence Refresh component kit delivery-proven
- Bundle used on at least one real Basic Cleanup engagement
- Scope stayed within defined ceiling
- Closeout template filled and on file

### Presence + Website (hardening → verification)
- Both component kits (Presence Refresh, Starter Website) delivery-proven
- Bundle used on at least one real combined engagement
- Combined go-live checklist completed without gaps
- Bundle closeout template filled and delivered to owner

### Full Starter Package (hardening → verification)
- All three component kits (Presence Refresh, Starter Website, Lead & Contact Setup) delivery-proven
- Bundle used on at least one real full-starter engagement
- All three delivery phases complete in sequence
- One master handoff delivered to owner
- Cross-channel QA passed

## Kit Files on Disk — Estimate & Job Status Communication (`lead_engine/delivery_kits/estimate_job_status_communication/`)

| File | Purpose |
|---|---|
| `status_map_worksheet.md` | Per-engagement status stage map — owner defines which stages are active, how each is triggered, and message direction |
| `message_template_pack.md` | Draft templates for all 7 status stages — owner reviews and approves each before go-live |
| `access_checklist.md` | Send platform, send-from identity, test destinations, existing tool audit — gates setup |
| `test_sequence.md` | Per-stage trigger/arrival/copy/timing checks — all active stages must pass before handoff |
| `handoff_closeout.md` | What was set up, how owner triggers each notification, safe-pause procedure, revision boundary |

## Kit Files on Disk — Client Approval / Estimate Portal (`lead_engine/delivery_kits/client_approval_estimate_portal/`)

| File | Purpose |
|---|---|
| `approval_flow_worksheet.md` | Per-engagement: client identity, what's being approved, format choice (PDF/Form/HTML), response method, deactivation path |
| `estimate_page_template.md` | Reusable estimate/approval presentation template with filled plumbing example |
| `access_checklist.md` | Client contact, estimate readiness gate, notification destination, delivery path, test verification |
| `qa_verification_checklist.md` | Mobile accessibility, content accuracy, response path, approval window, deactivation, data exposure |
| `closeout_and_rollback.md` | Post-approval steps, format-specific deactivation, change order path, client handoff message, closeout log |

## Kit Files on Disk — Follow-Up & Reminder Setup (`lead_engine/delivery_kits/follow_up_reminder_setup/`)

| File | Purpose |
|---|---|
| `cadence_worksheet.md` | Per-engagement cadence definition — owner sets active reminder stages, timing, and trigger method |
| `message_template_pack.md` | Draft templates for all reminder stages — owner reviews and approves each before go-live |
| `access_checklist.md` | Send platform, send-from identity, test destinations, existing tool audit — gates setup |
| `test_sequence.md` | Per-stage trigger/arrival/copy/timing checks — all active reminder stages must pass before handoff |
| `handoff_closeout.md` | What was set up, how owner manages reminders, safe-pause procedure, revision boundary |

## Kit Files on Disk — Review Request System (`lead_engine/delivery_kits/review_request_system/`)

| File | Purpose |
|---|---|
| `review_setup_worksheet.md` | Per-engagement: client type, trigger rule choice, review link destination, timing, and opt-out path |
| `review_copy_library.md` | Approved request message variations — owner reviews and approves before any send |
| `access_checklist.md` | Send path access, review profile link, test destination, existing review tool audit |
| `qa_checklist.md` | Trigger test, copy verification, link destination check, pause path confirmation |
| `handoff_closeout.md` | What was set up, how owner triggers review requests, pause procedure, revision boundary |

## Kit Files on Disk — Basic Cleanup (bundle) (`lead_engine/delivery_kits/basic_cleanup/`)

| File | Purpose |
|---|---|
| `bundle_scope_matrix.md` | Defines which Presence Refresh items are in-scope for the narrower Basic Cleanup ceiling |
| `activation_checklist.md` | Bundle-level gate checks before starting work — component readiness, access, asset confirmation |
| `closeout_template.md` | Simplified closeout for the bundle delivery — what was done, what wasn't, handoff summary |

## Kit Files on Disk — Presence + Website (bundle) (`lead_engine/delivery_kits/presence_website/`)

| File | Purpose |
|---|---|
| `bundle_intake_worksheet.md` | Combined intake for both components — presence assets, website content, access, timeline |
| `dependency_checklist.md` | Gate check: confirms each component's requirements are met before starting |
| `combined_go_live_checklist.md` | Sequential go-live checklist — presence then website, cross-channel consistency check |
| `bundle_closeout_template.md` | One combined owner-facing closeout covering both components |

## Kit Files on Disk — Full Starter Package (bundle) (`lead_engine/delivery_kits/full_starter_package/`)

| File | Purpose |
|---|---|
| `master_intake_worksheet.md` | Combined intake for all three components — presence, website, lead/contact setup |
| `dependency_sequencing_checklist.md` | Confirms all three component kits are ready and sequences the delivery order |

## Internal Flow

The internal operator workflow is:

1. Hardening Command
2. Consult Builder (Step 1–2 of wizard: Snapshot + Discovery)
3. Draft Recommendation (Step 3: Recommend)
4. Activation Packet Prefill (Steps 4–5: Confirm + Packet)
5. Deploy (Step 6: Action)
