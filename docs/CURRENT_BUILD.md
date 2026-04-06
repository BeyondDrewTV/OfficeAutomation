# Current Build Pass

Last Updated: 2026-04-05 (Queue / Pipeline redesign underway)

## Active Focus
Queue / Pipeline operator-workbench redesign

## Status
Pass 190–195 is complete, but it is no longer the active center of gravity.

## Current Repo Truth

- Out-of-band repo-truth hotfix, not a numbered pass: stranded-drafted recovery.
- Commit: `95c4b15890bc702394d5c02a0adab330671389fe`
- Files changed: `lead_engine/run_lead_engine.py`, `lead_engine/stranded_drafted.py`, `lead_engine/scripts/recover_stranded_drafted.py`
- Live audit result on current data: recoverable stranded `0`, already queued `274`, already sent `4`, excluded contactability `0`, drafted with no direct email `545`
- Known follow-up risk: `reset_queue_from_gmail.py` is still the prevention-side gap, and the queue still has `2` invalid emails plus `1` approved-without-email row outside this pass

## Archived: Pass 190–195

**Goal:** Make Follow-Up feel like a true operator-owned outcome surface — replied leads are visibly resolved, blocked rows have recovery paths, and exhausted rows are distinguished from actionable ones.

**Changes (frontend only — `lead_engine/dashboard_static/index.html`):**

- **Pass 190 — Reply continuity strip + toolbar nav:** `fqRender()` now computes `_replyNote` — when `_cvData.length > 0`, injects a green strip at top of `#fq-container`: "↩ N lead(s) replied — handed off to Conversations" with `"View →"` CTA calling `switchSubPage('pipeline','conversations',...)`. New `#fq-cv-nav-btn` button added to Follow-Up toolbar (always visible, green-tinted border): routes to Conversations and updates its label to show live count (`"💬 Conversations (N)"`) whenever `_cvData` is already loaded. Both are display/navigation only — no mutations.

- **Pass 191 — Blocked card recovery routing:** `_fqBestBtn()` blocked path (`followup_copy_ready === false`) now renders `"→ Fix in Outreach"` button (calls `fqOpenLead(idx)`) alongside existing Manual button. Replaces the inert amber "Needs context" text-only label. `fqOpenLead` navigates to the lead's panel in the Outreach sub-tab where the operator can add or strengthen an observation to unblock copy generation.

- **Pass 192 — Completed row distinction:** `_fqCard()` now checks `r.followup_status === 'completed'` and applies `.fq-dim` card class (dashed border, 60% opacity) to 3-touch-exhausted rows. `_fqBestBtn()` adds early guard: `if (!r.followup_touch_num)` → renders `"✓ 3-touch complete"` label + `"✕ Close"` button only, bypassing the misleading "Auto-send when due" label that previously appeared for these rows.

- **Pass 193–194 — Badge blocked count:** `fqRender()` now computes `blockedCount` client-side by scanning all follow-up rows for `followup_copy_ready === false`. Badge text upgraded to: `"N urgent · M total · P blocked"` when blocked rows exist; `"M due · P blocked"` when no urgent. Gives operator the outcome mix at a glance.

- **CSS:** `.fq-card.fq-dim{opacity:.6;border-style:dashed}` added after `.fq-card.fq-today` rule.

**Manual discipline:** `sendFollowup()` `confirm()` dialog intact. No code path triggers follow-up sends automatically. Reply note and Conversations button navigate only. `fqOpenLead()` navigates only — does not log or mutate.

**Files changed:** `lead_engine/dashboard_static/index.html`, `docs/`

**Protected-system status:** unchanged. No backend changes. No new API endpoints. No auto-follow-up introduced. No scheduler or sender touched.

## What Pass 166–171 Changed

**Goal:** Make approved review sessions behave like real Queue-owned sessions — track what happened (scheduled vs ready-now), show live progress, and give the operator clear post-session next steps.

**Changes (frontend only — `lead_engine/dashboard_static/index.html`):**

- **Pass 166 — `_qsScheduledKeys` + `outcomes.scheduled` + record functions:** New module-level `let _qsScheduledKeys = new Set()`. `_qsStart()` now initializes `outcomes: { repaired, blocked, scheduled: 0 }` and clears `_qsScheduledKeys`. New `_qsRecordScheduled(key)` — only fires during `cohortKey === 'approved'` sessions; idempotent (Set-guard prevents double-count on reschedule). New `_qsRecordUnscheduled(key)` — decrements only if key is tracked; handles mid-session schedule clears cleanly.

- **Pass 167 — `rowSchedule` / `rowUnschedule` hooks:** `rowSchedule` calls `_qsRecordScheduled` after successful API response. `rowUnschedule` calls `_qsRecordUnscheduled` before clearing `row.send_after`. Both no-op when not in an approved session.

- **Pass 168 — `panelScheduleTomorrow` / `panelUnschedule` / `panelReschedule` hooks:** `panelScheduleTomorrow` calls `_qsRecordScheduled` after `row.send_after = res.send_after`. `panelUnschedule` calls `_qsRecordUnscheduled` before clearing. `panelReschedule` calls `_qsRecordScheduled` (idempotent — reschedule of an already-tracked row is a no-op for the counter).

- **Pass 169 — Active banner live tally:** `_renderQueueSessionBanner` active state now computes `_liveScheduled = (qs.cohortKey === 'approved' && qs.outcomes?.scheduled > 0) ? ' · N scheduled' : ''`. Appended to the meta line alongside the existing `_liveOutcome` (repaired tally). Operator sees scheduling progress without opening any drawer.

