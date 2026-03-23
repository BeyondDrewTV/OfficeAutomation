# Copperline — Project Memory

2-minute orientation for any AI session joining this project.

---

## What Copperline Is

Copperline is a private, one-operator outbound acquisition system.
It is not a SaaS product. It is an internal tool built to run one business.

The operator uses it to find and contact local service businesses, convert
them into clients, and deploy a missed-call texting automation service to them.

---

## Business Model

Copperline is the acquisition engine for a one-person workflow consulting practice.

What is being sold: a personalized one-on-one engagement with the business owner or relevant decision-maker. Drew gets on a call, walks through how the operation actually runs, identifies where there are gaps or friction points that could be automated or improved, and builds a custom implementation plan specific to that business. If they want to move forward, Drew implements and maintains it for a monthly fee.

There is no standard product. The missed-call texting service is one possible solution in the toolkit — it may come up if it fits the business's situation — but it is not what the cold outreach is selling. The cold email is a soft ask for a conversation, not a product pitch.

The target clients are independent local service business owners: plumbers, HVAC, electricians, locksmiths, garage door, towing, roofing, landscaping, and similar trades. These businesses have real operational friction and the owner is usually the person handling it all.

---

## Lead Acquisition Focus

The current development priority is the discovery and outreach pipeline.

The operator draws a circle on a Leaflet map, selects an industry, and the
system queries the Google Places API to return matching businesses. Those
businesses become prospects. Outreach drafts are generated automatically.
The operator reviews drafts, approves them, and sends manually via Gmail.

This is intentionally manual. Auto-send is not enabled. The operator controls
every email before it goes out.

---

## Discovery Map Direction

Large-radius searches surface only prominent businesses — chains, franchises,
and heavily-reviewed operators. Independent local businesses appear only when
the search area is small.

The map system is being upgraded incrementally to support:
- Marker clustering for dense result sets (complete)
- A results side panel for reviewing discovered businesses (next)
- A "Search Visible Area" button that tiles the viewport into small cells
- Neighborhood-level grid discovery that systematically finds smaller operators

---

## Outreach Workflow

```
discover → draft → review → approve → send → log → follow-up
```

1. Operator runs a map discovery search
2. System creates prospect records in `prospects.csv`
3. `email_draft_agent.py` generates cold email drafts
4. Drafts land in `pending_emails.csv`
5. Operator reviews in the dashboard and approves
6. Emails sent manually via Gmail
7. Replies tracked, follow-ups scheduled automatically

---

## Long-Term Vision

Once the acquisition loop is reliable and producing conversations, the system
will expand to:

- Auto-send (after quality is proven)
- Territory management (track which areas and industries have been worked)
- Saturation view (see where to search next)
- Client onboarding workflow for the texting product

The infrastructure is being built incrementally. Nothing is added until the
prior layer is stable.

---

## What to Read Next

For current build status: `AI_CONTROL_PANEL.md`
For implementation scope: `docs/CURRENT_BUILD.md`
For what not to touch: `docs/PROTECTED_SYSTEMS.md`
