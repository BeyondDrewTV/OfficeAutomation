# Estimate & Job Status Communication — Access Checklist
Version: v1 | Kit: estimate_job_status_communication_v1

## Purpose
Confirm every access item before setup begins. If any required item is blank, setup does not start. Come back to this checklist when the missing item is resolved.

**Policy: The owner is always the sender identity. Drew configures the flow. The owner owns the send path, the send-from number, and the message content.**

---

## Required Access — Confirm Before Setup

### 1. Messaging Platform or Send Method

What tool will be used to send the status notifications?

| Option | Selected? | Details |
|---|---|---|
| Owner's existing SMS app (manual send) | ☐ | (no setup needed — owner sends manually) |
| Google Voice (free SMS, no automation) | ☐ | Account: |
| Twilio or similar SMS gateway | ☐ | Account access confirmed: ☐ Yes  ☐ No |
| Email (Gmail or other SMTP) | ☐ | Address: |
| HubSpot / CRM with email send | ☐ | Access confirmed: ☐ Yes  ☐ No |
| Other: _________________ | ☐ | Access confirmed: ☐ Yes  ☐ No |

**Drew needs:** login access or API credentials for any automated send path. For manual-send workflows, no platform access is required — Drew just configures the templates and instructions.

---

### 2. Send-From Identity

| Field | Value |
|---|---|
| Send-from phone number (for SMS) | |
| Send-from email address (for email) | |
| Display name (how the sender appears to the client) | |
| Owner confirmed this is the correct send identity: | ☐ Yes  ☐ No — correct identity: |

---

### 3. Owner Contact for Test Messages

Before go-live, Drew will send test messages through every active stage. The owner must be reachable at these destinations.

| Test destination | Value | Confirmed |
|---|---|---|
| Owner test phone (receives test SMS) | | ☐ |
| Owner test email (receives test email) | | ☐ |

---

### 4. Existing Workflow Tools (If Any)

If the owner already uses a scheduling tool, CRM, or booking app, note it here. This determines whether notifications can be triggered from existing tools or must be set up as a standalone flow.

| Tool | In Use? | Access for Drew? |
|---|---|---|
| Google Calendar / Booking | ☐ Yes  ☐ No | ☐ Yes  ☐ No |
| Square / Jobber / Housecall Pro | ☐ Yes  ☐ No | ☐ Yes  ☐ No |
| QuickBooks or invoicing tool | ☐ Yes  ☐ No | ☐ Yes  ☐ No |
| Other: _________________ | ☐ Yes  ☐ No | ☐ Yes  ☐ No |

**Note:** Integration with existing tools is out of scope unless explicitly agreed as part of this engagement. If the owner uses a tool Drew doesn't have access to, the default is a manual-trigger workflow or a standalone send path.

---

### 5. Test Destination Confirmed

Before any client-facing send path goes live:

- [ ] Test phone number is ready to receive test SMS
- [ ] Test email address is ready to receive test email (if email channel is active)
- [ ] Owner is available during the test window: [date/time agreed: ____________]
- [ ] All active-stage test messages will be sent and confirmed before handoff

---

## Access Checklist Sign-Off

- All required access confirmed: ☐ Yes  ☐ Outstanding items (see notes)
- Outstanding items:
- Confirmed by Drew: [date]
- Confirmed by owner: ☐ Yes / [date]
