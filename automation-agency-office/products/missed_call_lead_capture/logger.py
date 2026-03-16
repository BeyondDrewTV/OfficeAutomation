"""
logger.py — Structured event logger for Missed Call Lead Capture
Automation Biz | v1.3

LOG FILE:  logs/app.log  (rotates at 5 MB, keeps 5 backups)
FORMAT:    2026-03-14 18:32:11 UTC | INFO  | event=incoming_call | client=abc | from=+1...

EVENT REFERENCE
───────────────────────────────────────────────────────────────────────────────
  startup                            server started
  incoming_call                      voice webhook received
  auto_sms_sent                      auto-SMS delivered to caller
  auto_sms_failed                    auto-SMS failed after retries
  sms_received                       inbound SMS webhook received
  lead_captured                      row written to Google Sheets
  lead_capture_failed                Sheets write failed
  owner_sms_sent                     owner SMS delivered
  owner_sms_failed                   owner SMS failed
  owner_email_sent                   owner email delivered
  owner_email_failed                 owner email failed
  request_rejected                   missing/invalid fields
  request_rejected_twilio_signature  HMAC signature check failed  ← NEW v1.3
  rate_limit_hit                     caller exceeded rate limit
  dedup_blocked                      duplicate auto-SMS suppressed ← NEW v1.3
  unknown_number                     Twilio number not in clients.json
  config_reloaded                    /reload succeeded
  config_reload_failed               /reload failed

TROUBLESHOOTING GREP REFERENCE
───────────────────────────────────────────────────────────────────────────────
  Auto-SMS never arrived?
    grep "auto_sms" logs/app.log

  Lead not in Sheets?
    grep "lead_capture" logs/app.log

  Owner not notified?
    grep "owner_sms_failed\|owner_email_failed" logs/app.log

  Signature rejections (scanning/spoofing attempts)?
    grep "twilio_signature" logs/app.log

  Duplicate SMS suppressed legitimately vs spam?
    grep "dedup_blocked" logs/app.log

  Number not routing to any client?
    grep "unknown_number" logs/app.log

  Rate-limit events for a specific number?
    grep "rate_limit_hit" logs/app.log | grep "+18155551234"
───────────────────────────────────────────────────────────────────────────────
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime, timezone
from typing import Optional

# ── Config ─────────────────────────────────────────────────────────────────
LOG_DIR   = os.path.join(os.path.dirname(__file__), "logs")
LOG_FILE  = os.path.join(LOG_DIR, "app.log")
LOG_LEVEL = logging.DEBUG if os.environ.get("FLASK_DEBUG") == "1" else logging.INFO

_FMT      = "%(asctime)s UTC | %(levelname)-5s | %(message)s"
_DATE_FMT = "%Y-%m-%d %H:%M:%S"


def _build_logger() -> logging.Logger:
    os.makedirs(LOG_DIR, exist_ok=True)

    lg = logging.getLogger("mclc")
    lg.setLevel(LOG_LEVEL)

    if lg.handlers:
        return lg

    fmt = logging.Formatter(_FMT, datefmt=_DATE_FMT)
    fmt.converter = lambda *_: datetime.now(timezone.utc).timetuple()

    ch = logging.StreamHandler()
    ch.setLevel(LOG_LEVEL)
    ch.setFormatter(fmt)
    lg.addHandler(ch)

    fh = RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=5)
    fh.setLevel(LOG_LEVEL)
    fh.setFormatter(fmt)
    lg.addHandler(fh)

    lg.propagate = False
    return lg


# Module-level singleton — import `logger` or the typed helpers below
logger = _build_logger()


# ── Key=value formatter ────────────────────────────────────────────────────

def _fmt(**kwargs) -> str:
    return " | ".join(f"{k}={v}" for k, v in kwargs.items() if v is not None)


# ── Typed event helpers ────────────────────────────────────────────────────

def log_startup(port: int, client_count: int):
    logger.info(_fmt(event="startup", port=port, clients=client_count))


def log_incoming_call(client_id: str, to: str, from_: str, call_sid: str):
    logger.info(_fmt(event="incoming_call", client=client_id, to=to, from_=from_, call_sid=call_sid))


def log_auto_sms_sent(client_id: str, to: str, sid: str):
    logger.info(_fmt(event="auto_sms_sent", client=client_id, to=to, sid=sid))


def log_auto_sms_failed(client_id: str, to: str, reason: str):
    logger.error(_fmt(event="auto_sms_failed", client=client_id, to=to, reason=reason))


def log_sms_received(client_id: str, to: str, from_: str, sms_sid: str):
    logger.info(_fmt(event="sms_received", client=client_id, to=to, from_=from_, sid=sms_sid))


def log_lead_captured(client_id: str, caller: str, sheet: str):
    logger.info(_fmt(event="lead_captured", client=client_id, caller=caller, sheet=sheet))


def log_lead_capture_failed(client_id: str, caller: str, reason: str):
    logger.error(_fmt(event="lead_capture_failed", client=client_id, caller=caller, reason=reason))


def log_owner_sms_sent(client_id: str, to: str):
    logger.info(_fmt(event="owner_sms_sent", client=client_id, to=to))


def log_owner_sms_failed(client_id: str, to: str, reason: str):
    logger.error(_fmt(event="owner_sms_failed", client=client_id, to=to, reason=reason))


def log_owner_email_sent(client_id: str, to: str):
    logger.info(_fmt(event="owner_email_sent", client=client_id, to=to))


def log_owner_email_failed(client_id: str, to: str, reason: str):
    logger.error(_fmt(event="owner_email_failed", client=client_id, to=to, reason=reason))


def log_request_rejected(route: str, reason: str, detail: Optional[str] = None):
    logger.warning(_fmt(event="request_rejected", route=route, reason=reason, detail=detail))


def log_signature_rejected(route: str, from_: Optional[str] = None):
    """X-Twilio-Signature HMAC validation failed — likely spoofed or misconfigured."""
    logger.warning(_fmt(event="request_rejected_twilio_signature", route=route, from_=from_))


def log_rate_limit_hit(from_: str, route: str):
    logger.warning(_fmt(event="rate_limit_hit", from_=from_, route=route))


def log_dedup_blocked(from_: str, route: str, seconds_remaining: float):
    """Auto-SMS suppressed because one was already sent to this number recently."""
    logger.info(_fmt(event="dedup_blocked", from_=from_, route=route,
                     retry_in=f"{seconds_remaining:.0f}s"))


def log_unknown_number(number: str, route: str):
    logger.warning(_fmt(event="unknown_number", number=number, route=route))
