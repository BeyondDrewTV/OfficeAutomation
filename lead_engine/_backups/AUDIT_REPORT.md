# Copperline Data Integrity Audit — 2026-03-14

## Files Changed

| File | Change |
|---|---|
| queue/pending_emails.csv | Cleaned — junk rows removed, cross-city dupes collapsed, Dee's to_email cleared, Goode email cleared, UTM params stripped |
| discovery/auto_prospect_agent.py | Full rewrite with _is_asset_email() fix + UTM stripping in discover_prospects() |
| discovery/__init__.py | Created (package init — crash fix) |
| discovery/prospect_discovery_agent.py | Created (dedupe_key_for_prospect + load_prospects_from_csv — crash fix) |

## Root Causes Found

1. CROSS-CITY DUPLICATION
   Same businesses drafted multiple times across Rockford/Machesney Park/Loves Park runs.
   Dedupe key (business_name + website) failed when same business appeared with different city.
   Fix: UTM params now stripped from website URLs before storage, improving key matching.

2. JUNK CSV ROWS (4 rows removed)
   Raw email body text leaked into CSV as standalone rows due to CSV escaping bug in a previous run.
   Rows removed: "mail after hours?", "I help local service businesses...", 
   "Happy to share a quick example...", "— Drew"" / scoring_reason garbage row.

3. JUNK EMAIL: Goode Plumbing to_email = m-home-banner@2x.webp
   Asset extension filter in _is_asset_email() did not catch this because .webp appeared
   as a pseudo-TLD after "2x", not at the end of a simple string.
   Fix: New _is_asset_email() checks bare extension token against local AND domain parts.
   Goode Plumbing to_email cleared, approved reset to false.

4. SENT COUNT DISCREPANCY (dashboard 22 vs Gmail 18)
   The ~4 gap = rows where sent_at was set via dashboard "log contact" button,
   NOT via the SMTP sender. These rows have sent_at set but message_id is empty.
   Reliable sent count = rows where BOTH sent_at AND message_id are non-empty.
   No code change needed — this is a display/interpretation issue.

## Queue State After Cleanup

- Total rows: 109 (down from inflated 1,123 lines)
- Rows with sent_at set: ~22 (matches dashboard pre-cleanup)
- Rows with sent_at + message_id (confirmed SMTP sends): 18 (matches Gmail)
- Dee's Plumbing: kept, to_email cleared (was drewyomantas@gmail.com — your own address)
- Goode Plumbing: kept, to_email cleared, approved=false (was .webp filename)

## Duplicate Prevention Going Forward

- UTM query params now stripped from all website URLs at discovery time
- Deduplication key (business_name + clean_website) will now correctly catch 
  the same business discovered via different UTM-decorated URLs

## Send Approved Status

CONFIRMED MANUAL — no changes made to send pipeline.
process_pending_emails() called with dry_run=True by default.
send_live flag remains False unless explicitly set.

## Template Rotation / Industry Mapping

WORKING CORRECTLY — no issues found.
detect_industry() maps business names to industry via keyword signals.
Subject lines rotate via hash of business_name.
draft_version column (v4 on recent rows) correctly tracks template generations.

## Backup Location

Original pending_emails.csv backed up to:
lead_engine/_backups/pending_emails_BACKUP_20260314.csv
