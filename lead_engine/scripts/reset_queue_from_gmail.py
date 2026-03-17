"""
scripts/reset_queue_from_gmail.py

One-time queue reset utility for Copperline.

Purpose:
    After a debugging/testing cycle, the live queue (pending_emails.csv) may contain
    polluted, test, or stale rows. This script resets the queue to contain only
    businesses that were actually contacted via Gmail, based on a manually prepared
    gmail_sent.csv export.

Behavior:
    1. Creates a full timestamped backup of pending_emails.csv before any mutation.
    2. Loads the live queue and the gmail_sent.csv input file.
    3. Matches queue rows against Gmail sent using:
         - Primary:  normalized to_email == normalized gmail email
         - Fallback: normalized business_name match (when email absent or asset-like)
    4. Keeps matched rows only.
       For kept rows:
         - approved   = "true"
         - send_after = ""
         - sent_at    = preserved if present, else taken from gmail sent_date,
                        else set to SENT_AT_PLACEHOLDER
         - replied, replied_at, reply_snippet, conversation_notes,
           conversation_next_step, next_followup_at -- all preserved as-is
    5. Archives all unmatched rows to _backups/ (never deleted permanently).
    6. Writes the cleaned queue back to pending_emails.csv.
    7. Prints a full summary.

Usage:
    cd lead_engine
    python scripts/reset_queue_from_gmail.py --gmail path/to/gmail_sent.csv [--dry-run]

    --dry-run   Print what would change without writing any files.

Safety:
    - Never runs without creating a backup first.
    - Dry-run mode is safe to call repeatedly.
    - If backup write fails, script aborts before touching the live queue.
    - Schema is preserved exactly -- column order and naming are not changed.
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

# ── Path setup ────────────────────────────────────────────────────────────────

# Scripts live at lead_engine/scripts/ -- parent is lead_engine/
SCRIPT_DIR   = Path(__file__).resolve().parent
LEAD_ENGINE  = SCRIPT_DIR.parent
QUEUE_CSV    = LEAD_ENGINE / "queue" / "pending_emails.csv"
BACKUPS_DIR  = LEAD_ENGINE / "_backups"

# ── Constants ─────────────────────────────────────────────────────────────────

SENT_AT_PLACEHOLDER = "2026-03-16 (reset-preserved)"

# Asset-filename fragments that slip through as fake email addresses
_ASSET_FRAGS = (".webp", ".png", ".jpg", ".jpeg", ".svg", ".gif", ".css", ".js")

# ── Helpers ───────────────────────────────────────────────────────────────────

def _norm_email(email: str) -> str:
    """Lowercase + strip. Returns '' if value looks like an asset filename."""
    e = (email or "").strip().lower()
    if not e:
        return ""
    # Check if the domain-part contains an asset extension
    at_parts = e.split("@")
    domain = at_parts[-1] if len(at_parts) > 1 else e
    for frag in _ASSET_FRAGS:
        if e.endswith(frag) or frag.lstrip(".") in domain:
            return ""
    return e


def _norm_name(name: str) -> str:
    """
    Normalize a business name for fallback matching.
    Lowercase, strip punctuation, collapse whitespace.
    Does NOT strip industry noise words -- broad match is intentional here.
    """
    raw = (name or "").strip().lower()
    raw = re.sub(r"[^\w\s]", " ", raw)
    return " ".join(raw.split())


def _read_csv(path: Path) -> Tuple[List[str], List[Dict[str, str]]]:
    """Return (fieldnames, rows). Raises on missing file."""
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        rows = [dict(r) for r in reader]
    return fieldnames, rows


def _write_csv(path: Path, fieldnames: List[str], rows: List[Dict[str, str]]) -> None:
    """Write rows preserving exact fieldnames order."""
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def _backup(source: Path, backups_dir: Path, label: str = "pre_reset") -> Path:
    """
    Write a timestamped backup of source to backups_dir.
    Returns the backup path. Raises on failure -- caller must abort if this raises.
    """
    backups_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    dest = backups_dir / f"{source.stem}_{label}_{ts}{source.suffix}"
    dest.write_bytes(source.read_bytes())
    return dest


# ── Core logic ────────────────────────────────────────────────────────────────

def load_gmail_sent(gmail_path: Path):
    """
    Load gmail_sent.csv and build two lookup indexes.

    Returns:
        email_index  -- {norm_email: row}
        name_index   -- {norm_name: row}
        all_rows     -- raw list for reporting
    """
    _, rows = _read_csv(gmail_path)
    email_index: Dict[str, Dict] = {}
    name_index:  Dict[str, Dict] = {}

    for row in rows:
        # Only index rows where keep_for_reset is truthy (or column absent)
        keep = (row.get("keep_for_reset") or "true").strip().lower()
        if keep not in ("true", "1", "yes", ""):
            continue

        ne = _norm_email(row.get("email", ""))
        nn = _norm_name(row.get("business_name", ""))

        if ne:
            email_index[ne] = row
        if nn:
            name_index.setdefault(nn, row)  # keep first occurrence

    return email_index, name_index, rows


def match_queue_to_gmail(queue_rows, email_index, name_index):
    """
    Match each queue row to a gmail_sent entry.

    Match logic:
        1. Valid queue email found in email_index  --> match by email
        2. Fallback: normalized business name in name_index

    Returns:
        matched   -- list of (queue_row, gmail_row, method)
        unmatched -- list of queue_rows with no match
        matched_gmail_emails -- set of gmail emails that were matched
    """
    matched   = []
    unmatched = []
    matched_gmail_emails: Set[str] = set()

    for qrow in queue_rows:
        qemail = _norm_email(qrow.get("to_email", ""))
        qname  = _norm_name(qrow.get("business_name", ""))
        gmail_row = None
        method    = ""

        if qemail and qemail in email_index:
            gmail_row = email_index[qemail]
            method    = "email"
        elif qname and qname in name_index:
            gmail_row = name_index[qname]
            method    = "name"

        if gmail_row is not None:
            matched.append((qrow, gmail_row, method))
            ge = _norm_email(gmail_row.get("email", ""))
            if ge:
                matched_gmail_emails.add(ge)
        else:
            unmatched.append(qrow)

    return matched, unmatched, matched_gmail_emails


def apply_reset_fields(qrow: Dict[str, str], gmail_row: Dict) -> Dict[str, str]:
    """
    Return a copy of qrow with reset fields applied.

    Rules:
        approved    -> "true"
        send_after  -> ""
        sent_at     -> preserve if set; else use gmail sent_date; else placeholder
        replied / replied_at / reply_snippet / conversation_* / next_followup_at
                    -> preserved exactly (never fabricated)
    """
    row = dict(qrow)
    row["approved"]   = "true"
    row["send_after"] = ""

    existing_sent = (row.get("sent_at") or "").strip()
    if not existing_sent:
        gmail_date = (gmail_row.get("sent_date") or "").strip()
        row["sent_at"] = gmail_date if gmail_date else SENT_AT_PLACEHOLDER

    return row


# ── Main ──────────────────────────────────────────────────────────────────────

def run(gmail_path: Path, dry_run: bool = False) -> None:
    print()
    print("=" * 60)
    print("  Copperline Queue Reset -- Gmail Preservation Mode")
    print("=" * 60)
    if dry_run:
        print("  *** DRY RUN -- no files will be written ***")
    print()

    # 1. Verify inputs
    if not QUEUE_CSV.exists():
        print(f"ERROR: Queue not found at {QUEUE_CSV}")
        sys.exit(1)
    if not gmail_path.exists():
        print(f"ERROR: gmail_sent.csv not found at {gmail_path}")
        sys.exit(1)

    # 2. Backup FIRST -- abort if it fails
    backup_path = None
    if not dry_run:
        try:
            backup_path = _backup(QUEUE_CSV, BACKUPS_DIR, label="pre_reset")
            print(f"Backup created: {backup_path.name}")
        except Exception as e:
            print(f"ABORT: Backup failed -- {e}")
            print("  Queue was NOT modified.")
            sys.exit(1)
    else:
        print("  (dry-run: backup would be written to _backups/)")

    # 3. Load data
    fieldnames, queue_rows = _read_csv(QUEUE_CSV)
    email_index, name_index, gmail_all = load_gmail_sent(gmail_path)

    print(f"\n  Queue rows loaded:      {len(queue_rows)}")
    print(f"  Gmail sent entries:     {len(gmail_all)}")
    print(f"  Gmail email index:      {len(email_index)} valid emails")
    print(f"  Gmail name index:       {len(name_index)} business names")

    # 4. Match
    matched, unmatched, matched_gmail_emails = match_queue_to_gmail(
        queue_rows, email_index, name_index
    )
    email_matches = sum(1 for _, _, m in matched if m == "email")
    name_matches  = sum(1 for _, _, m in matched if m == "name")

    print(f"\n  Matched (keep):         {len(matched)}")
    print(f"    -> matched by email:  {email_matches}")
    print(f"    -> matched by name:   {name_matches}")
    print(f"  Unmatched (archive):    {len(unmatched)}")

    # 5. Build kept rows with reset fields applied
    kept_rows = [apply_reset_fields(qrow, gmail_row) for qrow, gmail_row, _ in matched]

    # 6. Report unmatched Gmail entries
    all_gmail_emails = {
        _norm_email(r.get("email", ""))
        for r in gmail_all
        if _norm_email(r.get("email", ""))
    }
    unmatched_gmail = all_gmail_emails - matched_gmail_emails
    if unmatched_gmail:
        print(f"\n  Gmail entries not matched to any queue row ({len(unmatched_gmail)}):")
        for e in sorted(unmatched_gmail):
            print(f"    {e}")
        print("  (These are real sends to businesses not currently in the queue.)")
    else:
        print(f"\n  All Gmail entries matched to queue rows.")

    # 7. Archive unmatched queue rows
    if not dry_run and unmatched:
        try:
            ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            archive_path = BACKUPS_DIR / f"pending_emails_archived_unmatched_{ts}.csv"
            _write_csv(archive_path, fieldnames, unmatched)
            print(f"\n  Archived {len(unmatched)} unmatched rows -> {archive_path.name}")
        except Exception as e:
            print(f"\n  WARNING: Archive write failed -- {e}")
            print("  Continuing -- unmatched rows will be removed from live queue.")
    elif dry_run and unmatched:
        print(f"\n  (dry-run: {len(unmatched)} rows would be archived to _backups/)")

    # 8. Write cleaned queue
    if not dry_run:
        try:
            _write_csv(QUEUE_CSV, fieldnames, kept_rows)
            print(f"  Live queue updated -> {len(kept_rows)} rows written.")
        except Exception as e:
            print(f"\nERROR: Failed to write live queue -- {e}")
            if backup_path:
                print(f"  Backup is safe at: {backup_path}")
            sys.exit(1)
    else:
        print(f"\n  (dry-run: would write {len(kept_rows)} kept rows to pending_emails.csv)")

    # 9. Summary
    print()
    print("-" * 60)
    print("  SUMMARY")
    print("-" * 60)
    print(f"  Original queue rows:    {len(queue_rows)}")
    print(f"  Kept (Gmail-matched):   {len(kept_rows)}")
    print(f"  Archived (unmatched):   {len(unmatched)}")
    print(f"  Unmatched Gmail rows:   {len(unmatched_gmail)}")
    if backup_path:
        print(f"  Backup:                 {backup_path.name}")
    print("-" * 60)
    print()
    if not dry_run:
        print("  Done. Restart the dashboard server to reload the queue.")
    else:
        print("  Dry run complete. Re-run without --dry-run to apply.")
    print()


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Reset Copperline queue to Gmail-confirmed outreach only."
    )
    parser.add_argument(
        "--gmail",
        required=True,
        help="Path to gmail_sent.csv (columns: email, business_name, sent_date, ...)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would change without writing any files.",
    )
    args = parser.parse_args()
    run(gmail_path=Path(args.gmail).resolve(), dry_run=args.dry_run)
