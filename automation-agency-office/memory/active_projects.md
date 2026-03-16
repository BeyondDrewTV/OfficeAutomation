# Active Projects

## Missed Call Lead Capture — v1.2
**Status:** Complete — hardened for production
**Location:** `products/missed_call_lead_capture/`
**Updated:** 2026-03-14

### Architecture
```
Inbound call → validate → rate limit → play voice → hangup → auto-SMS (retry x3)
Inbound SMS  → validate → rate limit → log to Sheets → notify owner → auto-reply
```

### Files
| File | Purpose |
|---|---|
| `app.py` | Flask server v1.2 — validation, rate limiting, structured logging |
| `logger.py` | Structured event logger — rotating file + console |
| `sms.py` | Twilio SMS with retry (3 attempts, exponential backoff) |
| `notify.py` | Owner SMS (retry) + email notifications |
| `sheets.py` | Google Sheets lead logging |
| `clients.py` | Multi-client config loader |
| `clients.json` | Client config — one block per client |
| `install_client.py` | Client onboarding CLI |
| `.env.example` | Environment variable template |
| `requirements.txt` | Python dependencies |
| `Procfile` | Gunicorn for Render/Railway |
| `Run Missed Call Service.bat` | Local launcher |
| `SETUP_MISSED_CALL.md` | Setup + test + deployment docs |

### Next Steps
1. Deploy v1.2 to Render
2. Run full test suite (SETUP_MISSED_CALL.md Tests 1–5)
3. Onboard first paying client via install_client.py
