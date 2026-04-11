# Copperline System Overview

## What Copperline Is

Copperline is the internal outbound acquisition engine for Drew's local business digital presence + customer flow offer. It is not a product catalog. It is the system Drew built to find, contact, and convert local service business owners into fixed-price project work.

What is being sold through this pipeline: a free consultation, a simple recommendation, and then project work. The commercial layer stays clean at the top level: core offers and bundles lead the conversation, and specialty modules sit underneath as delivery pieces when they strengthen the job.

The cold emails produced by this system are not product pitches. They are soft asks for a conversation. The voice is casual, specific to that business, and never mentions pricing or a menu of systems.

The system handles the full acquisition loop: discovery -> outreach -> follow-up -> conversation -> recommendation -> project work -> delivery modules.

---

## Core Workflow

```
discover businesses via map
  -> create prospect record in prospects.csv
    -> generate cold email draft
      -> review draft in dashboard
        -> approve and send via Gmail
          -> log contact attempt
            -> follow-up scheduled automatically
              -> move into Conversations
                -> package the core offer, bundle, and modules
                  -> hand off to Delivery
```

---

## Key Design Principles

- Dashboard is the command center for all operations
- No hidden background automation without operator awareness
- Email sending is manual until draft quality is proven reliable
- Keep the commercial front door simple
- Cold emails must sound human, under ~90 words, soft ask

---

## Repository Structure

```
OfficeAutomation/
├── lead_engine/
│   ├── run_lead_engine.py          # Core engine - protected
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
└── missed_call_service/            # Missed Call Recovery service
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
