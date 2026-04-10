# Lead & Contact Setup — Notification Preference Template
Version: v1 | Kit: lead_contact_setup_v1

## Purpose
Capture owner notification preferences before configuring any routing or alert. One wrong preference here means real leads get missed or the owner gets flooded. Confirm before building.

---

## Owner Notification Settings

| Field | Value |
|---|---|
| Owner name | |
| Preferred notification destination | ☐ Phone: ___  ☐ Email: ___  ☐ Both |
| Notification trigger | ☐ Every new lead  ☐ Missed calls only  ☐ All active channels |
| Timing | ☐ Real-time (immediate)  ☐ Once/day digest  ☐ Business hours only (define: ) |
| Format preference | ☐ Short SMS alert  ☐ Email with lead details  ☐ Both |

---

## Approved Notification Copy

Owner reviews and approves this copy before it goes live. Do not use placeholder copy in production.

### SMS Alert — Short Format
```
New lead — [Name] — [Phone/Email] — [Source]
Came in: [Time]
```
Owner approved: ☐ Yes  ☐ Revision needed — Notes:

### Email Alert — Detail Format
```
Subject: New lead from [Source] — [Business Name]

Name: [Name]
Contact: [Phone/Email]
Source: [Channel — Phone / Form / DM]
Message: [Brief summary if available]
Came in: [Date/Time]

Reply directly or call back at your convenience.
```
Owner approved: ☐ Yes  ☐ Revision needed — Notes:

---

## Notification Verification

- ☐ Test notification sent to owner destination
- ☐ Owner confirmed receipt in correct format
- ☐ Timing matched the agreed setting
- ☐ Owner knows how to pause notifications (documented in `handoff_closeout.md`)

---

## Notes / Special Cases
