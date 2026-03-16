import sys
sys.stdout.reconfigure(encoding='utf-8')
data = open(r'C:\Users\beyon\OneDrive\Desktop\OfficeAutomation\lead_engine\dashboard_static\index.html', encoding='utf-8').read()
lines = data.splitlines()

# Find the switchPage map branch
idx = next(i for i,l in enumerate(lines) if "name === 'map'" in l)
print('=== switchPage map branch ===')
for i in range(idx-1, idx+8): print(i+1, lines[i])

print()
# Find _mapInit
idx2 = next(i for i,l in enumerate(lines) if 'function _mapInit()' in l)
print('=== _mapInit ===')
for i in range(idx2, idx2+22): print(i+1, lines[i])

print()
# Find _mapPopulateIndustries
idx3 = next(i for i,l in enumerate(lines) if 'function _mapPopulateIndustries()' in l)
print('=== _mapPopulateIndustries ===')
for i in range(idx3, idx3+12): print(i+1, lines[i])

print()
# Find Leaflet tags in head
print('=== Leaflet tags ===')
for i,l in enumerate(lines[:15]):
    if 'leaflet' in l.lower(): print(i+1, l.strip()[:120])
