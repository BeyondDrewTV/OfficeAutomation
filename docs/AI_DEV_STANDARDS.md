# AI Development Standards

Copperline follows structured AI-assisted development practices.
These standards govern how every AI session interacts with this repository.

---

## Core Principles

1. **Small incremental passes**
   Each session implements one clearly scoped feature. No multi-feature
   commits. No scope creep. One pass, one commit, one report.

2. **Additive architecture**
   Extend working systems rather than replacing them. New behavior is layered
   on top of existing behavior. Working code is not refactored unless it is
   directly blocking the current pass.

3. **Protected system boundaries**
   Core engine files are off-limits for casual modification. See
   `PROTECTED_SYSTEMS.md`. Changes to protected systems require explicit
   operator approval and an isolated commit.

4. **Commit-linked documentation**
   Every completed pass is documented with its commit hash in `CHANGELOG_AI.md`
   and `PROJECT_STATE.md`. Documentation that cannot be traced to a commit is
   unreliable.

5. **Pass reports after every change**
   No implementation is complete without a structured pass report. The report
   must include: goal, files inspected, files changed, exact code changes,
   safety justification, verification steps, commit hash, and remaining risks.

6. **Repository self-documentation**
   The repository docs must always reflect actual project state — not aspirational
   or stale state. After each pass, update `PROJECT_STATE.md`, `CURRENT_BUILD.md`,
   `CHANGELOG_AI.md`, and `AI_CONTROL_PANEL.md`.

7. **Minimal context loading**
   AI sessions should be able to orient from 3–4 short files. The documentation
   system is designed to fit full project context under ~1,000 tokens. Keep
   docs files concise and current.

---

## What AI Assistants Must Not Do

- Guess project goals — always read the docs first
- Implement features not listed in `CURRENT_BUILD.md`
- Modify protected systems without operator approval
- Make large rewrites of working systems
- Leave changes uncommitted at the end of a session
- Make ambiguous commits like "fix bug" or "update files"
- Present untested behavior as verified

---

## Session Startup Checklist

Before writing any code, an AI session must:

- [ ] Read `AI_CONTROL_PANEL.md`
- [ ] Read `docs/PROJECT_STATE.md`
- [ ] Read `docs/CURRENT_BUILD.md`
- [ ] Confirm the pass scope is understood
- [ ] Confirm no protected systems are in scope

---

## File Naming Conventions

- Documentation files: `UPPER_SNAKE_CASE.md`
- Python modules: `lower_snake_case.py`
- Frontend: single `index.html` — no additional frontend files without approval
- No new directories without pass documentation explaining why

---

## Versioning Policy

`PROJECT_STATE.md` tracks a `Copperline Version` field.

Increment only when:
- A new major subsystem is added
- Discovery architecture changes significantly
- Outreach system is restructured
- Deployment infrastructure is introduced

Patch-level changes (UI fixes, clustering, panel additions) do not increment version.
