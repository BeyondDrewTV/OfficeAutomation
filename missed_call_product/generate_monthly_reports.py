"""
generate_monthly_reports.py — Monthly lead summary for each client
===================================================================
For each client in clients.json:
  1. Pull all leads from their Google Sheet for the previous calendar month.
  2. Calculate: total leads, unique callers, sample messages (first 3).
  3. Send a plain-text summary email to owner_email.
  4. Log a report_sent event.

Usage:
  python generate_monthly_reports.py               # runs for previous month
  python generate_monthly_reports.py --dry-run     # prints reports, sends nothing
  python generate_monthly_reports.py --month 2025-06  # specific month (YYYY-MM)
  python generate_monthly_reports.py --client client_001  # single client only

Credentials required in .env (same as the rest of the product):
  GMAIL_ADDRESS
  GMAIL_APP_PASSWORD
  GOOGLE_SERVICE_ACCOUNT_JSON
"""
from __future__ import annotations

import argparse
import logging
import os
import smtplib
import sys
from datetime import datetime, timezone
from email.message import EmailMessage
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


# ── Logging ───────────────────────────────────────────────────────────────────

LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
REPORT_LOG = LOG_DIR / "reports.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(REPORT_LOG, encoding="utf-8"),
    ],
)
log = logging.getLogger("monthly_reports")

# Import from the same package — run from missed_call_product/ directory
sys.path.insert(0, str(Path(__file__).resolve().parent))
from clients import get_all_clients  # noqa: E402


# ── Google Sheets ─────────────────────────────────────────────────────────────

def _sheets_service():
    """Return an authenticated Sheets API service object."""
    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    creds_file = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "service_account.json")
    scopes = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    creds = service_account.Credentials.from_service_account_file(
        creds_file, scopes=scopes
    )
    return build("sheets", "v4", credentials=creds, cache_discovery=False)


def fetch_leads_for_month(
    spreadsheet_id: str,
    sheet_name: str,
    year: int,
    month: int,
) -> List[Dict[str, str]]:
    """
    Return all lead rows whose Timestamp falls within (year, month).
    Sheet columns (A–E): Timestamp | Caller Number | Message | Status | Business
    Skips the header row. Safe if the sheet is empty or the tab is missing.
    """
    if not spreadsheet_id:
        return []

    try:
        svc = _sheets_service()
        result = svc.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=f"{sheet_name}!A:E",
        ).execute()
    except Exception as exc:
        log.error("Sheets fetch failed for sheet=%s id=%s: %s", sheet_name, spreadsheet_id, exc)
        return []

    rows = result.get("values", [])
    if len(rows) < 2:          # empty or header-only
        return []

    prefix = f"{year:04d}-{month:02d}"
    leads = []
    for row in rows[1:]:       # skip header
        if not row:
            continue
        padded = row + [""] * (5 - len(row))
        ts, caller, message, status, business = padded[:5]
        if ts.startswith(prefix):
            leads.append({
                "timestamp": ts,
                "caller_number": caller.strip(),
                "message": message.strip(),
                "status": status.strip(),
                "business": business.strip(),
            })
    return leads


# ── Report calculation ────────────────────────────────────────────────────────

def _month_label(year: int, month: int) -> str:
    """Return e.g. 'June 2025'."""
    return datetime(year, month, 1).strftime("%B %Y")


def calculate_report(leads: List[Dict]) -> Dict:
    """
    Summarise a list of lead rows into report metrics.

    Returns:
      total        — int, total rows in period
      unique       — int, distinct caller numbers
      samples      — list[str], first 3 non-empty messages
    """
    total = len(leads)
    unique = len({r["caller_number"] for r in leads if r["caller_number"]})
    samples = []
    for r in leads:
        msg = r["message"].strip()
        if msg and msg not in ("(missed call — awaiting reply)", ""):
            if msg not in samples:
                samples.append(msg)
        if len(samples) >= 3:
            break
    return {"total": total, "unique": unique, "samples": samples}


