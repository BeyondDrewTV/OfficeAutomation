# Follow-Up & Reminder Setup — Test Sequence
Version: v1 | Kit: follow_up_reminder_setup_v1

## Purpose
Run every active trigger and template through this sequence before handoff. Nothing goes live until all active templates pass. If a template fails, fix the issue and re-test before moving on.

---

## Pre-Test Setup

Before running any test:

- [ ] Test phone number and test email confirmed — no real client contact info used during testing
- [ ] Owner notified that tests are about to run
- [ ] Send platform is in test mode if available, or send path is set to test destination only
- [ ] Approved template pack is on hand — this is the source of truth for copy during testing

---

## Template Tests

Run each test for every active template. Skip rows for templates not in scope for this engagement.

---

### Template 1 — Estimate Follow-Up (Day 3)

| Step | Action | Result |
|---|---|---|
| 1 | Trigger the reminder manually or simulate the trigger condition | ☐ Triggered |
| 2 | Confirm message arrives at the correct test destination | ☐ Arrived  ☐ Did not arrive |
| 3 | Confirm copy matches approved template — no placeholder text remaining | ☐ Matches  ☐ Mismatch — fix before go-live |
| 4 | Confirm channel is correct (SMS / email / both) | ☐ Correct  ☐ Wrong channel |
| 5 | Confirm send-from identity is correct (owner's number/email, not Drew's) | ☐ Correct  ☐ Wrong sender |

**Template 1 result:** ☐ Pass  ☐ Fail — notes:

---

### Template 2 — Estimate Follow-Up (Day 7, Final)

| Step | Action | Result |
|---|---|---|
| 1 | Trigger the reminder manually or simulate the trigger condition | ☐ Triggered |
| 2 | Confirm message arrives at the correct test destination | ☐ Arrived  ☐ Did not arrive |
| 3 | Confirm copy matches approved template — no placeholder text remaining | ☐ Matches  ☐ Mismatch — fix before go-live |
| 4 | Confirm channel is correct | ☐ Correct  ☐ Wrong channel |
| 5 | Confirm send-from identity is correct | ☐ Correct  ☐ Wrong sender |

**Template 2 result:** ☐ Pass  ☐ Fail — notes:

---

### Template 3 — Post-Job Check-In

| Step | Action | Result |
|---|---|---|
| 1 | Trigger the reminder manually or simulate the trigger condition | ☐ Triggered |
| 2 | Confirm message arrives at the correct test destination | ☐ Arrived  ☐ Did not arrive |
| 3 | Confirm copy matches approved template — no placeholder text remaining | ☐ Matches  ☐ Mismatch — fix before go-live |
| 4 | Confirm channel is correct | ☐ Correct  ☐ Wrong channel |
| 5 | Confirm send-from identity is correct | ☐ Correct  ☐ Wrong sender |

**Template 3 result:** ☐ Pass  ☐ Fail — notes:

---

### Template 4 — Cold Lead Re-Engagement

| Step | Action | Result |
|---|---|---|
| 1 | Trigger the reminder manually or simulate the trigger condition | ☐ Triggered |
| 2 | Confirm message arrives at the correct test destination | ☐ Arrived  ☐ Did not arrive |
| 3 | Confirm copy matches approved template — no placeholder text remaining | ☐ Matches  ☐ Mismatch — fix before go-live |
| 4 | Confirm channel is correct | ☐ Correct  ☐ Wrong channel |
| 5 | Confirm send-from identity is correct | ☐ Correct  ☐ Wrong sender |

**Template 4 result:** ☐ Pass  ☐ Fail — notes:

---

### Template 5 — Appointment Reminder

| Step | Action | Result |
|---|---|---|
| 1 | Trigger the reminder manually or simulate the trigger condition | ☐ Triggered |
| 2 | Confirm message arrives at the correct test destination | ☐ Arrived  ☐ Did not arrive |
| 3 | Confirm copy matches approved template — no placeholder text remaining | ☐ Matches  ☐ Mismatch — fix before go-live |
| 4 | Confirm channel is correct | ☐ Correct  ☐ Wrong channel |
| 5 | Confirm send-from identity is correct | ☐ Correct  ☐ Wrong sender |

**Template 5 result:** ☐ Pass  ☐ Fail — notes:

---

### Additional Template (Owner-Defined)

| Step | Action | Result |
|---|---|---|
| 1 | Trigger the reminder manually or simulate the trigger condition | ☐ Triggered |
| 2 | Confirm message arrives at the correct test destination | ☐ Arrived  ☐ Did not arrive |
| 3 | Confirm copy matches approved template — no placeholder text remaining | ☐ Matches  ☐ Mismatch — fix before go-live |
| 4 | Confirm channel is correct | ☐ Correct  ☐ Wrong channel |
| 5 | Confirm send-from identity is correct | ☐ Correct  ☐ Wrong sender |

**Additional template result:** ☐ Pass  ☐ Fail  ☐ N/A — notes:

---

## Manual Process Only

If the setup is manual (no automation tool), confirm the following before handoff:

- [ ] Owner has the reference card with approved message copy and send instructions
- [ ] Owner can locate the correct template for each trigger without help
- [ ] Owner executed the first follow-up manually during the session (or in a dry run) and confirmed they can do it unassisted

---

## Summary Pass/Fail Table

| Template | In Scope? | Result |
|---|---|---|
| Estimate Follow-Up Day 3 | ☐ Yes  ☐ No | ☐ Pass  ☐ Fail  ☐ N/A |
| Estimate Follow-Up Day 7 | ☐ Yes  ☐ No | ☐ Pass  ☐ Fail  ☐ N/A |
| Post-Job Check-In | ☐ Yes  ☐ No | ☐ Pass  ☐ Fail  ☐ N/A |
| Cold Lead Re-Engagement | ☐ Yes  ☐ No | ☐ Pass  ☐ Fail  ☐ N/A |
| Appointment Reminder | ☐ Yes  ☐ No | ☐ Pass  ☐ Fail  ☐ N/A |
| Additional Template | ☐ Yes  ☐ No | ☐ Pass  ☐ Fail  ☐ N/A |

**Overall test result:** ☐ All active templates pass — cleared for handoff  ☐ Open failures — do not hand off

---

## Test Sign-Off

- Test sequence completed by Drew: [date]
- All active templates passed: ☐ Yes  ☐ No — open issues:
- Cleared for handoff: ☐ Yes  ☐ No
