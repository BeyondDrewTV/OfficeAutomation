# Review Request System — QA Checklist
Version: v1 | Kit: review_request_system_v1

## Purpose
Run this checklist before sending any review request to a real client. Every item must pass. If anything fails, fix it before going live.

A broken link or wrong copy sent to a real client cannot be recalled and directly harms the owner's credibility.

---

## QA Checks

### Review Link Integrity

- [ ] Google Business Profile review link opens the correct GBP listing from a phone browser (not just a desktop)
- [ ] GBP review link from a phone browser goes directly to the review prompt — not to the general GBP page
- [ ] If email channel is in scope: GBP review link is not broken or altered by the email client — tested on a real phone email app
- [ ] Facebook review link resolves to the correct Facebook page (if in scope)
- [ ] No untested review link has been inserted into any approved template

---

### Test Request

- [ ] Test review request sent to owner's own phone or email (not a real client)
- [ ] Test request arrived — not filtered to spam or blocked
- [ ] Copy matches the approved template — no placeholder text remaining (no [brackets] in the final sent message)
- [ ] Review link in the test message resolves correctly
- [ ] Send-from identity is correct — message came from owner's number or email, not Drew's

---

### Timing and Trigger

- [ ] Timing is set correctly — review request fires at the right point (correct number of days after trigger)
- [ ] Trigger condition is correctly defined — does not fire on wrong events

---

### One-Per-Job Rule

- [ ] One-per-job rule is enforced — document how:
  - If manual: ☐ Owner confirms they check the tracking record before sending
  - If automated: ☐ System is confirmed to send only once per job/client combination
- [ ] Tracking sheet or log location confirmed and accessible to owner
- [ ] Owner understands they must not send a second review request for the same job

---

### Compliance

- [ ] No review incentive language in any approved template (no "leave a review and get a discount" or similar)
- [ ] Copy is directed only at clients who completed a job — not at prospects, cold leads, or clients who expressed dissatisfaction
- [ ] No mass-send or list-based send in scope without explicit opt-in review

---

## QA Summary

| Check area | Result | Notes |
|---|---|---|
| Review link resolves correctly on mobile | ☐ Pass  ☐ Fail | |
| Review link works in email client (if email in scope) | ☐ Pass  ☐ N/A | |
| Test request received — arrives, looks right, links work | ☐ Pass  ☐ Fail | |
| No placeholder text in approved copy | ☐ Pass  ☐ Fail | |
| Timing and trigger correct | ☐ Pass  ☐ Fail | |
| One-per-job rule enforced and documented | ☐ Pass  ☐ Fail | |
| No review incentives in copy | ☐ Pass  ☐ Fail | |

**Overall result:** ☐ All checks pass — cleared to go live  ☐ Open issues — do not go live

---

## QA Sign-Off

- QA completed by Drew: [date]
- All checks passed: ☐ Yes  ☐ No — open issues:
- Cleared to go live: ☐ Yes  ☐ No
