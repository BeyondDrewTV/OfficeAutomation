"""
Missed Call Lead Capture — Multi-Client Flask Server
=====================================================
Handles Twilio call/SMS webhooks, logs leads to Google Sheets,
and notifies the business owner via SMS or Email.

Run:
    python app.py

Webhooks (set in Twilio console per phone number):
    Call webhook:  POST https://your-domain.com/incoming_call
    SMS  webhook:  POST https://your-domain.com/incoming_sms
"""
from __future__ import annotations

import json
import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, request, Response

from clients import get_client_by_twilio_number
from sheets import append_lead
from notifier import notify_owner
from sms import send_sms

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("missed_call")

app = Flask(__name__)


# ── Health check ──────────────────────────────────────────────────────────────

@app.route("/health")
def health():
    return {"status": "ok"}, 200


# ── Incoming call webhook ─────────────────────────────────────────────────────

@app.route("/incoming_call", methods=["POST"])
def incoming_call():
    """
    Twilio calls this when a call comes in.
    We answer with TwiML that rings the owner for 15 seconds.
    If unanswered, Twilio will call /call_status with DialCallStatus=no-answer.
    """
    called_number = request.form.get("Called", "")
    caller_number = request.form.get("From", "")

    client = get_client_by_twilio_number(called_number)
    if not client:
        log.warning("No client found for Twilio number: %s", called_number)
        # Still return valid TwiML so Twilio doesn't error
        return _twiml_reject()

    owner_phone = client.get("owner_phone", "")
    log.info("Incoming call: %s → %s (client: %s)", caller_number, called_number, client["business_name"])

    # Dial owner for 15 seconds; if no answer, hit /call_status
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Dial timeout="15" action="/call_status" method="POST">
    <Number>{owner_phone}</Number>
  </Dial>
</Response>"""
    return Response(twiml, mimetype="text/xml")


@app.route("/call_status", methods=["POST"])
def call_status():
    """
    Twilio posts here after the <Dial> completes.
    DialCallStatus values: completed | no-answer | busy | failed | canceled
    We only send the auto-text on missed calls.
    """
    dial_status = request.form.get("DialCallStatus", "")
    caller_number = request.form.get("From", "")
    called_number = request.form.get("Called", "")

    client = get_client_by_twilio_number(called_number)
    if not client:
        return _twiml_hangup()

    log.info(
        "Call status: %s | caller=%s | client=%s",
        dial_status, caller_number, client["business_name"],
    )

    if dial_status in ("no-answer", "busy", "failed", "canceled"):
        _handle_missed_call(caller_number, client)

    return _twiml_hangup()


def _handle_missed_call(caller_number: str, client: dict) -> None:
    """Send auto-text when a call is missed."""
    twilio_number = client["twilio_number"]
    message = client.get(
        "auto_sms_message",
        "Sorry we missed your call! How can we help you today?",
    )
    log.info("Sending auto-SMS to %s from %s", caller_number, twilio_number)
    send_sms(to=caller_number, from_=twilio_number, body=message)


# ── Incoming SMS webhook ──────────────────────────────────────────────────────

@app.route("/incoming_sms", methods=["POST"])
def incoming_sms():
    """
    Twilio calls this when an SMS arrives at a Twilio number.
    Log the lead and notify the owner.
    """
    twilio_number = request.form.get("To", "")
    caller_number = request.form.get("From", "")
    message_body = request.form.get("Body", "").strip()

    client = get_client_by_twilio_number(twilio_number)
    if not client:
        log.warning("No client found for SMS destination: %s", twilio_number)
        return _twiml_sms("")

    log.info(
        "Incoming SMS from %s → %s (client: %s): %s",
        caller_number, twilio_number, client["business_name"], message_body,
    )

    # 1. Log lead to Google Sheets
    try:
        append_lead(
            spreadsheet_id=client["spreadsheet_id"],
            caller_number=caller_number,
            message=message_body,
            business_name=client["business_name"],
        )
    except Exception as exc:
        log.error("Failed to log lead to Sheets: %s", exc)

    # 2. Notify the business owner
    try:
        notify_owner(client=client, caller_number=caller_number, message=message_body)
    except Exception as exc:
        log.error("Failed to notify owner: %s", exc)

    # 3. Optionally send an acknowledgment back to the caller
    ack = client.get("ack_sms_message", "")
    return _twiml_sms(ack)


# ── TwiML helpers ─────────────────────────────────────────────────────────────

def _twiml_hangup() -> Response:
    return Response(
        '<?xml version="1.0" encoding="UTF-8"?><Response><Hangup/></Response>',
        mimetype="text/xml",
    )


def _twiml_reject() -> Response:
    return Response(
        '<?xml version="1.0" encoding="UTF-8"?><Response><Reject/></Response>',
        mimetype="text/xml",
    )


def _twiml_sms(body: str) -> Response:
    if body:
        xml = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            f"<Response><Message>{body}</Message></Response>"
        )
    else:
        xml = '<?xml version="1.0" encoding="UTF-8"?><Response/>'
    return Response(xml, mimetype="text/xml")


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    log.info("Starting Missed Call Lead Capture on port %d", port)
    app.run(host="0.0.0.0", port=port, debug=debug)
