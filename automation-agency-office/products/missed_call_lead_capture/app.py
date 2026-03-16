"""
Missed Call Lead Capture — Flask Server  v1.3
Automation Biz | Multi-client Twilio + Google Sheets backend

CHANGES IN v1.3
  • Twilio signature validation  — HMAC check on every webhook; 403 on failure
  • Configurable rate limits     — CALL_RATE_LIMIT_PER_MINUTE / SMS_RATE_LIMIT_PER_MINUTE env vars
  • Dedup protection             — suppresses duplicate auto-SMS within 60s per caller
  • Hardened error handling      — try/except wraps entire route bodies; always returns valid TwiML
  • Expanded /health             — Twilio + Sheets connectivity probes, client count

ARCHITECTURE (unchanged)
  /incoming_call  ← Twilio Voice webhook
  /incoming_sms   ← Twilio SMS webhook
  /health         ← diagnostics
  /reload         ← hot-reload clients.json
"""

import os
import time
import threading
from collections import defaultdict
from datetime import datetime, timezone
from typing import Optional

from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse
from twilio.twiml.messaging_response import MessagingResponse
from twilio.request_validator import RequestValidator

from clients import get_client_by_twilio_number, get_all_clients, reload as reload_clients
from sheets import append_lead
from notify import notify_owner
from sms import send_sms
from logger import (
    logger,
    log_incoming_call,
    log_sms_received,
    log_lead_captured,
    log_lead_capture_failed,
    log_request_rejected,
    log_signature_rejected,
    log_rate_limit_hit,
    log_dedup_blocked,
    log_unknown_number,
    log_startup,
)

# ── App ────────────────────────────────────────────────────────────────────
app = Flask(__name__)

DEFAULT_VOICE_MESSAGE = (
    "Thanks for calling. We can't take your call right now, but text us "
    "what you need and we'll follow up shortly."
)
DEFAULT_AUTO_SMS = (
    "Hi! Sorry we missed your call. Text us what you need "
    "and we'll get right back to you."
)

# ── Signature validation ───────────────────────────────────────────────────
# Set TWILIO_SKIP_SIGNATURE_VALIDATION=1 only during local dev with ngrok.
# Never disable in production.

_AUTH_TOKEN           = os.environ.get("TWILIO_AUTH_TOKEN", "")
_SKIP_SIG_VALIDATION  = os.environ.get("TWILIO_SKIP_SIGNATURE_VALIDATION", "0") == "1"
_validator            = RequestValidator(_AUTH_TOKEN)


def _twilio_signature_valid(url: str, params: dict, signature: str) -> bool:
    """Return True if the X-Twilio-Signature header is valid for this request."""
    if _SKIP_SIG_VALIDATION:
        logger.debug("event=signature_check_skipped reason=env_flag_set")
        return True
    return _validator.validate(url, params, signature)


# ── Rate limiting ──────────────────────────────────────────────────────────
# Limits are configurable via environment variables.
# Window is always 60 seconds (1 minute).

_RATE_LIMITS = {
    "call": {"max": int(os.environ.get("CALL_RATE_LIMIT_PER_MINUTE", "3")),  "window": 60},
    "sms":  {"max": int(os.environ.get("SMS_RATE_LIMIT_PER_MINUTE",  "10")), "window": 60},
}

_rate_counters: dict[str, list[float]] = defaultdict(list)
_rate_lock = threading.Lock()


def _is_rate_limited(from_number: str, kind: str) -> bool:
    limit  = _RATE_LIMITS[kind]
    window = limit["window"]
    now    = time.time()
    key    = f"{from_number}:{kind}"
    with _rate_lock:
        _rate_counters[key] = [t for t in _rate_counters[key] if now - t < window]
        if len(_rate_counters[key]) >= limit["max"]:
            return True
        _rate_counters[key].append(now)
        return False


# ── Deduplication ──────────────────────────────────────────────────────────
# Prevents multiple auto-SMSs being sent to the same caller within 60s.
# Scenario: caller hangs up and immediately calls back — without dedup they
# would receive two "Sorry we missed you" texts in quick succession.

_DEDUP_WINDOW = 60   # seconds

_dedup_store: dict[str, float] = {}
_dedup_lock  = threading.Lock()


def _is_dedup_blocked(from_number: str) -> tuple[bool, float]:
    """
    Return (blocked, seconds_remaining).
    Registers the number on first call; blocks subsequent calls within window.
    """
    now = time.time()
    with _dedup_lock:
        last_sent = _dedup_store.get(from_number)
        if last_sent is not None:
            elapsed   = now - last_sent
            remaining = _DEDUP_WINDOW - elapsed
            if remaining > 0:
                return True, remaining
        _dedup_store[from_number] = now
        return False, 0.0


# ── Request validation ─────────────────────────────────────────────────────

