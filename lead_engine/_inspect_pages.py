import sys
sys.stdout.reconfigure(encoding='utf-8')

data = open(r'C:\Users\beyon\OneDrive\Desktop\OfficeAutomation\lead_engine\dashboard_static\index.html', encoding='utf-8').read()
lines = data.splitlines()

print("=== NAV TABS ===")
for i,l in enumerate(lines):
    if 'data-page=' in l and 'nav-tab' in l:
        print(i+1, l.strip()[:120])

print()
print("=== PAGE DIVS ===")
for i,l in enumerate(lines):
    if 'class="page' in l and 'id="page-' in l:
        print(i+1, l.strip()[:120])

print()
print("=== discover-bar ===")
for i,l in enumerate(lines):
    if 'class="discover-bar"' in l:
        print(i+1, l.strip()[:80])

print()
print("=== page-map ===")
for i,l in enumerate(lines):
    if 'page-map' in l:
        print(i+1, l.strip()[:120])
