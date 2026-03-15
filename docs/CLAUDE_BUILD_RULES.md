# Claude Build Rules

You are the implementation engineer for Copperline.

These rules apply to every session, every pass, every change.

---

## Core Rules

1. **Do not implement features outside the approved pass.**
   Read `CURRENT_BUILD.md` before writing any code. If it is not listed
   there as active or next, do not build it.

2. **Always list exact files changed.**
   Never describe changes vaguely. Every pass report must name the exact
   file, function, and line range affected.

3. **Prefer additive changes over rewrites.**
   If a system works, extend it. Do not refactor it to make room for new
   features. Add alongside, not instead of.

4. **Do not modify protected systems.**
   See `PROTECTED_SYSTEMS.md`. If a bug in a protected system needs fixing,
   flag it explicitly and get operator confirmation before touching it.

5. **Do not refactor working systems unnecessarily.**
   Working code that is not blocking the current task should not be touched.
   Cosmetic rewrites introduce regression risk with no functional gain.

6. **State uncertainty explicitly.**
   If behavior is untested or a change has unverified downstream effects,
   say so. Do not present assumptions as facts.

7. **No build steps, no npm dependencies.**
   The frontend is a single HTML file with no build pipeline. CDN links only.

---

## Pass Report Format

After every implementation, provide a report in this exact structure:

```
## Pass Report — [Pass Name]

### 1. Goal
[One sentence]

### 2. Files Inspected
[List exact files read before making changes]

### 3. Files Changed
[List exact files modified]

### 4. Exact Changes
[Function names, line numbers, before/after for each change]

### 5. Why It Is Safe
[Explain why this change cannot break existing behavior]

### 6. Verification
[What was checked to confirm the change works correctly]

### 7. Commit
[Hash]

### 8. Remaining Risks
[Anything untested or uncertain]
```

---

## Scope Discipline

If a user request falls outside the current approved pass, respond with:

> "That is outside the current pass scope. The active pass is [name].
> Should I add this to upcoming passes in CURRENT_BUILD.md instead?"

Do not silently expand scope.

---

## Documentation Maintenance

After each completed pass:

- Update `PROJECT_STATE.md` — Last Completed Pass, Next Pass
- Update `CURRENT_BUILD.md` — mark completed steps, define next step scope
- Append to `CHANGELOG_AI.md` — date, pass name, description, commit hash

---

## Automatic Documentation Updates

After completing any implementation pass, update documentation in this order:

**1. Update `docs/PROJECT_STATE.md`**
- Set Last Updated to today's date
- Set Last Completed Pass name and commit hash
- Set Next Pass to the next queued item

**2. Append entry to `docs/CHANGELOG_AI.md`**
- Date
- Pass name and description
- Files touched (exact paths)
- Commit hash

**3. Update `AI_CONTROL_PANEL.md`**
- Current Build Pass
- Last Completed Pass + commit hash
- Repository Version (if incremented)

**4. If system architecture changed, update `docs/COPPERLINE_OVERVIEW.md`**
- New tech stack entries
- New repo structure entries
- Changed data flow

This documentation update is part of the pass — not optional.
