# Client Approval / Estimate Portal — Closeout & Rollback
Version: v1 | Kit: client_approval_estimate_portal_v1

## Purpose
What to do after the client approves, and how to deactivate or roll back the approval flow if needed. Complete this document for every approval engagement.

---

## 1. Post-Approval Actions

When the client approves, do these steps in order:

- [ ] Mark the estimate as approved in Drew's log (see Closeout Log Entry below)
- [ ] Notify the owner that the client approved — include the client name, approval method, and approval date
- [ ] Move the job to delivery status (owner schedules the work, sets the job date)
- [ ] Deactivate the approval link or form (see Section 2 — the link should not stay open after approval)
- [ ] Send the client a booking confirmation (see the Estimate & Job Status Communication kit — Template 2: Booking Confirmed)

**Approval received from:** ___________________

**Approval method:** ☐ Text reply  ☐ Form submission  ☐ Button click / email

**Approval date:** ___________________

**Owner notified:** ☐ Yes  ☐ No — date: ___________________

---

## 2. How to Deactivate the Link or Form

Deactivate as soon as the job is confirmed. Do not leave approval links open indefinitely.

### PDF or Image (Shared via Text or Email)
No action needed to deactivate. The file is static — it cannot be "turned off." The expiration date communicated to the client serves as the closing boundary. If the client tries to approve after the window, do not honor it without checking with the owner.

### Google Form
1. Open the form in Google Forms (must be logged into the Google account that owns it)
2. Click the Settings gear icon
3. Under "Responses," toggle "Accepting responses" to Off
4. The form will show a closed message to anyone who tries to access it
5. Confirm the toggle is Off — do not just navigate away

### Hosted HTML Page
1. Log into the hosting platform (Netlify, GitHub Pages, or equivalent)
2. Find the deployment or site for this approval page
3. Delete the deployment, unpublish the site, or remove the specific page from the published build
4. Confirm the URL no longer loads a live page — test it from a browser
5. If the page is on a shared deployment with other content, remove only the approval page file, not the entire site

---

## 3. Change Order Path

If the client wants to change the scope after approving:

1. This is a change order — not an amendment to the original estimate
2. The original approval is noted as superseded
3. Drew creates a new approval flow (new estimate content, new link or form, new expiration window)
4. The client must approve the change order separately before any scope change begins
5. Log both approvals (original and change order) in the closeout log

**Change order received:** ☐ Yes  ☐ No

If yes, describe the change and document separately:

---

## 4. Handoff Note to Client

When the client approves, send this short confirmation message (adjust to match the owner's voice):

> "Hi [Client Name], we've received your approval — thank you! We'll be in touch shortly with your job date and next steps. Call or text [Owner Phone] if you have any questions before then. — [Owner Name]"

**Note:** This message should come from the owner's number or email, not a generic send path.

---

## 5. Closeout Log Entry

Record the approval here and in whatever log or sheet the owner uses.

| Field | Value |
|---|---|
| Client name | |
| Job type | |
| Estimate amount approved | $ |
| Approval date | |
| Approval method (text reply / form / button) | |
| Approval link or form deactivated? | ☐ Yes  ☐ N/A (PDF format) |
| Deactivation date | |
| Booking confirmation sent to client? | ☐ Yes |
| Change order required? | ☐ Yes  ☐ No |
| Record saved to (location / file name) | |

---

## Closeout Sign-Off

- Post-approval steps completed: ☐ Yes  ☐ No — open items:
- Approval link or form deactivated: ☐ Yes  ☐ N/A
- Closeout log entry saved: ☐ Yes
- Completed by Drew: [date]