- **Pass 170 — Done-state meaningful summary:** Done-state now branches on `qs.cohortKey`. For `'approved'`: computes `_scheduledInSession` + `_readyNow` (approved, unsent, unscheduled rows live in allRows). Renders `"N scheduled · M ready now"` or `"N rows reviewed · M ready now"`. `▶ Send Approved` shows live count `(M)`. If `_readyNow = 0` shows `"✓ All scheduled or sent"` instead of an unusable send button. For other cohort types: prior `repaired/blocked` logic unchanged.

- **Pass 171 — `_qsEnd()` restores send-ready strip:** When closing an approved session, `_qsEnd` now sets `_lastApprovedCount` from live allRows count (approved, unsent, with email). `_qsScheduledKeys` cleared. Since `_lastApprovedKeys` is empty (not restored), the send-ready strip reappears without a "→ Review" button — review is done. Non-approved session close behavior is unchanged.

**Files changed:** `lead_engine/dashboard_static/index.html`, docs

**Protected-system status:** unchanged. All schedule API calls route through existing `/api/schedule_email` endpoint. `confirmSend()` modal gate intact on all send paths. No auto-send introduced.

## What Pass 184–189 Changed

**Goal:** Make Follow-Ups feel like the next disciplined operator stage after send, with clear working-set continuity, clear due-vs-blocked state, and no auto-follow-up behavior.

**Changes (frontend only — `lead_engine/dashboard_static/index.html`):**

- **Pass 184 — Card "just sent" pill + `sent_at` meta + `fq-today` class fix:** `_fqCard(r)` now computes inline key `[business_name, city, state, website, to_email]` and checks against `_lastSentKeys` — if matched, renders a copper `↳ Just sent` pill next to the business name. `r.sent_at` rendered as `"sent X ago"` in the `.fq-meta` span line (gives timing context for the initial contact). Fixed bug: `fq-today` CSS class (defined but never applied) — now applied when `isToday === true`. `result.replace('_', ' ')` upgraded to `replace(/_/g,' ')` for multi-underscore results.

- **Pass 185 — Better blocked state visibility:** When `followup_copy_ready === false`, the blocked reason is now rendered as visible body text (not just a tooltip). `⚠ Blocked: {human-readable reason}` in amber, followed by first 120 chars of `followup_blocked_message` as a detail line. Reason codes mapped to human text: `weak_context` → "needs stronger context (obs or website)", `missing_anchor` → "no anchor phrase found", etc. `escHtml()` applied to both reason and message.

- **Pass 186 — `fqRender()` context note + richer badge:** When `_lastSentKeys.size > 0`, `fqRender()` scans all follow-up queue rows for key matches. If matches found: copper context note injected at top of `#fq-container` — "N row(s) from your recent send batch appear below — marked Just sent." If no matches (rows not yet follow-up eligible): blue note explaining the status. `#fq-total-badge` upgraded to show `"N urgent · M total"` with amber color when overdue+today > 0.

- **Pass 187 — `runFollowups()` inline result strip:** After running, `#fq-last-run` div (new DOM element, `display:none` by default) is shown with: green "✓ N drafts queued in Queue tab" or amber "⚠ N blocked for weak context" or muted "no drafts due yet". Shows timestamp. Blocked count also shown when both queued and blocked. Display-only — no mutations.

- **Pass 188 — `runFollowupsDryRun()` inline preview:** Dry-run result now shown in `#fq-last-run` inline (blue "🔍 Dry run preview" header, timestamp, up to 5 would-queue rows, up to 3 blocked rows with reason). Rows truncated with "N more — full list in console" note. `escHtml()` applied to all row data. `console.table` output preserved for full detail access.

- **Pass 189 — Docs truth-sync.**

**DOM change:** New `<div id="fq-last-run">` in `#page-followup` (after toolbar, before `#fq-container`), `display:none` by default.

**Files changed:** `lead_engine/dashboard_static/index.html`, docs

**Protected-system status:** unchanged. No backend changes. No new API endpoints. `sendFollowup()` `confirm()` dialog intact. No auto-follow-up introduced. All new UI elements are display-only.

## What Pass 178–183 Changed

**Goal:** Make freshly sent rows feel like a real Queue-adjacent working set with visible continuity into reply monitoring and follow-up readiness, without introducing auto-follow-up behavior.

**Changes (frontend only — `lead_engine/dashboard_static/index.html`):**

- **Pass 178 — `_lastSentKeys` foundation + `sendLive()` capture:** New module-level `let _lastSentKeys = new Set()`. `_qsStart()` clears it. In `sendLive()`: before the API call, snapshot `_preSendKeys` (approved + unsent + has email). On success with `s.sent > 0`: clear `_lastApprovedCount` and `_lastApprovedKeys` before `loadAll()` (clean banner render during reload); after `loadAll()`, verify which pre-send keys now have `sent_at` and persist as `_lastSentKeys`; call `_renderQueueSessionBanner()`. Backward-safe: if no rows sent, `_lastSentKeys` stays empty and no new strip appears.

- **Pass 179 — CSS + banner sent strip + `_qsDismissSent()`:** CSS `.qsb-sent` (green tint, green border — matches `.qsb-harvest` tone). Early-exit guard updated to include `!_lastSentKeys.size`. New banner state inserted after scheduled strip: `!qs && _lastSentKeys.size > 0` → green `qsb-sent` strip; live re-validates keys against allRows (`r.sent_at`); `→ Review (N)` CTA → `_startSentSession()`; `→ Follow-Ups` CTA → `switchSubPage('pipeline','followup',…)` (navigation only — no auto-generation); `✕ Dismiss` → `_qsDismissSent()`. `iconMap` gains `sent: '✉'`.

