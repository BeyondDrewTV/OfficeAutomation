data = open(r'C:\Users\beyon\OneDrive\Desktop\OfficeAutomation\lead_engine\dashboard_static\index.html', encoding='utf-8').read()
lines = data.splitlines()

markers = ['function _mapInit', 'function switchPage', 'invalidateSize', 'setTimeout(_mapInit', '_mapPopulateIndustries']
for m in markers:
    hits = [(i+1, lines[i].strip()[:120]) for i,l in enumerate(lines) if m in l]
    print(m, '->', hits[:4])
