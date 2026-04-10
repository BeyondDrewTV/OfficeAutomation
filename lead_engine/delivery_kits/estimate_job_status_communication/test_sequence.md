# Estimate & Job Status Communication — Test Sequence
Version: v1 | Kit: estimate_job_status_communication_v1

## Purpose
Test every active status stage before handing off to the owner. A stage does not pass until the notification arrives at the correct destination with the correct copy. Do not hand off until all active stages pass.

**Run this test against the owner's test phone/email — not a real client.**

---

## Pre-Test Setup

Complete all items before running stage tests.

- [ ] Status map worksheet is signed off and on file
- [ ] All active-stage message templates have owner approval
- [ ] Access checklist is complete — send path access confirmed
- [ ] Send-from identity is configured (correct name, number, email)
- [ ] Owner's test phone number confirmed and ready to receive messages
- [ ] Owner's test email confirmed and ready (if email channel is active)
- [ ] Owner is available during this test window: [date/time: ____________]

**Do not start stage tests until all pre-test items are checked.**

---

## Stage Tests

Run one test per active stage. Check off only when the notification arrives and all three verification points pass.

---

### Stage 1 — Estimate Sent

- [ ] Trigger the notification manually (simulate sending an estimate)
- [ ] Notification arrives at: ☐ Test phone (SMS)  ☐ Test email  ☐ Both
- [ ] Copy matches the approved template — no placeholder text remaining
- [ ] Send-from identity is correct (owner's name, number/email — not Drew's)
- [ ] Timing is correct: ☐ Immediate  ☐ Within agreed window

**Result:** ☐ Pass  ☐ Fail — Issue: ___________________

---

### Stage 2 — Estimate Approved / Booking Confirmed

- [ ] Trigger the notification manually (simulate client approval)
- [ ] Notification arrives at: ☐ Test phone (SMS)  ☐ Test email  ☐ Both
- [ ] Copy matches the approved template — date/time field formatted correctly
- [ ] Send-from identity is correct
- [ ] Timing is correct

**Result:** ☐ Pass  ☐ Fail — Issue: ___________________

---

### Stage 3 — Job Scheduled (Day-Before Reminder)

- [ ] Trigger the notification manually (simulate day-before reminder)
- [ ] Notification arrives at: ☐ Test phone (SMS)  ☐ Test email  ☐ Both
- [ ] Copy matches the approved template — arrival window is clear
- [ ] Send-from identity is correct
- [ ] Timing is correct: ☐ 24 hours before  ☐ Morning of

**Result:** ☐ Pass  ☐ Fail — Issue: ___________________

---

### Stage 4 — Job Started

- [ ] Trigger the notification manually (simulate job start)
- [ ] Notification arrives at: ☐ Test phone (SMS)  ☐ Test email  ☐ Both
- [ ] Copy matches the approved template
- [ ] Send-from identity is correct

**Result:** ☐ Pass  ☐ Fail — Issue: ___________________

---

### Stage 5 — Job Completed

- [ ] Trigger the notification manually (simulate job completion)
- [ ] Notification arrives at: ☐ Test phone (SMS)  ☐ Test email  ☐ Both
- [ ] Copy matches the approved template — review link present and working (if included)
- [ ] Send-from identity is correct

**Result:** ☐ Pass  ☐ Fail — Issue: ___________________

---

### Stage 6 — Invoice Sent

- [ ] Trigger the notification manually (simulate invoice send)
- [ ] Notification arrives at: ☐ Test phone (SMS)  ☐ Test email  ☐ Both
- [ ] Copy matches the approved template — payment instructions are correct
- [ ] Send-from identity is correct

**Result:** ☐ Pass  ☐ Fail — Issue: ___________________

---

### Stage 7 — Payment Received (Optional)

- [ ] Trigger the notification manually (simulate payment confirmation)
- [ ] Notification arrives at: ☐ Test phone (SMS)  ☐ Test email  ☐ Both
- [ ] Copy matches the approved template
- [ ] Send-from identity is correct

**Result:** ☐ Pass  ☐ Fail — Issue: ___________________

---

### Additional Stage: ___________________ (If Added)

- [ ] Trigger the notification manually
- [ ] Notification arrives at: ☐ Test phone (SMS)  ☐ Test email  ☐ Both
- [ ] Copy matches the approved template
- [ ] Send-from identity is correct

**Result:** ☐ Pass  ☐ Fail — Issue: ___________________

---

## Summary Pass/Fail Table

Fill in after running all active stage tests.

| Stage | Active? | Result | Issue (if any) |
|---|---|---|---|
| Estimate Sent | ☐ Yes  ☐ No | ☐ Pass  ☐ Fail  ☐ N/A | |
| Estimate Approved / Booking Confirmed | ☐ Yes  ☐ No | ☐ Pass  ☐ Fail  ☐ N/A | |
| Job Scheduled (Day-Before Reminder) | ☐ Yes  ☐ No | ☐ Pass  ☐ Fail  ☐ N/A | |
| Job Started | ☐ Yes  ☐ No | ☐ Pass  ☐ Fail  ☐ N/A | |
| Job Completed | ☐ Yes  ☐ No | ☐ Pass  ☐ Fail  ☐ N/A | |
| Invoice Sent | ☐ Yes  ☐ No | ☐ Pass  ☐ Fail  ☐ N/A | |
| Payment Received | ☐ Yes  ☐ No | ☐ Pass  ☐ Fail  ☐ N/A | |
| Additional Stage | ☐ Yes  ☐ No | ☐ Pass  ☐ Fail  ☐ N/A | |

**Overall result:** ☐ All active stages pass — cleared for handoff  ☐ Open issues — do not hand off

---

## Test Sign-Off

Handoff does not proceed until all active stages pass.

- Test completed by Drew: [date]
- Owner present during test: ☐ Yes  ☐ No
- All active stages passed: ☐ Yes  ☐ No — open issues:
- Cleared for handoff: ☐ Yes  ☐ No
