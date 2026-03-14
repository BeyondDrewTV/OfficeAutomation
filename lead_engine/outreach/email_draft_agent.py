from __future__ import annotations

import hashlib
import json
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Industry detection (unchanged — used by pipeline)
# ---------------------------------------------------------------------------

INDUSTRY_SIGNALS: List[Tuple[str, List[str]]] = [
    ("plumbing",     ["plumb", "sewer", "drain", "pipe", "rooter", "septic"]),
    ("hvac",         ["hvac", "heating", "cooling", "air condition", "furnace", "refrigerat"]),
    ("electrical",   ["electric", "wiring", "electrician", "panel", "generator"]),
    ("roofing",      ["roof", "gutter", "siding", "shingle"]),
    ("landscaping",  ["landscap", "lawn", "garden", "tree", "mow", "sod"]),
    ("pest_control", ["pest", "exterminator", "termite", "rodent", "bug"]),
    ("dental",       ["dental", "dentist", "orthodont", "oral"]),
    ("medical",      ["medical", "clinic", "doctor", "physician", "urgent care", "chiro"]),
    ("legal",        ["law", "attorney", "lawyer", "legal", "firm"]),
    ("real_estate",  ["real estate", "realty", "realtor", "property management"]),
    ("restaurant",   ["restaurant", "diner", "cafe", "catering", "bistro", "eatery", "pizza", "grill"]),
    ("auto",         ["auto", "mechanic", "car repair", "tire", "collision", "body shop"]),
    ("cleaning",     ["cleaning", "janitorial", "maid", "housekeeping", "pressure wash"]),
    ("construction", ["construction", "contractor", "remodel", "renovation", "carpent", "mason"]),
    ("insurance",    ["insurance", "insur", "agency", "broker"]),
    ("accounting",   ["account", "bookkeep", "tax", "cpa", "payroll"]),
    ("salon",        ["salon", "barber", "hair", "nail", "spa", "beauty"]),
    ("gym",          ["gym", "fitness", "personal train", "yoga", "pilates"]),
    ("moving",       ["moving", "mover", "storage", "relocation"]),
]


def detect_industry(business_name: str, provided_industry: str = "") -> str:
    if provided_industry and provided_industry.strip().lower() not in ("", "unknown", "n/a"):
        return provided_industry.strip().lower()
    name_lower = (business_name or "").lower()
    for industry, signals in INDUSTRY_SIGNALS:
        if any(sig in name_lower for sig in signals):
            return industry
    return "general"


# ---------------------------------------------------------------------------
# Signal-aware email templates (automation_opportunity driven)
# ---------------------------------------------------------------------------
# Each opportunity maps to 3 variants (selected deterministically by name hash).
# Keys: subject, body  — body is under 70 words, one paragraph, casual tone.
# Banned words: optimize, revolutionize, leverage, synergy, streamline,
#               game-changer, cutting-edge, robust, scalable, seamlessly.
# ---------------------------------------------------------------------------

# (subject, body) tuples — 3 variants per opportunity
_TEMPLATES: Dict[str, List[Tuple[str, str]]] = {

    "missed_after_hours": [
        (
            "Quick question about after-hours calls",
            "Hi {name} team - do after-hours calls ever go to voicemail? "
            "A lot of {industry} businesses in {city} lose jobs that way. "
            "There's a simple setup that texts callers back instantly and "
            "captures their info even when you're off the clock. "
            "Would that be worth a quick look?",
        ),
        (
            "After-hours leads slipping through?",
            "Hey {name} - saw your number on the site. "
            "Quick question: what happens when someone calls at 9pm and you're not there? "
            "Most {industry} shops lose those leads for good. "
            "I set up a simple auto-response that captures them before they call a competitor. "
            "Want me to show you how it works?",
        ),
        (
            "Missing calls after hours?",
            "Hi {name} team - one thing I see a lot with {industry} companies in {city}: "
            "calls after hours go to voicemail and the customer doesn't leave a message. "
            "I built a fix that auto-texts them back in seconds. "
            "Takes about a week to set up. "
            "Curious if that's a problem you're running into?",
        ),
    ],

    "no_chat": [
        (
            "Anyone responding to your website visitors?",
            "Hi {name} team - noticed you have a contact form but no live chat. "
            "Visitors who don't fill out forms usually just leave. "
            "A simple chat widget can catch those people before they go. "
            "I set these up for {industry} businesses in {city} pretty quickly. "
            "Worth a 15-minute look?",
        ),
        (
            "Website leads going quiet?",
            "Hey {name} - people landing on your site have a question right now "
            "but no quick way to ask it. "
            "A contact form is a barrier; a chat bubble isn't. "
            "I help {industry} shops in {city} add a lightweight chat that doesn't "
            "require anyone to be glued to a screen. "
            "Interested in how it works?",
        ),
        (
            "Quick thought on your site",
            "Hi {name} team - your site has a form, which is good. "
            "But most people won't fill one out on a first visit. "
            "A fast chat option can double the number of people who actually reach out. "
            "I've set this up for a few {industry} businesses in {city}. "
            "Want to see what it looks like?",
        ),
    ],

    "no_booking": [
        (
            "Are customers calling just to schedule?",
            "Hi {name} team - do you still take bookings over the phone? "
            "A lot of {industry} businesses in {city} lose customers who want to "
            "schedule at 11pm and won't wait until morning to call. "
            "I set up simple online booking that works around the clock. "
            "Want to see how other local shops are using it?",
        ),
        (
            "Online booking for {industry} - worth it?",
            "Hey {name} - quick one. "
            "If a customer visits your site at midnight ready to book, "
            "can they? Most {industry} shops in {city} still rely on phone calls, "
            "which means they lose the late-night decisions. "
            "I set up lightweight booking in about a week. "
            "Curious if that's something you've thought about?",
        ),
        (
            "Losing bookings to the phone?",
            "Hi {name} team - saw you're operating in {city}. "
            "One pattern I keep seeing with {industry} businesses: "
            "customers want to book but won't call during business hours. "
            "Adding online booking catches those quietly lost jobs. "
            "Takes less than a week to set up. "
            "Is that something on your radar?",
        ),
    ],

    "unknown": [
        (
            "Quick automation idea for {name}",
            "Hi {name} team - I work with {industry} businesses in {city} on one thing: "
            "cutting out the manual back-and-forth with customers. "
            "Scheduling, follow-ups, reminders - all the stuff that eats time "
            "but doesn't need a human. "
            "Worth a 15-minute call to see if any of it fits?",
        ),
        (
            "One idea for {name}",
            "Hey {name} - quick note. "
            "I help local {industry} shops in {city} stop losing time to repetitive customer tasks. "
            "Things like follow-ups, booking confirmations, and missed-call responses. "
            "Flat fee, set up in about a week. "
            "Want me to send over a quick example?",
        ),
        (
            "Saving time at {name}",
            "Hi {name} team - I specialize in simple automations for {industry} businesses in {city}. "
            "Nothing complicated - just cutting out the manual steps that eat your day. "
            "Most owners I work with are surprised how fast it runs. "
            "Interested in a quick look?",
        ),
    ],
}


