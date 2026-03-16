import sys
sys.stdout.reconfigure(encoding='utf-8')
data = open(r'C:\Users\beyon\OneDrive\Desktop\OfficeAutomation\lead_engine\dashboard_static\index.html', encoding='utf-8').read()
lines = data.splitlines()

for start_label, needle in [('switchPage map branch', "name === 'map'"), ('_mapInit function', 'function _mapInit()')]:
    idx = next(i for i,l in enumerate(lines) if needle in l)
    print(f'=== {start_label} (line {idx+1}) ===')
    for i in range(idx, idx+25):
        print(i+1, lines[i])
    print()