- **Pass 180 — `_startSentSession()` + `_qsDismissSent()`:** `_startSentSession()` sources rows from `_lastSentKeys`, filters to confirmed `sent_at` rows, opens as panel session with `cohortKey: 'sent'`. `_qsDismissSent()` clears `_lastSentKeys` only — does not touch any other state.

- **Pass 181 — `_queueTimelineNoteHtml()` sent filter case:** New `currentFilter === 'sent'` branch — tone `'info'`; shows sent count + replied count (copper-colored); directs operator to `🔁 Follow-Ups →` toolbar button. Approved session done-state now includes `_followupReadyBtn` when `_readyNow === 0` — `→ Follow-Ups` CTA (navigation only) surfaces when there's nothing left to send.

- **Pass 182 — State ordering final review.** Banner states are mutually exclusive and in priority order: hide → harvest → send-ready → scheduled → sent → qs done/active. Each strip uses `return`. Sent strip is last before the qs-branch — deliberate: it appears after the operator dismisses other strips, making the send→follow-up handoff the natural resting state after the full send flow completes.

- **Pass 183 — Docs truth-sync.**

**Files changed:** `lead_engine/dashboard_static/index.html`, docs

**Protected-system status:** unchanged. No backend changes. `confirmSend()` gate intact. No auto-send or auto-follow-up introduced. `_followupNavBtn` and `_followupReadyBtn` navigate only.

## What Pass 172–177 Changed

**Goal:** Make scheduled rows — especially those created during approved review work — feel like a real Queue-managed waiting set instead of a destination the operator has to hunt manually.

**Changes (frontend only — `lead_engine/dashboard_static/index.html`):**

- **Pass 172 — `_lastScheduledKeys` foundation:** New module-level `let _lastScheduledKeys = new Set()`. `_qsStart()` clears it (new session always resets). `_qsEnd()` persists `_qsScheduledKeys → _lastScheduledKeys` when closing an approved session with scheduled rows (`_qsScheduledKeys.size > 0`). New `_qsDismissScheduled()` clears `_lastScheduledKeys` and re-renders banner.

- **Pass 173 — Banner scheduled waiting strip + CSS:** Early-exit guard updated to include `!_lastScheduledKeys.size`. New 6th banner state: `!qs && _lastScheduledKeys.size > 0` → `qsb-scheduled` strip (blue tint). Shows live waiting count (re-checked against allRows to exclude rows already sent/cleared). `→ Review (N)` CTA calls `_startScheduledSession()`. Dismiss calls `_qsDismissScheduled()`. Send-ready strip (amber) extended with `· N scheduled` note in label when `_lastScheduledKeys.size > 0`. CSS `.qsb-scheduled` added (blue tint, blue border).

- **Pass 174 — `_startScheduledSession()` + timeline note CTA:** New `_startScheduledSession()` — collects all unsent scheduled rows from allRows, sorts by `send_after`, opens as panel session with `cohortKey: 'scheduled'`, label `Scheduled Review (N)`. `iconMap` gains `scheduled: '⏱'`. `_queueTimelineNoteHtml()` scheduled filter case now includes inline `→ Review (N)` CTA (same pattern as approved filter CTA).

- **Pass 175 — Scheduled stat in stats strip:** New `s-scheduled` stat element after `s-stale` — clickable (→ `setFilter('scheduled',…)`), blue color, label `Scheduled ↗`. New `_updateScheduledStat()` helper computes count client-side from `allRows` (backend has no scheduled count endpoint). Called from `loadStats()` and from `loadAll()` after `renderTable()`.

- **Pass 176 — Done-state "→ View Scheduled (N)":** Approved session done-state now includes `_viewScheduledBtn` when `_qsScheduledKeys.size > 0`. Button calls `_qsEnd()` then `setFilter('scheduled',…)` — closes session, persists `_lastScheduledKeys`, switches to scheduled filter. Renders before `▶ Send Approved` in the actions strip.

- **Pass 177 — Docs truth-sync.**

**Files changed:** `lead_engine/dashboard_static/index.html`, docs

**Protected-system status:** unchanged. No new API endpoints. `confirmSend()` gate intact. No auto-send introduced.

## What Pass 160–165 Changed

**Goal:** Make freshly approved rows actionable as a real working set from Queue — review, schedule, and send — without hunting through filters after approval work.

**Changes (frontend only — `lead_engine/dashboard_static/index.html`):**

- **Pass 160 — `_lastApprovedKeys`:** New module-level `Set`. Tracks keys of rows approved in the last batch action. Cleared by `_qsStart()` and `_qsDismissApproved()`. Populated by `_qsApproveRepaired()` (collects key per approved row) and `_cohortBulkApprove()` (same pattern).

- **Pass 161 — `_qsStartApprovedReview()`:** New function. Maps `_lastApprovedKeys` → allRows (filtered to unsent + has email). Calls `_qsStart('approved', rows, label)` + `openPanel(0, rows, label)`. Rows are snapshotted before `_qsStart` clears the Set — ordering is safe.

- **Pass 162 — Send-ready strip `→ Review (N)`:** `_renderQueueSessionBanner()` send-ready state now includes a `→ Review (N)` button (`.qsb-next`) calling `_qsStartApprovedReview()` when `_lastApprovedKeys.size > 0`. Positioned before `▶ Send Approved`. Operator can open the freshly-approved set as a session directly from the strip.

