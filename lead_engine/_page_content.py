import sys, re
sys.stdout.reconfigure(encoding='utf-8')
data = open(r'C:\Users\beyon\OneDrive\Desktop\OfficeAutomation\lead_engine\dashboard_static\index.html', encoding='utf-8').read()
lines = data.splitlines()

page_starts = {}
for i,l in enumerate(lines):
    m = re.search(r'id="(page-[^"]+)"', l)
    if m and 'class="page' in l:
        page_starts[m.group(1)] = i

# For each page, show first ~5 non-blank lines of content
for page_id, start in sorted(page_starts.items(), key=lambda x: x[1]):
    content_lines = []
    for l in lines[start+1:start+40]:
        stripped = l.strip()
        if stripped and not stripped.startswith('<div') and not stripped.startswith('<!--') and len(stripped) > 3:
            # strip HTML tags for readable preview
            text = re.sub(r'<[^>]+>', '', stripped).strip()
            if text and len(text) > 2:
                content_lines.append(text[:80])
        if len(content_lines) >= 3:
            break
    print(f'{page_id} (line {start+1})')
    for c in content_lines:
        print(f'  {c}')
    print()