def build_email_body(
    business_name: str,
    year: int,
    month: int,
    report: Dict,
) -> Tuple[str, str]:
    """
    Build (subject, plain-text body) for the monthly report email.
    Returns a no-leads variant if total == 0.
    """
    month_label = _month_label(year, month)
    subject = f"Your Missed Call Leads – {month_label}"

    if report["total"] == 0:
        body = (
            f"Hi,\n\n"
            f"Here's your missed call summary for {month_label}.\n\n"
            f"No missed call leads were captured this month. "
            f"If you expected activity, check that your Twilio number is "
            f"still pointed at the right webhook.\n\n"
            f"— Copperline"
        )
        return subject, body

    total   = report["total"]
    unique  = report["unique"]
    samples = report["samples"]

    lead_word   = "lead" if total == 1 else "leads"
    caller_word = "caller" if unique == 1 else "callers"

    sample_block = ""
    if samples:
        sample_lines = "\n".join(f'  • "{m}"' for m in samples)
        sample_block = (
            f"\nExamples of what they said:\n{sample_lines}\n"
        )

    body = (
        f"Hi,\n\n"
        f"Here's your missed call summary for {month_label}.\n\n"
        f"Last month you captured {total} missed call {lead_word} "
        f"from {unique} unique {caller_word}."
        f"{sample_block}\n"
        f"These are customers who called your number after hours "
        f"and might otherwise have called another company.\n\n"
        f"Reply to this email if you have any questions.\n\n"
        f"— Copperline"
    )
    return subject, body


# ── Email sender ──────────────────────────────────────────────────────────────

def send_report_email(to_email: str, subject: str, body: str) -> None:
    """Send a plain-text report email via Gmail SMTP."""
    sender       = os.getenv("GMAIL_ADDRESS", "").strip()
    app_password = os.getenv("GMAIL_APP_PASSWORD", "").strip()

    if not sender or not app_password:
        raise RuntimeError(
            "GMAIL_ADDRESS and GMAIL_APP_PASSWORD must be set to send reports."
        )

    msg = EmailMessage()
    msg["From"]    = f"Copperline <{sender}>"
    msg["To"]      = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, app_password)
        smtp.send_message(msg)


def _log_report_sent(client_id: str, business_name: str, to_email: str,
                     month_label: str, total: int) -> None:
    """Append a structured report_sent event to the report log."""
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    log.info(
        "report_sent | client=%s | business=%s | to=%s | month=%s | leads=%d",
        client_id, business_name, to_email, month_label, total,
    )


# ── Per-client report runner ──────────────────────────────────────────────────

def run_report_for_client(
    client_id: str,
    config: Dict,
    year: int,
    month: int,
    dry_run: bool = False,
) -> Dict:
    """
    Run the full report pipeline for one client.

    Returns a result dict:
      { client_id, business_name, owner_email, total, unique,
        sent (bool), skipped_reason (str or None), error (str or None) }
    """
    business_name = config.get("business_name", client_id)
    owner_email   = config.get("owner_email", "").strip()
    spreadsheet_id = config.get("spreadsheet_id", "").strip()
    sheet_name    = config.get("sheet_name", "Leads").strip() or "Leads"
    month_label   = _month_label(year, month)

    result: Dict = {
        "client_id":     client_id,
        "business_name": business_name,
        "owner_email":   owner_email,
        "total":         0,
        "unique":        0,
        "sent":          False,
        "skipped_reason": None,
        "error":         None,
    }

    if not owner_email:
        result["skipped_reason"] = "no owner_email configured"
        log.warning("Skipping %s — no owner_email", client_id)
        return result

    if not spreadsheet_id:
        result["skipped_reason"] = "no spreadsheet_id configured"
        log.warning("Skipping %s — no spreadsheet_id", client_id)
        return result

    leads  = fetch_leads_for_month(spreadsheet_id, sheet_name, year, month)
    report = calculate_report(leads)
    result["total"]  = report["total"]
    result["unique"] = report["unique"]

    subject, body = build_email_body(business_name, year, month, report)

    if dry_run:
        print(f"\n{'─'*60}")
        print(f"CLIENT : {business_name}  ({client_id})")
        print(f"TO     : {owner_email}")
        print(f"MONTH  : {month_label}")
        print(f"LEADS  : {report['total']} total | {report['unique']} unique callers")
        print(f"\nSUBJECT: {subject}")
        print(f"\n{body}")
        result["sent"] = False
        result["skipped_reason"] = "dry-run"
        return result

    try:
        send_report_email(owner_email, subject, body)
        _log_report_sent(client_id, business_name, owner_email, month_label, report["total"])
        result["sent"] = True
    except Exception as exc:
        log.error("Failed to send report for %s: %s", client_id, exc)
        result["error"] = str(exc)

    return result


