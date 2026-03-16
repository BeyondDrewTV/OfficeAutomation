import csv, sys

path = r'C:\Users\beyon\OneDrive\Desktop\OfficeAutomation\lead_engine\data\prospects.csv'

# Check with plain DictReader (no utf-8-sig) - same as _update_prospect_status uses
with open(path, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fns = list(reader.fieldnames or [])
    rows = [dict(r) for r in reader]

print('Fieldnames (utf-8):', fns)
print('None in fieldnames:', None in fns)
none_rows = [(i,r) for i,r in enumerate(rows) if None in r]
print('Rows with None key:', len(none_rows))
for i,r in none_rows[:5]:
    print(' row', i, r.get('business_name','?'), '| None-val:', repr(str(r.get(None,''))[:80]))

# Also check raw column count per line vs header
with open(path, encoding='utf-8-sig', newline='') as f:
    raw = list(csv.reader(f))
header_len = len(raw[0]) if raw else 0
print()
print('Header col count:', header_len)
bad_lines = [(i+1, len(row), row[0] if row else '') for i,row in enumerate(raw[1:]) if len(row) != header_len]
print('Lines with wrong col count:', len(bad_lines))
for lineno, cols, biz in bad_lines[:5]:
    print(f'  line {lineno}: {cols} cols (expected {header_len}), biz={biz!r}')