- **Pass 163 — `_startApprovedSession()` + approved filter CTA:** New `_startApprovedSession()` opens current `filteredRows` (approved filter view) as a panel session. `_queueTimelineNoteHtml()` approved filter case now includes an inline `→ Review (N)` button calling `_startApprovedSession()`. Mirrors the `→ Start Obs Review (N)` pattern for needs_obs.

- **Pass 164 — `_cohortBulkApprove()` feeds send-ready strip:** Previously, "✓ Approve All Ready" from the active view did not trigger the send-ready strip. Now sets `_lastApprovedCount` and `_lastApprovedKeys` after the loop, and calls `loadStats()`. Send-ready strip now appears after standalone bulk-approve.

- **Pass 165 — Banner polish for approved sessions:** `iconMap` gains `approved: '●'`. Done-state for `cohortKey === 'approved'` now includes `▶ Send Approved` button calling `confirmSend()` — completes the repair → approve → review/schedule → send loop at the banner level.

**Files changed:** `lead_engine/dashboard_static/index.html`, docs

**Protected-system status:** unchanged. `confirmSend()` routes through existing modal gate on all new send paths. No auto-send introduced.

## What Pass 154–159 Changed

**Goal:** Carry freshly approved work into the operator's next real outbound actions — review, schedule, and send readiness — without breaking manual-send discipline.

**Changes (frontend only — `lead_engine/dashboard_static/index.html`):**

- **Pass 154 — `_lastApprovedCount` + CSS:** New module-level `let _lastApprovedCount = 0`. Tracks rows approved in last batch action. CSS: `#queue-session-banner.qsb-send-ready` (amber-accent banner variant, distinct from copper active / green done+harvest).

- **Pass 155 — Session lifecycle hooks:** `_qsStart` clears `_lastApprovedCount = 0` on new session. `_qsApproveRepaired()` sets `_lastApprovedCount = approved` immediately before clearing harvest state — count is captured before any reset. New `_qsDismissApproved()` clears `_lastApprovedCount` and refreshes banner.

- **Pass 156 — Send-readiness banner state:** `_renderQueueSessionBanner()` now has five distinct states. Early-exit guard updated to include `!_lastApprovedCount`. Harvest strip condition tightened to `!qs && _lastRepairedKeys.size > 0` (was `!qs`). New fourth state `!qs && _lastApprovedCount > 0` renders amber `qsb-send-ready` strip: label "✓ N approved — ready to schedule or send", "▶ Send Approved (N)" button calling `confirmSend()` (existing confirmation modal — no auto-send), "✕ Dismiss". If all approved rows are already sent, shows "✓ All approved rows sent" in place of send button. States are mutually exclusive: harvest strip takes priority if `_lastRepairedKeys` is non-empty.

- **Pass 157 — Stats strip "Approved" clickable:** `<div class="stat">` wrapping the approved count now has `cursor:pointer`, `onclick="setFilter('approved', ...)"`, and a `title`. Label updated to "Approved ↗" to signal interactivity. Matches the existing pattern of "Replied" and "Stale Copy" clickable stats.

- **Pass 158 — `_queueTimelineNoteHtml` approved filter upgrade:** Computes live `approvedSendReady = allRows.filter(r => r.approved === 'true' && !r.sent_at && r.to_email).length`. Note now reads "Approved — N ready to send" with explicit guidance to schedule with 🕐 or use ▶ Send Approved.

- **Verifier fix — `if (!qs)` → `if (!qs && _lastRepairedKeys.size > 0)`:** Verifier caught that the original `if (!qs)` branch in `_renderQueueSessionBanner()` would intercept the send-ready state before it could render. Fixed by tightening the condition. Without this fix, the send-ready strip would never show.

**Files changed:** `lead_engine/dashboard_static/index.html`, docs

**Protected-system status:** unchanged. `confirmSend()` routes through the existing modal gate — no auto-send introduced.

## What Pass 148–153 Changed

**Goal:** Make recovered rows land clearly into ready-state and make that ready-state easy to act on from Queue — one flow from exception repair through graduation through approval.

**Changes (frontend only — `lead_engine/dashboard_static/index.html`):**

- **Pass 148 — `_lastRepairedKeys` + CSS:** New module-level `Set` that persists repaired row keys from a closed session. CSS: `#queue-session-banner.qsb-harvest` (green-tinted, distinct from copper active / green done-state) and `.qsb-approve` (green button).

- **Pass 149 — Session lifecycle hooks:** `_qsStart` clears `_lastRepairedKeys` on new session start. `_qsEnd` copies `_qsRepairedKeys → _lastRepairedKeys` before clearing, so repaired keys survive the session close.

- **Pass 150 — `_qsApproveRepaired()`:** New async function. Takes repaired keys from `_qsRepairedKeys` (session active/done) or `_lastRepairedKeys` (post-session). Iterates rows by key, calls `/api/approve_row` for each unapproved row with a valid email, mutates `row.approved = 'true'`. Clears all harvest state manually (bypasses `_qsEnd` so it does not re-snapshot). Calls `_renderQueueSessionBanner()`, `renderTable()`, `loadStats()`. Toasts count + skip count.

- **Pass 151 — Done-state banner: harvest action:** When `qs.outcomes.repaired > 0`, done-state banner shows `"✓ Approve N repaired"` as the first action button (`.qsb-approve` style). Operator can approve the full repaired set with one click without leaving Queue.

