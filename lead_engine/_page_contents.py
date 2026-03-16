import sys, re
sys.stdout.reconfigure(encoding='utf-8')
data = open(r'C:\Users\beyon\OneDrive\Desktop\OfficeAutomation\lead_engine\dashboard_static\index.html', encoding='utf-8').read()
lines = data.splitlines()

pages = []
for i,l in enumerate(lines):
    if 'class="page' in l and 'id="page-' in l:
        m = re.search(r'id="page-([^"]+)"', l)
        pages.append((i, m.group(1) if m else '?'))

for idx, (start, name) in enumerate(pages):
    end = pages[idx+1][0] if idx+1 < len(pages) else start+80
    snippet = lines[start:min(start+8, end)]
    # Grab any h2 or section header text
    headers = [l.strip() for l in snippet if '<h2' in l or 'section-hdr' in l or 'ops-section-hdr' in l]
    buttons = [re.sub(r'<[^>]+>','',l).strip() for l in snippet if 'btn btn-primary' in l or 'btn btn-ghost' in l]
    print(f'  page-{name} (line {start+1})')
    for h in headers[:2]: print(f'    H: {re.sub(chr(60)+"[^>]+>","",h)[:80]}')
    for b in buttons[:3]: print(f'    B: {b[:60]}')
