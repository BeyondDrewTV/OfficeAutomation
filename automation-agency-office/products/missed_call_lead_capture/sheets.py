"""
sheets.py — Google Sheets integration

Public API:
  append_lead(client, lead)          → append a lead row during live operation
  ensure_sheet_tab_exists(sid, name) → called by install_client.py at onboarding

Auth: service account JSON key file.
Set GOOGLE_SERVICE_ACCOUNT_FILE env var, or place service_account.json here.
"""

import os
import logging

from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

log = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

_HEADERS = [
    "Timestamp (UTC)",
    "Caller Number",
    "Message",
    "Status",
    "Business Name",
    "Client ID",
]


# ── Internal ───────────────────────────────────────────────────────────────

def _get_service():
    key_file = os.environ.get(
        "GOOGLE_SERVICE_ACCOUNT_FILE",
        os.path.join(os.path.dirname(__file__), "service_account.json"),
    )
    creds = Credentials.from_service_account_file(key_file, scopes=SCOPES)
    return build("sheets", "v4", credentials=creds, cache_discovery=False)


def _get_existing_sheet_names(service, spreadsheet_id: str) -> list[str]:
    meta = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    return [s["properties"]["title"] for s in meta.get("sheets", [])]


def _write_headers(service, spreadsheet_id: str, sheet_name: str):
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"{sheet_name}!A1",
        valueInputOption="RAW",
        body={"values": [_HEADERS]},
    ).execute()
    log.info("Header row written | sheet=%s", sheet_name)


# ── Public: onboarding ─────────────────────────────────────────────────────

def ensure_sheet_tab_exists(spreadsheet_id: str, sheet_name: str) -> bool:
    """
    Called once during client onboarding (install_client.py).

    - If the named tab already exists: no-op, returns False.
    - If it doesn't exist: creates the tab and writes the header row,
      returns True.

    Raises on any API / auth error so install_client.py can surface it
    before writing clients.json.
    """
    service = _get_service()
    existing = _get_existing_sheet_names(service, spreadsheet_id)

    if sheet_name in existing:
        log.info("Sheet tab already exists: %s", sheet_name)
        return False

    # Add the new tab
    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "requests": [
                {"addSheet": {"properties": {"title": sheet_name}}}
            ]
        },
    ).execute()
    log.info("Sheet tab created: %s", sheet_name)

    _write_headers(service, spreadsheet_id, sheet_name)
    return True


# ── Public: live operation ─────────────────────────────────────────────────

def append_lead(client: dict, lead: dict):
    """Append one lead row to the client's Google Sheet tab."""
    spreadsheet_id = client.get("spreadsheet_id")
    sheet_name     = client.get("sheet_name", "Leads")

    if not spreadsheet_id:
        raise ValueError(
            f"Client {client.get('client_id')} has no spreadsheet_id configured."
        )

    service = _get_service()

    # Safety net: ensure tab + headers exist before every append.
    # This is a cheap metadata read and handles edge cases gracefully.
    existing = _get_existing_sheet_names(service, spreadsheet_id)
    if sheet_name not in existing:
        log.warning("Tab '%s' missing at append time — creating now", sheet_name)
        service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={"requests": [{"addSheet": {"properties": {"title": sheet_name}}}]},
        ).execute()
        _write_headers(service, spreadsheet_id, sheet_name)
    else:
        # Check headers present (A1 empty = headers missing)
        result = (
            service.spreadsheets()
            .values()
            .get(spreadsheetId=spreadsheet_id, range=f"{sheet_name}!A1:F1")
            .execute()
        )
        if not result.get("values"):
            _write_headers(service, spreadsheet_id, sheet_name)

    row = [
        lead.get("timestamp", ""),
        lead.get("caller_number", ""),
        lead.get("message", ""),
        lead.get("status", "new"),
        lead.get("business_name", ""),
        lead.get("client_id", ""),
    ]

    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=f"{sheet_name}!A1",
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body={"values": [row]},
    ).execute()

    log.info("Lead appended | sheet=%s caller=%s", sheet_name, lead.get("caller_number"))
