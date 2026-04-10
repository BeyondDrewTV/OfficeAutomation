# Lead & Contact Setup — Routing Test Script
Version: v1 | Kit: lead_contact_setup_v1

## Purpose
Verify every active intake path end-to-end before handoff. A channel is not confirmed working until this script passes for that channel.

**Rule: Do not hand off until every active channel reaches ☐ Pass. Any Fail blocks closeout.**

---

## Pre-Test Setup

- ☐ Use a test phone number not associated with a real client
- ☐ Use a test email address not associated with a real client
- ☐ Notify owner in advance — they will see test alerts arrive
- ☐ Confirm test logging destination is separate from production log (or clearly mark test rows)
- ☐ Plan to delete or mark all test records after verification

---

## Test Sequence

### Test 1 — Phone / Missed Call (if in scope)

| Step | Action | Expected Result | Result |
|---|---|---|---|
| 1.1 | Call the business number from the test phone. Do not answer. | Call goes to voicemail or triggers missed-call path | ☐ Pass  ☐ Fail |
| 1.2 | Wait for the auto-response window | Auto-text sent to the test phone within agreed time | ☐ Pass  ☐ Fail |
| 1.3 | Check the owner notification destination | Owner notification received with correct format | ☐ Pass  ☐ Fail |
| 1.4 | Check the lead log | Test lead row logged with name / phone / time / source | ☐ Pass  ☐ Fail |
| 1.5 | Verify auto-response copy | Matches approved copy from notification template | ☐ Pass  ☐ Fail |

Notes on failures:

### Test 2 — Contact Form / Email (if in scope)

| Step | Action | Expected Result | Result |
|---|---|---|---|
| 2.1 | Submit a test inquiry via the website form or send a test email | Submission received at routing destination | ☐ Pass  ☐ Fail |
| 2.2 | Check for auto-reply to sender | Auto-reply received at test address (if configured) | ☐ Pass  ☐ Fail |
| 2.3 | Check the owner notification destination | Owner notification received with correct format | ☐ Pass  ☐ Fail |
| 2.4 | Check the lead log | Test lead row logged correctly | ☐ Pass  ☐ Fail |

Notes on failures:

### Test 3 — Follow-Up Path (if in scope)

| Step | Action | Expected Result | Result |
|---|---|---|---|
| 3.1 | Confirm the follow-up trigger timing is set | Timing matches the agreed schedule from the worksheet | ☐ Pass  ☐ Fail |
| 3.2 | Simulate a no-response lead and wait or force-trigger the follow-up | First follow-up fires at the correct time | ☐ Pass  ☐ Fail |
| 3.3 | Check the follow-up message | Matches approved copy, sent to the correct destination | ☐ Pass  ☐ Fail |

Notes on failures:

### Test 4 — Owner Notification Final Check

| Step | Action | Expected Result | Result |
|---|---|---|---|
| 4.1 | Confirm notification arrived at the confirmed destination | Delivered to correct phone / email | ☐ Pass  ☐ Fail |
| 4.2 | Confirm format matches the approved preference | Short SMS or email detail, as agreed | ☐ Pass  ☐ Fail |
| 4.3 | Confirm timing matches the agreed setting | Immediate or batched, as agreed | ☐ Pass  ☐ Fail |

Notes on failures:

---

## Test Summary

| Channel | Result | Notes |
|---|---|---|
| Phone / missed call | ☐ Pass  ☐ Fail  ☐ N/A | |
| Contact form / email | ☐ Pass  ☐ Fail  ☐ N/A | |
| Follow-up path | ☐ Pass  ☐ Fail  ☐ N/A | |
| Owner notification | ☐ Pass  ☐ Fail  ☐ N/A | |

---

## Test Sign-Off

- Tested by Drew: [date]
- All active channels passed: ☐ Yes  ☐ No
- Open failures resolved before handoff: ☐ Yes  ☐ N/A
- Ready for handoff: ☐ Yes — proceed to `handoff_closeout.md`
