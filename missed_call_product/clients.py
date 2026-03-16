"""
clients.py — Multi-client config loader
Reads clients.json from the same directory as this file.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Optional

log = logging.getLogger("missed_call")

_CLIENTS_FILE = Path(__file__).resolve().parent / "clients.json"
_clients_cache: Optional[dict] = None


def _load_clients() -> dict:
    global _clients_cache
    if _clients_cache is not None:
        return _clients_cache
    if not _CLIENTS_FILE.exists():
        raise FileNotFoundError(
            f"clients.json not found at {_CLIENTS_FILE}. "
            "Copy clients.example.json to clients.json and fill in your client data."
        )
    with _CLIENTS_FILE.open("r", encoding="utf-8") as f:
        _clients_cache = json.load(f)
    log.info("Loaded %d client(s) from clients.json", len(_clients_cache))
    return _clients_cache


def get_client_by_twilio_number(twilio_number: str) -> Optional[dict]:
    """Return the client config dict whose twilio_number matches, or None."""
    # Normalize: strip spaces, ensure E.164 format
    number = twilio_number.strip()
    clients = _load_clients()
    for client_id, config in clients.items():
        if config.get("twilio_number", "").strip() == number:
            return {"client_id": client_id, **config}
    return None


def get_all_clients() -> dict:
    return _load_clients()


def reload_clients() -> None:
    """Force a re-read of clients.json (useful for hot-reloading without restart)."""
    global _clients_cache
    _clients_cache = None
    _load_clients()