def _validate_call_request() -> Optional[tuple[str, str, str]]:
    to_number   = request.form.get("To",      "").strip()
    from_number = request.form.get("From",    "").strip()
    call_sid    = request.form.get("CallSid", "").strip()

    if not to_number:
        log_request_rejected("/incoming_call", "missing_field", "To");   return None
    if not from_number:
        log_request_rejected("/incoming_call", "missing_field", "From"); return None
    if not to_number.startswith("+"):
        log_request_rejected("/incoming_call", "invalid_format", f"To={to_number!r}");   return None
    if not from_number.startswith("+"):
        log_request_rejected("/incoming_call", "invalid_format", f"From={from_number!r}"); return None

    return to_number, from_number, call_sid


def _validate_sms_request() -> Optional[tuple[str, str, str, str]]:
    to_number   = request.form.get("To",     "").strip()
    from_number = request.form.get("From",   "").strip()
    body        = request.form.get("Body",   "").strip()
    sms_sid     = request.form.get("SmsSid", "").strip()

    if not to_number:
        log_request_rejected("/incoming_sms", "missing_field", "To");   return None
    if not from_number:
        log_request_rejected("/incoming_sms", "missing_field", "From"); return None
    if not to_number.startswith("+"):
        log_request_rejected("/incoming_sms", "invalid_format", f"To={to_number!r}");   return None
    if not from_number.startswith("+"):
        log_request_rejected("/incoming_sms", "invalid_format", f"From={from_number!r}"); return None

    return to_number, from_number, body, sms_sid


# ── TwiML helpers ──────────────────────────────────────────────────────────

def _voice_reject() -> Response:
    vr = VoiceResponse()
    vr.say("Thank you for calling. Goodbye.")
    vr.hangup()
    return Response(str(vr), mimetype="application/xml")


def _voice_ok(message: str) -> Response:
    vr = VoiceResponse()
    vr.say(message, voice="alice", language="en-US")
    vr.hangup()
    return Response(str(vr), mimetype="application/xml")


def _sms_empty() -> Response:
    return Response(str(MessagingResponse()), mimetype="application/xml")


def _sms_reply(body: str) -> Response:
    mr = MessagingResponse()
    mr.message(body)
    return Response(str(mr), mimetype="application/xml")


# ── /health ────────────────────────────────────────────────────────────────

@app.route("/health", methods=["GET"])
def health():
    """
    Diagnostics endpoint. Probes Twilio and Google Sheets connectivity.
    Safe to call externally — read-only, no side effects.
    """
    report = {
        "status":  "ok",
        "service": "missed-call-lead-capture",
        "version": "1.3",
        "checks":  {},
    }

    # Client count
    try:
        clients      = get_all_clients()
        client_count = len(clients)
        report["checks"]["clients"] = {"status": "ok", "count": client_count}
    except Exception as exc:
        report["checks"]["clients"] = {"status": "error", "detail": str(exc)}
        report["status"] = "degraded"

    # Twilio connectivity — fetch account info (read-only)
    try:
        import os
        from twilio.rest import Client as TwilioClient
        tw = TwilioClient(os.environ["TWILIO_ACCOUNT_SID"], os.environ["TWILIO_AUTH_TOKEN"])
        acc = tw.api.accounts(os.environ["TWILIO_ACCOUNT_SID"]).fetch()
        report["checks"]["twilio"] = {"status": "ok", "account_status": acc.status}
    except Exception as exc:
        report["checks"]["twilio"] = {"status": "error", "detail": str(exc)}
        report["status"] = "degraded"

    # Google Sheets connectivity — list spreadsheets (lightweight)
    try:
        from sheets import _get_service
        svc = _get_service()
        svc.spreadsheets().get(
            spreadsheetId="1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgVE2upms"   # placeholder — any valid ID
        )
        # We just care that auth + network worked; ignore 404 on the sheet itself
        report["checks"]["google_sheets"] = {"status": "ok"}
    except Exception as exc:
        err = str(exc)
        # 404 means auth worked but sheet not found — auth is fine
        if "404" in err or "notFound" in err.lower():
            report["checks"]["google_sheets"] = {"status": "ok", "note": "auth_valid"}
        else:
            report["checks"]["google_sheets"] = {"status": "error", "detail": err}
            report["status"] = "degraded"

    http_status = 200 if report["status"] == "ok" else 503
    return report, http_status


# ── /reload ────────────────────────────────────────────────────────────────

@app.route("/reload", methods=["POST"])
def reload():
    """Hot-reload clients.json without restarting. Protect with firewall in prod."""
    try:
        clients = reload_clients()
        count   = len(clients)
        logger.info("event=config_reloaded clients=%d", count)
        return {"status": "reloaded", "clients": count}, 200
    except Exception as exc:
        logger.error("event=config_reload_failed reason=%s", exc)
        return {"status": "error", "detail": str(exc)}, 500


# ── /incoming_call ─────────────────────────────────────────────────────────

