from __future__ import annotations

import csv
import re
import sys
from pathlib import Path
from typing import Dict, List

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lead_memory
from discovery.prospect_discovery_agent import clean_website_for_key, dedupe_key_for_prospect

_ASSET_FRAGMENTS = (".webp", ".png", ".jpg", ".jpeg", ".svg", ".gif", ".css", ".js")
_EXCLUDED_CONTACTABILITY = {
    "website_contact_only",
    "no_website",
    "website_unreachable",
    "directory_or_ambiguous",
    "directory_skipped",
}
_BLOCKING_MEMORY_STATES = {
    "contacted",
    "suppressed",
    "deleted_intentionally",
    "do_not_contact",
    "hold",
}


def _valid_direct_email(value: str) -> bool:
    email = (value or "").strip().lower()
    if not email or "@" not in email:
        return False
    return not any(email.endswith(frag) for frag in _ASSET_FRAGMENTS)


def _norm(value: str) -> str:
    return (value or "").strip().lower()


def _norm_name(value: str) -> str:
    return " ".join(re.sub(r"[^\w\s]", " ", (value or "").strip().lower()).split())


def _load_sent_reference_rows(path: Path | None) -> List[Dict[str, str]]:
    if not path or not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        return [dict(row) for row in reader]


def classify_drafted_prospects(
    prospects: List[Dict[str, str]],
    pending_rows: List[Dict[str, str]],
    sent_reference_csv: Path | None = None,
) -> Dict[str, List[Dict[str, str]]]:
    queued_keys = {dedupe_key_for_prospect(row) for row in pending_rows}
    queued_emails = {
        _norm(row.get("to_email", ""))
        for row in pending_rows
        if _valid_direct_email(row.get("to_email", ""))
    }
    queued_domains = {
        clean_website_for_key(row.get("website", ""))
        for row in pending_rows
        if clean_website_for_key(row.get("website", ""))
    }

    sent_rows = [
        row for row in pending_rows
        if (row.get("sent_at") or "").strip() and (row.get("message_id") or "").strip()
    ]
    sent_rows.extend(_load_sent_reference_rows(sent_reference_csv))

    sent_keys = {dedupe_key_for_prospect(row) for row in sent_rows}
    sent_names = {
        _norm_name(row.get("business_name") or row.get("name") or "")
        for row in sent_rows
        if _norm_name(row.get("business_name") or row.get("name") or "")
    }
    sent_emails = {
        _norm(row.get("to_email") or row.get("email") or "")
        for row in sent_rows
        if _valid_direct_email(row.get("to_email") or row.get("email") or "")
    }
    sent_domains = {
        clean_website_for_key(row.get("website", ""))
        for row in sent_rows
        if clean_website_for_key(row.get("website", ""))
    }
    blocked_memory_keys = {
        key
        for key, record in lead_memory.get_all_records().items()
        if record.get("current_state") in _BLOCKING_MEMORY_STATES
    }

    report = {
        "recoverable": [],
        "already_queued": [],
        "already_sent": [],
        "excluded_contactability": [],
        "non_email": [],
    }

    for prospect in prospects:
        if _norm(prospect.get("status")) != "drafted":
            continue

        email = prospect.get("to_email", "")
        if not _valid_direct_email(email):
            report["non_email"].append(prospect)
            continue

        contactability = _norm(prospect.get("contactability", ""))
        if contactability in _EXCLUDED_CONTACTABILITY:
            report["excluded_contactability"].append(prospect)
            continue

        dedupe_key = dedupe_key_for_prospect(prospect)
        email_key = _norm(email)
        domain_key = clean_website_for_key(prospect.get("website", ""))
        name_key = _norm_name(prospect.get("business_name", ""))
        memory_key = lead_memory.lead_key(prospect)

        if dedupe_key in queued_keys or email_key in queued_emails or (domain_key and domain_key in queued_domains):
            report["already_queued"].append(prospect)
            continue

        if (
            dedupe_key in sent_keys
            or name_key in sent_names
            or email_key in sent_emails
            or (domain_key and domain_key in sent_domains)
            or memory_key in blocked_memory_keys
            or _norm(prospect.get("email_sent", "")) == "true"
            or bool((prospect.get("sent_at") or "").strip())
        ):
            report["already_sent"].append(prospect)
            continue

        report["recoverable"].append(prospect)

    return report


def scan_stranded_drafted(
    prospects_csv: Path,
    pending_csv: Path,
    sent_reference_csv: Path | None = None,
    sample_limit: int = 20,
) -> Dict[str, object]:
    with prospects_csv.open("r", newline="", encoding="utf-8-sig") as handle:
        prospects = [dict(row) for row in csv.DictReader(handle)]

    if pending_csv.exists():
        with pending_csv.open("r", newline="", encoding="utf-8") as handle:
            pending_rows = [dict(row) for row in csv.DictReader(handle)]
    else:
        pending_rows = []

    report = classify_drafted_prospects(prospects, pending_rows, sent_reference_csv)

    def sample(rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
        return [
            {
                "business_name": row.get("business_name", ""),
                "to_email": row.get("to_email", ""),
                "contactability": row.get("contactability", ""),
                "website": row.get("website", ""),
                "status": row.get("status", ""),
            }
            for row in rows[:sample_limit]
        ]

    return {
        "recoverable_count": len(report["recoverable"]),
        "already_queued_count": len(report["already_queued"]),
        "already_sent_count": len(report["already_sent"]),
        "excluded_contactability_count": len(report["excluded_contactability"]),
        "non_email_count": len(report["non_email"]),
        "recoverable_details": sample(report["recoverable"]),
    }
