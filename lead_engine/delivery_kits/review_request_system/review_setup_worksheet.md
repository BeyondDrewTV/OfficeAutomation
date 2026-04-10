# Review Request System — Review Setup Worksheet
Version: v1 | Kit: review_request_system_v1

## How to Use This Worksheet
Fill this out with the owner during the intake call or within 24 hours after. Every aspect of the review request flow must be defined here before setup begins. Do not configure any send path until the worksheet is complete and owner-reviewed.

---

## 1. Business Identity

| Field | Value |
|---|---|
| Business name | |
| Primary service type (e.g., plumbing, roofing, HVAC) | |
| Owner / primary contact | |
| Owner phone | |
| Owner email | |
| Primary service area | |

---

## 2. Review Destinations

| Platform | Status | Link / URL |
|---|---|---|
| Google Business Profile (required) | ☐ In scope  ☐ Not in scope | |
| Facebook (optional) | ☐ In scope  ☐ Not in scope | |
| Other: _________________ | ☐ In scope  ☐ Not in scope | |

**Note:** The Google Business Profile review link must be tested before go-live. Confirm it resolves to the correct GBP listing from a phone browser.

---

## 3. Review Request Trigger

What causes a review request to be sent to a client? Select one or more.

| # | Trigger | Active? | Notes |
|---|---|---|---|
| 1 | Job completed — owner sends manually | ☐ Yes  ☐ No | Owner decides when to send, job by job |
| 2 | Job completed — auto-send via SMS gateway (if tool exists) | ☐ Yes  ☐ No | Automated send after job is marked complete |
| 3 | Invoice paid | ☐ Yes  ☐ No | Triggered when payment is confirmed |
| 4 | Post-job check-in reply from client | ☐ Yes  ☐ No | Triggered after positive reply to check-in message |
| 5 | Owner decides case by case | ☐ Yes  ☐ No | No fixed trigger — owner evaluates each job |

---

## 4. Send Configuration

| Field | Answer |
|---|---|
| Channel | ☐ SMS  ☐ Email  ☐ Both |
| Who sends it | ☐ Owner manually  ☐ Automated |
| Timing — how many days after the trigger? | |
| Max requests per client per job | 1 — do not send a review request more than once per completed job per client |

---

## 5. Client Tracking

How will the owner track which clients have already been asked for a review?

| Method | Active? | Location / Notes |
|---|---|---|
| Note in phone contacts | ☐ Yes  ☐ No | |
| Row in a tracking spreadsheet | ☐ Yes  ☐ No | |
| Note in CRM or scheduling tool | ☐ Yes  ☐ No | |
| Other: _________________ | ☐ Yes  ☐ No | |

**Tracking is required.** Before any review request is sent, confirm in the tracking record that this client has not already received a request for this job.

---

## 6. Scope Ceiling (Bounded Scope Enforcement)

This setup covers one review request per completed job per client.

**What is in scope:**
- ☐ Review request copy — approved templates for the channels in scope
- ☐ Review link(s) — confirmed working on mobile
- ☐ Trigger definition and setup
- ☐ Send-from identity (owner's name and number/email)
- ☐ Tracking method confirmed
- ☐ Test sequence

**Explicitly out of scope — any of these requires a change order:**
- Mass-sending review requests to past clients (requires explicit opt-in review before any batch send)
- Automated batching or list-based send
- Review management or response handling
- Incentivized review programs
- Adding new channels or platforms after setup is complete

**Hard rule:** One review request per completed job per client. No exceptions without explicit review and owner approval.

---

## 7. Worksheet Sign-Off

Owner confirms the review destinations, triggers, and scope above are correct before setup begins.

- Completed by Drew: [date]
- Owner name: ____________________________
- Owner reviewed and confirmed this review setup plan: ☐ Yes  ☐ Changes needed (see notes)
- Notes / open items:
