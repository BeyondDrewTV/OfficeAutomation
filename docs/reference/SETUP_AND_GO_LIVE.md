# Copperline — How to Get Your First Client This Week

## What this system does for you

Finds local service businesses, drafts personalised outreach, and sends it.  
Your job: approve emails, answer replies, get on calls, close deals.

---

## Step 1 — Start the dashboard

Double-click **`Launch Dashboard.bat`** (this file, in this folder)  
Opens at http://localhost:5000

---

## Step 2 — Find leads and send emails (do this today)

1. Pick an industry: **plumbing**, **hvac**, or **electrical** to start
2. Type your city and state
3. Set limit to **20**
4. Click **⚡ Discover + Draft**  
   → Finds businesses, scrapes emails & social links, drafts outreach automatically
5. The **⚡ Active** tab shows only unsent leads, sorted by Opportunity Score
6. Click any row to open the review panel — read the email, edit anything that sounds off
7. Click **✓ Approve** on the ones you're happy with
8. Click **▶ Send Approved**

That's it. You just sent cold outreach. Do this every week in a new city or industry.

---

## Step 3 — Follow up (do this 3 days later)

- Open the **🔁 Follow-Up** tab — overdue leads are flagged in red
- Click **✉ Follow-Up Email** to log and re-engage
- Check **💬 Conversations** for any replies — respond fast, that is where the core offer, bundle, and modules get selected
- Move won work into **Delivery** for the post-yes handoff

---

## Step 4 — Expand territory

- Open **🗺 Territory** to see which cities and industries you've covered
- Click a city to expand, then **⚡ Run Next** to fill gaps

---

## Tips

- **No email found?** The lead shows in the **📲 Social** tab — reach via Facebook DM or contact form
- **Stale copy?** Run Discover + Draft again in the same city — existing leads regenerate automatically
- **Reply comes in?** Dashboard polls Gmail every 5 min and flags it with a ★ pulse on the Replied stat
- **Target industries:** plumbing, hvac, electrical, locksmith, roofing, pest control, landscaping, cleaning

---

## Credentials needed (in `.env`)

```
GOOGLE_PLACES_API_KEY   — get free at console.cloud.google.com (enable Places API)
GMAIL_SENDER            — your Gmail address
GMAIL_APP_PASSWORD      — Gmail → Security → App Passwords
ANTHROPIC_API_KEY       — claude.ai/settings → API keys
```
