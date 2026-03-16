# SETUP_MISSED_CALL.md
# Missed Call Lead Capture — Setup, Deployment & Test Guide
# Automation Biz | v1.1

---

## SYSTEM OVERVIEW

```
CALL FLOW
  Caller dials Twilio number
    → /incoming_call webhook fires
    → Twilio plays voice message to caller
    → Twilio hangs up cleanly
    → Auto-SMS fires to caller: "Sorry we missed your call..."

SMS FLOW
  Caller texts back (or texts number directly)
    → /incoming_sms webhook fires
    → Lead logged to Google Sheets (timestamp, number, message, status)
    → Owner notified via SMS
    → Owner notified via email
    → Auto-reply sent to caller confirming receipt
```

No forwarding. No dial timeout. Every call is treated as missed — 100% reliable.

---

## PREREQUISITES

| Requirement | Notes |
|---|---|
| Python 3.10+ | `python --version` to check |
| Twilio account | twilio.com — free trial works for testing |
| Google Cloud project | For Sheets API + service account |
| Gmail account | Separate notifications account recommended |
| Public URL | ngrok (dev) or Render/Railway (prod) |

---

## STEP 1 — Install Python Dependencies

```bat
cd products\missed_call_lead_capture

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

---

## STEP 2 — Configure Environment

```bat
copy .env.example .env
```

Open `.env` and fill in:

```
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_token

SMTP_USER=notifications@gmail.com
SMTP_PASS=xxxx_xxxx_xxxx_xxxx        ← Gmail App Password only

GOOGLE_SERVICE_ACCOUNT_FILE=service_account.json
```

---

## STEP 3 — Set Up Google Sheets

### 3a. Enable the API
1. Go to console.cloud.google.com
2. Create a project (or reuse one)
3. Enable **Google Sheets API**
4. Go to **IAM & Admin → Service Accounts → Create Service Account**
5. Download the JSON key → save as `service_account.json` in this folder
   ⚠️  Never commit this file. Add it to .gitignore.

### 3b. Create the Client Sheet
1. Create a new Google Sheet for the client
2. Note the ID from the URL:
   `https://docs.google.com/spreadsheets/d/[SHEET_ID]/edit`
3. Share the sheet with the **service account email** (Editor access)
   — looks like: `name@your-project.iam.gserviceaccount.com`

---

## STEP 4 — Set Up Gmail SMTP

1. Enable 2-Step Verification on the Gmail account
2. Go to myaccount.google.com → Security → **App Passwords**
3. Create: App = Mail, Device = Other → name it "AutomationBiz"
4. Copy the 16-character password → use as `SMTP_PASS` in `.env`

---

## STEP 5 — Add Client to clients.json

Open `clients.json` and add a block:

```json
{
  "client_abc": {
    "business_name": "ABC Plumbing",
    "owner_phone":   "+18155551234",
    "owner_email":   "owner@abcplumbing.com",
    "twilio_number": "+18155559876",
    "spreadsheet_id": "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgVE2upms",
    "sheet_name": "Leads"
  }
}
```

Optional overrides (omit to use defaults):
```json
    "voice_message": "Custom greeting for this business.",
    "auto_sms":      "Custom auto-text for this business."
```

All phone numbers must be **E.164 format**: `+1XXXXXXXXXX`

---

## STEP 6 — Get a Public URL

### Local dev (ngrok)
```bat
ngrok http 5000
```
Copy the `https://xxxx.ngrok-free.app` URL — use in Twilio webhooks below.

### Production (Render.com — recommended)
1. Push this folder to a GitHub repo
2. render.com → New Web Service → connect repo
3. Set:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
4. Add all `.env` variables in Render → Environment settings
5. Upload `service_account.json` as a Secret File (path: `service_account.json`)
6. Deploy → copy the `https://your-app.onrender.com` URL

---

## STEP 7 — Configure Twilio Webhooks

For **each Twilio number** in clients.json:

1. Go to console.twilio.com → Phone Numbers → Manage → Active Numbers
2. Click the number
3. Under **Voice & Fax**:
   - "A call comes in" → **Webhook** → `POST`
   - URL: `https://your-domain.com/incoming_call`
4. Under **Messaging**:
   - "A message comes in" → **Webhook** → `POST`
   - URL: `https://your-domain.com/incoming_sms`
5. Save

---

## STEP 8 — Run the Server

```bat
REM Option A: Use the launcher batch file
"Run Missed Call Service.bat"

REM Option B: Manual
venv\Scripts\activate
python app.py
```

Server starts on http://localhost:5000

---

## DEPLOYMENT PROCESS — Per New Client Checklist

```
[ ] 1. Buy Twilio number for client (~$1/month)
        console.twilio.com → Buy a Number → search area code
[ ] 2. Create Google Sheet for client
        Share with service account email (Editor)
        Copy the Sheet ID from the URL
[ ] 3. Add client block to clients.json
        Fill: business_name, owner_phone, owner_email,
              twilio_number, spreadsheet_id, sheet_name
[ ] 4. Restart the Flask server (or redeploy on Render)
[ ] 5. Set Twilio webhooks on the new number:
        Voice:   POST https://your-domain.com/incoming_call
        SMS:     POST https://your-domain.com/incoming_sms
[ ] 6. Run test procedure below
[ ] 7. Give client the Google Sheet link (read-only or Editor access)
```

**Estimated time per new client: 10–15 minutes once server is live.**

---

## TEST PROCEDURE — Local Validation

Run these tests before handing off to any client.

### Setup
```bat
REM 1. Start the server
venv\Scripts\activate
python app.py

REM 2. In a second terminal, start ngrok
ngrok http 5000

REM 3. Set Twilio webhooks to the ngrok URL
```

---

### TEST 1 — Health Check
```
GET https://your-ngrok-url.ngrok-free.app/health
```
**Expected response:**
```json
{"status": "ok", "service": "missed-call-lead-capture", "version": "1.1"}
```

---

### TEST 2 — Incoming Call (voice + auto-SMS)

**Action:** Call the Twilio number from any phone.

**Expected sequence:**
1. Twilio picks up within 1–2 rings
2. Voice message plays ("Thanks for calling...")
3. Call ends cleanly
4. Within ~5 seconds, the calling phone receives auto-SMS

**Check server logs for:**
```
Incoming call | To=+1XXX  From=+1YYY  CallSid=CA...
Auto-SMS sent to +1YYY
```

**Check Twilio logs:**
- console.twilio.com → Monitor → Logs → Calls → should show 200 response
- Monitor → Logs → Messages → should show outbound SMS

---

### TEST 3 — SMS Reply (lead logging + owner notification)

**Action:** Reply to the auto-SMS with: `I need my pipes fixed ASAP`

**Expected sequence:**
1. Twilio fires `/incoming_sms`
2. Lead row appears in Google Sheet with correct fields
3. Owner receives SMS notification
4. Owner receives email notification
5. Caller receives auto-reply: "Got it — thanks! We'll get back to you shortly."

**Check Google Sheet for row:**
```
| 2026-03-14 18:32:11 UTC | +1YYY | I need my pipes fixed ASAP | new | ABC Plumbing | client_abc |
```

**Check server logs for:**
```
Incoming SMS | From=+1YYY  To=+1XXX  SID=SM...
Lead logged to Sheets | client=client_abc
Owner notified | client=client_abc
```

---

### TEST 4 — Unknown Number (graceful handling)

**Action:** Simulate a POST to `/incoming_sms` from a number not in clients.json.

```bat
curl -X POST http://localhost:5000/incoming_sms ^
  -d "To=+19999999999&From=+18005550100&Body=test"
```

**Expected:** 200 OK with empty TwiML response, warning in logs:
```
No client config for +19999999999 — SMS ignored
```

---

### TEST 5 — Direct text to Twilio number (non-reply)

**Action:** Text the Twilio number directly (not as a reply).

**Expected:** Same as TEST 3 — logs, sheets, owner notification, auto-reply.
This confirms both the reply-to-auto-SMS path AND the direct-text path work.

---

## ASSUMPTIONS & LIMITATIONS

