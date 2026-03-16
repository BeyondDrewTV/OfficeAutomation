# Current Build Pass

## Active System
Outreach Queue Safety + Scheduled Send Foundations

## Status
Pass 9a complete. Pass 9b blocked pending protected-system approval.

---

## Completed: Step 2 — Marker Clustering — `38da7c3`
## Completed: Step 3 — Results Side Panel — `c0caa17`
## Completed: Step 4 — Map Result Usability Polish — `a19bc16`
## Completed: Step 5 — Discovery Coverage Memory — `f27a472`
## Completed: Step 6 — Discovery History List — `6d79c64`
## Completed: Step 7 — Human-Readable Discovery Labels — `3f86767`
## Completed: Step 8 — Search Visible Area Button — `32ff2bf`
## Completed: Step 8a — Decouple Search Visible Area Button — `651df94`

---

## Completed: Pass 9a — Queue Visual Safety — `f712909`

Frontend-only. No backend changes. No protected systems touched.

**CSS added (lines ~235–241):**
- `.badge-scheduled` — amber pill, matches `.badge-stale` styling
- `tbody tr.row-scheduled td:first-child` — amber left border on scheduled rows
- `.panel-save-state` + `.saving` / `.saved` / `.save-err` state variants

**`statusBadge(row)` extended:**
New priority slot between stale and approved:
```
if (row.send_after && !row.sent_at)
  → '🕐 Scheduled' badge with send_after timestamp as tooltip
```

**Filter tab added:**
`🕐 Scheduled` tab appended after `High Score` in outreach toolbar.
`applyFiltersAndSort()` handles `currentFilter === 'scheduled'`
  → `rows.filter(r => r.send_after && !r.sent_at)`

**`renderTable()` extended:**
`scheduledClass` variable added alongside `sentClass`/`repliedClass`.
Applied to `<tr class="...">` template string.

**`panelFieldChanged()` extended:**
Body edits now drive `#panel-save-state` indicator:
- On keystroke → `Saving…` (amber)
- On API `.then()` → `Saved ✓` (green)
- On API `.catch()` → `Error saving` (red)
Subject/email edits unaffected (silent save, same as before).

---

## Blocked: Pass 9b — Schedule Action

**Blocker:** `_write_pending_rows()` in `run_lead_engine.py` serializes the
CSV using only `PENDING_COLUMNS`. A `send_after` field written by any new
API route will be silently stripped the next time the engine runs.

**Required before Pass 9b can proceed:**
Operator must explicitly approve adding `send_after` to `PENDING_COLUMNS`
in `run_lead_engine.py`. This is a protected-system change.

**Pass 9b scope (ready to build once unblocked):**
- Add `send_after` to `PENDING_COLUMNS` in `run_lead_engine.py`
- Add `SEND_WINDOWS` const to `index.html` (industry → morning send time)
- Add "Schedule for Tomorrow" button in review panel
- Add `/api/schedule_email` route to `dashboard_server.py`
  - Validates row by index + `business_name` match
  - Writes `send_after` only, touches no other fields
  - Does not trigger any send

---

## Upcoming Passes

| Pass | Description | Status |
|---|---|---|
| Pass 9b | Schedule Action | Blocked — needs PENDING_COLUMNS approval |
| Pass 10 | Territory heatmap overlay | Not yet scoped |
| Pass 11 | Industry saturation view | Not yet scoped |
