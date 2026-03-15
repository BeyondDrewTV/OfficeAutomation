# Protected Systems

The following components must not be modified casually or as part of routine
feature work. They require deliberate, isolated attention if a confirmed bug
needs fixing.

---

## Protected Files

| File | Reason |
|---|---|
| `lead_engine/run_lead_engine.py` | Core engine orchestration |
| `lead_engine/queue/pending_emails.csv` | Live email draft queue |
| Queue schema (field order and naming) | Downstream readers depend on column positions |
| Email sender module | Controls outbound communication |
| Follow-up scheduler | Manages timing of contact sequences |
| `safe_autopilot_eligible` logic | Guards against premature auto-send |
| Exception router | Routes failed jobs without data loss |

---

## Why These Are Protected

A prior repair script (`_repair_queue_csv.py`) caused significant queue data
loss by rewriting the CSV with incorrect schema assumptions. That event
established the protected status of these systems.

---

## Rules

1. Do not rewrite CSV pipeline logic without a full audit of downstream readers
2. Do not change queue schema (column names, order, or types) without updating
   all consumers simultaneously
3. Do not create new repair or migration scripts that write to `pending_emails.csv`
   or `prospects.csv` without operator review
4. Prefer adding new fields at the end of existing schema, never reordering
5. Treat all engine components as additive — extend, do not replace

---

## Safe Change Patterns

These are always safe:
- Frontend-only changes (`index.html` UI, CSS, JS behavior)
- New API endpoints that read data without mutating CSV files
- New documentation files
- New utility scripts that only read (not write) data

These require caution:
- Any Python script that opens and writes to `prospects.csv` or `pending_emails.csv`
- Changes to `dashboard_server.py` routes that trigger queue mutations
- Changes to `run_lead_engine.py` scheduling or state logic