- **Pass 152 — Post-session harvest strip:** `_renderQueueSessionBanner()` now has a third render path: when `!_queueSession && _lastRepairedKeys.size > 0`, renders a harvest strip (`qsb-harvest` class) showing "N repaired rows are ready" with live `approveCount` (rows still unapproved, with email), "Approve N repaired" button, and "Dismiss" button. If all are already approved, shows "✓ All repaired rows approved" in place of the approve button. New `_qsDismissHarvest()` clears `_lastRepairedKeys` and refreshes banner + table.

- **Pass 153 — `renderTable` pill: post-session persistence:** Cohort pill check extended to also test `_lastRepairedKeys.has(_pillKey)` for `bulk_safe` rows. `cp-repaired` pill persists in the table after session close until next session start or dismiss — giving the operator a stable visual reference for rows just repaired.

**Files changed:** `lead_engine/dashboard_static/index.html`, docs

**Protected-system status:** unchanged.

## What Pass 142–147 Changed

**Goal:** Queue owns the recovery outcome, not just the repair action. Operators see what happened after exceptions are worked — how many rows graduated, how many are still blocked — both mid-session and in the done-state summary.

**Changes (frontend only — `lead_engine/dashboard_static/index.html`):**

- **Pass 142 — Outcome tracking foundation:** `_queueSession` now includes `outcomes: { repaired: 0, blocked: 0 }`. `_qsRepairedKeys = new Set()` (module-level) resets on each `_qsStart`. New `_qsRecordOutcome(key, type)` helper increments the counter, adds the key to `_qsRepairedKeys` when type is 'repaired', and refreshes the banner.

- **Pass 143 — `_rowSaveObsAndRegen` graduation toast:** After obs save + regen, computes `_pipelineCohort(row)` on the mutated row. If now `bulk_safe` → calls `_qsRecordOutcome(key, 'repaired')` and toasts "✓ [name] → Ready to Approve". Otherwise → 'blocked' outcome and retains informational toast.

- **Pass 144 — `_rowDirectRegen` graduation toast:** Same pattern — after draft fields are updated, re-evaluates cohort. Stale rows with an observation always graduate to `bulk_safe` after regen, so this path consistently shows "✓ [name] → Ready to Approve".

- **Pass 145 — Done-state banner outcome summary:** `_renderQueueSessionBanner` done-state now reads `qs.outcomes`. If any outcomes were recorded, shows "N repaired · M blocked" instead of generic "N rows in set". If no outcomes (e.g., session ended by navigation only), falls back to row count.

- **Pass 146 — Active-session banner live tally:** Mid-session banner appends " · N repaired" to the meta line whenever `qs.outcomes.repaired > 0`. Operator sees repair progress without opening any drawer.

- **Pass 147 — Repaired cohort pill:** `renderTable` cohort pill block checks `_qsRepairedKeys.has(_panelMakeKey(row))` for rows that are now `bulk_safe`. If matched, renders `<span class="cohort-pill cp-repaired">✓ repaired</span>` (green accent). CSS: `.cp-repaired { background:rgba(52,199,89,.12); color:var(--green); border:1px solid rgba(52,199,89,.2) }`.

**Files changed:** `lead_engine/dashboard_static/index.html`, docs

**Protected-system status:** unchanged.

## What Pass 136–141 Changed

**Goal:** Queue sessions survive normal operator movement. More exception repair happens inline. Session completion/position state stays accurate across all paths.

**Changes (frontend only — `lead_engine/dashboard_static/index.html`):**

- **Pass 136 — Stable `_panelMakeKey`:** Removed `row.subject` from the key. Key is now business_name + city + state + website + to_email only. Subject is mutable (changes after regen), so it was causing session-current highlight to break silently after any draft regeneration.

- **Pass 137 — `_panelAdvanceAfterAction` pos sync + reliable done-state:** After advancing via approve/schedule/skip, calls `_qsUpdatePos(nextIdx)` to keep `_queueSession.pos` accurate. Calls `_qsMarkDone()` when advancing past last row. Done-state banner now reads from `allRows` (not `filteredRows`) when counting next-cohort rows — correct regardless of which filter tab is active.

- **Pass 138 — `_rowDirectRegen` session advance:** After a successful inline regen, calls `_qsUpdatePos(nextPos)` or `_qsMarkDone()` so the session bookmark moves forward. Previously the banner stayed frozen at the same row after a repair.

- **Pass 139 — Outreach page hook:** `_runPageHooks('outreach')` now calls `_renderQueueSessionBanner()` + `renderTable()`. Returning from Social DMs or other sub-pages now refreshes the session banner correctly.

- **Pass 140 — Inline obs repair for `needs_obs` rows:** New `◎ Quick Obs` button on needs_obs row actions. Calls `_rowToggleInlineObs(gi)` which inserts an expandable `<tr class="inline-obs-row">` directly below the row with a textarea and Save + Regen / Cancel buttons. `_rowSaveObsAndRegen(gi)` saves obs via `/api/update_observation`, then regens via `/api/regenerate_draft`, advances the session, removes the inline form, and re-renders. No drawer required for standard obs work. CSS: `.inline-obs-row`, `.inline-obs-form`, `.inline-obs-textarea`, `.inline-obs-actions`, `.inline-obs-save`, `.inline-obs-cancel`.

