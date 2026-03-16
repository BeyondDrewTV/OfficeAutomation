import subprocess, csv, io, os

BASE = r"C:\Users\beyon\OneDrive\Desktop\OfficeAutomation"

# Check what's in the stash
print("=== GIT STASH CONTENTS ===")
stash_files = subprocess.run(
    ["git", "-C", BASE, "stash", "show", "--name-only", "stash@{0}"],
    capture_output=True, text=True
)
print(stash_files.stdout or "(no output)")

# Check if pending_emails.csv is in the stash
stash_csv = subprocess.run(
    ["git", "-C", BASE, "stash", "show", "-p", "stash@{0}", "--", "lead_engine/queue/pending_emails.csv"],
    capture_output=True, text=True, encoding="utf-8", errors="replace"
)
if stash_csv.stdout.strip():
    lines = stash_csv.stdout.splitlines()
    print(f"pending_emails.csv in stash: {len(lines)} diff lines")
    # Count + lines (added) to estimate rows
    added = [l[1:] for l in lines if l.startswith("+") and not l.startswith("+++")]
    print(f"  Added lines in diff: {len(added)}")
    print(f"  First 5 added lines:")
    for l in added[:5]:
        print(f"    {repr(l[:100])}")
else:
    print("pending_emails.csv NOT in stash")
print()

# Check prospects.csv row count and status distribution
print("=== PROSPECTS.CSV ===")
with open(BASE + r"\lead_engine\data\prospects.csv", encoding="utf-8-sig") as f:
    prospects = list(csv.DictReader(f))
print(f"Total prospects: {len(prospects)}")
if prospects:
    print(f"Columns: {list(prospects[0].keys())}")
    # Status distribution
    from collections import Counter
    status_counts = Counter(p.get("status","") for p in prospects)
    print(f"Status distribution: {dict(status_counts)}")
    sent_count = sum(1 for p in prospects if p.get("email_sent","").lower() == "true" or p.get("status","") == "sent")
    print(f"email_sent=true or status=sent: {sent_count}")
    drafted = sum(1 for p in prospects if p.get("status","") == "drafted")
    print(f"status=drafted: {drafted}")
    print(f"\nFirst 3 prospects:")
    for p in prospects[:3]:
        print(f"  {p.get('business_name','')} | status={p.get('status','')} | email_sent={p.get('email_sent','')}")
