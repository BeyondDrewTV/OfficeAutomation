# Client Approval / Estimate Portal — Approval Flow Worksheet
Version: v1 | Kit: client_approval_estimate_portal_v1

## How to Use This Worksheet
Fill this out for each specific engagement that uses the approval flow. One worksheet per client. Do not send a real approval link until this worksheet is complete and the QA checklist has been run.

**What this is:** A lightweight link or form that lets the client see the estimate and respond (approve, ask a question, or decline). It is not a web app, not a client account, not a CRM portal. It is one page or form per estimate.

---

## 1. Client Identity

| Field | Value |
|---|---|
| Client name | |
| Client phone | |
| Client email | |
| Best way to reach this client | ☐ Text  ☐ Email |
| Job type / service | |

---

## 2. What Is Being Approved

| Field | Value |
|---|---|
| What this approval covers | ☐ Initial estimate  ☐ Revised estimate  ☐ Change order  ☐ Other: _______ |
| Estimate total | $ |
| Approval window (how long is this estimate valid?) | e.g., 7 days — expires [date] |
| Any deadline or urgency note for the client? | |

---

## 3. Approval Link Format

Choose one delivery format for this engagement. The format should match what the client is comfortable with and what Drew can set up quickly.

| Format | Selected | Notes |
|---|---|---|
| ☐ PDF or image shared via text or email | ☐ | Lowest friction. Drew creates the estimate as a PDF, owner sends it. Client replies YES to approve. No hosting needed. |
| ☐ Google Form with approval field | ☐ | Low-code. Drew builds a Google Form with the estimate summary and an approval field. Client submits the form. Responses go to a Google Sheet Drew monitors or shares with owner. |
| ☐ Hosted HTML page with approve button | ☐ | Drew-built one-pager with estimate content and a button that sends an email or logs a response. Requires a hosting location (Netlify or equivalent). |

**Selected format:** ___________________

---

## 4. How the Client Responds

Based on the format chosen above, how does the client actually respond?

| Format | Client action |
|---|---|
| PDF / image | Client replies to the text or email with "YES" (or asks a question) |
| Google Form | Client submits the form — picks "Approve," "Have a question," or "Decline" |
| Hosted HTML page | Client clicks the Approve button — triggers an email to Drew or owner |

**Confirm the client response method:** ___________________

**What happens if the client has a question?** ___________________

**What happens if the client declines?** ___________________

---

## 5. How Drew Gets Notified

When the client responds, Drew (or the owner) needs to know immediately.

| Format | Notification method |
|---|---|
| PDF / image | Owner sees the text/email reply directly in their inbox |
| Google Form | Google Form sends email notification to: _________________ |
| Hosted HTML page | Approve button sends email to: _________________ |

**Notification destination confirmed:** ☐ Yes  ☐ Not yet — destination: ___________________

---

## 6. How the Link or Form Gets Deactivated After Approval

Once the client approves and the job is confirmed, the approval path should be closed.

| Format | Deactivation method |
|---|---|
| PDF / image | Nothing to deactivate — it's a static file. No action needed. |
| Google Form | Drew closes the form (Form Settings → Accepting responses: Off) |
| Hosted HTML page | Drew unpublishes the page or removes it from the hosting path |

**Deactivation step for this engagement:** ___________________

**Who is responsible for deactivating?** ☐ Drew  ☐ Owner

---

## 7. Scope Ceiling (Bounded Scope Enforcement)

This approval flow covers one estimate or change order for one client.

**In scope:**
- Presenting the estimate content in a format the client can read
- Capturing the client's approval (or question or decline)
- Notifying Drew or the owner when the client responds
- Deactivating the link or form after approval

**Explicitly out of scope — requires a change order:**
- Payment processing or collection
- Legal e-signature (binding contract execution)
- Client account creation or login system
- CRM data entry or automation beyond what is described here
- Storing client data beyond what is needed for this approval

---

## Worksheet Sign-Off

- Completed by Drew: [date]
- Client identity confirmed: ☐ Yes
- Format selected: ☐ Yes
- Notification path confirmed: ☐ Yes
- Deactivation path confirmed: ☐ Yes
- Notes / open items:
