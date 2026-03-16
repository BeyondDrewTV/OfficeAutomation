"""
Missed Call Lead Capture — Flask Server
Handles Twilio webhooks, logs leads to Google Sheets, notifies business owners.

Run: python app.py
"""
from __future__ import annotations

import json
import logging
import os
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, Response, request
from twilio.rest import Client as TwilioClient
from twilio.twiml.voice_response import VoiceResponse
from twilio.twiml.messaging_response import MessagingResponse

from sheets import append_lead, get_or_create_sheet

# ── Setup ──────────────────────────────────────────────────────────────────────
load_dotenv(Path(__file__).parent.parent / ".env")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("missed_call")

app = Flask(__name__)

CLIENTS_DIR = Path(__file__).parent / "clients"

# ── Client Config ──────────────────────────────────────────────────────────────

def load_clients() -> dict:
    """Load all client configs from clients/clients.json"""
    config_path = CLIENTS_DIR / "clients.json"
    if not config_path.exists():
        log.warning("clients.json not found — no clients configured.")
        return {}
    with config_path.open(encoding="utf-8") as f:
        return json.load(f)


def get_client_by_twilio_number(twilio_number: str) -> tuple[str, dict] | tuple[None, None]:
    """Return (client_id, config) for a given Twilio number, or (None, None)."""
    clients = load_clients()
    for client_id, cfg in clients.items():
        if cfg.get("twilio_number", "").replace(" ", "") == twilio_number.replace(" ", ""):
            return client_id, cfg
    return None, None


# ── Twilio Helpers ─────────────────────────────────────────────────────────────

def get_twilio_client() -> TwilioClient:
    sid = os.getenv("TWILIO_ACCOUNT_SID", "")
    token = os.getenv("TWILIO_AUTH_TOKEN", "")
    if not sid or not token:
        raise RuntimeError("TWILIO_ACCOUNT_SID or TWILIO_AUTH_TOKEN not set in .env")
    return TwilioClient(sid, token)


def send_sms(to: str, from_: str, body: str) -> None:
    """Send an SMS via Twilio."""
    client = get_twilio_client()
    msg = client.messages.create(to=to, from_=from_, body=body)
    log.info("SMS sent to %s — SID: %s", to, msg.sid)


# ── Email Helpers ──────────────────────────────────────────────────────────────

def send_email_notification(owner_email: str, subject: str, body_html: str) -> None:
    """Send owner notification via Gmail SMTP."""
    gmail = os.getenv("GMAIL_ADDRESS", "")
    password = os.getenv("GMAIL_APP_PASSWORD", "")
    sender_name = os.getenv("SENDER_DISPLAY_NAME", "Lead Capture System")
    if not gmail or not password:
        log.warning("Gmail credentials not set — skipping email notification.")
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{sender_name} <{gmail}>"
    msg["To"] = owner_email
    msg.attach(MIMEText(body_html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail, password)
        server.sendmail(gmail, owner_email, msg.as_string())
    log.info("Email notification sent to %s", owner_email)


# ── Webhook: Incoming Call ─────────────────────────────────────────────────────

@app.route("/incoming_call", methods=["POST"])
def incoming_call():
    """
    Twilio hits this when a call comes in.
    We let it ring for 15 seconds. If unanswered, the call drops here
    and Twilio's status callback fires handle_missed_call.
    """
    called_number = request.form.get("Called", "")
    caller_number = request.form.get("From", "")
    log.info("Incoming call from %s to %s", caller_number, called_number)

    client_id, cfg = get_client_by_twilio_number(called_number)

    resp = VoiceResponse()
    if cfg:
        business_name = cfg.get("business_name", "us")
        resp.say(
            f"Thank you for calling {business_name}. "
            "Please hold while we connect you.",
            voice="alice",
        )
        # Dial the owner — if no answer, the status callback triggers auto-SMS
        dial = resp.dial(
            action="/call_status",
            timeout=15,
            method="POST",
        )
        dial.number(cfg.get("owner_phone", ""))
    else:
        log.warning("No client found for number %s", called_number)
        resp.say("Thank you for calling. Please try again later.", voice="alice")

    return Response(str(resp), mimetype="application/xml")


# ── Webhook: Call Status (missed-call trigger) ─────────────────────────────────

@app.route("/call_status", methods=["POST"])
def call_status():
    """
    Fires after the Dial action completes.
    DialCallStatus = 'no-answer' | 'busy' | 'failed' means missed call.
    """
    dial_status = request.form.get("DialCallStatus", "")
    caller_number = request.form.get("From", "")
    called_number = request.form.get("Called", "")
    log.info("Call status: %s | from %s to %s", dial_status, caller_number, called_number)

    if dial_status in ("no-answer", "busy", "failed", "canceled"):
        client_id, cfg = get_client_by_twilio_number(called_number)
        if cfg:
            _handle_missed_call(caller_number, called_number, cfg, client_id)
        else:
            log.warning("Missed call but no client config for %s", called_number)

    resp = VoiceResponse()
    if dial_status in ("no-answer", "busy", "failed", "canceled"):
        resp.say(
            "We missed your call and will text you shortly. Thank you.",
            voice="alice",
        )
    resp.hangup()
    return Response(str(resp), mimetype="application/xml")


def _handle_missed_call(caller: str, twilio_number: str, cfg: dict, client_id: str) -> None:
    """Core logic: send auto-SMS to caller, log lead, notify owner."""
    business_name = cfg.get("business_name", "the business")

    # 1. Auto-SMS to caller
    auto_msg = (
        f"Hi! Sorry we missed your call at {business_name}. "
        "How can we help? Reply here and we'll get right back to you."
    )
    try:
        send_sms(to=caller, from_=twilio_number, body=auto_msg)
        log.info("Auto-SMS sent to missed caller %s", caller)
    except Exception as exc:
        log.error("Failed to send auto-SMS: %s", exc)

    # 2. Log lead to Google Sheets (message = blank until they reply)
    try:
        ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
        append_lead(
            client_id=client_id,
            sheet_name=cfg.get("sheet_name", client_id),
            row={
                "timestamp": ts,
                "caller_number": caller,
                "message": "(missed call — awaiting reply)",
                "status": "new",
            },
        )
    except Exception as exc:
        log.error("Failed to log lead to Sheets: %s", exc)

    # 3. Notify owner via SMS
    owner_phone = cfg.get("owner_phone", "")
    if owner_phone:
        try:
            owner_sms = (
                f"[{business_name}] Missed call from {caller}. "
                "Auto-text sent. Check Sheets for updates."
            )
            send_sms(to=owner_phone, from_=twilio_number, body=owner_sms)
        except Exception as exc:
            log.error("Failed to send owner SMS: %s", exc)

    # 4. Notify owner via Email
    owner_email = cfg.get("owner_email", "")
    if owner_email:
        try:
            subject = f"🚨 Missed Call — {caller} — {business_name}"
            body = _build_missed_call_email(caller, business_name, twilio_number)
            send_email_notification(owner_email, subject, body)
        except Exception as exc:
            log.error("Failed to send owner email: %s", exc)


# ── Webhook: Incoming SMS (reply capture) ─────────────────────────────────────

@app.route("/incoming_sms", methods=["POST"])
def incoming_sms():
    """
    Twilio hits this when the caller replies to the auto-SMS.
    We capture their message, update Sheets, and notify the owner.
    """
    from_number = request.form.get("From", "")
    to_number = request.form.get("To", "")   # This is the Twilio number (our client's)
    body = request.form.get("Body", "").strip()
    log.info("SMS reply from %s: %s", from_number, body)

    client_id, cfg = get_client_by_twilio_number(to_number)
    business_name = cfg.get("business_name", "the business") if cfg else "unknown"

    # 1. Log reply to Sheets
    if cfg:
        try:
            ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
            append_lead(
                client_id=client_id,
                sheet_name=cfg.get("sheet_name", client_id),
                row={
                    "timestamp": ts,
                    "caller_number": from_number,
                    "message": body,
                    "status": "replied",
                },
            )
        except Exception as exc:
            log.error("Failed to log SMS reply: %s", exc)

    # 2. Notify owner via SMS
    if cfg:
        owner_phone = cfg.get("owner_phone", "")
        if owner_phone:
            try:
                fwd = (
                    f"[{business_name}] Reply from {from_number}:\n"
                    f"\"{body}\"\n"
                    "— Log: check Google Sheets"
                )
                send_sms(to=owner_phone, from_=to_number, body=fwd)
            except Exception as exc:
                log.error("Failed to forward reply to owner: %s", exc)

        # 3. Notify owner via Email
        owner_email = cfg.get("owner_email", "")
        if owner_email:
            try:
                subject = f"💬 Lead Reply — {from_number} — {business_name}"
                html = _build_reply_email(from_number, body, business_name)
                send_email_notification(owner_email, subject, html)
            except Exception as exc:
                log.error("Failed to email owner about reply: %s", exc)

    # 4. Auto-reply to caller
    resp = MessagingResponse()
    resp.message(
        f"Thanks! We got your message and will follow up with you shortly. "
        f"— {business_name}"
    )
    return Response(str(resp), mimetype="application/xml")


# ── Email Templates ────────────────────────────────────────────────────────────

def _build_missed_call_email(caller: str, business_name: str, twilio_number: str) -> str:
    ts = datetime.utcnow().strftime("%B %d, %Y at %H:%M UTC")
    return f"""
    <div style="font-family:Arial,sans-serif;max-width:480px;margin:auto;padding:24px;border:1px solid #e5e7eb;border-radius:8px">
      <h2 style="color:#e05c24;margin-bottom:4px">🚨 Missed Call Alert</h2>
      <p style="color:#6b7280;margin-bottom:20px;font-size:14px">{ts}</p>
      <table style="width:100%;border-collapse:collapse;font-size:15px">
        <tr><td style="padding:8px;color:#6b7280;width:120px">Business</td>
            <td style="padding:8px;font-weight:600">{business_name}</td></tr>
        <tr style="background:#f9fafb"><td style="padding:8px;color:#6b7280">Caller</td>
            <td style="padding:8px;font-weight:600">{caller}</td></tr>
        <tr><td style="padding:8px;color:#6b7280">Twilio #</td>
            <td style="padding:8px">{twilio_number}</td></tr>
        <tr style="background:#f9fafb"><td style="padding:8px;color:#6b7280">Status</td>
            <td style="padding:8px;color:#059669;font-weight:600">Auto-text sent ✓</td></tr>
      </table>
      <p style="margin-top:20px;font-size:13px;color:#6b7280">
        The caller was automatically texted. Their reply will appear in Google Sheets and trigger another notification.
      </p>
    </div>
    """


def _build_reply_email(caller: str, message: str, business_name: str) -> str:
    ts = datetime.utcnow().strftime("%B %d, %Y at %H:%M UTC")
    return f"""
    <div style="font-family:Arial,sans-serif;max-width:480px;margin:auto;padding:24px;border:1px solid #e5e7eb;border-radius:8px">
      <h2 style="color:#2563eb;margin-bottom:4px">💬 Lead Replied</h2>
      <p style="color:#6b7280;margin-bottom:20px;font-size:14px">{ts}</p>
      <table style="width:100%;border-collapse:collapse;font-size:15px">
        <tr><td style="padding:8px;color:#6b7280;width:120px">Business</td>
            <td style="padding:8px;font-weight:600">{business_name}</td></tr>
        <tr style="background:#f9fafb"><td style="padding:8px;color:#6b7280">From</td>
            <td style="padding:8px;font-weight:600">{caller}</td></tr>
      </table>
      <div style="margin-top:16px;background:#f0f9ff;border-left:4px solid #2563eb;padding:14px;border-radius:4px;font-size:15px">
        {message}
      </div>
      <p style="margin-top:16px;font-size:13px;color:#6b7280">
        Lead logged in Google Sheets. Follow up within 15 minutes to maximize conversion.
      </p>
    </div>
    """


# ── Health Check ───────────────────────────────────────────────────────────────

@app.route("/health")
def health():
    from flask import jsonify
    clients = load_clients()
    return jsonify({"status": "ok", "clients_loaded": len(clients)})


if __name__ == "__main__":
    print("\n  Missed Call Lead Capture — Running on http://localhost:8080\n")
    app.run(host="0.0.0.0", port=8080, debug=False)
