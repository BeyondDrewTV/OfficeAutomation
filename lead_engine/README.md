# Copperline — Operations Hub

## Start the dashboard

Double-click **`Launch Dashboard.bat`** in the root folder.  
Opens automatically at http://localhost:5000

That's the only launcher you need. Everything runs from the dashboard.

---

## Daily workflow

1. **Discover leads** — pick industry + city, click ⚡ Discover + Draft  
   Finds businesses via Google Places, scrapes emails & social links, drafts outreach. One click.

2. **Review & approve** — click any row to open the review panel  
   Edit subject/body if needed, click ✓ Approve on the ones you're happy with.

3. **Send** — click ▶ Send Approved  
   Only approved rows with a real email get sent.

4. **Follow up** — check the 🔁 Follow-Up tab for overdue leads  
   Reply tracking runs automatically every 5 minutes.

---

## Tabs

| Tab | What it does |
|---|---|
| ⚡ Outreach | Main queue — default shows Active (unsent, non-terminal) leads sorted by Opp Score |
| 🔁 Follow-Up | Leads due for follow-up, grouped by urgency |
| 📲 Social | Leads without email — reach via Facebook, Instagram, or contact form |
| ⚡ Sprint | One lead at a time — fast outreach mode |
| 💬 Conversations | Leads that have replied — manage the conversation |
| 🗺 Territory | City × Industry coverage map |
| 📞 Clients | Missed Call Text-Back clients |
| 🔍 Searches | History of every Discover run |

---

## Folder layout

```
lead_engine/
  dashboard_server.py      ← Flask backend, all API routes
  dashboard_static/        ← Frontend (single index.html)
  run_lead_engine.py       ← Pipeline: discover → scan → score → draft
  city_planner.py          ← Territory tracking
  discovery/               ← Google Places discovery agent
  intelligence/            ← Website scanner, lead insight generator
  scoring/                 ← Opportunity scoring (0-100)
  outreach/                ← Email + social DM draft generation
  send/                    ← Approved email sender
  queue/pending_emails.csv ← Main data store (109 leads)
  data/prospects.csv       ← Source prospects
  logs/                    ← Server + reply logs
  _archive/                ← Old scripts no longer needed
```

---

## Environment variables (`.env` in root)

```
GOOGLE_PLACES_API_KEY=...   # Google Places API — required for Discover
GMAIL_SENDER=...            # Gmail address to send from
GMAIL_APP_PASSWORD=...      # Gmail App Password (not your account password)
ANTHROPIC_API_KEY=...       # Claude AI — used for email drafts
```

---

## Useful one-off scripts

```bash
# Preview which drafts are stale (before regenerating)
python lead_engine/reset_stale_queue.py --dry-run

# Apply stale reset (removes old drafts so they re-draft on next run)
python lead_engine/reset_stale_queue.py
```
