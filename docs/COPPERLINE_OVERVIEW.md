# Copperline System Overview

## What Copperline Is

## What Copperline Is

Copperline is the internal outbound acquisition engine for a one-person workflow consulting practice. It is not a product — it is the system Drew built to find, contact, and convert local service business owners into consulting clients.

What is being sold through this pipeline: a personalized one-on-one engagement. Drew gets on a call with the owner or relevant decision-maker, walks through how the business actually operates, identifies the operational gaps or friction points that could be automated or improved, and builds a custom implementation plan. If the owner wants to move forward, Drew builds and maintains whatever makes sense for their specific operation — for a monthly fee.

The cold emails produced by this system are NOT product pitches. They are soft asks for a conversation. The voice is casual, specific to that business, and never mentions products, pricing, or "solutions." The missed-call texting service is one possible deliverable Drew might build for a client — it is not what is being sold.

The system handles the full acquisition loop: discovery → outreach → follow-up → conversation → custom plan → implementation → monthly maintenance.

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
