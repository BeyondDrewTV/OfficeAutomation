from __future__ import annotations

import argparse
import csv
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
LEAD_ENGINE = SCRIPT_DIR.parent
sys.path.insert(0, str(LEAD_ENGINE))

from discovery.prospect_discovery_agent import clean_website_for_key, dedupe_key_for_prospect, load_prospects_from_csv
from run_lead_engine import (
    DEFAULT_PENDING_CSV,
    DEFAULT_PROSPECTS_CSV,
    _build_pending_row,
    _build_queue_dedupe_sets,
    _read_pending_rows,
    _write_pending_rows,
)
from stranded_drafted import classify_drafted_prospects

SENT_REFERENCE_CSV = SCRIPT_DIR / "gmail_sent_preserve_set_for_reset.csv"
BACKUPS_DIR = LEAD_ENGINE / "_backups"


def _backup_queue(path: Path) -> Path:
    BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    backup = BACKUPS_DIR / f"{path.stem}_pre_stranded_recovery_{stamp}{path.suffix}"
    backup.write_bytes(path.read_bytes())
    return backup


def _summarize(report: dict) -> None:
    print("criteria:")
    print("  status=drafted")
    print("  valid direct to_email present")
    print("  contactability not in website_contact_only/no_website/website_unreachable/directory_or_ambiguous/directory_skipped")
    print("  not already queued by dedupe key, email, or website domain")
    print("  not blocked by confirmed queue send, Gmail preserve set, durable lead-memory state, prospect sent_at, or email_sent=true")
    print()
    print(f"recoverable:            {len(report['recoverable'])}")
    print(f"already queued:         {len(report['already_queued'])}")
    print(f"already sent:           {len(report['already_sent'])}")
    print(f"excluded contactability:{len(report['excluded_contactability'])}")
    print(f"non-email drafted:      {len(report['non_email'])}")
    print()
    for row in report["recoverable"][:10]:
        print(f"  - {row.get('business_name','')} | {row.get('to_email','')} | {row.get('contactability','')}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Recover drafted leads with direct emails missing from pending_emails.csv.")
    parser.add_argument("--apply", action="store_true", help="Append recoverable rows to pending_emails.csv.")
    parser.add_argument("--limit", type=int, default=0, help="Only recover the first N eligible rows.")
    parser.add_argument("--scan", action="store_true", help="Re-scan websites while rebuilding recovered rows.")
    args = parser.parse_args()

    prospects = load_prospects_from_csv(DEFAULT_PROSPECTS_CSV)
    pending_rows = _read_pending_rows(DEFAULT_PENDING_CSV)
    report = classify_drafted_prospects(prospects, pending_rows, SENT_REFERENCE_CSV)
    print(f"website_scans={'enabled' if args.scan else 'disabled'}")
    _summarize(report)

    recoverable = list(report["recoverable"])
    if args.limit > 0:
        recoverable = recoverable[:args.limit]

    if not args.apply:
        print()
        print(f"dry run only: would recover {len(recoverable)} row(s)")
        return

    if not recoverable:
        print()
        print("nothing to recover")
        return

    existing_keys, existing_emails, existing_domains = _build_queue_dedupe_sets(pending_rows)
    appended = []
    skipped_duplicates = 0
    skipped_failed = 0

    for prospect in recoverable:
        dedupe_key = dedupe_key_for_prospect(prospect)
        email = (prospect.get("to_email") or "").strip().lower()
        domain = clean_website_for_key(prospect.get("website", ""))

        if dedupe_key in existing_keys or (email and email in existing_emails) or (domain and domain in existing_domains):
            skipped_duplicates += 1
            continue

        try:
            new_row = _build_pending_row(prospect, skip_scan=not args.scan)
        except ValueError:
            skipped_failed += 1
            continue

        pending_rows.append(new_row)
        appended.append(new_row)
        existing_keys.add(dedupe_key)
        if email:
            existing_emails.add(email)
        if domain:
            existing_domains.add(domain)

    backup = _backup_queue(DEFAULT_PENDING_CSV)
    _write_pending_rows(DEFAULT_PENDING_CSV, pending_rows)

    print()
    print(f"backup:                 {backup.name}")
    print(f"recovered:              {len(appended)}")
    print(f"skipped duplicates:     {skipped_duplicates}")
    print(f"skipped draft failures: {skipped_failed}")

    if appended:
        print()
        print("recovered sample:")
        for row in appended[:10]:
            print(f"  - {row.get('business_name','')} | {row.get('to_email','')}")


if __name__ == "__main__":
    main()
