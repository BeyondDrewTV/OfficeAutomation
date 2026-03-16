"""
clients.py — Multi-client config loader

Reads clients.json and provides lookup by Twilio number.

clients.json schema per client:
  business_name   str   Display name of the business
  owner_phone     str   E.164 — receives SMS alerts
  owner_email     str   Receives email alerts
  twilio_number   str   E.164 — the Twilio number Twilio calls this webhook on
  spreadsheet_id  str   Google Sheets ID for lead logging
  sheet_name      str   Tab name (default: "Leads")
  voice_message   str   (optional) Override the default voice greeting
  auto_sms        str   (optional) Override the default auto-SMS text
"""

import json
import os
import logging
from typing import Optional

log = logging.getLogger(__name__)

_CLIENTS_FILE = os.path.join(os.path.dirname(__file__), "clients.json")
_cache: Optional[dict] = None


def _load() -> dict:
    global _cache
    if _cache is None:
        with open(_CLIENTS_FILE, "r") as f:
            _cache = json.load(f)
    return _cache


def get_client_by_twilio_number(twilio_number: str) -> Optional[dict]:
    """Return client config dict for the given Twilio number, or None."""
    clients = _load()
    for client_id, cfg in clients.items():
        if cfg.get("twilio_number") == twilio_number:
            return {**cfg, "client_id": client_id}
    log.warning("No client found for number: %s", twilio_number)
    return None


def get_all_clients() -> dict:
    return _load()


def reload() -> dict:
    """Force reload from disk (call after editing clients.json)."""
    global _cache
    _cache = None
    return _load()
