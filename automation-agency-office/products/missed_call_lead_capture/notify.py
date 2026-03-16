"""
notify.py — Owner notification via SMS and Email
Automation Biz | v1.2

Both channels attempted independently.
Owner SMS uses same retry logic as sms.py (via shared _send_with_retry).
Email uses a single attempt — SMTP failures are logged and do not block.
"""

import os
import time
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from twilio.rest import Client as TwilioClient
from twilio.base.exceptions import TwilioRestException

from logger import (
    log_owner_sms_sent,
    log_owner_sms_failed,
    log_owner_email_sent,
    log_owner_email_failed,
)

log = logging.getLogger("mclc.notify")

_PERMANENT_ERROR_CODES = {21211, 21610, 21408, 30003, 30004, 30005, 30006}
_MAX_ATTEMPTS = 3
_BACKOFF_BASE = 1.0


# ── Public ─────────────────────────────────────────────────────────────────

def notify_owner(client: dict, lead: dict):
    """Fire SMS + email notifications to the business owner. Non-blocking."""
    client_id     = client.get("client_id", "unknown")
    owner_phone   = client.get("owner_phone")
    owner_email   = client.get("owner_email")
    twilio_number = client.get("twilio_number")
    business_name = client.get("business_name", "Your Business")

    caller    = lead.get("caller_number", "Unknown")
    message   = lead.get("message", "(no message)")
    timestamp = lead.get("timestamp", "")

    if owner_phone and twilio_number:
        body = (
            f"🔔 NEW LEAD — {business_name}\n"
            f"Caller: {caller}\n"
            f"Message: {message}\n"
            f"→ Call or text them back directly."
        )
        try:
            _send_owner_sms_with_retry(
                client_id=client_id,
                to=owner_phone,
                from_=twilio_number,
                body=body,
            )
        except Exception as exc:
            log_owner_sms_failed(client_id=client_id, to=owner_phone, reason=str(exc))
    else:
        log.info("Owner SMS skipped | client=%s reason=owner_phone_or_twilio_number_missing", client_id)

    if owner_email:
        try:
            _send_owner_email(
                client_id=client_id,
                to=owner_email,
                business=business_name,
                caller=caller,
                message=message,
                timestamp=timestamp,
            )
        except Exception as exc:
            log_owner_email_failed(client_id=client_id, to=owner_email, reason=str(exc))
    else:
        log.info("Owner email skipped | client=%s reason=owner_email_not_set", client_id)


# ── Owner SMS with retry ───────────────────────────────────────────────────

def _send_owner_sms_with_retry(client_id: str, to: str, from_: str, body: str):
    last_exc = None

    for attempt in range(1, _MAX_ATTEMPTS + 1):
        try:
            twilio = TwilioClient(
                os.environ["TWILIO_ACCOUNT_SID"],
                os.environ["TWILIO_AUTH_TOKEN"],
            )
            twilio.messages.create(to=to, from_=from_, body=body)
            log_owner_sms_sent(client_id=client_id, to=to)
            return

        except TwilioRestException as exc:
            last_exc = exc
            if exc.code in _PERMANENT_ERROR_CODES:
                raise TwilioRestException(
                    status=exc.status,
                    uri=exc.uri,
                    msg=f"permanent_error code={exc.code}",
                    code=exc.code,
                )
            wait = _BACKOFF_BASE * (2 ** (attempt - 1))
            log.warning(
                "Owner SMS attempt %d/%d failed | client=%s code=%s — retry in %.0fs",
                attempt, _MAX_ATTEMPTS, client_id, exc.code, wait,
            )
            if attempt < _MAX_ATTEMPTS:
                time.sleep(wait)

        except Exception as exc:
            last_exc = exc
            wait = _BACKOFF_BASE * (2 ** (attempt - 1))
            log.warning(
                "Owner SMS attempt %d/%d failed | client=%s err=%s — retry in %.0fs",
                attempt, _MAX_ATTEMPTS, client_id, exc, wait,
            )
            if attempt < _MAX_ATTEMPTS:
                time.sleep(wait)

    raise last_exc


# ── Owner email ────────────────────────────────────────────────────────────

def _send_owner_email(
    client_id: str, to: str, business: str,
    caller: str, message: str, timestamp: str,
):
    smtp_host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_user = os.environ["SMTP_USER"]
    smtp_pass = os.environ["SMTP_PASS"]

    subject = f"🚨 Missed Call Lead — {business} — {caller}"

    html = f"""
    <div style="font-family:Arial,sans-serif;max-width:520px;margin:0 auto">
      <div style="background:#e05c24;color:#fff;padding:16px 24px;border-radius:8px 8px 0 0">
        <h2 style="margin:0;font-size:18px">🔔 Missed Call Lead</h2>
        <p style="margin:4px 0 0;opacity:.85;font-size:14px">{business}</p>
      </div>
      <div style="background:#f8f7f4;padding:24px;border:1px solid #e5e7eb;
                  border-top:none;border-radius:0 0 8px 8px">
        <table style="width:100%;border-collapse:collapse;font-size:14px">
          <tr>
            <td style="padding:9px 0;color:#6b7280;width:120px;vertical-align:top">Caller</td>
            <td style="padding:9px 0;font-weight:600">{caller}</td>
          </tr>
          <tr>
            <td style="padding:9px 0;color:#6b7280;vertical-align:top">Message</td>
            <td style="padding:9px 0">{message}</td>
          </tr>
          <tr>
            <td style="padding:9px 0;color:#6b7280;vertical-align:top">Time</td>
            <td style="padding:9px 0;color:#6b7280">{timestamp}</td>
          </tr>
        </table>
        <div style="margin-top:18px;padding:12px 16px;background:#fff3cd;
                    border-left:4px solid #f59e0b;border-radius:4px;font-size:13px">
          ⚡ <strong>Reply within 15 minutes</strong> to maximise your chance
          of winning the job. Call or text <strong>{caller}</strong> directly.
        </div>
      </div>
    </div>
    """

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = smtp_user
    msg["To"]      = to
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.ehlo()
        server.starttls()
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, to, msg.as_string())

    log_owner_email_sent(client_id=client_id, to=to)
