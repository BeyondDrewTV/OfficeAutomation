import sys, re
sys.stdout.reconfigure(encoding='utf-8')
data = open(r'C:\Users\beyon\OneDrive\Desktop\OfficeAutomation\lead_engine\dashboard_static\index.html', encoding='utf-8').read()
lines = data.splitlines()

# 1. Current nav tabs
print('=== NAV TABS ===')
for i,l in enumerate(lines):
    if 'data-page=' in l and 'nav-tab' in l:
        m = re.search(r'data-page="([^"]+)"', l)
        print(f'  {i+1:4d}  {m.group(1) if m else "?"}')

# 2. Page divs
print()
print('=== PAGE DIVS ===')
for i,l in enumerate(lines):
    m = re.search(r'id="(page-[^"]+)"', l)
    if m and 'class="page' in l:
        print(f'  {i+1:4d}  {m.group(1)}')

# 3. Leaflet / clustering libs already loaded?
print()
print('=== CDN SCRIPTS ===')
for i,l in enumerate(lines[:15]):
    if '<script' in l or '<link' in l:
        print(f'  {i+1}  {l.strip()[:100]}')

# 4. Map JS vars currently declared
print()
print('=== MAP JS VARS ===')
for i,l in enumerate(lines):
    if re.match(r'\s*(let|var|const)\s+_map', l):
        print(f'  {i+1}  {l.strip()[:80]}')

# 5. discover_area route check in server
srv = open(r'C:\Users\beyon\OneDrive\Desktop\OfficeAutomation\lead_engine\dashboard_server.py', encoding='utf-8').read()
print()
print('=== BACKEND ROUTES (area/geo) ===')
for i,l in enumerate(srv.splitlines()):
    if 'discover_area' in l or 'geo' in l.lower() or 'cluster' in l.lower():
        print(f'  {i+1}  {l.strip()[:80]}')

# 6. city_planner capabilities
cp = open(r'C:\Users\beyon\OneDrive\Desktop\OfficeAutomation\lead_engine\city_planner.py', encoding='utf-8').read()
print()
print('=== CITY_PLANNER PUBLIC METHODS ===')
for l in cp.splitlines():
    if l.strip().startswith('def ') and not l.strip().startswith('def _'):
        print(f'  {l.strip()[:80]}')