| Item | Detail |
|---|---|
| Every call is treated as missed | This is intentional for v1 reliability. The business should use a separate real number as their primary line. Twilio number is the overflow/after-hours number. |
| No deduplication | If someone calls 3 times, 3 auto-SMSs fire. Could be addressed in v2 with a short-term call log. |
| No conversation threading | All inbound texts log as new leads. No "is this the same person?" detection in v1. |
| SMTP rate limits | Gmail free tier limits to ~500 emails/day. More than enough for a small agency's first few clients. |
| clients.json is loaded once | Server restart required after editing clients.json. On Render, redeploy. Consider a /reload endpoint for v2. |
| No auth on webhooks | Twilio request signature validation is not implemented in v1. Add it before scaling to high-volume clients. |
| service_account.json must be present | The file must exist at the configured path. Keep it out of git. |


---

## CLIENT ONBOARDING PROCESS

**Target: under 2 minutes per new client once the server is live.**

### Prerequisites (one-time, already done)
- Server deployed on Render (or ngrok running locally)
- `.env` populated with Twilio + Google + SMTP credentials
- `service_account.json` present
- Google Sheets API enabled on the service account project

---

### Step-by-step for each new client

**1. Create the Google Sheet (30 seconds)**
- New Google Sheet → name it after the client
- Copy the Sheet ID from the URL
- Share with the service account email → Editor

**2. Buy a Twilio number (30 seconds)**
- console.twilio.com → Phone Numbers → Buy a Number
- Search by area code matching the client's market
- ~$1/month

**3. Run install_client.py (60 seconds)**

```bat
cd products\missed_call_lead_capture
venv\Scripts\activate
python install_client.py
```

Answer the prompts:

```
  Business name (required): ABC Plumbing
  Client ID (unique key) [abc_plumbing]:
  Owner phone (E.164, e.g. +18155551234) (required): +18155551234
  Owner email (required): owner@abcplumbing.com
  Twilio number (E.164, e.g. +18155550200) (required): +18155559876

  Google Sheet ID (required): 1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgVE2upms
  Sheet tab name [ABC Plumbing]:

  Custom voice message (optional, Enter to skip):
  Custom auto-SMS text (optional, Enter to skip):
```

On success you'll see:

```
  ✅  CLIENT ONBOARDED SUCCESSFULLY
  Client ID      : abc_plumbing
  Business       : ABC Plumbing
  Twilio number  : +18155559876
  Owner SMS      : +18155551234
  Owner email    : owner@abcplumbing.com
  Sheet tab      : ABC Plumbing
  Spreadsheet ID : 1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgVE2upms

  Next steps:
  1. Set Twilio webhooks for +18155559876:
       Voice: POST https://your-domain.com/incoming_call
       SMS:   POST https://your-domain.com/incoming_sms
  2. Restart (or redeploy) the Flask server
  3. Call the Twilio number to verify the flow end-to-end
```

**4. Set Twilio webhooks (30 seconds)**
- console.twilio.com → Phone Numbers → click the new number
- Voice → "A call comes in" → Webhook → POST → `https://your-domain.com/incoming_call`
- Messaging → "A message comes in" → Webhook → POST → `https://your-domain.com/incoming_sms`
- Save

**5. Restart the server**
- Render: trigger a manual redeploy (or it's automatic on git push)
- Local: Ctrl+C → run `Run Missed Call Service.bat` again

**6. Smoke test (60 seconds)**
- Call the Twilio number → hear voice message → receive auto-SMS
- Reply to the SMS → check Google Sheet for the row → owner should get SMS + email

---

### Onboarding time breakdown

| Task | Time |
|---|---|
| Create Google Sheet + share | ~30s |
| Buy Twilio number | ~30s |
| Run install_client.py | ~60s |
| Set Twilio webhooks | ~30s |
| Restart server | ~10s |
| Smoke test | ~60s |
| **Total** | **~3–4 minutes** |

---

### What install_client.py will NOT do (by design)

- It will not buy the Twilio number for you — do that in the Twilio console
- It will not create the Google Sheet — you create it and share it first
- It will not set the Twilio webhooks — do that in the Twilio console after running
- It will not restart the server — do that manually after running

These are intentional: they require external logins and shouldn't be automated
in v1 without OAuth flows. The script handles everything that can be automated
locally: validation, config writing, and Sheets tab provisioning.
