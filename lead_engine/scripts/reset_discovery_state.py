"""
scripts/reset_discovery_state.py

Reset Phase 2: archive and clean discovery-layer data files.

Operates on:
  - data/prospects.csv       -- discovery pool (drives "Discovered" KPI card)
  - data/search_history.json -- discovery run history (drives History tab)
  - data/city_planner.json   -- territory/city metadata

Does NOT touch:
  - queue/pending_emails.csv -- cleaned in Pass 17a, must remain intact

For each file:
  1. Archives current version to _backups/ with timestamp
  2. Resets to clean state

prospects.csv reset rule:
  Keep only rows whose email or business_name matches gmail_sent_preserve_set_for_reset.csv
  (same match logic used in Pass 17a queue reset)

Usage:
    cd lead_engine
    python scripts/reset_discovery_state.py [--dry-run]
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR  = Path(__file__).resolve().parent
LEAD_ENGINE = SCRIPT_DIR.parent
BACKUPS_DIR = LEAD_ENGINE / "_backups"

PROSPECTS_CSV    = LEAD_ENGINE / "data" / "prospects.csv"
SEARCH_HIST_JSON = LEAD_ENGINE / "data" / "search_history.json"
CITY_PLANNER_JSON = LEAD_ENGINE / "data" / "city_planner.json"
QUEUE_CSV        = LEAD_ENGINE / "queue" / "pending_emails.csv"
GMAIL_CSV        = LEAD_ENGINE / "scripts" / "gmail_sent_preserve_set_for_reset.csv"

_ASSET_FRAGS = ('.webp', '.png', '.jpg', '.jpeg', '.svg', '.gif', '.css', '.js')


def _norm_email(e):
    e = (e or '').strip().lower()
    if not e:
        return ''
    dom = e.split('@')[-1] if '@' in e else e
    for f in _ASSET_FRAGS:
        if e.endswith(f) or f.lstrip('.') in dom:
            return ''
    return e


def _norm_name(n):
    n = (n or '').strip().lower()
    n = re.sub(r'[^\w\s]', ' ', n)
    return ' '.join(n.split())


def _backup(source: Path, label: str) -> Path:
    BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    dest = BACKUPS_DIR / f'{source.stem}_{label}_{ts}{source.suffix}'
    dest.write_bytes(source.read_bytes())
    return dest


def _queue_row_count() -> int:
    if not QUEUE_CSV.exists():
        return 0
    with QUEUE_CSV.open('r', newline='', encoding='utf-8') as f:
        return sum(1 for _ in csv.DictReader(f))


def load_gmail_index():
    if not GMAIL_CSV.exists():
        print(f'WARNING: gmail_sent CSV not found at {GMAIL_CSV}')
        print('  prospects.csv will be cleared entirely.')
        return {}, {}
    with GMAIL_CSV.open('r', newline='', encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(f))
    email_idx = {}
    name_idx  = {}
    for r in rows:
        keep = (r.get('keep_for_reset') or 'true').strip().lower()
        if keep not in ('true', '1', 'yes', ''):
            continue
        ne = _norm_email(r.get('email', ''))
        nn = _norm_name(r.get('business_name', ''))
        if ne:
            email_idx[ne] = r
        if nn:
            name_idx.setdefault(nn, r)
    return email_idx, name_idx


def run(dry_run: bool = False) -> None:
    print()
    print('=' * 60)
    print('  Copperline Discovery State Reset')
    print('=' * 60)
    if dry_run:
        print('  *** DRY RUN -- no files will be written ***')
    print()

    # Safety: confirm queue is intact before doing anything
    queue_rows = _queue_row_count()
    print(f'  Live queue rows (must stay intact): {queue_rows}')
    if queue_rows == 0:
        print('  WARNING: live queue is empty -- verify pending_emails.csv before continuing')
    print()

    # ── 1. prospects.csv ──────────────────────────────────────────────────
    if not PROSPECTS_CSV.exists():
        print('  prospects.csv not found -- skipping')
    else:
        with PROSPECTS_CSV.open('r', newline='', encoding='utf-8-sig') as f:
            reader     = csv.DictReader(f)
            fieldnames = list(reader.fieldnames or [])
            prospects  = list(reader)

        email_idx, name_idx = load_gmail_index()

        keep = []
        drop = []
        for row in prospects:
            e = _norm_email(row.get('to_email', ''))
            n = _norm_name(row.get('business_name', ''))
            if (e and e in email_idx) or (n and n in name_idx):
                keep.append(row)
            else:
                drop.append(row)

        print(f'  prospects.csv:')
        print(f'    Current rows:  {len(prospects)}')
        print(f'    Keep (matched): {len(keep)}')
        print(f'    Archive:        {len(drop)}')

        if not dry_run:
            # Backup full file
            bp = _backup(PROSPECTS_CSV, 'pre_reset_phase2')
            print(f'    Backup:         {bp.name}')

            # Archive dropped rows
            if drop:
                ts = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
                arc = BACKUPS_DIR / f'prospects_archived_unmatched_{ts}.csv'
                with arc.open('w', newline='', encoding='utf-8') as f:
                    w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
                    w.writeheader()
                    w.writerows(drop)
                print(f'    Archived rows:  {arc.name}')

            # Write cleaned prospects.csv
            with PROSPECTS_CSV.open('w', newline='', encoding='utf-8') as f:
                w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
                w.writeheader()
                w.writerows(keep)
            print(f'    Written:        {len(keep)} rows to prospects.csv')
        else:
            print(f'    (dry-run: would write {len(keep)} rows, archive {len(drop)})')

    print()

    # ── 2. search_history.json ────────────────────────────────────────────
    if not SEARCH_HIST_JSON.exists():
        print('  search_history.json not found -- skipping')
    else:
        with SEARCH_HIST_JSON.open(encoding='utf-8') as f:
            history = json.load(f)

        print(f'  search_history.json:')
        print(f'    Current entries: {len(history)}')

        if not dry_run:
            bp = _backup(SEARCH_HIST_JSON, 'pre_reset_phase2')
            print(f'    Backup:          {bp.name}')
            with SEARCH_HIST_JSON.open('w', encoding='utf-8') as f:
                json.dump([], f)
            print(f'    Reset to:        [] (empty)')
        else:
            print(f'    (dry-run: would clear {len(history)} entries)')

    print()

    # ── 3. city_planner.json ──────────────────────────────────────────────
    if not CITY_PLANNER_JSON.exists():
        print('  city_planner.json not found -- skipping')
    else:
        with CITY_PLANNER_JSON.open(encoding='utf-8') as f:
            city_data = json.load(f)

        city_count = len(city_data) if isinstance(city_data, (list, dict)) else 0
        print(f'  city_planner.json:')
        print(f'    Current entries: {city_count}')

        if not dry_run:
            bp = _backup(CITY_PLANNER_JSON, 'pre_reset_phase2')
            print(f'    Backup:          {bp.name}')
            with CITY_PLANNER_JSON.open('w', encoding='utf-8') as f:
                # Preserve structure: write empty dict if was dict, empty list if was list
                json.dump({} if isinstance(city_data, dict) else [], f)
            print(f'    Reset to:        empty')
        else:
            print(f'    (dry-run: would clear {city_count} entries)')

    print()

    # ── Final check: queue still intact ──────────────────────────────────
    if not dry_run:
        final_queue = _queue_row_count()
        print(f'  Queue integrity check: {final_queue} rows in pending_emails.csv')
        if final_queue != queue_rows:
            print(f'  ERROR: queue row count changed! Was {queue_rows}, now {final_queue}')
        else:
            print(f'  Queue intact.')

    print()
    print('-' * 60)
    print('  SUMMARY')
    print('-' * 60)
    if dry_run:
        print('  Dry run complete -- re-run without --dry-run to apply')
    else:
        print('  Discovery state reset complete.')
        print('  Restart dashboard server to reload all data.')
    print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Reset Copperline discovery state (Phase 2).')
    parser.add_argument('--dry-run', action='store_true', help='Preview without writing.')
    args = parser.parse_args()
    run(dry_run=args.dry_run)
