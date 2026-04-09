# Copperline — Claude Startup Contract

Read this first. Then read PROJECT_STATE.md, CURRENT_BUILD.md, PROTECTED_SYSTEMS.md.

---

## Startup Read Order

1. This file (CLAUDE.md)
2. PROJECT_STATE.md -- live implementation truth
3. CURRENT_BUILD.md -- approved scope for this session
4. PROTECTED_SYSTEMS.md -- what must not be touched

Do not write code before completing this read order.

Reference only (not required startup reading):
- AI_CONTROL_PANEL.md -- pipeline-specific constraints and high-risk file list
- AI_DEV_STANDARDS.md -- engineering rules and pass discipline
- COPPERLINE_OVERVIEW.md -- durable system overview

---

## Blast-Radius Rules

Before editing any file, confirm:
- The file is listed in the approved pass scope (CURRENT_BUILD.md)
- The file is not in the protected list (PROTECTED_SYSTEMS.md)
- You have read the relevant section of the file you are editing

If any of these is not confirmed: stop and ask.

---

## Verification Expectations

For every behavior change:
- Restart the server after edits
- Hard-refresh the browser
- Confirm no JS console errors
- Confirm the specific changed behavior works
- State what was verified and what was not

For docs-only passes:
- Confirm this was docs-only in the pass report

---

## Protected System Handling

These are off-limits for casual edits:
- `lead_engine/run_lead_engine.py`
- `lead_engine/queue/pending_emails.csv` and queue schema
- Email sender module
- Follow-up scheduler core
- `safe_autopilot_eligible` logic

If a protected system is blocking the pass: stop, explain, get explicit approval before touching it.
Never bundle protected-system changes with feature passes.

---

## Anti-Scope-Creep Rules

- One goal per pass
- Minimal diff -- solve the stated problem only
- No "while I'm in here" changes to unrelated areas
- If a second goal appears mid-pass: stop, report it, do not act on it
- Do not refactor working systems unless they are directly blocking the current goal
- Do not clean up adjacent code, CSS, or functions that were not part of the pass goal

---

## Doc Update Policy

After every completed pass, update in this order:
1. PROJECT_STATE.md -- last completed pass, current focus
2. CURRENT_BUILD.md -- active pass status, what changed
3. AI_CONTROL_PANEL.md -- current state field
4. CHANGELOG_AI.md -- append new entry (never edit prior entries)

Update docs only when this pass materially changed truth.
Do not update docs to appear thorough.

---

## Pass Report Format

Every completed pass requires a report with:
1. Goal (one sentence)
2. Files inspected
3. Files changed (exact paths)
4. Exact changes (function names, before/after)
5. Why it is safe (no regression path)
6. Verification (what was checked)
7. Commit hash
8. Remaining risks

Optional at end if justified:
Tool/workflow opportunity (use the format in AI_DEV_STANDARDS.md)

---

## Epistemic Discipline

- Label uncertain findings as FACT / INFERENCE / UNKNOWN
- Do not claim repo behavior without reading the relevant file
- Do not present untested changes as verified
- If root cause is not confirmed, report findings instead of patching speculatively