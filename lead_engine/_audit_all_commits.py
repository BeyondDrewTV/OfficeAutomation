import subprocess, csv, io

BASE = r"C:\Users\beyon\OneDrive\Desktop\OfficeAutomation"

# Check the pending_emails.csv at stash@{0}^ (the base commit when stash was made)
for ref in ["stash@{0}^", "stash@{0}^2"]:
    r = subprocess.run(
        ["git", "-C", BASE, "show", f"{ref}:lead_engine/queue/pending_emails.csv"],
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    if r.returncode == 0:
        lines = r.stdout.splitlines()
        try:
            rows = list(csv.DictReader(io.StringIO(r.stdout)))
        except:
            rows = []
        print(f"{ref}: {len(lines)} raw lines, {len(rows)} csv rows")
        if rows:
            print(f"  First: {rows[0].get('business_name','?')!r}")
            print(f"  Last:  {rows[-1].get('business_name','?')!r}")
    else:
        print(f"{ref}: returncode={r.returncode} {r.stderr[:60]}")

print()

# Check prospects.csv at stash base
for ref in ["stash@{0}^", "stash@{0}^2"]:
    r = subprocess.run(
        ["git", "-C", BASE, "show", f"{ref}:lead_engine/data/prospects.csv"],
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    if r.returncode == 0:
        lines = r.stdout.splitlines()
        try:
            rows = list(csv.DictReader(io.StringIO(r.stdout)))
        except:
            rows = []
        print(f"{ref} prospects: {len(lines)} raw lines, {len(rows)} csv rows")
        if rows:
            print(f"  Cols: {list(rows[0].keys())}")
            print(f"  Status dist: {dict(__import__('collections').Counter(r.get('status','') for r in rows))}")
    else:
        print(f"{ref} prospects: returncode={r.returncode}")

print()
# Check all remaining git refs for any large pending_emails.csv
all_refs = subprocess.run(
    ["git", "-C", BASE, "log", "--all", "--oneline"],
    capture_output=True, text=True
)
print("All commits:")
print(all_refs.stdout)

# Try to find the 109-row file by checking each commit
for line in all_refs.stdout.splitlines():
    sha = line.split()[0]
    r = subprocess.run(
        ["git", "-C", BASE, "show", f"{sha}:lead_engine/queue/pending_emails.csv"],
        capture_output=True, text=True, encoding="utf-8", errors="replace"
    )
    if r.returncode == 0:
        raw_lines = len(r.stdout.splitlines())
        if raw_lines > 5:
            print(f"  FOUND ROWS at {sha}: {raw_lines} lines")
