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

The product being sold is a missed-call texting service. When a local service
business misses a call, the system sends an automatic text to the caller so
they stay engaged until someone follows up.

The target clients are independent local operators: plumbers, HVAC companies,
electricians, locksmiths, garage door companies, restoration contractors.
These businesses lose revenue every time they miss a call. The product solves
a real, immediate problem.

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
