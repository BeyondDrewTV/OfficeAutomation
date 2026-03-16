import sys
sys.stdout.reconfigure(encoding='utf-8')
data = open(r'C:\Users\beyon\OneDrive\Desktop\OfficeAutomation\lead_engine\dashboard_static\index.html', encoding='utf-8').read()
lines = data.splitlines()

# Find ALL _mapInstance declarations and usages
print('=== _mapInstance declarations (let/var/const) ===')
for i,l in enumerate(lines):
    if 'let _mapInstance' in l or 'var _mapInstance' in l or 'const _mapInstance' in l:
        print(i+1, l.strip())

print()
print('=== _mapResultMarkers declaration ===')
for i,l in enumerate(lines):
    if 'let _mapResultMarkers' in l:
        print(i+1, l.strip())

print()
print('=== All map variable declarations in order ===')
for i,l in enumerate(lines):
    if any(x in l for x in ['let _map', 'let MAP_DEFAULT']):
        print(i+1, l.strip()[:80])

print()
# Show lines around where _mapResultMarkers is declared
idx = next((i for i,l in enumerate(lines) if 'let _mapResultMarkers' in l), None)
if idx:
    print('=== context around _mapResultMarkers ===')
    for i in range(max(0,idx-3), idx+10): print(i+1, lines[i])
