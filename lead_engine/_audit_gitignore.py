import subprocess, csv, io

BASE = r"C:\Users\beyon\OneDrive\Desktop\OfficeAutomation"

# The .gitignore might explain why pending_emails.csv was never committed with data
gitignore = open(BASE + r"\lead_engine\.venv\.gitignore", encoding="utf-8", errors="replace").read()
print("=== .venv/.gitignore ===")
print(gitignore[:500])
print()

# Check root .gitignore
try:
    root_gi = open(BASE + r"\.gitignore", encoding="utf-8", errors="replace").read()
    print("=== root .gitignore ===")
    print(root_gi)
except:
    print("No root .gitignore")

print()

# Check if there's a lead_engine-level gitignore
import os
for root, dirs, files in os.walk(BASE + r"\lead_engine"):
    for f in files:
        if f == ".gitignore":
            path = os.path.join(root, f)
            print(f"=== {path} ===")
            print(open(path, encoding="utf-8", errors="replace").read())
    # Don't recurse into .venv
    dirs[:] = [d for d in dirs if d not in (".venv", "__pycache__")]
