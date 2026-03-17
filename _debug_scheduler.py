"""Pass 31 diagnostic — run from repo root."""
import csv
import sys
from datetime import datetime
from pathlib import Path

CSV_PATH = Path("lead_engine/queue/pending_emails.csv")

with CSV_PATH.open("r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

now = datetime.now()
print(f"Current local time : {now.isoformat()}")
print(f"Total rows         : {len(rows)}")

scheduled = [r for r in rows if (r.get("send_after") or "").strip()]
print(f"Scheduled rows     : {len(scheduled)}\n")

for r in scheduled[:8]:
    sa = (r.get("send_after") or "").strip()
    approved = r.get("approved", "").strip().lower()
    sent_at  = (r.get("sent_at") or "").strip()
    msg_id   = (r.get("message_id") or "").strip()
    name     = r.get("business_name", "")[:40]
    try:
        sa_dt  = datetime.fromisoformat(sa)
        is_due = now >= sa_dt
        delta  = (now - sa_dt).total_seconds()
    except Exception as e:
        sa_dt  = None
        is_due = None
        delta  = None

    print(f"  [{name}]")
    print(f"    send_after  = {sa!r}")
    print(f"    parsed_dt   = {sa_dt}")
    print(f"    now >= sa   = {is_due}  (delta_seconds={delta:.0f})" if delta is not None else f"    PARSE ERROR")
    print(f"    approved    = {approved!r}")
    print(f"    sent_at     = {sent_at!r}")
    print(f"    message_id  = {bool(msg_id)}")
    print()

# Also test _is_send_eligible logic verbatim from email_sender_agent
print("--- Eligibility trace ---")
sys.path.insert(0, "lead_engine")
from send.email_sender_agent import _is_send_eligible

for r in scheduled[:8]:
    name = r.get("business_name", "")[:40]
    eligible = _is_send_eligible(r)
    sa = (r.get("send_after") or "").strip()
    print(f"  {name!r:45s}  send_after={sa!r:22s}  eligible={eligible}")
