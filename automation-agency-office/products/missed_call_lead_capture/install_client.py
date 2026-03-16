"""
install_client.py — Client onboarding CLI for Missed Call Lead Capture
Automation Biz | v1.1

Usage:
    python install_client.py

What it does:
  1. Prompts for all required + optional client fields
  2. Validates all inputs before writing anything
  3. Adds the client block to clients.json
  4. Creates the Google Sheet tab (if sheet doesn't have it yet)
  5. Prints a clean success summary

Requirements:
  - .env must be populated (Twilio + Google creds)
  - service_account.json must be present
  - The target Google Sheet must already exist and be shared
    with the service account email (Editor)
"""

import json
import os
import re
import sys
from pathlib import Path

# Load .env before anything else
from dotenv import load_dotenv
load_dotenv()

from sheets import ensure_sheet_tab_exists

# ── Paths ──────────────────────────────────────────────────────────────────
BASE_DIR     = Path(__file__).parent
CLIENTS_FILE = BASE_DIR / "clients.json"


# ── Helpers ────────────────────────────────────────────────────────────────

E164_RE = re.compile(r"^\+1\d{10}$")

def _e164(value: str, field: str) -> str:
    """Validate E.164 US number. Returns cleaned value or raises."""
    v = value.strip()
    if not E164_RE.match(v):
        raise ValueError(
            f"{field} must be E.164 format (+1XXXXXXXXXX). Got: {v!r}"
        )
    return v


def _require(value: str, field: str) -> str:
    v = value.strip()
    if not v:
        raise ValueError(f"{field} is required and cannot be empty.")
    return v


def _ask(prompt: str, required: bool = True, default: str = "") -> str:
    suffix = f" [{default}]" if default else (" (required)" if required else " (optional, Enter to skip)")
    while True:
        raw = input(f"  {prompt}{suffix}: ").strip()
        if not raw and default:
            return default
        if not raw and not required:
            return ""
        if not raw and required:
            print("    ✗ This field is required.")
            continue
        return raw


def _load_clients() -> dict:
    if CLIENTS_FILE.exists():
        with open(CLIENTS_FILE, "r") as f:
            return json.load(f)
    return {}


def _save_clients(clients: dict):
    with open(CLIENTS_FILE, "w") as f:
        json.dump(clients, f, indent=2)
        f.write("\n")


def _slug(name: str) -> str:
    """Turn 'ABC Plumbing' → 'abc_plumbing' as a suggested client_id."""
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


# ── Main ───────────────────────────────────────────────────────────────────

def main():
    print()
    print("=" * 58)
    print("  MISSED CALL LEAD CAPTURE — Client Onboarding")
    print("  Automation Biz")
    print("=" * 58)
    print()

    clients = _load_clients()

    # ── Step 1: Collect inputs ─────────────────────────────────────────────
    print("Step 1 — Client details")
    print("-" * 40)

    # Business name first so we can suggest a client_id
    business_name = _require(_ask("Business name"), "business_name")
    suggested_id  = _slug(business_name)

    client_id = _require(
        _ask("Client ID (unique key)", default=suggested_id),
        "client_id"
    )

    owner_phone  = _ask("Owner phone (E.164, e.g. +18155551234)")
    owner_email  = _require(_ask("Owner email"), "owner_email")
    twilio_number = _ask("Twilio number (E.164, e.g. +18155550200)")

    print()
    print("Step 2 — Google Sheets")
    print("-" * 40)
    spreadsheet_id = _require(_ask("Google Sheet ID"), "spreadsheet_id")
    sheet_name     = _ask("Sheet tab name", default=business_name)

    print()
    print("Step 3 — Optional overrides (Enter to use defaults)")
    print("-" * 40)
    voice_message = _ask("Custom voice message", required=False)
    auto_sms      = _ask("Custom auto-SMS text", required=False)

    # ── Step 2: Validate ───────────────────────────────────────────────────
    print()
    print("Validating...")

    errors = []

    try:
        owner_phone = _e164(owner_phone, "owner_phone")
    except ValueError as e:
        errors.append(str(e))

    try:
        twilio_number = _e164(twilio_number, "twilio_number")
    except ValueError as e:
        errors.append(str(e))

    if client_id in clients:
        errors.append(
            f"client_id '{client_id}' already exists in clients.json. "
            "Choose a different ID."
        )

    existing_twilio = {
        cfg["twilio_number"]: cid
        for cid, cfg in clients.items()
        if "twilio_number" in cfg
    }
    if twilio_number in existing_twilio:
        errors.append(
            f"twilio_number {twilio_number} is already assigned to "
            f"client '{existing_twilio[twilio_number]}'."
        )

    if errors:
        print()
        print("  ✗ Validation failed:")
        for e in errors:
            print(f"    • {e}")
        print()
        sys.exit(1)

    print("  ✓ All fields valid")

    # ── Step 3: Provision Google Sheet tab ────────────────────────────────
    print()
    print(f"Provisioning Google Sheet tab '{sheet_name}'...")
    try:
        created = ensure_sheet_tab_exists(spreadsheet_id, sheet_name)
        if created:
            print(f"  ✓ Tab '{sheet_name}' created with header row")
        else:
            print(f"  ✓ Tab '{sheet_name}' already exists — no changes made")
    except Exception as exc:
        print(f"  ✗ Google Sheets error: {exc}")
        print()
        print("  Client was NOT saved. Fix the Sheets issue and re-run.")
        sys.exit(1)

    # ── Step 4: Save to clients.json ──────────────────────────────────────
    entry = {
        "business_name":  business_name,
        "owner_phone":    owner_phone,
        "owner_email":    owner_email,
        "twilio_number":  twilio_number,
        "spreadsheet_id": spreadsheet_id,
        "sheet_name":     sheet_name,
    }
    if voice_message:
        entry["voice_message"] = voice_message
    if auto_sms:
        entry["auto_sms"] = auto_sms

    clients[client_id] = entry
    _save_clients(clients)
    print(f"  ✓ Client saved to clients.json")

    # ── Step 5: Success summary ────────────────────────────────────────────
    print()
    print("=" * 58)
    print("  ✅  CLIENT ONBOARDED SUCCESSFULLY")
    print("=" * 58)
    print(f"  Client ID      : {client_id}")
    print(f"  Business       : {business_name}")
    print(f"  Twilio number  : {twilio_number}")
    print(f"  Owner SMS      : {owner_phone}")
    print(f"  Owner email    : {owner_email}")
    print(f"  Sheet tab      : {sheet_name}")
    print(f"  Spreadsheet ID : {spreadsheet_id}")
    if voice_message:
        print(f"  Voice message  : (custom)")
    if auto_sms:
        print(f"  Auto-SMS       : (custom)")
    print()
    print("  Next steps:")
    print(f"  1. Set Twilio webhooks for {twilio_number}:")
    print( "       Voice: POST https://your-domain.com/incoming_call")
    print( "       SMS:   POST https://your-domain.com/incoming_sms")
    print( "  2. Restart (or redeploy) the Flask server")
    print( "  3. Call the Twilio number to verify the flow end-to-end")
    print()


if __name__ == "__main__":
    main()
