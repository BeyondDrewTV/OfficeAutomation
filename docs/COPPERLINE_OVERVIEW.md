# Copperline System Overview

## What Copperline Is

Copperline is an internal outbound acquisition engine for a one-person
automation consultancy. The product being sold is a missed-call texting
automation service for local service businesses (plumbers, HVAC, roofers,
electricians, landscapers, etc.).

The system handles the full acquisition loop: discovery → outreach → follow-up
→ close → deploy.

---

## Core Workflow

```
discover businesses via map
  → create prospect record in prospects.csv
    → generate cold email draft
      → review draft in dashboard
        → approve and send via Gmail
          → log contact attempt
            → follow-up scheduled automatically
              → close client
                → deploy missed-call texting system
```

---

## Key Design Principles

- Dashboard is the command center for all operations
- No hidden background automation without operator awareness
- Email sending is manual until draft quality is proven reliable
- Minimize CLI usage — all actions happen in the dashboard
- Cold emails must sound human, under ~90 words, soft ask

---

## Repository Structure

```
OfficeAutomation/
├── lead_engine/
│   ├── run_lead_engine.py          # Core engine — protected
│   ├── dashboard_server.py         # Flask API
│   ├── dashboard_static/
│   │   └── index.html              # Full frontend (single file)
│   ├── data/
│   │   └── prospects.csv           # Prospect records
│   ├── queue/
│   │   └── pending_emails.csv      # Draft email queue
│   ├── discovery/
│   │   └── prospect_discovery_agent.py
│   ├── outreach/
│   │   └── email_draft_agent.py
│   ├── scoring/
│   │   └── opportunity_scoring_agent.py
│   └── intelligence/
│       └── website_scan_agent.py
├── docs/                           # AI control panel (this folder)
├── automation-agency-office/       # Memory and brand assets
└── missed_call_product/            # Product demo assets
```

---

## Data Sources

| File | Purpose |
|---|---|
| `data/prospects.csv` | One row per discovered business |
| `queue/pending_emails.csv` | Outreach drafts awaiting approval |

Key fields on prospects: `last_contact_channel`, `last_contacted_at`,
`contact_attempt_count`, `contact_result`, `next_followup_at`, `campaign_key`

---

## Email Policy

- Emails generated as drafts, never auto-sent
- Operator reviews in dashboard, sends manually via Gmail
- Auto-send will only be enabled after generation quality is proven

---

## Cold Email Style

Must sound human. Target: under 90 words, specific problem, soft ask.

Banned phrases: "AI-powered", "streamline operations", "maximize efficiency",
"revolutionize", "cutting-edge technology"

---

## Current Tech Stack

- Backend: Python / Flask
- Frontend: Single-file HTML/CSS/JS (no build step)
- Map: Leaflet.js + OpenStreetMap
- Clustering: Leaflet.markercluster
- Data: CSV files (no database)
- Email: Gmail (manual send)