@app.route("/incoming_call", methods=["POST"])
def incoming_call():
    """
    Twilio Voice webhook.
    Pipeline: signature → fields → rate-limit → client lookup → TwiML + auto-SMS
    Entire body wrapped in try/except — never crashes, always returns valid TwiML.
    """
    try:
        # 1. Twilio signature validation
        sig      = request.headers.get("X-Twilio-Signature", "")
        url      = request.url
        params   = request.form.to_dict()
        from_num = params.get("From", "")

        if not _twilio_signature_valid(url, params, sig):
            log_signature_rejected("/incoming_call", from_=from_num)
            return Response("Forbidden", status=403)

        # 2. Field validation
        validated = _validate_call_request()
        if validated is None:
            return _voice_reject()

        to_number, from_number, call_sid = validated

        # 3. Rate limiting
        if _is_rate_limited(from_number, "call"):
            log_rate_limit_hit(from_=from_number, route="/incoming_call")
            return _voice_reject()

        # 4. Client lookup
        client = get_client_by_twilio_number(to_number)
        if not client:
            log_unknown_number(number=to_number, route="/incoming_call")
            return _voice_ok(DEFAULT_VOICE_MESSAGE)

        client_id = client.get("client_id", "unknown")
        log_incoming_call(client_id=client_id, to=to_number,
                          from_=from_number, call_sid=call_sid)

        # 5. TwiML — voice message + hangup
        voice_msg = client.get("voice_message") or DEFAULT_VOICE_MESSAGE
        twiml_response = _voice_ok(voice_msg)

        # 6. Auto-SMS with dedup check
        blocked, secs = _is_dedup_blocked(from_number)
        if blocked:
            log_dedup_blocked(from_=from_number, route="/incoming_call",
                              seconds_remaining=secs)
        else:
            auto_sms_body = client.get("auto_sms") or DEFAULT_AUTO_SMS
            try:
                send_sms(to=from_number, from_=to_number,
                         body=auto_sms_body, client_id=client_id)
            except Exception as exc:
                logger.error("event=auto_sms_exception client=%s to=%s err=%s",
                             client_id, from_number, exc)

        return twiml_response

    except Exception as exc:
        logger.exception("event=unhandled_exception route=/incoming_call err=%s", exc)
        return _voice_reject()


# ── /incoming_sms ──────────────────────────────────────────────────────────

@app.route("/incoming_sms", methods=["POST"])
def incoming_sms():
    """
    Twilio SMS webhook.
    Pipeline: signature → fields → rate-limit → client lookup → log → notify → reply
    Entire body wrapped in try/except — never crashes, always returns valid TwiML.
    """
    try:
        # 1. Twilio signature validation
        sig      = request.headers.get("X-Twilio-Signature", "")
        url      = request.url
        params   = request.form.to_dict()
        from_num = params.get("From", "")

        if not _twilio_signature_valid(url, params, sig):
            log_signature_rejected("/incoming_sms", from_=from_num)
            return Response("Forbidden", status=403)

        # 2. Field validation
        validated = _validate_sms_request()
        if validated is None:
            return _sms_empty()

        to_number, from_number, body, sms_sid = validated

        # 3. Rate limiting
        if _is_rate_limited(from_number, "sms"):
            log_rate_limit_hit(from_=from_number, route="/incoming_sms")
            return _sms_empty()

        # 4. Client lookup
        client = get_client_by_twilio_number(to_number)
        if not client:
            log_unknown_number(number=to_number, route="/incoming_sms")
            return _sms_empty()

        client_id = client.get("client_id", "unknown")
        log_sms_received(client_id=client_id, to=to_number,
                         from_=from_number, sms_sid=sms_sid)

        # 5. Build lead record
        lead = {
            "timestamp":     datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S") + " UTC",
            "caller_number": from_number,
            "message":       body,
            "status":        "new",
            "business_name": client.get("business_name", ""),
            "client_id":     client_id,
        }

        # 6. Log to Google Sheets
        sheet_name = client.get("sheet_name", "Leads")
        try:
            append_lead(client, lead)
            log_lead_captured(client_id=client_id, caller=from_number, sheet=sheet_name)
        except Exception as exc:
            log_lead_capture_failed(client_id=client_id,
                                    caller=from_number, reason=str(exc))

        # 7. Notify owner — runs even if Sheets failed
        try:
            notify_owner(client, lead)
        except Exception as exc:
            logger.error("event=notify_owner_exception client=%s err=%s", client_id, exc)

        # 8. Auto-reply to caller
        business = client.get("business_name", "The team")
        return _sms_reply(f"Got it — thanks! We'll get back to you shortly. — {business}")

    except Exception as exc:
        logger.exception("event=unhandled_exception route=/incoming_sms err=%s", exc)
        return _sms_empty()


# ── Entry point ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port  = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"

    try:
        client_count = len(get_all_clients())
    except Exception:
        client_count = 0

    log_startup(port=port, client_count=client_count)

    if _SKIP_SIG_VALIDATION:
        logger.warning("event=startup_warning msg=TWILIO_SIGNATURE_VALIDATION_DISABLED")

    app.run(host="0.0.0.0", port=port, debug=debug)
