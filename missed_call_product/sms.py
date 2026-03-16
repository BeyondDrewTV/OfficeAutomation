"""
sms.py — Twilio SMS wrapper
"""
from __future__ import annotations

import logging
import os

log = logging.getLogger("missed_call")


def _get_twilio_client():
    try:
        from twilio.rest import Client
    except ImportError:
        raise ImportError("twilio is required. Run: pip install twilio")

    account_sid = os.getenv("TWILIO_ACCOUNT_SID", "").strip()
    auth_token = os.getenv("TWILIO_AUTH_TOKEN", "").strip()

    if not account_sid or not auth_token:
        raise RuntimeError(
            "TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN must be set in .env"
        )
    from twilio.rest import Client
    return Client(account_sid, auth_token)


def send_sms(to: str, from_: str, body: str) -> str:
    """Send an SMS via Twilio. Returns the message SID."""
    client = _get_twilio_client()
    msg = client.messages.create(to=to, from_=from_, body=body)
    log.info("SMS sent: SID=%s to=%s", msg.sid, to)
    return msg.sid
