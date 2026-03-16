import os, csv, io, glob

BASE = r"C:\Users\beyon\OneDrive\Desktop\OfficeAutomation"

# Search entire OfficeAutomation directory for ANY csv file that could
# be the 109-row queue. Look for files > 20KB (109 rows would be ~50-200KB)
print("=== ALL CSV FILES IN OfficeAutomation (searching for 109-row queue) ===")
csv_files = []
for root, dirs, files in os.walk(BASE):
    # Skip node_modules and .git objects
    dirs[:] = [d for d in dirs if d not in ("node_modules", ".git", "__pycache__")]
    for f in files:
        if f.endswith(".csv"):
            path = os.path.join(root, f)
            size = os.path.getsize(path)
            csv_files.append((size, path))

csv_files.sort(reverse=True)
for size, path in csv_files:
    rel = path.replace(BASE + "\\", "")
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            content = fh.read()
        lines = content.splitlines()
        # Quick row count
        try:
            rows = list(csv.DictReader(io.StringIO(content)))
            n = len(rows)
            cols = list(rows[0].keys()) if rows else []
            first_biz = rows[0].get("business_name","?") if rows else "?"
        except:
            n = max(0, len(lines)-1)
            cols = []
            first_biz = lines[1][:40] if len(lines) > 1 else "?"
        print(f"  {size:>10,} B  {n:>4} rows  {rel}")
        if n > 5:
            print(f"             cols ({len(cols)}): {cols[:5]}")
            print(f"             first biz: {first_biz!r}")
    except Exception as e:
        print(f"  {size:>10,} B  ERR  {rel}: {e}")

# Also check the automation-agency-office memory folder for any queue data
print()
print("=== MEMORY CSVs ===")
mem_path = BASE + r"\automation-agency-office\memory"
for f in os.listdir(mem_path):
    if f.endswith(".csv"):
        path = os.path.join(mem_path, f)
        size = os.path.getsize(path)
        with open(path, encoding="utf-8", errors="replace") as fh:
            rows = list(csv.DictReader(fh))
        print(f"  {f}: {len(rows)} rows, {size:,} B")
        if rows:
            print(f"    cols: {list(rows[0].keys())}")
