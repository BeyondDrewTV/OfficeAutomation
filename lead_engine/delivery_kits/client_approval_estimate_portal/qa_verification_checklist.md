# Client Approval / Estimate Portal — QA Verification Checklist
Version: v1 | Kit: client_approval_estimate_portal_v1

## Purpose
Run this checklist before sending the approval link or form to a real client. Every item must pass. If anything fails, fix it before sending.

This is not optional — a bad approval experience (broken link, wrong numbers, no notification to Drew) directly harms the client relationship and the owner's credibility.

---

## QA Checks

### Accessibility

- [ ] Approval link or form opens successfully from a phone browser (not just a desktop)
- [ ] Page or form loads in under 5 seconds on a mobile connection
- [ ] Content is readable without zooming — no text overflow or clipped sections
- [ ] Approve / submit action is reachable without scrolling past the content (or clearly visible at the bottom)

---

### Estimate Content Accuracy

- [ ] Business name and owner contact info are correct
- [ ] Client name is correct — no placeholder text ([Client Name], etc.)
- [ ] Job description accurately reflects the agreed scope
- [ ] Dollar amount is correct — matches the final estimate the owner approved
- [ ] Inclusions and exclusions are correct
- [ ] Expiration date is correct
- [ ] No placeholder text remaining — search for [ ] brackets before sending
- [ ] Owner reviewed and confirmed the estimate content: ☐ Yes  ☐ Not yet — block send

---

### Response Path

- [ ] Client response method is clear (e.g., "Reply YES to this text" or "Submit this form")
- [ ] Test response submitted and received — Drew can confirm the response path works
- [ ] Drew notification received at correct destination when test response was submitted
- [ ] Response path works on mobile (client does not need a desktop to approve)

---

### Approval Window

- [ ] Expiration date is visible to the client
- [ ] Expiration date is correct — not in the past, not blank
- [ ] If the client doesn't respond before the expiration, the owner has a follow-up plan

---

### Deactivation / Expiry Path

- [ ] Deactivation method is confirmed for the format in use:
  - PDF / image: no action needed — static file, note the expiration date in the message
  - Google Form: confirmed Drew can close the form when needed (Form Settings → Accepting responses: Off)
  - Hosted HTML page: confirmed Drew can unpublish or remove the page from the hosting path
- [ ] Deactivation step is documented in the closeout/rollback doc for this engagement

---

### Data Exposure Check

- [ ] Only the intended estimate content is visible to the client — no other job info, client list, or internal notes
- [ ] No sensitive business data (pricing for other clients, internal notes, personal addresses) is exposed
- [ ] Google Form (if used) does not show other respondents' answers
- [ ] Hosted page (if used) is not indexed or guessable — direct link only, no public listing

---

## QA Summary

| Check area | Result | Notes |
|---|---|---|
| Accessible on phone | ☐ Pass  ☐ Fail | |
| Estimate content accurate — no placeholders | ☐ Pass  ☐ Fail | |
| Response path works | ☐ Pass  ☐ Fail | |
| Drew notification received | ☐ Pass  ☐ Fail | |
| Approval window correct | ☐ Pass  ☐ Fail | |
| Deactivation path confirmed | ☐ Pass  ☐ Fail | |
| No sensitive data exposed | ☐ Pass  ☐ Fail | |

**Overall result:** ☐ All checks pass — cleared to send  ☐ Open issues — do not send

---

## QA Sign-Off

- QA completed by Drew: [date]
- All checks passed: ☐ Yes  ☐ No — open issues:
- Cleared to send to real client: ☐ Yes  ☐ No
