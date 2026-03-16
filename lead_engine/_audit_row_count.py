import subprocess, sys, csv, io

BASE = r"C:\Users\beyon\OneDrive\Desktop\OfficeAutomation"

# --- All git commits that touched pending_emails.csv ---
result = subprocess.run(
    ["git", "-C", BASE, "log", "--oneline", "--all", "--", "lead_engine/queue/pending_emails.csv"],
    capture_output=True, text=True
)
commits = [line.split()[0] for line in result.stdout.strip().splitlines() if line.strip()]
print("Commits touching pending_emails.csv:", commits)
print()

# --- Row count at each commit ---
for sha in commits:
    raw = subprocess.run(
        ["git", "-C", BASE, "show", f"{sha}:lead_engine/queue/pending_emails.csv"],
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    if raw.returncode != 0:
        print(f"  {sha}: ERROR - {raw.stderr[:60]}")
        continue
    content = raw.stdout
    lines = content.splitlines()
    # Try csv parse for accurate row count
    try:
        reader = list(csv.DictReader(io.StringIO(content)))
        row_count = len(reader)
        col_count = len(reader[0]) if reader else 0
        first_col = list(reader[0].keys())[:4] if reader else []
    except Exception as e:
        row_count = max(0, len(lines) - 1)
        col_count = len(lines[0].split(",")) if lines else 0
        first_col = []
    print(f"  {sha}: {row_count} data rows, {col_count} cols, first cols: {first_col}")

# --- Also check current live file ---
print()
with open(BASE + r"\lead_engine\queue\pending_emails.csv", encoding="utf-8") as f:
    cur = list(csv.DictReader(f))
print(f"  LIVE FILE: {len(cur)} data rows, {len(cur[0])} cols")

# --- Check all backups ---
import os, glob
backup_dir = BASE + r"\lead_engine\_backups"
print()
print("Backups:")
for fpath in glob.glob(backup_dir + r"\*.csv"):
    try:
        with open(fpath, encoding="utf-8", errors="replace") as f:
            content = f.read()
        rows = list(csv.DictReader(io.StringIO(content)))
        print(f"  {os.path.basename(fpath)}: {len(rows)} rows, {len(rows[0]) if rows else 0} cols")
        if rows:
            print(f"    first biz: {rows[0].get('business_name','?')!r}")
    except Exception as e:
        lines = open(fpath, encoding="utf-8", errors="replace").read().splitlines()
        print(f"  {os.path.basename(fpath)}: {len(lines)} raw lines, parse error: {e}")
