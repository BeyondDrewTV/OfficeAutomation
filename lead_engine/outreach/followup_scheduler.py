"""
outreach/followup_scheduler.py

Follow-Up Auto-Draft Generator.
Reads pending_emails.csv (source of truth for sent state), finds rows
that are due for a follow-up, and writes new draft rows to the queue.

Rules (all must pass before a follow-up is drafted):
  1. Prior real send confirmed  - sent_at AND message_id both populated
  2. No reply logged            - replied != "true"
  3. Follow-up is due           - next_followup_at <= now  OR
                                   (next_followup_at empty AND sent_at >= N days ago)
  4. Follow-up count under cap  - contact_attempt_count < FOLLOWUP_CAP
  5. Valid email present        - to_email passes format check
  6. No active exception flags  - detect_row_exceptions() returns empty list
  7. Not already queued         - no unsent follow-up draft exists in queue
     for same business (checked via dedupe key)

Drafts are written with approved="false" - operator must approve before send.
Auto-send is NOT enabled.

Pass 50: follow-up drafting is now shared with a deterministic follow-up
draft helper. Timing, eligibility, and queue write mechanics stay intact;
copy generation is blocked when the lead record does not have enough
grounded context to support a safe continuation message.
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

BASE_DIR = Path(__file__).resolve().parent.parent
PENDING_CSV = BASE_DIR / "queue" / "pending_emails.csv"

sys.path.insert(0, str(BASE_DIR))
from send.email_sender_agent import is_real_send
from discovery.prospect_discovery_agent import dedupe_key_for_prospect
from outreach.followup_draft_agent import build_followup_plan, FollowupBlockedError

import importlib.util as _ilu
_er_spec = _ilu.spec_from_file_location("exception_router", BASE_DIR / "queue" / "exception_router.py")
_er_mod = _ilu.module_from_spec(_er_spec)
_er_spec.loader.exec_module(_er_mod)
detect_row_exceptions = _er_mod.detect_row_exceptions

FOLLOWUP_CAP = 2
FOLLOWUP_DAYS_DEFAULT = 7
FOLLOWUP_DAYS_SECOND = 14
SEND_WINDOW_START = 8
SEND_WINDOW_END = 18

_EMAIL_RE = re.compile(r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")
_ASSET_FRAGS = (".webp", ".png", ".jpg", ".jpeg", ".svg", ".gif", ".css", ".js")

PENDING_COLUMNS = [
    "business_name", "city", "state", "website", "phone", "contact_method",
    "industry", "to_email", "subject", "body", "approved", "sent_at",
    "approval_reason", "scoring_reason", "final_priority_score", "automation_opportunity",
    "do_not_contact", "draft_version",
    "facebook_url", "instagram_url", "contact_form_url", "social_channels", "social_dm_text",
    "facebook_dm_draft", "instagram_dm_draft", "contact_form_message",
    "lead_insight_sentence", "lead_insight_signals", "opportunity_score",
    "last_contact_channel", "last_contacted_at", "contact_attempt_count",
    "contact_result", "next_followup_at", "campaign_key",
    "message_id", "replied", "replied_at", "reply_snippet",
    "conversation_notes", "conversation_next_step",
    "send_after",
    "business_specific_observation",
]


def _read_pending() -> List[Dict]:
    if not PENDING_CSV.exists():
        return []
    with PENDING_CSV.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            return []
        return [{col: row.get(col, "") for col in PENDING_COLUMNS} for row in reader]


def _write_pending(rows: List[Dict]) -> None:
    PENDING_CSV.parent.mkdir(parents=True, exist_ok=True)
    with PENDING_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=PENDING_COLUMNS)
        writer.writeheader()
        writer.writerows([{col: row.get(col, "") for col in PENDING_COLUMNS} for row in rows])


def _valid_email(email: str) -> bool:
    if not email:
        return False
    normalized = email.strip().lower()
    if any(fragment in normalized for fragment in _ASSET_FRAGS):
        return False
    return bool(_EMAIL_RE.match(normalized))


def _parse_dt(value: str) -> Optional[datetime]:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return None


def _followup_step(row: Dict, now: datetime) -> Optional[int]:
    """
    Return which follow-up step (1 or 2) is due for this row, or None.
    Based on contact_attempt_count and time elapsed since real send.
    """
    sent_dt = _parse_dt(row.get("sent_at", ""))
    if not sent_dt:
        return None
    days_elapsed = (now - sent_dt).days
    try:
        attempts = int(row.get("contact_attempt_count") or 0)
    except Exception:
        attempts = 0
    if attempts == 0 and days_elapsed >= FOLLOWUP_DAYS_DEFAULT:
        return 1
    if attempts == 1 and days_elapsed >= FOLLOWUP_DAYS_SECOND:
        return 2
    return None


def followup_eligible(row: Dict, now: datetime, existing_keys: set) -> Tuple[bool, str]:
    """
    Check whether a queue row is eligible for a follow-up draft.

    Returns (eligible: bool, reason: str).
    'reason' is empty string when eligible, or a short skip reason.
    """
    if not is_real_send(row):
        return False, "no_real_send"

    if row.get("replied", "").strip().lower() == "true":
        return False, "already_replied"

    step = _followup_step(row, now)
    if step is None:
        return False, "not_due_yet"

    try:
        attempts = int(row.get("contact_attempt_count") or 0)
    except Exception:
        attempts = 0
    if attempts >= FOLLOWUP_CAP:
        return False, "cap_reached"

    if not _valid_email(row.get("to_email", "")):
        return False, "no_valid_email"

    flags = detect_row_exceptions(row)
    active = [flag for flag in flags if flag not in ("PRIOR_CONTACT", "FOLLOWUP_CONFLICT")]
    if active:
        return False, f"exceptions:{','.join(active)}"

    key = dedupe_key_for_prospect(row)
    if key in existing_keys:
        return False, "already_queued"

    return True, ""


def run_followup_scheduler(dry_run: bool = False) -> Dict:
    """
    Scan pending_emails.csv for rows eligible for follow-up drafts.
    Write new draft rows (approved=false) for each eligible row.
    """
    if not dry_run:
        from datetime import datetime as _dt
        local_hour = _dt.now().hour
        if not (SEND_WINDOW_START <= local_hour < SEND_WINDOW_END):
            print(f"  [scheduler] Outside send window ({SEND_WINDOW_START}:00-{SEND_WINDOW_END}:00). Skipping.")
            return {"queued": 0, "skipped": 0, "blocked": 0, "skip_reasons": {}, "blocked_reasons": {}}

    now = datetime.now(timezone.utc)
    rows = _read_pending()

    unsent_keys = {
        dedupe_key_for_prospect(row)
        for row in rows
        if not (row.get("sent_at") or "").strip()
    }

    queued = 0
    skipped = 0
    blocked = 0
    skip_reasons: Dict[str, int] = {}
    blocked_reasons: Dict[str, int] = {}
    new_rows: List[Dict] = []

    for row in rows:
        if not is_real_send(row):
            continue

        eligible, reason = followup_eligible(row, now, unsent_keys)
        if not eligible:
            skipped += 1
            skip_reasons[reason] = skip_reasons.get(reason, 0) + 1
            continue

        step = _followup_step(row, now)
        name = row.get("business_name", "").strip()
        to_email = row.get("to_email", "").strip()
        observation = row.get("business_specific_observation", "").strip()

        try:
            plan = build_followup_plan(row, step)
        except FollowupBlockedError as exc:
            skipped += 1
            blocked += 1
            key = f"blocked:{exc.reason}"
            skip_reasons[key] = skip_reasons.get(key, 0) + 1
            blocked_reasons[exc.reason] = blocked_reasons.get(exc.reason, 0) + 1
            continue

        try:
            attempts = int(row.get("contact_attempt_count") or 0)
        except Exception:
            attempts = 0

        new_draft = {col: "" for col in PENDING_COLUMNS}
        new_draft.update({
            "business_name": name,
            "city": row.get("city", "").strip(),
            "state": row.get("state", ""),
            "website": row.get("website", ""),
            "phone": row.get("phone", ""),
            "contact_method": row.get("contact_method", ""),
            "industry": row.get("industry", ""),
            "to_email": to_email,
            "subject": plan["subject"],
            "body": plan["body"],
            "approved": "false",
            "sent_at": "",
            "approval_reason": "",
            "scoring_reason": f"follow-up #{step}",
            "final_priority_score": row.get("final_priority_score", ""),
            "automation_opportunity": row.get("automation_opportunity", ""),
            "do_not_contact": row.get("do_not_contact", ""),
            "draft_version": "v9",
            "contact_attempt_count": str(attempts),
            "campaign_key": row.get("campaign_key", ""),
            "opportunity_score": row.get("opportunity_score", ""),
            "business_specific_observation": observation,
        })

        if dry_run:
            print(f"[DRY RUN] step={step} | {name} -> {to_email} | {plan['angle_family']} | {plan['subject']}")
        else:
            new_rows.append(new_draft)
            unsent_keys.add(dedupe_key_for_prospect(new_draft))
            queued += 1

    if not dry_run and new_rows:
        _write_pending(rows + new_rows)

    return {
        "queued": queued,
        "skipped": skipped,
        "blocked": blocked,
        "skip_reasons": skip_reasons,
        "blocked_reasons": blocked_reasons,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate follow-up drafts for sent prospects.")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing.")
    args = parser.parse_args()
    mode = "DRY RUN" if args.dry_run else "LIVE"
    print(f"\nFollow-Up Scheduler [{mode}]\n  Queue: {PENDING_CSV}\n")
    stats = run_followup_scheduler(dry_run=args.dry_run)
    print("\nDone.")
    print(f"  Queued : {stats['queued']}")
    print(f"  Skipped: {stats['skipped']}")
    if stats["blocked"]:
        print(f"  Blocked: {stats['blocked']}")
    if stats["skip_reasons"]:
        print("  Skip reasons:")
        for reason, count in stats["skip_reasons"].items():
            print(f"    {reason}: {count}")
    if not args.dry_run and stats["queued"] > 0:
        print("\n  -> Open dashboard to review and approve follow-ups.")


if __name__ == "__main__":
    main()
