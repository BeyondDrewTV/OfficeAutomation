"""
sheets.py — Google Sheets lead logging
Appends a lead row to the client's designated spreadsheet.

Sheet columns: timestamp | caller_number | message | status | business_name
"""
from __future__ import annotations

import logging
import os
from datetime import datetime, timezone
from typing import Optional

log = logging.getLogger("missed_call")


def _get_service():
    """Build and return an authenticated Google Sheets service object."""
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError:
        raise ImportError(
            "google-api-python-client and google-auth are required. "
            "Run: pip install google-api-python-client google-auth"
        )

    creds_file = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "service_account.json")
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = service_account.Credentials.from_service_account_file(creds_file, scopes=scopes)
    return build("sheets", "v4", credentials=creds, cache_discovery=False)


def append_lead(
    spreadsheet_id: str,
    caller_number: str,
    message: str,
    business_name: str,
    status: str = "new",
    sheet_name: str = "Leads",
) -> None:
    """Append one lead row to the Google Sheet."""
    if not spreadsheet_id:
        log.warning("No spreadsheet_id configured for client %s — skipping Sheets log", business_name)
        return

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    row = [[timestamp, caller_number, message, status, business_name]]
    range_ = f"{sheet_name}!A:E"

    try:
        service = _get_service()
        service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=range_,
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body={"values": row},
        ).execute()
        log.info("Lead logged to Sheets: %s | %s", business_name, caller_number)
    except Exception as exc:
        log.error("Sheets append failed: %s", exc)
        raise


def ensure_header_row(spreadsheet_id: str, sheet_name: str = "Leads") -> None:
    """Write the header row if the sheet is empty. Call once during onboarding."""
    service = _get_service()
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=f"{sheet_name}!A1:E1",
    ).execute()
    existing = result.get("values", [])
    if not existing:
        headers = [["Timestamp", "Caller Number", "Message", "Status", "Business"]]
        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=f"{sheet_name}!A1",
            valueInputOption="RAW",
            body={"values": headers},
        ).execute()
        log.info("Header row written to sheet: %s", sheet_name)
