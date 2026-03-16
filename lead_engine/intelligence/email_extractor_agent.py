"""
Email Extractor Agent
Scans business websites and Google search for contact email addresses.
Reads prospects.csv, finds emails, writes results back to CSV.

Usage:
    python lead_engine/intelligence/email_extractor_agent.py
    python lead_engine/intelligence/email_extractor_agent.py --limit 10
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Set
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

BASE_DIR = Path(__file__).resolve().parent.parent
PROSPECTS_CSV   = BASE_DIR / "data" / "prospects.csv"
PENDING_CSV     = BASE_DIR / "queue" / "pending_emails.csv"

TIMEOUT = 10
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}
JUNK_DOMAINS = {
    "sentry.io", "wixpress.com", "squarespace.com", "shopify.com",
    "wordpress.com", "godaddy.com", "amazonaws.com", "cloudfront.net",
    "googletagmanager.com", "google.com", "facebook.com", "twitter.com",
    "instagram.com", "tiktok.com", "youtube.com", "example.com",
    "yourdomain.com", "domain.com", "email.com", "placeholder.com",
    "w3.org", "schema.org", "bootstrapcdn.com", "cdnjs.com",
}
JUNK_PREFIXES = {
    "noreply", "no-reply", "donotreply", "do-not-reply",
    "unsubscribe", "bounce", "mailer", "postmaster", "webmaster",
    "admin", "info@example", "test@", "user@",
}

def _fetch(url: str) -> str:
    """Fetch URL with realistic headers. Falls back to https if http fails."""
    urls_to_try = [url]
    # if http, also try https version
    if url.startswith("http://"):
        urls_to_try.append("https://" + url[7:])
    for u in urls_to_try:
        try:
            req = Request(u, headers=HEADERS)
            with urlopen(req, timeout=TIMEOUT) as r:
                raw = r.read()
                # try utf-8 first, then latin-1
                try:
                    return raw.decode("utf-8")
                except UnicodeDecodeError:
                    return raw.decode("latin-1", errors="ignore")
        except Exception:
            continue
    return ""


def _clean_email(email: str) -> Optional[str]:
    e = email.strip().lower()
    domain = e.split("@")[-1] if "@" in e else ""
    if domain in JUNK_DOMAINS:
        return None
    if any(e.startswith(p) for p in JUNK_PREFIXES):
        return None
    if len(e) > 80 or "." not in domain:
        return None
    # skip emails that look like filenames/code
    if any(c in e for c in ["=", "{", "}", "//", "\\", "(", ")", "<", ">"]):
        return None
    return e


def _extract_emails_from_html(html: str) -> List[str]:
    found: List[str] = []
    # decode mailto: links first (highest confidence)
    for mailto in re.findall(r'mailto:([^"\'>\s?&]+)', html, re.IGNORECASE):
        cleaned = _clean_email(re.split(r'[?&]', mailto)[0])
        if cleaned:
            found.append(cleaned)
    # then visible text emails
    for email in EMAIL_RE.findall(html):
        cleaned = _clean_email(email)
        if cleaned and cleaned not in found:
            found.append(cleaned)
    return found


def _contact_page_urls(base_url: str, html: str) -> List[str]:
    """Return likely contact/about page URLs found in the homepage."""
    contact_paths = ["/contact", "/contact-us", "/about", "/about-us",
                     "/reach-us", "/get-in-touch", "/support"]
    base = urlparse(base_url)
    root = f"{base.scheme}://{base.netloc}"
    urls = [urljoin(root, p) for p in contact_paths]
    # also pick up any href that mentions contact/about
    for href in re.findall(r'href=["\']([^"\'#]+)', html, re.IGNORECASE):
        lower = href.lower()
        if any(k in lower for k in ["contact", "about", "reach", "touch"]):
            abs_url = urljoin(base_url, href)
            if urlparse(abs_url).netloc == base.netloc and abs_url not in urls:
                urls.append(abs_url)
    return urls[:8]  # cap pages tried


def find_email_for_business(business_name: str, website: str) -> tuple[Optional[str], str]:
    """Return (email_or_None, scan_reason) for logging in CSV."""
    if not website or not website.startswith(("http://", "https://")):
        return None, "no website"

    homepage = _fetch(website)
    if not homepage:
        return None, "website unreachable"

    emails = _extract_emails_from_html(homepage)
    source = "homepage"

    if not emails:
        contact_pages = _contact_page_urls(website, homepage)
        for url in contact_pages:
            page = _fetch(url)
            if page:
                emails = _extract_emails_from_html(page)
                if emails:
                    source = url.split("/")[-1] or "contact page"
                    break

    if not emails:
        return None, "scanned — no email found"

    # Prefer emails whose domain matches the business website
    site_domain = urlparse(website).netloc.replace("www.", "")
    emails.sort(key=lambda e: 0 if site_domain and site_domain in e else 1)
    return emails[0], f"found on {source}"


def _read_csv(path: Path) -> tuple[list, list]:
    """Return (fieldnames, rows)."""
    if not path.exists():
        return [], []
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = list(reader.fieldnames or [])
    return fieldnames, rows


def _write_csv(path: Path, fieldnames: list, rows: list) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def enrich_prospects_with_emails(csv_path: Path, limit: int = 0,
                                  overwrite: bool = False) -> Dict[str, int]:
    """
    Read prospects.csv, find emails for rows missing them, write back.
    Also updates matching rows in pending_emails.csv.
    Returns stats dict.
    """
    with csv_path.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)

    for col in ("to_email", "scan_note"):
        if col not in fieldnames:
            fieldnames.append(col)

    targets = [r for r in rows if overwrite or not (r.get("to_email") or "").strip()]
    if limit > 0:
        targets = targets[:limit]

    found = 0
    not_found = 0

    for row in targets:
        name    = row.get("business_name", "")
        website = row.get("website", "").strip()
        print(f"  Scanning: {name} ...", end=" ", flush=True)
        email, reason = find_email_for_business(name, website)
        row["scan_note"] = reason
        if email:
            row["to_email"] = email
            found += 1
            print(f"✓ {email} ({reason})")
        else:
            not_found += 1
            print(f"— {reason}")
        time.sleep(0.3)  # be polite to servers

    _write_csv(csv_path, fieldnames, rows)

    # Also patch pending_emails.csv if it exists
    _patch_pending_emails(rows)

    return {"scanned": len(targets), "found": found, "not_found": not_found}


def _patch_pending_emails(prospect_rows: list) -> None:
    """Copy found emails into matching pending_emails.csv rows."""
    if not PENDING_CSV.exists():
        return
    with PENDING_CSV.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        pending_fieldnames = list(reader.fieldnames or [])
        pending_rows = list(reader)

    # Build lookup: business_name (lower) -> email
    email_map = {
        r.get("business_name", "").strip().lower(): r.get("to_email", "").strip()
        for r in prospect_rows if r.get("to_email", "").strip()
    }

    updated = 0
    for row in pending_rows:
        key = row.get("business_name", "").strip().lower()
        if key in email_map and not (row.get("to_email") or "").strip():
            row["to_email"] = email_map[key]
            updated += 1

    if updated:
        _write_csv(PENDING_CSV, pending_fieldnames, pending_rows)
        print(f"\n  ✓ Also updated {updated} rows in pending_emails.csv")


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract emails from business websites.")
    parser.add_argument("--input", default=str(PROSPECTS_CSV))
    parser.add_argument("--limit", type=int, default=0,
                        help="Limit rows to scan (0 = all missing emails)")
    parser.add_argument("--overwrite", action="store_true",
                        help="Re-scan even rows that already have an email")
    args = parser.parse_args()

    path = Path(args.input)
    print(f"\nEmail Extractor — scanning: {path}\n")
    stats = enrich_prospects_with_emails(path, limit=args.limit, overwrite=args.overwrite)
    print(f"\nDone. Found: {stats['found']} | Not found: {stats['not_found']}")


if __name__ == "__main__":
    main()
