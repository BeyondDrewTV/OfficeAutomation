import sys
sys.stdout.reconfigure(encoding='utf-8')
data = open(r'C:\Users\beyon\OneDrive\Desktop\OfficeAutomation\lead_engine\dashboard_static\index.html', encoding='utf-8').read()
lines = data.splitlines()

print('=== NAV TABS (in order) ===')
for i,l in enumerate(lines):
    if 'data-page=' in l and 'nav-tab' in l:
        # extract data-page value
        import re
        m = re.search(r'data-page="([^"]+)"', l)
        label_m = re.search(r'>[^<]*([A-Za-z][A-Za-z\s\-/]+)', l.replace('<!--',''))
        page = m.group(1) if m else '?'
        print(f'  line {i+1:4d}  page={page}')

print()
print('=== PAGE DIVS (id=page-*) in order ===')
for i,l in enumerate(lines):
    if 'class="page' in l and 'id="page-' in l:
        import re
        m = re.search(r'id="(page-[^"]+)"', l)
        print(f'  line {i+1:4d}  {m.group(1) if m else "?"}')
