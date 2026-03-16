"""
reset_stale_queue.py — Remove stale email drafts so they are regenerated on the next pipeline run.

What this does:
  1. Reads pending_emails.csv.
  2. For every row that has NOT been sent AND whose draft_version != CURRENT_DRAFT_VERSION:
     - REMOVES the row from pending_emails.csv entirely (so the dedup key is gone).
  3. Resets status = "new" in prospects.csv for all removed business names
     so run_lead_engine.py will re-draft them.

Rows that HAVE been sent (sent_at is set) are never touched.

Usage:
  python lead_engine/reset_stale_queue.py --dry-run   # preview only
  python lead_engine/reset_stale_queue.py             # apply changes

After running, re-draft with:
  python lead_engine/run_lead_engine.py
"""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PENDING_CSV   = BASE_DIR / "queue" / "pending_emails.csv"
PROSPECTS_CSV = BASE_DIR / "data" / "prospects.csv"

sys.path.insert(0, str(BASE_DIR))
from outreach.email_draft_agent import DRAFT_VERSION as CURRENT_VERSION


def _remove_stale_from_pending(dry_run: bool) -> list[str]:
    """
    Remove unsent stale rows from pending_emails.csv.
    Returns list of affected business names (lowercase).
    """
    if not PENDING_CSV.exists():
        print("pending_emails.csv not found — nothing to do.")
        return []

    with PENDING_CSV.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)

    keep_rows = []
    removed_names: list[str] = []

    for row in rows:
        # Always keep sent rows — never remove them
        if row.get("sent_at", "").strip():
            keep_rows.append(row)
            continue

        version = row.get("draft_version", "").strip()
        is_stale = (version != CURRENT_VERSION)

        # Also treat blank-body rows as stale regardless of version tag
        body_blank = not row.get("body", "").strip()
        subj_blank = not row.get("subject", "").strip()

        if is_stale or body_blank or subj_blank:
            name = row.get("business_name", "").strip()
            if dry_run:
                print(f"  [DRY RUN] Would remove: {name!r}  (version={version!r})")
            else:
                removed_names.append(name.lower())
        else:
            keep_rows.append(row)

    if not dry_run:
        with PENDING_CSV.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(keep_rows)

    removed_count = len(rows) - len(keep_rows) if not dry_run else (len(rows) - sum(
        1 for r in rows
        if r.get("sent_at", "").strip()
        or (r.get("draft_version", "").strip() == CURRENT_VERSION
            and r.get("body", "").strip()
            and r.get("subject", "").strip())
    ))

    print(f"\n  {'[DRY RUN] Would remove' if dry_run else 'Removed'} "
          f"{removed_count} stale row(s) from pending_emails.csv")
    if not dry_run:
        print(f"  Kept {len(keep_rows)} row(s) (sent rows are never removed)")
    return removed_names


def _reset_prospects_to_new(affected_names: list[str], dry_run: bool) -> None:
    """Set status = 'new' in prospects.csv for affected business names."""
    if not affected_names or not PROSPECTS_CSV.exists():
        return

    with PROSPECTS_CSV.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)

    if "status" not in fieldnames:
        fieldnames.append("status")

    updated = 0
    for row in rows:
        name = row.get("business_name", "").strip().lower()
        if name in affected_names:
            current = row.get("status", "")
            if current != "sent":   # never un-send a sent row
                if dry_run:
                    print(f"  [DRY RUN] Would reset prospects.csv: {name!r} ({current!r} → 'new')")
                else:
                    row["status"] = "new"
                updated += 1

    if not dry_run and updated:
        with PROSPECTS_CSV.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    print(f"  {'[DRY RUN] Would update' if dry_run else 'Updated'} "
          f"{updated} row(s) in prospects.csv → status=new")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Remove stale email drafts so the pipeline regenerates them."
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview changes without writing anything.")
    args = parser.parse_args()

    print(f"\nCurrent template version : {CURRENT_VERSION}")
    print(f"Mode                     : {'DRY RUN' if args.dry_run else 'LIVE'}\n")

    affected = _remove_stale_from_pending(dry_run=args.dry_run)
    _reset_prospects_to_new(affected, dry_run=args.dry_run)

    if not args.dry_run and affected:
        print(f"\n  Done. Now run:")
        print(f"  python lead_engine/run_lead_engine.py\n")
    elif args.dry_run:
        print(f"\n  Re-run without --dry-run to apply.\n")
    else:
        print(f"\n  Nothing to reset — all unsent drafts are on {CURRENT_VERSION}.\n")


if __name__ == "__main__":
    main()
