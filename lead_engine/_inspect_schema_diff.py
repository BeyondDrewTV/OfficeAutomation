import csv

path = r'C:\Users\beyon\OneDrive\Desktop\OfficeAutomation\lead_engine\data\prospects.csv'
agent_cols = [
    "business_name", "city", "state", "website",
    "phone", "contact_method", "industry", "likely_opportunity", "priority_score",
    "to_email", "status", "email_sent", "sent_at", "followup_due",
    "scan_notes", "contactability",
    "facebook_url", "instagram_url", "contact_form_url",
    "social_channels", "social_dm_text",
]

with open(path, encoding='utf-8-sig', newline='') as f:
    existing_header = next(csv.reader(f))

print('Existing header cols:', len(existing_header))
print('Agent PROSPECTS_COLUMNS cols:', len(agent_cols))
print()
extra = [c for c in agent_cols if c not in existing_header]
missing = [c for c in existing_header if c not in agent_cols]
print('In agent but NOT in existing header (would overflow on append):', extra)
print('In existing header but NOT in agent (would be dropped on append):', missing)
print()
# _append_to_prospects unified header logic
unified = list(existing_header)
for col in agent_cols:
    if col not in unified:
        unified.append(col)
print('Unified header after append:', len(unified), 'cols')
print('Unified:', unified)
