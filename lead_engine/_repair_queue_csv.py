"""
_repair_queue_csv.py — Authoritative rewrite of pending_emails.csv
Run from: lead_engine directory OR any path since it uses absolute path.

Writes both rows from scratch with known-correct values.
All values verified against: original CSV, AUDIT_REPORT.md, code analysis.
"""
import csv
import io
import shutil
from pathlib import Path

BASE = Path(r"C:\Users\beyon\OneDrive\Desktop\OfficeAutomation\lead_engine")
Q    = BASE / "queue" / "pending_emails.csv"
BK   = BASE / "_backups" / "pending_emails_PRE_final_repair.csv"

PENDING_COLUMNS = [
    "business_name", "city", "state", "website", "phone", "contact_method",
    "industry", "to_email", "subject", "body", "approved", "sent_at",
    "approval_reason", "scoring_reason", "final_priority_score", "automation_opportunity",
    "do_not_contact", "draft_version",
    "facebook_url", "instagram_url", "contact_form_url",
    "social_channels", "social_dm_text",
    "facebook_dm_draft", "instagram_dm_draft", "contact_form_message",
    "lead_insight_sentence", "lead_insight_signals", "opportunity_score",
    "last_contact_channel", "last_contacted_at", "contact_attempt_count",
    "contact_result", "next_followup_at", "campaign_key",
    "message_id", "replied", "replied_at", "reply_snippet",
    "conversation_notes", "conversation_next_step",
]

# Dee's Plumbing — phone contact, got reply, NO email/SMTP send
# replied/replied_at/reply_snippet confirmed from original 40-col CSV positional data
DEE = {col: "" for col in PENDING_COLUMNS}
DEE.update({
    "business_name":         "Dee's Plumbing & Construction,Inc.",
    "city":                  "Rockford",
    "state":                 "IL",
    "website":               "",
    "phone":                 "8156364626",
    "contact_method":        "phone",
    "industry":              "",
    "to_email":              "",
    "subject":               "Saving Dee's Plumbing & Construction,Inc. time on after-hours call capture",
    "body": (
        "Hi Dee's Plumbing & Construction,Inc. team,\n\n"
        "I work with service businesses in Rockford on one specific problem: "
        "dispatching jobs manually and missing after-hours calls.\n\n"
        "I built a after-hours call capture and job dispatching automation system that "
        "capture every after-hours lead automatically and route jobs to the right tech "
        "without phone tag. Most businesses I work with see it running within a week.\n\n"
        "Happy to show you a quick demo \u2014 no pitch, just a look at what it does. Interested?\n\n"
        "Best,\nDrew"
    ),
    "approved":              "true",
    "sent_at":               "2026-03-14T20:17:10.854799+00:00",
    "approval_reason":       "",
    "scoring_reason":        "No website found; high automation opportunity.",
    "final_priority_score":  "5",
    "automation_opportunity": "",
    "do_not_contact":        "",
    "draft_version":         "",
    "opportunity_score":     "0",
    "last_contact_channel":  "",
    "last_contacted_at":     "",
    "contact_attempt_count": "1",
    "contact_result":        "replied",
    "next_followup_at":      "",
    "campaign_key":          "",
    "message_id":            "",
    "replied":               "true",
    "replied_at":            "2026-03-14T22:51:59.271740+00:00",
    "reply_snippet":         "Hi Dee's Plumbing & Construction,Inc. team...",
    "conversation_notes":    "",
    "conversation_next_step": "",
})

# Lars Plumbing — email sent (via log_contact, not SMTP), no reply yet
# contact_attempt_count confirmed as '0' from original positional analysis
LARS = {col: "" for col in PENDING_COLUMNS}
LARS.update({
    "business_name":         "Lars Plumbing",
    "city":                  "Rockford",
    "state":                 "IL",
    "website":               "https://www.larsplumbing.com/contact-us",
    "phone":                 "8153788686",
    "contact_method":        "email",
    "industry":              "",
    "to_email":              "john@larsplumbing.com",
    "subject":               "Quick question about calls",
    "body": (
        "Hi Lars Plumbing,\n\n"
        "Do you guys ever miss calls when the crew is out on jobs?\n\n"
        "I built a simple setup that automatically texts the caller back so you can "
        "follow up instead of losing the job.\n\n"
        "Happy to send a quick example if you're curious.\n\n"
        "\u2013 Drew"
    ),
    "approved":              "true",
    "sent_at":               "2026-03-14T20:40:05.989155+00:00",
    "approval_reason":       "",
    "scoring_reason":        "Good Fit \u2014 high-fit industry (plumbing) (+2); has website (+1); has email (+1)",
    "final_priority_score":  "4",
    "automation_opportunity": "unknown",
    "do_not_contact":        "",
    "draft_version":         "",
    "opportunity_score":     "0",
    "last_contact_channel":  "",
    "last_contacted_at":     "",
    "contact_attempt_count": "0",
    "contact_result":        "",
    "next_followup_at":      "",
    "campaign_key":          "",
    "message_id":            "",
    "replied":               "",
    "replied_at":            "",
    "reply_snippet":         "",
    "conversation_notes":    "",
    "conversation_next_step": "",
})


def repair():
    BK.parent.mkdir(exist_ok=True)
    if Q.exists():
        shutil.copy2(Q, BK)
        print(f"Backup: {BK}")

    rows = [DEE, LARS]

    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=PENDING_COLUMNS)
    writer.writeheader()
    writer.writerows(rows)
    with Q.open("w", newline="", encoding="utf-8") as f:
        f.write(buf.getvalue())

    # Verify
    with Q.open("r", newline="", encoding="utf-8") as f:
        r2 = csv.DictReader(f)
        vcols = list(r2.fieldnames or [])
        vrows = [dict(x) for x in r2]

    d, l = vrows[0], vrows[1]
    checks = {
        "41 cols":              len(vcols) == 41,
        "header exact":         vcols == PENDING_COLUMNS,
        "2 rows":               len(vrows) == 2,
        "dee subject clean":    d["subject"] == "Saving Dee's Plumbing & Construction,Inc. time on after-hours call capture",
        "dee replied=true":     d["replied"] == "true",
        "dee replied_at":       "2026-03-14T22:51:59" in d["replied_at"],
        "dee reply_snippet":    "Dee" in d["reply_snippet"],
        "dee message_id=''":    d["message_id"] == "",
        "dee next_fu=''":       d["next_followup_at"] == "",
        "dee campaign_key=''":  d["campaign_key"] == "",
        "dee attempt=1":        d["contact_attempt_count"] == "1",
        "dee result=replied":   d["contact_result"] == "replied",
        "lars email":           l["to_email"] == "john@larsplumbing.com",
        "lars lcc=''":          l["last_contact_channel"] == "",
        "lars attempt=0":       l["contact_attempt_count"] == "0",
        "lars contact_result=''": l["contact_result"] == "",
        "lars message_id=''":   l["message_id"] == "",
        "lars replied=''":      l["replied"] == "",
    }
    failed = [k for k, v in checks.items() if not v]
    if failed:
        print("FAIL:", failed)
        for k in failed:
            col = k.split("=")[0].replace("dee ", "").replace("lars ", "").replace(" ","_").strip()
            print(f"  {k}: dee={d.get(col,'?')!r}  lars={l.get(col,'?')!r}")
    else:
        print("ALL CHECKS PASS")
    print(f"Output: {len(vcols)} columns, {len(vrows)} rows")


if __name__ == "__main__":
    repair()
