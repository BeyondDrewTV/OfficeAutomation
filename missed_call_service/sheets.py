"""
sheets.py — Google Sheets integration for Missed Call Lead Capture.

Each client gets their own tab (sheet_name) in a shared Google Spreadsheet.
Columns: timestamp | caller_number | message | status

Setup:
1. Create a Google Cloud service account with Sheets API access.
2. Download the JSON key, place it at: missed_call_service/clients/google_creds.json
3. Create a Google Sheet and share it with the service account email (Editor).
4. Set GOOGLE_SHEET_ID in .env
"""
from __future__ import annotations

import logging
import os
from pathlib import Path

log = logging.getLogger("missed_call.sheets")

CREDS_PATH = Path(__file__).parent / "clients" / "google_creds.json"
SHEET_COLUMNS = ["timestamp", "caller_number", "message", "status"]


def _get_service():
    """Return an authenticated Google Sheets service object."""
    try:
        from google.oauth2.service_account import Credentials
        from googleapiclient.discovery import build
    except ImportError:
        raise RuntimeError(
            "google-api-python-client not installed. "
            "Run: pip install google-api-python-client google-auth"
        )

    if not CREDS_PATH.exists():
        raise FileNotFoundError(
            f"Google credentials not found at {CREDS_PATH}. "
            "See SETUP_MISSED_CALL.md for instructions."
        )

    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(str(CREDS_PATH), scopes=scopes)
    return build("sheets", "v4", credentials=creds, cache_discovery=False)


def get_or_create_sheet(service, spreadsheet_id: str, sheet_name: str) -> None:
    """Ensure a sheet tab with `sheet_name` exists, creating it if needed."""
    meta = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    existing = [s["properties"]["title"] for s in meta.get("sheets", [])]
    if sheet_name not in existing:
        body = {"requests": [{"addSheet": {"properties": {"title": sheet_name}}}]}
        service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id, body=body
        ).execute()
        log.info("Created sheet tab: %s", sheet_name)
        # Write header row
        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=f"{sheet_name}!A1",
            valueInputOption="RAW",
            body={"values": [SHEET_COLUMNS]},
        ).execute()


def append_lead(client_id: str, sheet_name: str, row: dict) -> None:
    """
    Append one lead row to the Google Sheet tab for this client.

    row keys: timestamp, caller_number, message, status
    """
    spreadsheet_id = os.getenv("GOOGLE_SHEET_ID", "")
    if not spreadsheet_id:
        log.warning("GOOGLE_SHEET_ID not set — skipping Sheets logging.")
        return

    try:
        service = _get_service()
        get_or_create_sheet(service, spreadsheet_id, sheet_name)

        values = [[row.get(col, "") for col in SHEET_COLUMNS]]
        service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=f"{sheet_name}!A1",
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body={"values": values},
        ).execute()
        log.info("Lead logged to Sheets [%s]: %s", sheet_name, row.get("caller_number"))
    except Exception as exc:
        log.error("Sheets error for client %s: %s", client_id, exc)
        raise
