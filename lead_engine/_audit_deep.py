import subprocess, csv, io

BASE = r"C:\Users\beyon\OneDrive\Desktop\OfficeAutomation"

# Dump raw content of each older commit's pending_emails.csv
for sha in ["56eee0d", "a4fdce6", "a77839b"]:
    raw = subprocess.run(
        ["git", "-C", BASE, "show", f"{sha}:lead_engine/queue/pending_emails.csv"],
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    content = raw.stdout
    lines = content.splitlines()
    print(f"=== {sha} ===")
    print(f"  Raw line count: {len(lines)}")
    print(f"  First 3 lines:")
    for l in lines[:3]:
        print(f"    {repr(l[:120])}")
    print(f"  Last 2 lines:")
    for l in lines[-2:]:
        print(f"    {repr(l[:120])}")
    print()

# Check AUDIT_REPORT for the 109-row claim
audit = open(BASE + r"\lead_engine\_backups\AUDIT_REPORT.md", encoding="utf-8").read()
for line in audit.splitlines():
    if "109" in line or "row" in line.lower() or "clean" in line.lower():
        print("AUDIT:", line)
print()

# Check the git stash - there might be stashed rows
stash = subprocess.run(
    ["git", "-C", BASE, "stash", "list"],
    capture_output=True, text=True
)
print("Git stash list:", stash.stdout or "(empty)")

# Check git reflog for any lost commits
reflog = subprocess.run(
    ["git", "-C", BASE, "reflog", "--oneline", "-20"],
    capture_output=True, text=True
)
print("Git reflog (last 20):")
print(reflog.stdout)
