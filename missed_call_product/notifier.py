"""
notifier.py — Owner notification: SMS or Email
Reads client config to decide which channel to use.
"""
from __future__ import annotations

import logging
import os
import smtplib
from email.message import EmailMessage

from sms import send_sms

log = logging.getLogger("missed_call")


def notify_owner(client: dict, caller_number: str, message: str) -> None:
    """Notify the business owner via their preferred channel."""
    channel = client.get("notification_channel", "sms").lower()

    if channel == "email":
        _notify_via_email(client, caller_number, message)
    else:
        _notify_via_sms(client, caller_number, message)


def _notify_via_sms(client: dict, caller_number: str, message: str) -> None:
    owner_phone = client.get("owner_phone", "").strip()
    twilio_number = client.get("twilio_number", "").strip()
    business_name = client.get("business_name", "your business")

    if not owner_phone:
        log.warning("No owner_phone set for %s — skipping SMS notification", business_name)
        return

    body = (
        f"[{business_name}] New lead from {caller_number}:\n"
        f"\"{message}\"\n"
        f"Reply to this number to reach them."
    )
    send_sms(to=owner_phone, from_=twilio_number, body=body)
    log.info("Owner notified via SMS: %s", owner_phone)


def _notify_via_email(client: dict, caller_number: str, message: str) -> None:
    owner_email = client.get("owner_email", "").strip()
    business_name = client.get("business_name", "your business")

    if not owner_email:
        log.warning("No owner_email set for %s — skipping email notification", business_name)
        return

    sender = os.getenv("GMAIL_ADDRESS", "").strip()
    app_password = os.getenv("GMAIL_APP_PASSWORD", "").strip()

    if not sender or not app_password:
        raise RuntimeError("GMAIL_ADDRESS and GMAIL_APP_PASSWORD must be set for email notifications.")

    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = owner_email
    msg["Subject"] = f"[{business_name}] New lead from {caller_number}"
    msg.set_content(
        f"You received a new lead via your missed call capture system.\n\n"
        f"Caller: {caller_number}\n"
        f"Message: {message}\n\n"
        f"Reply directly to their number to follow up."
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, app_password)
        smtp.send_message(msg)

    log.info("Owner notified via email: %s", owner_email)
