import csv, sys

path = r'C:\Users\beyon\OneDrive\Desktop\OfficeAutomation\lead_engine\data\prospects.csv'
with open(path, 'rb') as f:
    first4 = f.read(4)
print('First 4 bytes hex:', first4.hex())

with open(path, encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    fns = list(reader.fieldnames or [])
    rows = [dict(r) for r in reader]

print('Fieldnames:', fns)
print('None in fieldnames:', None in fns)
print('Total rows:', len(rows))

none_rows = [(i, r) for i, r in enumerate(rows) if None in r]
print('Rows with None key:', len(none_rows))
for i, r in none_rows[:3]:
    print('  row', i, r.get('business_name', '?'), '| None=', repr(str(r.get(None, ''))[:60]))

extra_cols = [k for k in fns if k not in (None, '') and k.startswith(' ')]
print('Fieldnames with leading space:', extra_cols)

print('contact_note in fieldnames:', 'contact_note' in fns)
print('All fieldnames:')
for f in fns:
    print(' ', repr(f))
