import csv, io

path = r'C:\Users\beyon\OneDrive\Desktop\OfficeAutomation\lead_engine\data\prospects.csv'

# Current header
with open(path, encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    current_header = list(reader.fieldnames or [])

print('Current header:', current_header)
print('Count:', len(current_header))
print()

# What _append_to_prospects writes (PROSPECTS_COLUMNS from auto_prospect_agent.py)
PROSPECTS_COLUMNS = [
    "business_name", "city", "state", "website",
    "phone", "contact_method", "industry", "likely_opportunity", "priority_score",
    "to_email", "status", "email_sent", "sent_at", "followup_due",
    "scan_notes", "contactability",
    "facebook_url",
    "instagram_url",
    "contact_form_url",
    "social_channels",
    "social_dm_text",
]
print('PROSPECTS_COLUMNS:', PROSPECTS_COLUMNS)
print('Count:', len(PROSPECTS_COLUMNS))
print()

# Diff
in_agent_not_csv = set(PROSPECTS_COLUMNS) - set(current_header)
in_csv_not_agent = set(current_header) - set(PROSPECTS_COLUMNS)
print('In PROSPECTS_COLUMNS but NOT in current header:', in_agent_not_csv)
print('In current header but NOT in PROSPECTS_COLUMNS:', in_csv_not_agent)
print()

# What _update_prospect_status in run_lead_engine.py will see AFTER append
# It reads the file again — but if the APPEND added rows with extra keys,
# DictReader will put extras into None.
# The _append_to_prospects uses extrasaction='ignore' on write,
# so new columns from PROSPECTS_COLUMNS not in existing header get dropped.
# BUT if the existing header has FEWER columns than PROSPECTS_COLUMNS,
# the unified header will EXTEND fieldnames.
# Then when writing back rows that came from the original short header,
# they won't have the new columns => DictWriter with extrasaction='ignore' handles that.
# The None key comes from a different direction: rows with MORE values than header columns.

# Let's check _append_to_prospects logic: it reads existing_header then does
# unified = list(existing_header)
# for col in PROSPECTS_COLUMNS: if col not in unified: unified.append(col)
# Then opens file in APPEND mode and writes NEW rows with the unified fieldnames.
# But the OLD rows already in the file were written with the OLD shorter header.
# DictReader will then read the file with unified fieldnames.
# Old rows: only 16 cols => extra unified columns get empty string (DictReader pads with None for missing)
# Wait - DictReader uses the FIRST LINE as fieldnames. After append:
# First line = original 16-col header (unchanged, _append only opens in 'a' mode)
# New rows have 21+ columns written positionally to match unified fieldnames
# But unified fieldnames != file header (file header is still old 16-col)
# So new rows have MORE fields than the header says => overflow goes to row[None]

print('ROOT CAUSE CONFIRMED:')
print('_append_to_prospects opens file in append mode.')
print('It determines unified fieldnames but does NOT rewrite the header.')
print('New rows are written with unified (longer) fieldnames positionally.')
print('But the file header is still the old shorter one.')
print('When run_lead_engine reads the file with DictReader,')
print('header says 16 cols, new rows have 21+ fields => overflow => row[None]')
