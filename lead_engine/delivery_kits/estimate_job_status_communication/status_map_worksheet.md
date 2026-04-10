# Estimate & Job Status Communication — Status Map Worksheet
Version: v1 | Kit: estimate_job_status_communication_v1

## How to Use This Worksheet
Fill this out with the owner during the intake call or within 24 hours after. Every status stage the owner wants to notify clients about must be defined here before setup begins. Do not configure any send path until the status map is complete and owner-signed.

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

## 2. Status Stages

Below is a starter set of common contractor status stages. Check every stage the business actually uses. Cross out any that don't apply. Add stages at the bottom if the business uses something not listed.

| # | Stage | Active? | Notes |
|---|---|---|---|
| 1 | Estimate Sent | ☐ Yes  ☐ No | Client receives the estimate for review |
| 2 | Estimate Approved / Booking Confirmed | ☐ Yes  ☐ No | Client has approved — job is now scheduled |
| 3 | Job Scheduled | ☐ Yes  ☐ No | Date and time confirmed — day-before reminder |
| 4 | Job Started | ☐ Yes  ☐ No | Crew is on site and work has begun |
| 5 | Job Completed | ☐ Yes  ☐ No | Work is finished — client receives completion notice |
| 6 | Invoice Sent | ☐ Yes  ☐ No | Invoice delivered with payment instructions |
| 7 | Payment Received | ☐ Yes  ☐ No | Payment confirmed — optional thank-you message |
| 8 | (Add stage) | ☐ Yes  ☐ No | |
| 9 | (Add stage) | ☐ Yes  ☐ No | |

---

## 3. Stage Detail — Fill In One Row Per Active Stage

Complete this section for every stage checked Yes above. Leave blank for stages not in use.

### Stage: Estimate Sent

| Field | Answer |
|---|---|
| Who triggers this notification? | ☐ Owner (manually, after sending estimate)  ☐ Drew (automated trigger) |
| How is the client notified? | ☐ Text  ☐ Email  ☐ Both |
| When is it sent? | ☐ Immediately when estimate is ready  ☐ Within [_] hours |
| Message direction (key info to include) | Estimate amount, how to respond (approve or ask questions), reply contact |

---

### Stage: Estimate Approved / Booking Confirmed

| Field | Answer |
|---|---|
| Who triggers this notification? | ☐ Owner (manually, after client approves)  ☐ Drew (automated trigger) |
| How is the client notified? | ☐ Text  ☐ Email  ☐ Both |
| When is it sent? | ☐ Same day as approval  ☐ Within [_] hours |
| Message direction | Confirmed job date and time, who to call with questions |

---

### Stage: Job Scheduled (Day-Before Reminder)

| Field | Answer |
|---|---|
| Who triggers this notification? | ☐ Owner (manually, evening before job)  ☐ Drew (automated, 24h before) |
| How is the client notified? | ☐ Text  ☐ Email  ☐ Both |
| When is it sent? | ☐ Day before job  ☐ Morning of job |
| Message direction | Reminder of date/time, arrival window, who to call if questions |

---

### Stage: Job Started

| Field | Answer |
|---|---|
| Who triggers this notification? | ☐ Owner (manually, when crew arrives)  ☐ Drew (automated trigger) |
| How is the client notified? | ☐ Text  ☐ Email  ☐ Both |
| When is it sent? | ☐ When crew is on site |
| Message direction | Work is starting today, what is being done, reply contact |

---

### Stage: Job Completed

| Field | Answer |
|---|---|
| Who triggers this notification? | ☐ Owner (manually, when job is done)  ☐ Drew (automated trigger) |
| How is the client notified? | ☐ Text  ☐ Email  ☐ Both |
| When is it sent? | ☐ Same day work finishes  ☐ Next morning |
| Message direction | Job is complete, thank you, review request (optional), next steps |

---

### Stage: Invoice Sent

| Field | Answer |
|---|---|
| Who triggers this notification? | ☐ Owner (manually, with invoice)  ☐ Drew (automated trigger) |
| How is the client notified? | ☐ Text  ☐ Email  ☐ Both |
| When is it sent? | ☐ Same day job completes  ☐ Next business day |
| Message direction | Invoice amount, how to pay (link or instructions), due date |

---

### Stage: Payment Received

| Field | Answer |
|---|---|
| Who triggers this notification? | ☐ Owner (manually, after payment confirmed)  ☐ Drew (automated trigger) |
| How is the client notified? | ☐ Text  ☐ Email  ☐ Both |
| When is it sent? | ☐ Same day payment is received |
| Message direction | Thank you, payment confirmed, any warranty or follow-up info |

---

### Additional Stage: ___________________

| Field | Answer |
|---|---|
| Who triggers this notification? | ☐ Owner (manually)  ☐ Drew (automated trigger) |
| How is the client notified? | ☐ Text  ☐ Email  ☐ Both |
| When is it sent? | |
| Message direction | |

---

## 4. Scope Ceiling (Bounded Scope Enforcement)

This setup covers only client status notifications — messages sent to the client when a job reaches a defined stage.

**What is in scope:**
- ☐ Status notification messages for the stages checked above
- ☐ Send-from identity (owner's name and number/email)
- ☐ Channel setup (SMS, email, or both — per stage)
- ☐ Template review and approval
- ☐ Test sequence

**Explicitly out of scope — any of these requires a change order:**
- Payment processing or invoicing software
- CRM implementation or contact database
- Auto-invoicing or billing automation
- Multi-location or crew-management notifications
- Marketing messages, promotions, or campaigns

---

## 5. Worksheet Sign-Off

Owner confirms the status stages and scope above are correct before setup begins.

- Completed by Drew: [date]
- Owner name: ____________________________
- Owner reviewed and confirmed this status map: ☐ Yes  ☐ Changes needed (see notes)
- Notes / open items:
