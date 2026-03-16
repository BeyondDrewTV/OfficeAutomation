# Missed Call Lead Capture — Setup & Deployment Guide

## What this product does
When someone calls a business and no one answers, Twilio detects the miss,
automatically texts the caller back, captures their reply, logs it to Google
Sheets, and notifies the business owner — all without anyone touching a phone.

---

## Architecture

```
Incoming call
     ↓
Twilio (client's phone number)
     ↓
POST /incoming_call  → rings owner for 15s
     ↓ (no answer)
POST /call_status    → triggers auto-SMS to caller
     ↓
Caller replies (SMS)
     ↓
POST /incoming_sms   → log to Google Sheets + notify owner
```

---

## One-Time Server Setup (you do this once)

### 1. Get a server to host the app

Cheapest options (pick one):
- **Railway** (railway.app) — free tier works, ~$5/month after
- **Render** (render.com) — free tier spins down, $7/month for always-on
- **DigitalOcean** — $6/month droplet, simplest for long-term

The server needs a public HTTPS URL. Twilio won't POST to plain HTTP.

For local dev/testing: use **ngrok**
```
ngrok http 8080
```
This gives you a temporary HTTPS URL like `https://abc123.ngrok.io`

### 2. Clone / copy the project to your server

```bash
git clone <your-repo> missed_call_product
cd missed_call_product
```

Or just upload the folder via SFTP / Railway deploy.

### 3. Install dependencies

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

### 4. Copy and fill in .env

```bash
cp .env.example .env
```

Edit `.env`:
```
TWILIO_ACCOUNT_SID=ACxxxxxxxxxx        ← from twilio.com/console
TWILIO_AUTH_TOKEN=your_token           ← from twilio.com/console
GOOGLE_SERVICE_ACCOUNT_JSON=service_account.json
GMAIL_ADDRESS=you@gmail.com            ← only needed if using email notifications
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx ← only needed if using email notifications
PORT=8080
```

### 5. Set up Google Sheets API (one time)

1. Go to https://console.cloud.google.com
2. Create a project (or use an existing one)
3. Enable **Google Sheets API**
4. Go to IAM → Service Accounts → Create Service Account
5. Download the JSON key → save as `service_account.json` in this folder
6. ⚠️ Add `service_account.json` to `.gitignore` (never commit credentials)

### 6. Start the server

```bash
python app.py
```

Confirm it's running:
```
curl https://your-domain.com/health
# → {"status": "ok"}
```

---

## Per-Client Deployment (you do this for EVERY new client)

### Step 1 — Buy a Twilio phone number

1. Log into twilio.com
2. Phone Numbers → Buy a Number
3. Pick a local area code matching the client's city
4. Cost: ~$1/month per number

### Step 2 — Create a Google Sheet for this client

1. Go to sheets.google.com → New blank spreadsheet
2. Name it: `[Client Name] — Leads`
3. Copy the Sheet ID from the URL:
   `https://docs.google.com/spreadsheets/d/THIS_IS_THE_ID/edit`
4. Share the sheet with the service account email
   (find it in `service_account.json` → `"client_email"` field)
   Give it **Editor** access

### Step 3 — Run the header setup script

```bash
python onboard_client.py --spreadsheet-id YOUR_SHEET_ID
```

This writes the column headers to row 1. Do this once per client.

### Step 4 — Add client to clients.json

Copy `clients.example.json` to `clients.json` if it doesn't exist yet.
Add a new entry:

```json
{
  "client_rockford_plumbing": {
    "business_name": "Rockford Plumbing Co.",
    "owner_phone": "+18155550101",
    "owner_email": "owner@rockfordplumbing.com",
    "twilio_number": "+18155550001",
    "spreadsheet_id": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgVE2upms",
    "notification_channel": "sms",
    "auto_sms_message": "Hi! This is Rockford Plumbing. Sorry we missed your call — how can we help?",
    "ack_sms_message": "Thanks! We'll get back to you shortly."
  }
}
```

**notification_channel options:**
- `"sms"` — texts the owner (recommended, fastest)
- `"email"` — emails the owner (requires Gmail env vars)

### Step 5 — Point Twilio webhooks to your server

In the Twilio console:
1. Go to Phone Numbers → Manage → Active Numbers
2. Click the client's number
3. Under **Voice & Fax → A call comes in**:
   - Webhook: `https://your-domain.com/incoming_call`
   - Method: `HTTP POST`
4. Under **Messaging → A message comes in**:
   - Webhook: `https://your-domain.com/incoming_sms`
   - Method: `HTTP POST`
5. Save

### Step 6 — Test it

**Test missed call:**
1. Call the Twilio number from your personal phone
2. Don't answer (let it ring through)
3. You should receive an auto-SMS within a few seconds
4. Reply to that SMS
5. Check the Google Sheet — a row should appear
6. The owner (you during testing) should get notified

**Test direct SMS:**
1. Text the Twilio number directly
2. Check the Sheet and owner notification

### Step 7 — Hand off to client

Tell the client:
> "Your number is live. When anyone calls after hours or you miss a call,
> they'll automatically get a text back from your business number.
> When they reply, you'll get a notification and their message logs here:
> [paste Google Sheet link]"

Give them view access (or editor if they want to update the status column).

---

## clients.json field reference

| Field | Required | Description |
|-------|----------|-------------|
| `business_name` | ✓ | Used in notification messages |
| `owner_phone` | ✓ (SMS) | E.164 format, e.g. `+18155551234` |
| `owner_email` | ✓ (email) | Only needed if channel=email |
| `twilio_number` | ✓ | The Twilio number in E.164 format |
| `spreadsheet_id` | ✓ | Google Sheet ID from the URL |
| `notification_channel` | ✓ | `"sms"` or `"email"` |
| `auto_sms_message` | optional | Default: "Sorry we missed your call! How can we help?" |
| `ack_sms_message` | optional | If set, sent back to caller after they reply. Leave blank to skip. |

---

## Adding a second client (quick version)

1. Buy Twilio number (~$1/mo)
2. Create Google Sheet, share with service account
3. Run `python onboard_client.py --spreadsheet-id NEW_ID`
4. Add entry to `clients.json`
5. Set Twilio webhooks on the new number
6. Test → done

No code changes. No server restart needed (app reads clients.json on each request).

---

## Monthly cost per client

| Item | Cost |
|------|------|
| Twilio phone number | ~$1/mo |
| Twilio SMS (inbound) | $0.0075/msg |
| Twilio SMS (outbound) | $0.0079/msg |
| Google Sheets API | Free |
| Server (shared across all clients) | ~$0–7/mo |
| **Total per active client** | **~$3–5/mo** |

You charge $150/month. Your cost is ~$5. Margin: ~97%.

---

## Pricing to tell clients

> "Setup is $900. After that it's $150/month and I handle everything —
> the phone number, the system, and any issues that come up."

If they push back on monthly: "The number costs $1/month just to hold it.
The $150 covers maintenance, monitoring, and my time if anything breaks."

---

## Troubleshooting

**Auto-SMS not sending after missed call:**
- Check Twilio logs at console.twilio.com → Monitor → Logs → Calls
- Verify `/incoming_call` webhook is set correctly (must be HTTPS)
- Check that `timeout="15"` in TwiML isn't being changed

**Lead not logging to Sheets:**
- Confirm the service account has Editor access on the sheet
- Check server logs for "Sheets append failed"
- Verify `spreadsheet_id` in clients.json is correct

**Owner not getting notified:**
- For SMS: check `owner_phone` is E.164 format with country code
- For email: confirm Gmail App Password is set (not regular password)

**No client found for number:**
- Twilio may send numbers in different formats (+1... vs 1...)
- All numbers in clients.json should be E.164: `+18155551234`