# ── Orchestrator ──────────────────────────────────────────────────────────────

def run_all_reports(
    year: int,
    month: int,
    dry_run: bool = False,
    only_client: Optional[str] = None,
) -> List[Dict]:
    """
    Run reports for all clients (or a single client if only_client is set).
    Returns a list of result dicts, one per client attempted.
    """
    try:
        all_clients = get_all_clients()
    except FileNotFoundError as exc:
        log.error("Cannot load clients: %s", exc)
        return []

    if not all_clients:
        log.warning("No clients found in clients.json — nothing to report.")
        return []

    if only_client:
        if only_client not in all_clients:
            log.error("Client '%s' not found in clients.json", only_client)
            return []
        all_clients = {only_client: all_clients[only_client]}

    month_label = _month_label(year, month)
    mode = "DRY RUN" if dry_run else "LIVE"
    log.info(
        "Starting monthly reports [%s] | month=%s | clients=%d",
        mode, month_label, len(all_clients),
    )

    results = []
    for client_id, config in all_clients.items():
        result = run_report_for_client(client_id, config, year, month, dry_run=dry_run)
        results.append(result)

    return results


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate and send monthly missed-call lead reports to clients."
    )
    parser.add_argument(
        "--month",
        default=None,
        metavar="YYYY-MM",
        help="Month to report on (default: previous calendar month).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print reports to stdout; do not send any emails.",
    )
    parser.add_argument(
        "--client",
        default=None,
        metavar="CLIENT_ID",
        help="Run for a single client_id only.",
    )
    return parser.parse_args()


def _resolve_month(month_arg: Optional[str]) -> Tuple[int, int]:
    """Return (year, month) from a 'YYYY-MM' string or default to last month."""
    if month_arg:
        try:
            dt = datetime.strptime(month_arg, "%Y-%m")
            return dt.year, dt.month
        except ValueError:
            print(f"ERROR: --month must be in YYYY-MM format, got: {month_arg!r}")
            sys.exit(1)

    # Default: previous calendar month
    now = datetime.now(timezone.utc)
    if now.month == 1:
        return now.year - 1, 12
    return now.year, now.month - 1


def main() -> None:
    args = _parse_args()
    year, month = _resolve_month(args.month)

    results = run_all_reports(
        year=year,
        month=month,
        dry_run=args.dry_run,
        only_client=args.client,
    )

    if not results:
        return

    sent    = sum(1 for r in results if r["sent"])
    skipped = sum(1 for r in results if r["skipped_reason"])
    errors  = sum(1 for r in results if r["error"])

    print(f"\n{'═'*60}")
    print(f"Monthly Reports — {_month_label(year, month)}")
    print(f"  Sent    : {sent}")
    print(f"  Skipped : {skipped}")
    print(f"  Errors  : {errors}")
    for r in results:
        if r["error"]:
            print(f"  ✗ {r['business_name']}: {r['error']}")
        elif r["skipped_reason"] and r["skipped_reason"] != "dry-run":
            print(f"  – {r['business_name']}: skipped ({r['skipped_reason']})")
    print(f"{'═'*60}\n")


if __name__ == "__main__":
    main()