- **Pass 141 — `_qsRefreshKeys` session reconciliation:** New function called in `loadAll()` after `allRows` is refreshed. Re-resolves each session row key against the fresh `allRows` by business_name+city+state identity, re-keys it with `_panelMakeKey`, prunes rows no longer in queue. Prevents session from going stale after a full reload while preserving position.

**Files changed:** `lead_engine/dashboard_static/index.html`, docs

**Protected-system status:** unchanged.

## What Pass 130–135 Changed

**Goal:** Queue becomes a disciplined working session surface. Cohort/session work is deliberate, progress is visible at table level, and exception cleanup has clear start/progress/complete states.

**Changes (frontend only — `lead_engine/dashboard_static/index.html`):**

- **Pass 130 — Queue session banner (CSS + DOM):** `#queue-session-banner` div inserted after mode bar, before stats strip. Shows session label, row N of M, remaining count, Resume and End buttons. Copper accent in active state; green accent in done state. CSS classes: `.qsb-label`, `.qsb-meta`, `.qsb-actions`, `.qsb-btn`, `.qsb-resume`, `.qsb-end`, `.qsb-next`.

- **Pass 131 — Session-current row highlight:** `renderTable()` computes `_sessionCurrentKey` (the row key at current session position). Matching row gets `.session-current` CSS class — subtle copper left-rail accent on the checkbox cell. Gives the operator a visual bookmark in the table when the drawer is closed.

- **Pass 132 — End-of-session signal:** `navigatePanel(dir)` now calls `_qsMarkDone()` when advancing past the last row in a scoped session. Banner transitions to green "✓ [Label] complete" state with next-cohort suggestion and Close button. Previously: silent failure at boundary.

- **Pass 133 — Cohort session labels with live counts:** `_cohortStartSession()` now generates labels like `"Obs Review (7)"`, `"Stale Review (3)"`, `"No-Email Review (5)"` instead of generic `"Review"`. Count reflects live row count at session start.

- **Pass 134 — Queue session persistence across close:** `closePanel()` saves `panelIdx` into `_queueSession.pos` before clearing panel state. `navigatePanel()` keeps `_queueSession.pos` in sync on every advance. Resume picks up where the operator left off.

- **Pass 135 — Session lifecycle API:** New global `_queueSession` (null when inactive). New functions: `_qsStart(cohortKey, rows, label)`, `_qsUpdatePos(pos)`, `_qsMarkDone()`, `_qsEnd()`, `_qsResume()`, `_renderQueueSessionBanner()`. `renderTable()` calls `_renderQueueSessionBanner()` on every render. Banner next-cohort suggestion picks the highest-priority cohort (needs_obs → stale → no_email) with live rows.

**Files changed:** `lead_engine/dashboard_static/index.html`, docs

**Protected-system status:** unchanged.

## What Pass 124–129 Changed

**Goal:** Queue becomes disciplined — every cohort row gets a consistent action pattern, blocker explanation, and next-step treatment. Drawer narrowed to deep review and manual recovery only.

**Changes (frontend only — `lead_engine/dashboard_static/index.html`):**
- Row action block replaced with cohort-aware `_rowActionHtml` switch:
  - `no_email` (Pass 124): Approve + Edit removed; `📲 Social →` as primary (calls `_setWorkbenchMode('social')`); dim `Review` opens drawer for inspection
  - `needs_obs` (Pass 125): generic Edit removed; obs-focused `openPanelForRefresh` button IS the drawer entry
  - `stale` (Pass 126): generic Edit removed; if obs exists → `↻ Regen` calls `_rowDirectRegen(gi)` directly; if no obs → `Add Obs` opens drawer focused; dim `Review` secondary
  - `bulk_safe` (Pass 127): `Edit` renamed to `Review` (dimmed, 10px) to signal depth not requirement; Approve remains primary
- Blocker banners upgraded (Pass 128): stale banner adds `↻ Regen now` button (calls `panelRegenerateDraft()`); no_email banner adds `📲 Social DMs →` button (calls `_setWorkbenchMode('social')` + `closePanel()`)
- New `_rowDirectRegen(gi)` function (Pass 129): fetches obs from row, calls `/api/regenerate_draft`, updates `row.subject/body/draft_version/dm_draft` in memory, calls `renderTable()` — no drawer required

**Files changed:** `lead_engine/dashboard_static/index.html`, docs

**Protected-system status:** unchanged.

## What Pass 118–123 Changed

**Goal:** All cohort exception paths Queue-native. Legacy surfaces visually demoted.

**Changes:**
- Stale CTA: dual buttons — bulk regen + scoped `→ Review Stale` session
- No-email CTA: dual buttons — scoped `→ Review No-Email` session + `📲 Social DMs →` mode switch
- Mode bar: `<span class="wb-mode-sep">` separator inserted between Email Queue and secondary tools; Social DMs + Focus Mode get `.wb-mode-tool` (0.7 opacity, 10px font) — demotion without deletion
- CSS: `.wb-mode-sep`, `.wb-mode-tool`, `.wb-mode-tool.active`, `.wb-mode-tool:hover`

**Files changed:** `lead_engine/dashboard_static/index.html`, docs

**Protected-system status:** unchanged.

## What Pass 112–117 Changed

**Goal:** Make Queue the real operating system — exception rows self-explanatory inline, needs_obs cohort actionable without drawer.