# ---------------------------------------------------------------------------
# Core draft function
# ---------------------------------------------------------------------------

_BANNED = [
    "optimize", "revolutionize", "leverage", "synergy", "streamline",
    "game-changer", "game changer", "cutting-edge", "cutting edge",
    "robust", "scalable", "seamlessly", "seamless",
]

_WORD_LIMIT = 70


def _variant(business_name: str, n: int = 3) -> int:
    digest = hashlib.sha256(business_name.strip().lower().encode()).hexdigest()
    return int(digest[:8], 16) % n


_SIGN_OFF = "\n\nBest,\nDrew\nCopperline"


def _fill(template: str, name: str, city: str, industry: str) -> str:
    industry_display = industry.replace("_", " ")
    return (
        template
        .replace("{name}", name)
        .replace("{city}", city)
        .replace("{industry}", industry_display)
    )


def _word_count(text: str) -> int:
    return len(text.split())


def _check_banned(text: str) -> None:
    text_lower = text.lower()
    hits = [w for w in _BANNED if w in text_lower]
    if hits:
        raise ValueError(f"Banned word(s) in generated email: {hits}")


def draft_email(prospect: Dict[str, str], final_priority_score: int) -> Tuple[str, str]:
    """
    Generate a signal-aware cold email under 70 words.

    Returns (subject, body) strings — pipeline-compatible.
    Also internally produces the JSON payload logged below.
    """
    business_name = (prospect.get("business_name") or "").strip()
    city          = (prospect.get("city") or "").strip()

    if not business_name:
        raise ValueError("Cannot draft email without business_name.")
    if not city:
        raise ValueError(f"Cannot draft email for {business_name} without city.")

    industry     = detect_industry(business_name, prospect.get("industry", ""))
    opportunity  = (prospect.get("automation_opportunity") or "unknown").strip().lower()

    # Fallback to "unknown" if key not in templates
    if opportunity not in _TEMPLATES:
        opportunity = "unknown"

    variants     = _TEMPLATES[opportunity]
    idx          = _variant(business_name, len(variants))
    subject_tmpl, body_tmpl = variants[idx]

    subject = _fill(subject_tmpl, business_name, city, industry)
    body_text = _fill(body_tmpl, business_name, city, industry)

    # Guard: word count (sign-off excluded from limit)
    wc = _word_count(body_text)
    if wc > _WORD_LIMIT:
        sentences = body_text.replace("?", ".").split(".")
        trimmed = []
        running = 0
        for s in sentences:
            words = len(s.split())
            if running + words > _WORD_LIMIT:
                break
            trimmed.append(s)
            running += words
        body_text = ". ".join(trimmed).strip() + "."

    body = body_text + _SIGN_OFF

    # Guard: banned words
    _check_banned(body)

    return subject, body


def draft_email_json(prospect: Dict[str, str], final_priority_score: int) -> Dict:
    """
    Same as draft_email but returns the full JSON payload.

    {
        "subject": "...",
        "email_body": "...",
        "tone": "casual"
    }
    """
    subject, body = draft_email(prospect, final_priority_score)
    return {
        "subject": subject,
        "email_body": body,
        "tone": "casual",
    }


# ── Legacy helpers ────────────────────────────────────────────────────────────

def pick_best_pitch_angle(likely_opportunity: str) -> str:
    """Kept for backward compatibility."""
    return (likely_opportunity or "booking automation").strip() or "booking automation"
