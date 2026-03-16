import subprocess

BASE = r"C:\Users\beyon\OneDrive\Desktop\OfficeAutomation"

# The 109-row queue was ONLY ever on disk, never in git (gitignored).
# The AUDIT_REPORT says it was cleaned to 109 rows from 1,123 lines.
# Check if the AUDIT_REPORT backup (pending_emails_BACKUP_20260314.csv) 
# was the pre-cleanup file that should have had the 109 rows.
backup = open(BASE + r"\lead_engine\_backups\pending_emails_BACKUP_20260314.csv", encoding="utf-8", errors="replace").read()
print("=== pending_emails_BACKUP_20260314.csv FULL CONTENT ===")
print(repr(backup))
print()

# Check git log for the ORIG_HEAD - there may have been a large file that got overwritten
orig_head = subprocess.run(
    ["git", "-C", BASE, "show", "ORIG_HEAD:lead_engine/queue/pending_emails.csv"],
    capture_output=True, text=True, encoding="utf-8", errors="replace"
)
print(f"ORIG_HEAD pending_emails: returncode={orig_head.returncode}")
if orig_head.stdout:
    lines = orig_head.stdout.splitlines()
    print(f"  Lines: {len(lines)}")
    print(f"  First: {lines[0][:100]}")

# Check if there's a git stash with csv data in a different path
stash_stat = subprocess.run(
    ["git", "-C", BASE, "stash", "show", "stash@{0}", "--stat"],
    capture_output=True, text=True
)
print()
print("=== Stash stat ===")
print(stash_stat.stdout)

# Check if the data CSVs in the stash have anything
for sha_ref in ["stash@{0}^", "stash@{0}^2", "stash@{0}^3"]:
    r = subprocess.run(
        ["git", "-C", BASE, "ls-tree", "--name-only", "-r", sha_ref],
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    if r.returncode == 0 and r.stdout.strip():
        csvs = [l for l in r.stdout.splitlines() if l.endswith(".csv")]
        if csvs:
            print(f"{sha_ref} CSVs: {csvs}")

# Check the automation-agency-office memory prospects.csv content
mem_prospects = open(BASE + r"\automation-agency-office\memory\prospects.csv", encoding="utf-8", errors="replace").read()
print()
print("=== memory/prospects.csv ===")
print(repr(mem_prospects[:300]))