**Changes:**
- CSS: `.cohort-pill`, `.cp-needs-obs`, `.cp-stale`, `.cp-no-email` — per-row state badge styles
- `needs_obs` cohort CTA replaced: dim "open each row" text → `→ Start Obs Review (N)` button wired to `_cohortStartSession('needs_obs')`
- New `_cohortStartSession(cohortKey)`: filters `filteredRows` to the cohort, sets `panelOpenIntent='refresh'` for needs_obs, opens a scoped panel session via `openPanel(0, rows, label)`
- Per-row cohort pill computed in `renderTable`: `_rowCohort = !row.sent_at ? _pipelineCohort(row) : 'bulk_safe'`; injected into `td-biz` next to business name — visible in ALL filter views (active, pending, all, stale, etc.)
- Active filter timeline note updated: now explains cohort structure instead of generic "work you can handle right now"

**Files changed:** `lead_engine/dashboard_static/index.html`, docs

**Protected-system status:** unchanged.

## What Pass 106–111 Changed

**Goal:** Unify Social/Sprint/Outreach into one workbench surface; make the drawer exception-aware.

**Changes:**
- Social and Sprint nav tabs hidden (`display:none`); Outreach tab renamed to "Queue"
- Mode bar at top of page-outreach: Email Queue / Social DMs / Focus Mode buttons
- `_setWorkbenchMode(mode)`: switches sub-page via `switchSubPage()`, toggles active button
- "← Back to Queue" button on page-social and page-sprint
- `#panel-blocker` div in drawer: shows cohort-specific blocker banner for exception rows
- Blocker logic in `fillPanel()`: `needs_obs` → amber "Missing observation" + auto-sets panelOpenIntent; `stale` → blue "Stale draft"; `no_email` → dim "No email path"; `bulk_safe` → hidden
- CSS: `.wb-mode-bar`, `.wb-mode-btn`, `.panel-blocker`, `.wb-back-btn`

**Files changed:** `lead_engine/dashboard_static/index.html`, docs

**Protected-system status:** unchanged.

## What Pass 103–105 Changed

**Goal:** Make Actionable view bulk-first with cohort-based grouping.

**Changes:**
- `_pipelineCohort(row)`: classifies each actionable row into bulk_safe | needs_obs | stale | no_email
- `_cohortHeaderHtml(key, count)`: renders section header with count + scoped CTA per cohort
- `_cohortBulkApprove()`: approves all bulk_safe rows in one pass (no drawer required)
- `renderTable()`: when filter is 'active', stable-sorts filteredRows by cohort order then injects cohort header rows between groups
- CSS: `.cohort-hdr` row styling
- Shipped cohorts: Ready to Approve (✓ Approve All Ready), Needs Observation, Stale Draft (↻ Regen All Stale), No Email Path (→ Social Queue)
- All other filters, bulk actions, drawer, and send gates unchanged

**Files changed:** `lead_engine/dashboard_static/index.html`, docs

**Protected-system status:** unchanged.

## What Pass 97–99 Changed

**Goal:** Turn Search History into a real action surface. Fix re-run destination. Add load-without-rerun. Reduce column scan noise.

**Root cause fixed:** `_shRerun()` navigated to Outreach — wrong surface since CC became canonical in Pass 82.

**Changes:**
- Added `_shLoadCC(city, state, industry)`: fills CC command bar inputs, navigates to `command-center`. No search fires.
- Rewrote `_shRerun()`: calls `_shLoadCC()` then `ccCmdDiscover()` after 200ms delay. Lands on CC, not Outreach.
- Added "→ Load" button on each history row (calls `_shLoadCC`).
- Merged City + ST columns into "Location" (6 cols). Updated thead and all 4 colspan instances.

**Files changed:**
- `lead_engine/dashboard_static/index.html`
- `docs/PROJECT_STATE.md`, `docs/CURRENT_BUILD.md`, `docs/AI_CONTROL_PANEL.md`, `docs/CHANGELOG_AI.md`

**Protected-system status:** unchanged.

## Verification Completed
Pending live server verification — see live check below.

## Next Pass
TBD

---

## What Pass 94–96 Changed

**Goal:** Fix Discovery History blank sub-tab. Smallest correct structural fix only.

**Root cause:** `page-searches` was nested inside `page-command-center`. Activating the searches page removed `.active` from `page-command-center`, making it `display:none` and hiding its child regardless.

**Fix:**
- Moved `page-searches` DOM block to after `</div><!-- /page-command-center -->`
- No JS changes. No nav logic changes.
- Div balance verified: 767/767

**Files changed:**
- `lead_engine/dashboard_static/index.html`
- `docs/PROJECT_STATE.md`, `docs/CURRENT_BUILD.md`, `docs/AI_CONTROL_PANEL.md`, `docs/CHANGELOG_AI.md`

**Protected-system status:** unchanged.

## Verification Completed (Pass 94–96)
1. Server restarted; hard-refreshed
2. Command Center boots, map, territory panel, queue rail ✓
3. History tab: Search History renders (437 searches) ✓
4. Map+Territory returns after History ✓
5. Pipeline intact ✓
6. Zero JS console errors ✓

---

## What Pass 93 Changed

**Goal:** Improve Command Center UI/UX hierarchy — stronger panel zone framing, denser information layout, clearer operator command surface. No new features.

