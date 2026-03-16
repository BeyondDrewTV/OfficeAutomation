import csv, io

path = r'C:\Users\beyon\OneDrive\Desktop\OfficeAutomation\lead_engine\data\prospects.csv'
with open(path, encoding='utf-8-sig') as f:
    content = f.read()

lines = content.splitlines()
print('Total lines:', len(lines))

reader = csv.DictReader(io.StringIO(content))
fieldnames = list(reader.fieldnames or [])
print('Header cols:', len(fieldnames))

rows = list(reader)
print('Data rows:', len(rows))

none_rows = [(i, r) for i, r in enumerate(rows) if None in r]
print('Rows with None key:', len(none_rows))
for i, r in none_rows[:5]:
    biz = r.get('business_name', '?')
    print('  row', i, 'biz=', repr(biz))
    print('  None value:', repr(r[None]))

# Also check the contact_note column added by seed script
print()
print('Columns:', fieldnames)
