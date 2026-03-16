"""
sms.py — Twilio SMS sending with retry logic
Automation Biz | v1.2

Retry strategy:
  - Up to 3 attempts
  - Exponential backoff: 1s, 2s, 4s
  - Only retries on transient Twilio errors (5xx, connection issues)
  - Does NOT retry on permanent failures (invalid number, unsubscribed, etc.)

Twilio error codes that are permanent (no retry):
  21211 — invalid 'To' number
  21610 — attempted to send to unsubscribed number
  21408 — permission to send to this region is not enabled
  30003 — unreachable destination handset
  30004 — message blocked
  30005 — unknown destination handset
  30006 — landline or unreachable carrier
"""

import os
import time
import logging

from twilio.rest import Client as TwilioClient
from twilio.base.exceptions import TwilioRestException

from logger import log_auto_sms_sent, log_auto_sms_failed

log = logging.getLogger("mclc.sms")

# Twilio error codes that mean "this number will never work" — don't retry
_PERMANENT_ERROR_CODES = {21211, 21610, 21408, 30003, 30004, 30005, 30006}

_MAX_ATTEMPTS = 3
_BACKOFF_BASE = 1.0   # seconds


def _get_client() -> TwilioClient:
    return TwilioClient(
        os.environ["TWILIO_ACCOUNT_SID"],
        os.environ["TWILIO_AUTH_TOKEN"],
    )


def send_sms(to: str, from_: str, body: str, client_id: str = "unknown") -> str:
    """
    Send an SMS via Twilio with retry on transient errors.

    Returns the Twilio message SID on success.
    Raises the final exception if all attempts fail.
    """
    last_exc = None

    for attempt in range(1, _MAX_ATTEMPTS + 1):
        try:
            twilio = _get_client()
            message = twilio.messages.create(to=to, from_=from_, body=body)
            log_auto_sms_sent(client_id=client_id, to=to, sid=message.sid)
            return message.sid

        except TwilioRestException as exc:
            last_exc = exc
            if exc.code in _PERMANENT_ERROR_CODES:
                log_auto_sms_failed(
                    client_id=client_id,
                    to=to,
                    reason=f"permanent_error code={exc.code} msg={exc.msg}",
                )
                raise  # No point retrying

            wait = _BACKOFF_BASE * (2 ** (attempt - 1))
            log.warning(
                "SMS attempt %d/%d failed (transient) | to=%s code=%s — retrying in %.0fs",
                attempt, _MAX_ATTEMPTS, to, exc.code, wait,
            )
            if attempt < _MAX_ATTEMPTS:
                time.sleep(wait)

        except Exception as exc:
            last_exc = exc
            wait = _BACKOFF_BASE * (2 ** (attempt - 1))
            log.warning(
                "SMS attempt %d/%d failed (unexpected) | to=%s err=%s — retrying in %.0fs",
                attempt, _MAX_ATTEMPTS, to, exc, wait,
            )
            if attempt < _MAX_ATTEMPTS:
                time.sleep(wait)

    log_auto_sms_failed(
        client_id=client_id,
        to=to,
        reason=f"all_{_MAX_ATTEMPTS}_attempts_failed last={last_exc}",
    )
    raise last_exc
