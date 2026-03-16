data = open(r'C:\Users\beyon\OneDrive\Desktop\OfficeAutomation\lead_engine\dashboard_static\index.html', encoding='utf-8').read()
lines = data.splitlines()

page_map_start = next(i for i,l in enumerate(lines) if 'id="page-map"' in l)
depth = 0
block = []
for i in range(page_map_start, page_map_start + 60):
    l = lines[i]
    depth += l.count('<div') - l.count('</div>')
    block.append((i+1, l))
    if i > page_map_start and depth <= 0:
        break

print('page-map block (%d lines):' % len(block))
for lineno, l in block:
    print(lineno, l[:100])

has_style = any('<style>' in l for _, l in block)
print()
print('style tag inside page-map:', has_style)
print('map CSS in head:', '#map-container' in data[:data.index('</style>')])
print('</script> count:', data.count('</script>'))
print('</body> count:', data.count('</body>'))
print('</html> count:', data.count('</html>'))
print('total lines:', len(lines))
