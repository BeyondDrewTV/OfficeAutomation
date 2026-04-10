# Follow-Up & Reminder Setup — Cadence Worksheet
Version: v1 | Kit: follow_up_reminder_setup_v1

## How to Use This Worksheet
Fill this out with the owner during the intake call or within 24 hours after. Every follow-up trigger the owner wants active must be defined here before any setup begins. Do not configure any send path or template until the cadence map is complete and owner-reviewed.

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

## 2. Follow-Up Triggers

Below are the most common follow-up triggers for contractors. Check every trigger the business actively wants to use. Cross out any that don't apply. Add triggers at the bottom if the business uses something not listed.

| # | Trigger | Active? | N (days) | Notes |
|---|---|---|---|---|
| 1 | Estimate sent but not approved after N days | ☐ Yes  ☐ No | | Client hasn't responded to the estimate |
| 2 | Form inquiry received but no reply from owner yet | ☐ Yes  ☐ No | | Owner is reminded to respond to a new lead |
| 3 | Job completed — checking in after N days | ☐ Yes  ☐ No | | Post-job client check-in |
| 4 | Cold lead who expressed interest but went quiet | ☐ Yes  ☐ No | | Lead re-engagement after silence |
| 5 | Appointment reminder — day before or morning of | ☐ Yes  ☐ No | | Confirm the appointment is still on |
| 6 | Other (owner defines) | ☐ Yes  ☐ No | | |

---

## 3. Trigger Detail — Fill In One Row Per Active Trigger

Complete this section for every trigger checked Yes above. Leave blank for triggers not in use.

### Trigger: Estimate Sent — No Response

| Field | Answer |
|---|---|
| Who receives the reminder? | ☐ Owner (reminded to follow up)  ☐ Client (receives the follow-up message) |
| Channel | ☐ SMS  ☐ Email  ☐ Both |
| Timing — first follow-up | [_] days after estimate sent |
| Timing — second follow-up (if any) | [_] days after estimate sent |
| Max number of follow-ups per estimate | |
| Who sends it? | ☐ Owner manually  ☐ Automated from setup  ☐ Drew sends on owner's behalf (with permission) |

---

### Trigger: Form Inquiry Received — Owner Hasn't Replied

| Field | Answer |
|---|---|
| Who receives the reminder? | ☐ Owner (reminded to respond to the inquiry) |
| Channel | ☐ SMS  ☐ Email  ☐ Both |
| Timing | [_] hours / days after inquiry comes in |
| Max reminders per inquiry | |
| Who sends it? | ☐ Owner manually  ☐ Automated from setup |

---

### Trigger: Job Completed — Client Check-In

| Field | Answer |
|---|---|
| Who receives the reminder? | ☐ Client (check-in message from owner) |
| Channel | ☐ SMS  ☐ Email  ☐ Both |
| Timing | [_] days after job marked complete |
| Max check-ins per job | |
| Who sends it? | ☐ Owner manually  ☐ Automated from setup  ☐ Drew sends on owner's behalf (with permission) |

---

### Trigger: Cold Lead Re-Engagement

| Field | Answer |
|---|---|
| Who receives the reminder? | ☐ Owner (reminded to reach out)  ☐ Client (receives re-engagement message directly) |
| Channel | ☐ SMS  ☐ Email  ☐ Both |
| Timing | [_] days after last contact |
| Max re-engagement attempts | |
| Who sends it? | ☐ Owner manually  ☐ Automated from setup |

---

### Trigger: Appointment Reminder

| Field | Answer |
|---|---|
| Who receives the reminder? | ☐ Client (reminder of scheduled appointment) |
| Channel | ☐ SMS  ☐ Email  ☐ Both |
| Timing | ☐ Day before  ☐ Morning of  ☐ Both |
| Who sends it? | ☐ Owner manually  ☐ Automated from setup |

---

### Additional Trigger: ___________________

| Field | Answer |
|---|---|
| Who receives the reminder? | ☐ Owner  ☐ Client |
| Channel | ☐ SMS  ☐ Email  ☐ Both |
| Timing | |
| Max reminders | |
| Who sends it? | ☐ Owner manually  ☐ Automated from setup |

---

## 4. Scope Ceiling (Bounded Scope Enforcement)

This setup covers follow-up cadence definition and initial setup only.

**What is in scope:**
- ☐ Defining the triggers and timing for each active follow-up
- ☐ Message templates for each active trigger (reviewed and approved by owner)
- ☐ Send-from identity (owner's name and number/email)
- ☐ Channel setup (SMS, email, or both — per trigger)
- ☐ Test sequence

**Explicitly out of scope — any of these requires a change order:**
- Building automation where only a manual process was agreed on
- Adding new triggers or channels after setup is complete
- CRM implementation or contact database
- Inbound reply handling or conversation management
- Marketing messages, promotions, or campaigns

**Note:** Manual follow-up reminders are always a valid option. If no automation tool exists, setup defaults to a reference card the owner uses to send follow-ups manually.

---

## 5. Worksheet Sign-Off

Owner confirms the triggers and scope above are correct before setup begins.

- Completed by Drew: [date]
- Owner name: ____________________________
- Owner reviewed and confirmed this cadence map: ☐ Yes  ☐ Changes needed (see notes)
- Notes / open items:
