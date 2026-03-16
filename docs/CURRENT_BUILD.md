# Current Build Pass

## Active System
Outreach Queue Safety + Scheduled Send Foundations

## Status
Pass 9b complete. All three commits verified and pushed.

---

## Completed: Step 2 — Marker Clustering — `38da7c3`
## Completed: Step 3 — Results Side Panel — `c0caa17`
## Completed: Step 4 — Map Result Usability Polish — `a19bc16`
## Completed: Step 5 — Discovery Coverage Memory — `f27a472`
## Completed: Step 6 — Discovery History List — `6d79c64`
## Completed: Step 7 — Human-Readable Discovery Labels — `3f86767`
## Completed: Step 8 — Search Visible Area Button — `32ff2bf`
## Completed: Step 8a — Decouple Search Visible Area Button — `651df94`
## Completed: Pass 9a — Queue Visual Safety — `f712909`

---

## Completed: Pass 9b — Scheduled Send Intent

Three commits. Protected systems modified deliberately (schema append only).
Scheduling is intent-only — writes `send_after` field, does NOT trigger send.

### Commit A — `24dc5b2`
Queue schema alignment + reply_checker truncation fix.

**Files changed:**
- `lead_engine/run_lead_engine.py` — appended `"send_after"` to `PENDING_COLUMNS`
- `lead_engine/dashboard_server.py` — appended `"send_after"` to `PENDING_COLUMNS`
- `lead_engine/send/email_sender_agent.py` — appended `"send_after"` to `PENDING_EMAIL_COLUMNS`
- `lead_engine/outreach/followup_scheduler.py` — appended `"send_after"` to `PENDING_COLUMNS`
- `lead_engine/outreach/reply_checker.py` — replaced truncated 20-col `PENDING_COLUMNS`
  with full 42-col schema matching all other queue readers/writers

**Verification (all passed):**
- All 5 modules: 42 columns, `send_after` last, first-41 col order preserved
- `pending_emails.csv` loads 174 rows cleanly, `send_after` defaults to `""`
- No existing column names changed or moved

### Commit B — `52dd64a`
`POST /api/schedule_email` route in `dashboard_server.py`.

**Validation chain:**
1. `index` must be present and an integer
2. `business_name` must be non-empty
3. `send_after` must be non-empty
4. Row `business_name` at `index` must match supplied name (index-drift guard, 409 on mismatch)
5. Index must be in bounds

**Action:** writes `rows[index]["send_after"] = send_after` via `_write_pending()`. No other fields touched. No send. No background work.

**Verification (all passed):**
- Route present, all rejection cases present
- No `sent_at`/`approved`/`replied` writes in route body
- No `process_pending_emails` or `_send_email_via_gmail` call in route body
- Uses existing `_write_pending` helper

### Commit C — `a5f09c5`
Dashboard schedule button in `index.html`.

**Changes:**
- `SEND_WINDOWS` const: maps `industry` → local morning send time (HH:MM)
- `panelScheduleTomorrow()`: computes `tomorrow YYYY-MM-DD + window time`, POSTs to
  `/api/schedule_email`, updates `row.send_after` in memory, calls `renderTable()` +
  `fillPanel()`, shows toast `Scheduled for tomorrow HH:MM`
- `#panel-schedule-btn` added to panel footer, using `.btn-secondary`
- `fillPanel` extended: button hidden when `row.sent_at` set; visible on unsent rows
- No send trigger, no Gmail launch, no auto-send

**Verification (all passed):**
- 19/19 static checks passed (SEND_WINDOWS, function, API call, row update, toast,
  button HTML, show/hide wiring, no-send guard, approve intact, save indicator intact)

---

## Notes on Protected System Changes

The audit (Pass 9b audit) revealed that `reply_checker.py` had a pre-existing
data-loss risk: its `PENDING_COLUMNS` was truncated to 20 fields, meaning
any write operation on a reply-matched row would strip 21 fields from that row.
This was fixed in Commit A as part of the atomic schema alignment.

All five `PENDING_COLUMNS` lists were updated in a single commit.
All use `csv.DictWriter(fieldnames=PENDING_COLUMNS)` — named access only.
No positional column indexing exists anywhere in the queue pipeline.

---

## Next: Pass 10 — TBD

Candidates:
- Territory heatmap overlay
- Industry saturation view
- Tiled backend improvements

Define scope before starting.