**Changes (frontend only — `lead_engine/dashboard_static/index.html`):**
- Copper divider bar: `2px / opacity:.7` → `3px / opacity:.85`
- `.nav-tab.active`: + copper background tint (`rgba(200,136,74,.06)`)
- `.cc-tp-header`: + `border-top:2px solid var(--copper)` — territory panel zone authority
- `.cc-tp-title`: `10px / muted` → `11px / var(--text)` — panel header legible
- `.cc-tp-stat strong`: `600` → `700 / 12px / mono` — territory stats numbers dominant
- `.cc-tp-pane` border-left: `var(--border)` → `var(--border-hi)` — clearer zone separation
- `.cc-qr-stat-n`: `16px` → `18px`; `.cc-qr-stat-l`: `8px` → `9px`
- `.stat` pipeline padding: `16px 24px` → `12px 20px` — denser stat strip
- `.tp-progress-bar`: `80px / 6px` → `88px / 7px`
- `.ftab.active`: + inset shadow for depth
- `.cc-cmd-bar` border-top: copper tint (`rgba(184,115,51,.2)`)
- `.db-stat-n`: `22px / 600` → `24px / 700`
- Delivery board column top accents: `#db-col-won` amber, `#db-col-deployment_pending` blue, `#db-col-live` green

**Files changed:**
- `lead_engine/dashboard_static/index.html`
- `docs/PROJECT_STATE.md`, `docs/CURRENT_BUILD.md`, `docs/AI_CONTROL_PANEL.md`, `docs/CHANGELOG_AI.md`

**Protected-system status:** unchanged. No backend, queue, scheduler, send-path, or autopilot changes.

## Verification Completed
1. Server restarted; hard-refreshed
2. CC boots, map loads, territory panel loads, queue rail loads ✓
3. Pipeline stat strip denser, table intact ✓
4. Delivery empty state correct, active tab tint visible ✓
5. Zero JS console errors ✓
6. DOM inspect: `cc-tp-header` border-top `2px solid copper` ✓; queue stat `18px/700/DM Mono` ✓

## Next Pass
TBD

---

## What This Milestone Changed (Pass 90–92)

**Goal:** Bring repo into truth alignment. Fix Delivery blank-page. Remove legacy DOM debt.

**Files changed:**
- `docs/AI_CONTROL_PANEL.md` — updated last completed pass, current focus
- `docs/PROJECT_STATE.md` — DRAFT_VERSION v18 → v20, last completed pass updated, Pass 88 added to recent passes
- `docs/CURRENT_BUILD.md` — active pass and status updated; stale "Next Pass: Pass 86" footer removed
- `docs/CHANGELOG_AI.md` — milestone entry appended
- `lead_engine/dashboard_static/index.html`:
  - `_parentDefaults` and `_parentLastPage`: added `delivery: 'delivery-board'`
  - Removed: empty `page-cities` stub (was "kept for JS compat" — verified not activated by any live nav path)
  - Removed: empty `page-map` stub (same; empty div, never activated)
  - Removed: hidden `mc-wrap` legacy territory planner block (tp-*, cp-* IDs duplicated live in CC right pane)
  - Removed: second hidden `page-map` block (all IDs duplicated in live CC — bnd-*, cmd-*, map-*, mrp-*, btn* etc.)

**Protected-system status:** unchanged. No backend, queue, scheduler, send-path, or autopilot changes.

## Next Pass
TBD

---

## What Pass 85 Builds
- Conversations panel now includes an operator-visible Offer + Deployment Readiness block
- Fixed package menu (5 standard Copperline offers):
  - Missed Call Recovery
  - Lead Intake + Routing
  - Follow-Up Reactivation
  - Review Request System
  - Estimate / Job Status Communication
- Deterministic best-fit recommendation (operator can accept or override)
- Lifecycle handoff stage selector:
  discovered -> drafted -> contacted -> replied -> call booked -> proposal ready -> won -> deployment pending -> live
- Deployment checklist:
  intake complete, phone/vendor access collected, copy approved, routing logic defined, testing complete, live
- New API endpoint: `POST /api/update_delivery_profile` (lead-memory only; no queue mutation)
- `GET /api/conversation_queue` now returns normalized `delivery_profile` for replied leads
- Durable storage in `lead_engine/data/lead_memory.json` via new `lead_memory` helper functions

**Files changed:**
- `lead_engine/dashboard_static/index.html`
- `lead_engine/dashboard_server.py`
- `lead_engine/lead_memory.py`

**Protected-system status:** unchanged. No edits to queue schema, sender core, scheduler core, or run orchestrator.

## Verification Completed
1. `python -m py_compile lead_engine/lead_memory.py lead_engine/dashboard_server.py`
2. JS parse check of `lead_engine/dashboard_static/index.html` script block via Node `vm.Script`
3. Flask test client check:
   - `GET /api/conversation_queue` returns 200
   - `POST /api/update_delivery_profile` accepts valid payload and returns normalized profile

---

## Pass 83 -- CC Layout QA (complete)
- Page containment: `#page-command-center.active` height-constrained
- `cc-wrap` height: `100%` (inherits constrained parent)
- Duplicate `#map-layout` rules consolidated
- `cc-map-pane` padding reduced; `min-width:500px` added
- Territory pane: 300px -> 260px; queue rail: 300px -> 280px
- cmd-bar CC override: padding tightened
- `map-page-wrap` made flex column in CC context
- Queue rail: stat numbers 13px -> 16px; copper top accent + title
- Row padding: 7px -> 6px; cc-qrow-bot margin 3px -> 2px

---

## Pass 82 -- Command Center unified layout (complete)
- CC is default landing tab
- Map-dominant layout, right queue rail, persistent bottom command bar
- ccQueueRender / ccQueueFilter / ccQueueUpdateStats / ccQueueOpenRow
- ccCmdDiscover wired to Pipeline discovery
- Full View button preserves Pipeline access

---
