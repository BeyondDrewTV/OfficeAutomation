from __future__ import annotations

import hashlib
import re
from typing import Dict, List, Optional, Tuple

DRAFT_VERSION = "v21"

# ---------------------------------------------------------------------------
# Copperline Voice Rules
# Applied to all first-touch and fallback drafts.
# This is the authoritative voice contract for email_draft_agent.py.
# Full version lives in docs/VOICE_RULES.md.
# ---------------------------------------------------------------------------

COPPERLINE_VOICE_RULES = """
Write like a real person, not a marketing system.
Keep it professional but conversational.
Be clear, direct, and natural.

Do:
- Use plain English
- Keep sentences fairly short
- Sound grounded and confident
- Sound like a human operator who understands the business
- Be friendly without being fluffy
- Be specific without sounding scripted
- Make the email feel one-to-one, not campaign-written
- Use owner-language: missed calls, callbacks, estimates, follow-up, scheduling

Do not:
- Use em dashes
- Use buzzwords: streamlined, optimized, unlock, transform, synergy, or similar
- Sound like a press release, a SaaS company, or an SDR sequence
- Sound overly polished, corporate, or performative
- Use fake warmth: "hope this finds you well", "hope you're doing well"
- Use filler: "just reaching out", "wanted to introduce myself"

Target feel:
One capable person reaching out to another about a real business issue they can help fix.
Not a pitch deck. Not a networking intro. Not an AI-generated cold email.
"""

# ---------------------------------------------------------------------------
# Industry-keyed fallback drafts (no observation available)
# Written in Drew's voice — specific to the trade, not generic.
# ---------------------------------------------------------------------------

_INDUSTRY_FALLBACK_BODIES: Dict[str, List[str]] = {
    "plumbing": [
        "I work with plumbing shops pretty regularly and the thing I see most is that the day fills up before the extra work does. Callbacks to return, estimates to follow up on, customer coordination between jobs. Not enough to justify bringing someone on for it, but enough to slow things down.\n\nI sit down with owners one on one, look at how things are actually running, find where the friction is, and build something specific to address it. I set it up and keep it running.\n\nI'd like to take a look and tell you what I'd address first.",
    ],
    "hvac": [
        "I work with HVAC owners pretty regularly and the thing I see most is that the coordination side never really settles. Quote follow-up, scheduling between calls, keeping up with customers during a busy stretch. Not a full-time job on its own, but it adds up faster than it gets cleared.\n\nI sit down with owners one on one, look at how things are actually running, find where the friction is, and build something specific to handle it. I set it up and keep it running from there.\n\nI'd like to take a look and tell you what I'd address first.",
    ],
    "electrical": [
        "I work with electrical contractors pretty regularly and the thing I see most is that the back office side fills up while the crew is on-site. Estimate requests coming in, customer follow-through, scheduling coordination. Not enough to justify a hire, but enough to create gaps.\n\nI sit down with owners one on one, look at how things are actually running, find where the friction is, and build something specific to address it. I set it up and keep it running.\n\nI'd like to take a look and tell you what I'd address first.",
    ],
    "roofing": [
        "I work with roofing contractors pretty regularly and the thing I see most is that tracking open estimates and following up with leads is harder to stay on top of than the actual job work. It piles up in the background, especially when the crew is stretched.\n\nI sit down with owners one on one, look at how things are actually running, find where the friction is, and build something specific to address it. I set it up and keep it running from there.\n\nI'd like to take a look and tell you what I'd address first.",
    ],
    "towing": [
        "I work with towing companies pretty regularly and the thing I see most is that the operational back-and-forth fills up the day faster than dispatch does. Billing follow-up, coordination with customers, keeping track of what's pending. Not enough to hire for, but enough to create drag.\n\nI sit down with owners one on one, look at how things are actually running, find where the friction is, and build something specific to handle it. I set it up and keep it running.\n\nI'd like to take a look and tell you what I'd address first.",
    ],
    "auto": [
        "I work with auto shops pretty regularly and the thing I see most is that the front desk is doing five things at once and the follow-through side is the first to slip. Appointment coordination, parts follow-up, customer communication between jobs. None of it is huge on its own, but it stacks up.\n\nI sit down with owners one on one, look at how things are actually running, find where the friction is, and build something specific to address it. I set it up and keep it running.\n\nI'd like to take a look and tell you what I'd address first.",
    ],
    "landscaping": [
        "I work with landscaping companies pretty regularly and the thing I see most is that the customer-facing side of the operation takes more time than it should. Estimate coordination, scheduling follow-up, keeping up with the back-and-forth between seasons. Not enough to justify a dedicated hire, but enough to slow things down.\n\nI sit down with owners one on one, look at how things are actually running, find where the friction is, and build something specific to handle it. I set it up and keep it running from there.\n\nI'd like to take a look and tell you what I'd address first.",
    ],
    "painting": [
        "I work with painting contractors pretty regularly and the thing I see most is that the estimate side is well-handled but the follow-up after isn't. Leads go cold not because the price is wrong but because no one circled back in time. That kind of thing tends to compound.\n\nI sit down with owners one on one, look at how things are actually running, find where the friction is, and build something specific to address it. I set it up and keep it running.\n\nI'd like to take a look and tell you what I'd address first.",
    ],
    "cleaning": [
        "I work with cleaning businesses pretty regularly and the thing I see most is that managing recurring clients is smooth, but the new inquiry side is slower than it needs to be. Intake handling, follow-through, getting back to people quickly. It adds up when you're running the operation yourself.\n\nI sit down with owners one on one, look at how things are actually running, find where the friction is, and build something specific to handle it. I set it up and keep it running from there.\n\nI'd like to take a look and tell you what I'd address first.",
    ],
    "concrete": [
        "I work with concrete contractors pretty regularly and the thing I see most is that the estimate-to-job gap is long and most of the delay is on the follow-up side. It's not a sales problem, it's a follow-through problem, and it compounds when the owner is in the field running other work.\n\nI sit down with owners one on one, look at how things are actually running, find where the friction is, and build something specific to address it. I set it up and keep it running.\n\nI'd like to take a look and tell you what I'd address first.",
    ],
    "tree_service": [
        "I work with tree service companies pretty regularly and the thing I see most is that demand spikes create coordination problems the normal process wasn't built for. Estimates pile up, follow-up slips, and a lot of good leads just go quiet. Not a marketing problem, a follow-through problem.\n\nI sit down with owners one on one, look at how things are actually running, find where the friction is, and build something specific to handle it. I set it up and keep it running from there.\n\nI'd like to take a look and tell you what I'd address first.",
    ],
    "flooring": [
        "I work with flooring contractors pretty regularly and the thing I see most is that the back-and-forth between estimate and install takes more attention than it should. Supplier coordination, customer follow-up, keeping the job pipeline moving. It's not dramatic, just a constant drain.\n\nI sit down with owners one on one, look at how things are actually running, find where the friction is, and build something specific to address it. I set it up and keep it running.\n\nI'd like to take a look and tell you what I'd address first.",
    ],
    "appliance_repair": [
        "I work with appliance repair shops pretty regularly and the thing I see most is that scheduling and parts coordination creates more back-and-forth than the actual repairs do. Confirming appointments, following up on parts, keeping customers in the loop. It fills the day in the background.\n\nI sit down with owners one on one, look at how things are actually running, find where the friction is, and build something specific to handle it. I set it up and keep it running from there.\n\nI'd like to take a look and tell you what I'd address first.",
    ],
    "moving": [
        "I work with moving companies pretty regularly and the thing I see most is that the gap between quote request and confirmed booking is where most of the manual work lives. Follow-up, customer coordination, keeping the schedule straight. Not huge in isolation, but it compounds.\n\nI sit down with owners one on one, look at how things are actually running, find where the friction is, and build something specific to address it. I set it up and keep it running.\n\nI'd like to take a look and tell you what I'd address first.",
    ],
    "pressure_washing": [
        "I work with pressure washing businesses pretty regularly and the thing I see most is that the booking side fills up faster than the seasonal schedule can absorb. Coordinating availability, following up on estimates, keeping up with the back-and-forth. It's the kind of work that doesn't feel heavy until it's already slowing things down.\n\nI sit down with owners one on one, look at how things are actually running, find where the friction is, and build something specific to handle it. I set it up and keep it running from there.\n\nI'd like to take a look and tell you what I'd address first.",
    ],
    "construction": [
        "I work with general contractors pretty regularly and the thing I see most is that the coordination side of the business takes more time than it should. Sub scheduling, estimate follow-up, supplier back-and-forth. Not the kind of thing that justifies a full hire, but enough to create real drag when the owner is already stretched.\n\nI sit down with owners one on one, look at how things are actually running, find where the friction is, and build something specific to address it. I set it up and keep it running.\n\nI'd like to take a look and tell you what I'd address first.",
    ],
    "pest_control": [
        "I work with pest control companies pretty regularly and the thing I see most is that managing recurring accounts is handled well but the new client intake side is slower than it could be. Getting back to inquiries, scheduling initial visits, following through. It piles up in the background.\n\nI sit down with owners one on one, look at how things are actually running, find where the friction is, and build something specific to handle it. I set it up and keep it running from there.\n\nI'd like to take a look and tell you what I'd address first.",
    ],
}

# Generic fallback for any industry not specifically mapped
_GENERIC_FALLBACK_BODIES: List[str] = [
    "I work with service business owners pretty regularly and the thing I see most is that the operational side of the business takes more of the day than the actual work does. Back-and-forth with customers, follow-through on estimates, small process gaps that don't justify a hire but don't go away on their own.\n\nI sit down with owners one on one, look at how things are actually running, find where the friction is, and build something specific to address it. I set it up and keep it running from there.\n\nI'd like to take a look and tell you what I'd address first.",
    "I work with small business owners across a lot of trades and the pattern I see most is that the work itself is manageable. It's the stuff around it that fills the day. Repetitive back-and-forth, follow-through gaps, tasks that keep coming back because nothing is handling them consistently. Not enough to justify another hire, but enough to slow things down.\n\nI sit down with owners one on one, look at how things are actually running, find what's creating the most drag, and build something specific to address it. I set it up and keep it running.\n\nI'd like to take a look and tell you what I'd address first.",
]

_FALLBACK_SUBJECTS: List[str] = [
    "repetitive work",
    "too many hats",
]


def _build_no_obs_draft(
    prospect: Dict[str, str],
    channel: str = "email",
) -> str:
    """
    Build a draft when no observation is available.
    Industry-specific, in Drew's voice, no generic filler.
    Feels like Drew knows the trade — just not this specific business yet.
    """
    industry = detect_industry(
        prospect.get("business_name", ""),
        prospect.get("industry", ""),
    )
    bodies = _INDUSTRY_FALLBACK_BODIES.get(industry, _GENERIC_FALLBACK_BODIES)
    # Deterministic variant pick
    name_hash = int(hashlib.md5(
        (prospect.get("business_name", "") + industry).encode()
    ).hexdigest(), 16)
    body = bodies[name_hash % len(bodies)]
    name = (prospect.get("business_name") or "").strip()
    city = (prospect.get("city") or "").strip()

    if channel == "dm":
        p1 = f"Hey{chr(10)}{chr(10)}My name is Drew."
    else:
        p1 = "My name is Drew."

    return f"{p1}\n\n{body}"



# ---------------------------------------------------------------------------
# Industry detection (pipeline-compatible, unchanged)
# ---------------------------------------------------------------------------

INDUSTRY_SIGNALS: List[Tuple[str, List[str]]] = [
    ("plumbing", ["plumb", "sewer", "drain", "pipe", "rooter", "septic"]),
    ("hvac", ["hvac", "heating", "cooling", "air condition", "furnace", "refrigerat"]),
    ("electrical", ["electric", "wiring", "electrician", "panel", "generator"]),
    ("locksmith", ["locksmith", "lock", "key", "lockout", "rekey"]),
    ("garage_door", ["garage door", "garage", "overhead door"]),
    ("towing", ["tow", "towing", "roadside", "wrecker", "recovery"]),
    ("roofing", ["roof", "gutter", "siding", "shingle"]),
    ("pest_control", ["pest", "exterminator", "termite", "rodent", "bug"]),
    ("auto", ["auto", "mechanic", "car repair", "tire", "collision", "body shop"]),
    ("construction", ["construction", "contractor", "remodel", "renovation", "carpent", "mason"]),
    ("dental", ["dental", "dentist", "orthodont", "oral"]),
    ("medical", ["medical", "clinic", "doctor", "physician", "urgent care", "chiro"]),
    ("legal", ["law", "attorney", "lawyer", "legal", "firm"]),
    ("real_estate", ["real estate", "realty", "realtor", "property management"]),
    ("restaurant", ["restaurant", "diner", "cafe", "catering", "bistro", "eatery", "pizza", "grill"]),
    ("cleaning", ["cleaning", "janitorial", "maid", "housekeeping", "pressure wash"]),
    ("insurance", ["insurance", "insur", "agency", "broker"]),
    ("accounting", ["account", "bookkeep", "tax", "cpa", "payroll"]),
    ("salon", ["salon", "barber", "hair", "nail", "spa", "beauty"]),
    ("gym", ["gym", "fitness", "personal train", "yoga", "pilates"]),
    ("moving", ["moving", "mover", "storage", "relocation"]),
    ("landscaping", ["landscap", "lawn", "garden", "tree", "mow", "sod"]),
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
# Banned language
# ---------------------------------------------------------------------------

_BANNED_WORDS = [
    # Generic SaaS / AI-agency openers
    "just reaching out", "wanted to introduce myself", "curious if",
    "would love to chat", "another set of eyes",
    # Product / tech positioning
    "ai", "software", "dashboard", "platform", "automation", "automate",
    "solution", "system integration", "ai-powered", "ai powered",
    # Business-speak
    "optimize", "revolutionize", "leverage", "synergy", "streamline",
    "game-changer", "game changer", "cutting-edge", "cutting edge",
    "robust", "scalable", "seamlessly", "seamless",
    "transform", "unlock", "roi", "maximize efficiency",
    "streamline operations", "unlock growth", "transform your business",
    # Lead-gen / sales-y
    "lead capture", "lead gen",
    "book more", "book appointments", "booked appointments",
    "never miss a lead", "fill your calendar", "autopilot",
    "capture leads", "follow-up system", "follow up system",
    "business growth", "grow your business", "scale your",
    "schedule a call", "book a call", "let's hop on", "hop on a call",
    "free audit", "free consultation",
    # Soft filler
    "happy to", "worth a look", "doesn't have to be complicated",
    "from the business side", "workflow gap",
]

_SUBJECT_BANNED_PHRASES = [
    "ai", "automation", "automate", "solution", "opportunity", "support",
    "checking in", "increase revenue", "grow your business", "urgent",
    "last chance", "free audit", "free consultation",
    "quick question", "had a question", "wanted to ask", "just checking",
    "touching base", "following up",
]

_VAGUE_POSITIONING_PHRASES = [
    "workflow gap", "from the business side", "not the agency side",
    "another set of eyes", "operational stuff", "compare notes sometime",
    "worth comparing notes", "site is pretty explicit about",
    "the mess shows up", "if that is a live issue there",
    "where i'd start", "what i'd look at first", "first place i'd look",
    "just wanted to", "just reaching out", "wanted to introduce",
    "curious if you", "would love to", "i'd love to",
    # Fake warmth — voice rules
    "hope this finds you", "hope you're doing well", "hope you're well",
    "hope all is well", "i hope this email finds you",
]

_FORMAL_OPENER_SUBS = [
    ("I noticed that ", ""), ("I wanted to reach out ", ""),
    ("I wanted to reach out", ""), ("my name is", "My name is"),
    ("We are a leading", ""), ("we are a leading", ""),
    ("we help businesses like yours", ""), ("We help businesses like yours", ""),
    ("I help businesses ", ""), ("We offer ", ""), ("We offer", ""),
    ("AI-powered", "simple"), ("ai-powered", "simple"),
    ("streamline", "speed up"), ("optimize", "improve"),
    ("solution", "fix"), ("platform", "system"),
]


# ---------------------------------------------------------------------------
# Genericity detection
# ---------------------------------------------------------------------------

_GENERIC_OBSERVATION_PHRASES = [
    "noticed you do ", "saw you're in ", "looks like you help homeowners",
    "noticed you offer ", "saw you do ", "you do landscaping", "you do roofing",
    "you do concrete", "you do plumbing", "you do hvac", "you do electrical",
]

# Concrete signals - expanded to cover natural consequence/offer language
_CONCRETE_SERVICE_SIGNALS = [
    "missed-call text back", "text-back", "missed calls",
    "after-hours response", "after-hours reply", "after-hours calls",
    "lead tracking", "contact form routing", "inquiry routing",
    "estimate follow-up", "quote follow-up", "callback recovery",
    "intake capture", "pipeline", "calls", "callbacks", "estimate requests",
    "quotes", "follow-up", "slow follow-up", "inquiries", "new leads",
    "new requests", "service requests", "getting back to people",
    "response side", "sit", "stack up", "pile up", "slip", "fall through",
    "go cold", "gone cold", "gone somewhere else", "moved on",
    "unanswered", "not get returned", "never sees", "no idea",
    "outside of that", "leaking", "falling through", "go unanswered",
]


# ---------------------------------------------------------------------------
# Observation validation
# ---------------------------------------------------------------------------

class ObservationMissingError(ValueError):
    """Raised when first-touch generation is attempted without an observation."""


class DraftInvalidError(ValueError):
    """Raised when a generated draft fails validation rules."""


def _require_observation(observation: Optional[str]) -> str:
    obs = (observation or "").strip()
    if not obs:
        raise ObservationMissingError(
            "First-touch draft blocked: observation is required."
        )
    if len(obs) < 15:
        raise ObservationMissingError(
            "Observation too short. Write a specific detail about this business."
        )
    return obs


def _is_generic_observation(obs: str) -> bool:
    return any(phrase in obs.lower() for phrase in _GENERIC_OBSERVATION_PHRASES)


def validate_draft(body: str, observation: str) -> None:
    """Deterministic validation. Raises DraftInvalidError with specific reason."""
    body_lower = body.lower()

    # Em dash ban — voice rules
    if "\u2014" in body:
        raise DraftInvalidError(
            "Draft contains an em dash. Use plain punctuation instead."
        )

    hits = [w for w in _BANNED_WORDS if w in body_lower]
    if hits:
        raise DraftInvalidError(f"Banned word(s) in draft: {hits}")

    filler_openers = [
        "i wanted to reach out", "we are a leading",
        "we help businesses like yours", "i help businesses like",
    ]
    for filler in filler_openers:
        if body_lower.startswith(filler):
            raise DraftInvalidError(f"Draft opens with filler: '{filler}'")

    vague_hits = [p for p in _VAGUE_POSITIONING_PHRASES if p in body_lower]
    if vague_hits:
        raise DraftInvalidError(f"Vague positioning in draft: {vague_hits}")

    hard_cta = [
        "schedule a call", "book a call", "book a meeting",
        "let's hop on", "hop on a call", "set up a call",
        "click here", "visit our website", "check out our",
    ]
    for cta in hard_cta:
        if cta in body_lower:
            raise DraftInvalidError(f"Hard CTA found: '{cta}'")

    if re.search(r"https?://", body):
        raise DraftInvalidError("Draft must not contain links.")

    if re.search(r"\$\d+|\bper month\b|\b/mo\b|\bmonthly\b", body_lower):
        raise DraftInvalidError("Draft must not mention pricing.")

    stop_words = {
        "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for", "of",
        "with", "is", "are", "was", "were", "you", "your", "i", "it", "its",
        "that", "this", "they", "them", "their", "have", "has", "be", "been",
        "not", "do", "does", "did", "from", "by", "as", "so", "if", "we", "my",
        "saw", "just", "there", "those", "when", "out", "up", "no", "its",
    }
    obs_tokens = {
        w.lower().strip(".,;:!?\"'()")
        for w in observation.split()
        if w.lower().strip(".,;:!?\"'()") not in stop_words and len(w) > 3
    }
    body_text = re.sub(r"\n\n-\s*\w+\s*$", "", body, flags=re.IGNORECASE)
    body_tokens = {w.lower().strip(".,;:!?\"'()") for w in body_text.split()}
    if not (obs_tokens & body_tokens):
        raise DraftInvalidError("Draft does not reflect the observation.")

    if not any(s in body_lower for s in _CONCRETE_SERVICE_SIGNALS):
        raise DraftInvalidError(
            "Draft does not mention a concrete business problem or gap."
        )

    # Fixer/operator line check — value prop must be visible
    _FIXER_LINE_SIGNALS = [
        "i help service businesses", "i help owners", "i help small businesses",
        "help fix", "help tighten", "help stop losing", "help owners fix",
        "help owners clean", "fix the operational", "fix the follow",
        "fix the gaps", "plug the leaks", "stop losing work",
        "stop losing jobs", "get more out of",
    ]
    if not any(s in body_lower for s in _FIXER_LINE_SIGNALS):
        raise DraftInvalidError(
            "Draft missing fixer/operator line — value prop must be visible by sentence 3."
        )

    # Reply-first CTA check
    _CTA_SIGNALS = [
        "worth a quick call", "worth a conversation", "would it be worth",
        "worth getting on", "want to get on", "worth a short conversation",
        "worth a quick conversation",
    ]
    if not any(s in body_lower for s in _CTA_SIGNALS):
        raise DraftInvalidError(
            "Draft missing reply-first CTA — must close with a soft question."
        )

    # Complaint-risk linting
    exclamation_count = body.count("!")
    if exclamation_count > 1:
        raise DraftInvalidError(
            f"Draft uses too many exclamation marks ({exclamation_count}). Keep tone flat."
        )
    link_count = len(re.findall(r"https?://", body))
    if link_count > 1:
        raise DraftInvalidError("Draft must not contain multiple links.")
    cta_phrases = ["worth a quick call", "would it be worth", "worth getting on",
                   "want to get on", "worth a conversation", "worth a short"]
    cta_hits = sum(1 for p in cta_phrases if p in body_lower)
    if cta_hits > 2:
        raise DraftInvalidError("Draft has multiple CTAs — keep to one reply-first close.")


def validate_subject(subject: str) -> None:
    subj = (subject or "").strip().lower()
    if not subj:
        raise DraftInvalidError("Subject must not be empty.")
    if len(subj) > 48:
        raise DraftInvalidError("Subject is too long.")
    if len(subj.split()) > 6:
        raise DraftInvalidError("Subject uses too many words.")
    if "!" in subj:
        raise DraftInvalidError("Subject must not use hype punctuation.")
    hits = [p for p in _SUBJECT_BANNED_PHRASES if p in subj]
    if hits:
        raise DraftInvalidError(f"Banned phrase(s) in subject: {hits}")


# ---------------------------------------------------------------------------
# Post-processing (light — voice does not need heavy cleanup)
# ---------------------------------------------------------------------------

_SIGN_OFF = "\n\nDrew"


def enforce_human_style(body_text: str) -> str:
    """Light cleanup only. Drew's voice is already direct — don't over-process."""
    if not body_text:
        return body_text
    # Voice rules: em dashes are not permitted. Replace with comma+space or period.
    # Pattern: "word — and/but/so" -> "word, and/but/so"
    body_text = re.sub(r"\s*\u2014\s*(and|but|so|or|nor)\b", r", \1", body_text)
    # Pattern: "word — Word" (capital after dash = new sentence)
    body_text = re.sub(r"\s*\u2014\s*([A-Z])", r". \1", body_text)
    # Remaining em dashes -> comma space
    body_text = body_text.replace("\u2014", ", ")
    # Kill any formal opener subs that sneak through
    for pattern, replacement in _FORMAL_OPENER_SUBS:
        if pattern in body_text:
            body_text = body_text.replace(pattern, replacement)
    # Clean up double spaces
    body_text = re.sub(r" {2,}", " ", body_text)
    body_text = re.sub(r"\s+([,.?!])", r"\1", body_text)
    return body_text.strip()


# ---------------------------------------------------------------------------
# Angle detection
# ---------------------------------------------------------------------------

_ANGLE_KEYWORDS: List[Tuple[str, List[str]]] = [
    ("after_hours_response", [
        "emergency", "after hours", "after-hours", "24/7", "24 7",
        "same day", "same-day", "urgent", "nights", "weekend",
    ]),
    ("estimate_follow_up", [
        "estimate", "estimates", "quote", "quotes", "financing",
        "proposal", "proposals",
    ]),
    ("service_requests", [
        "booking", "book online", "schedule", "scheduling",
        "appointment", "appointments",
    ]),
    ("inquiry_routing", [
        "contact form", "form", "chat", "message", "messages",
        "text", "texting",
    ]),
    ("callback_recovery", [
        "phone", "phones", "call", "calls", "callback", "callbacks",
        "voicemail", "dispatch",
    ]),
]


def _component_variant_index(
    prospect: Dict[str, str],
    observation: str,
    angle: str,
    component: str,
    n: int,
    *,
    channel: str = "email",
) -> int:
    if n <= 0:
        return 0
    business_name = (prospect.get("business_name") or "").strip().lower()
    city = (prospect.get("city") or "").strip().lower()
    industry = (prospect.get("industry") or "").strip().lower()
    obs_norm = re.sub(r"\s+", " ", (observation or "").strip().lower())
    digest = hashlib.sha256(
        f"{component}|{channel}|{angle}|{business_name}|{city}|{industry}|{obs_norm}".encode()
    ).hexdigest()
    return int(digest[:8], 16) % n


def _pick_offer_angle(prospect: Dict[str, str], observation: str) -> str:
    obs_lower = observation.lower()
    for angle, keywords in _ANGLE_KEYWORDS:
        if any(kw in obs_lower for kw in keywords):
            return angle
    likely = (prospect.get("likely_opportunity") or "").lower()
    if "after" in likely or "missed" in likely or "call" in likely:
        return "callback_recovery"
    if "estimate" in likely or "quote" in likely or "follow" in likely:
        return "estimate_follow_up"
    return "owner_workflow"


# ---------------------------------------------------------------------------
# Voice-matched body construction (v17)
#
# Structure: 4 short paragraphs, line break between each.
# P1: "My name is Drew. Saw [specific observation]."
# P2: Consequence — "A lot of those probably..." natural, hedged.
# P3: Positioning — one on one, full picture, specific to how they run things.
# P4: Real close question. Never "happy to", never "worth a look".
#
# What Drew sells: personalized one-on-one consultation, looks at the whole
# operation, builds custom systems specific to that business. Not a product.
# ---------------------------------------------------------------------------

def _build_observation_opener(obs: str) -> str:
    """
    Convert the stored observation into a clean grammatically correct sentence.
    Always produces: "I noticed [something specific about you/your business]."
    """
    import re as _re
    o = obs.strip().rstrip(".")

    # Run replacements BEFORE stripping opener prefixes, so "your site pushes"
    # gets converted to "you're pushing" while it's still intact
    replacements = [
        ("your site is very focused on ", "your site is very focused on "),
        ("your site is pretty explicit about ", "your site is very focused on "),
        ("your site is explicit about ", "your site is focused on "),
        ("your site focuses heavily on ", "you're focused heavily on "),
        ("your site lists ", "you're listing "),
        ("your site pushes ", "you're pushing "),
        ("your site advertises ", "you're advertising "),
        ("your site keeps ", "you keep "),
        ("your site splits ", "you split "),
        ("your site leans ", "you lean toward "),
        ("your site has ", "you have "),
        ("your homepage has ", "you have "),
        ("your homepage centers ", "you're centering "),
        ("site is pretty explicit about ", "your site is very focused on "),
        ("site is explicit about ", "your site is focused on "),
        ("site pushes ", "you're pushing "),
        ("site lists ", "you're listing "),
        ("site has ", "you have "),
        ("site advertises ", "you're advertising "),
    ]
    o_lower = o.lower()
    for old, new in replacements:
        if o_lower.startswith(old):
            o = new + o[len(old):]
            o_lower = o.lower()
            break

    # Now strip any explicit opener the operator or agent may have typed
    o = _re.sub(
        r"^(saw that\s*|noticed that\s*|i noticed\s*|i saw\s*|saw\s*|noticed\s*"
        r"|looks like\s*|came across\s*[-—]?\s*)",
        "", o, flags=_re.IGNORECASE,
    ).strip()

    # Ensure observations starting with a bare noun phrase get a natural lead-in
    # e.g. "estimate form is..." → "your estimate form is..."
    o_lower = o.lower()
    needs_your = (
        "estimate form", "contact form", "quote form", "request form",
        "booking widget", "chat widget", "scheduling widget", "website ",
        "homepage ", "main page ",
    )
    starts_with_noun_verb = any(o_lower.startswith(n) for n in needs_your)
    if starts_with_noun_verb and not o_lower.startswith("your ") and not o_lower.startswith("you"):
        o = "your " + o[0].lower() + o[1:]
        o_lower = o.lower()

    # Bare noun with no verb — add natural connector
    first_words = o_lower.split()[:4]
    has_early_verb = any(w in first_words for w in (
        "is", "are", "was", "were", "has", "have", "had",
        "does", "do", "did", "shows", "uses", "lists", "pushes",
        "advertises", "offers", "includes", "focuses", "keeps",
    ))
    if not has_early_verb:
        if any(o_lower.startswith(n) for n in ("dispatch number", "voicemail box", "voicemail only")):
            o = "you're relying on " + o[0].lower() + o[1:]
        elif any(o_lower.startswith(n) for n in ("phone number",)):
            o = "you have " + o[0].lower() + o[1:]

    # Ensure first character is lowercase for clean sentence assembly
    if o and o[0].isalpha():
        o = o[0].lower() + o[1:]

    return f"I noticed {o}."


def _build_consequence_sentence(obs: str, angle: str) -> str:
    """
    One direct sentence about what that specific detail probably means for their business.
    Specific, grounded, not vague. Avoids 'a lot of those probably' as a crutch.
    """
    o = obs.lower()

    if any(p in o for p in (
        "no confirmation", "no immediate", "nothing back",
        "no next step", "no acknowledgment", "unclear",
    )) and any(p in o for p in ("form", "submit", "contact", "inquiry")):
        return "When there's no confirmation after a form submission, most people assume it didn't go through and move on."

    if any(p in o for p in ("voicemail", "dispatch number", "dispatch line")):
        return "Most people who hit voicemail on a service call don't leave a message — they call the next number on the list."

    if any(p in o for p in (
        "only contact", "only way", "no other contact",
        "just a phone", "single phone", "phone is the main", "phone number prominently",
    )):
        return "If that number goes unanswered while you're on a job, that lead is usually gone before you can call back."

    if any(p in o for p in ("24/7", "24 7", "emergency service", "same-day response", "same day response")):
        return "That's a real commitment to back up operationally — most businesses that advertise it can't consistently deliver it."

    if any(p in o for p in ("after-hours", "after hours", "weekend", "nights")):
        return "After-hours requests that don't get a same-day response almost never convert — people make a decision and move on quickly."

    if any(p in o for p in (
        "estimate request form", "estimate form", "primary call to action",
        "free estimate", "quote request form", "free quote",
    )):
        return "Quote requests that sit for more than a few hours usually end up going to whoever responds first."

    if any(p in o for p in ("quote button", "quote on every page", "push free quote")):
        return "When there's a quote request and no fast follow-up, most people have already contacted someone else by the time you get back to them."

    if any(p in o for p in (
        "proposal request", "proposal form", "free in-home",
    )):
        return "Proposal requests that don't get a quick acknowledgment tend to go cold — people interpret silence as disinterest."

    if any(p in o for p in ("chat widget", "text-back", "text back", "few different places", "couple different")):
        return "When inquiries are coming in through multiple channels, it's easy for things to fall through between the cracks."

    if any(p in o for p in ("online booking", "booking widget", "scheduling widget")):
        return "Online bookings that don't get a quick confirmation call tend to generate no-shows — people aren't sure if it actually went through."

    if any(p in o for p in ("water heater", "financing", "explicit about")):
        return "Businesses that are very focused on one service sometimes have a harder time converting customers who want the full picture upfront."

    # Angle fallbacks — direct, not passive
    fallbacks = {
        "after_hours_response":
            "After-hours requests that don't get a fast response almost never convert.",
        "estimate_follow_up":
            "Slow estimate follow-up is usually the difference between winning and losing the job.",
        "service_requests":
            "New service requests that sit unacknowledged for more than a few hours rarely turn into customers.",
        "inquiry_routing":
            "Inquiries that fall through without a quick response are usually already talking to someone else.",
        "callback_recovery":
            "Missed calls that don't get a callback within the hour rarely convert.",
        "owner_workflow":
            "When the owner is also running operations, things that need attention tend to stack up faster than they get resolved.",
    }
    return fallbacks.get(angle, fallbacks["owner_workflow"])


def _build_offer_sentence(obs: str, angle: str, variant: int) -> str:
    """
    Drew's positioning: clearly states what he helps fix, then grounds it in
    one-on-one, specific-to-their-operation work.
    Fixer/operator line must be visible — no burying the value prop at the end.
    """
    o = obs.lower()

    # Angle-specific fixer lines
    if angle == "callback_recovery":
        variants = [
            "I help service businesses stop losing work to missed calls and slow callbacks. I work one on one with owners to fix the specific gaps in how they handle incoming work.",
            "I help owners tighten up the callback side so calls that come in actually turn into jobs. One on one, built around how they actually run things.",
            "I help service businesses get more out of the calls they're already getting by fixing the follow-up leaks that cost them work.",
        ]
    elif angle == "estimate_follow_up":
        variants = [
            "I help service businesses tighten estimate follow-up so quotes don't go cold. I work one on one with owners, built around how they actually run their operation.",
            "I help owners stop losing jobs to slow follow-up on estimates. I work one on one to fix the operational gaps that let good work slip away.",
            "I help service businesses close more of the estimates they're already sending by fixing the follow-up timing that loses jobs.",
        ]
    elif angle == "after_hours_response":
        variants = [
            "I help service businesses handle after-hours and overflow inquiries so leads don't go cold before the next business day. One on one, specific to how they operate.",
            "I help owners fix the after-hours gap so calls and requests that come in outside of business hours don't just disappear.",
            "I help service businesses stop losing after-hours work by fixing how inquiries get handled when the owner isn't available.",
        ]
    elif angle == "inquiry_routing":
        variants = [
            "I help service businesses fix the intake side so inquiries that come in actually get routed and followed up. I work one on one with owners to plug the leaks.",
            "I help owners tighten up how new inquiries are handled so leads don't fall through between the form submission and the callback.",
            "I help service businesses stop losing leads in the gap between when someone reaches out and when someone actually gets back to them.",
        ]
    else:
        variants = [
            "I help service businesses fix the operational gaps that lose jobs. I work one on one with owners to build something specific to how they actually run things.",
            "I help owners clean up the follow-up and intake leaks that cost them work. One on one, built around their operation.",
            "I help service businesses get more out of the leads they already have by fixing the gaps in follow-up, callbacks, and estimate handling.",
        ]

    return variants[variant % len(variants)]


def _build_close_sentence(obs: str, angle: str, variant: int, channel: str) -> str:
    """
    Direct soft question. Not permission-seeking. Not vague.
    Drew closes with a real question that assumes the conversation is worth having.
    """
    o = obs.lower()

    if any(p in o for p in ("24/7", "emergency", "same-day", "same day")):
        closes = [
            "Would it be worth a quick call to talk through it?",
            "Worth getting on a call to look at it together?",
            "Want to get on a quick call and walk through how that's working?",
        ]
    elif channel == "dm":
        closes = [
            "Worth a quick conversation?",
            "Want to jump on a quick call about it?",
            "Would it be worth a short conversation?",
        ]
    else:
        closes = [
            "Worth a quick call to look at it together?",
            "Would it be worth getting on a call to walk through it?",
            "Want to get on a quick call and see if there's something worth addressing?",
        ]

    return closes[variant % len(closes)]


def _subject_options_for_angle(angle: str, observation: str) -> List[str]:
    obs_lower = observation.lower()
    if angle == "after_hours_response":
        if "emergency" in obs_lower or "urgent" in obs_lower:
            return ["emergency calls", "after-hours calls", "after-hours follow-up"]
        if "weekend" in obs_lower or "nights" in obs_lower:
            return ["after-hours calls", "after-hours follow-up", "weekend calls"]
        return ["after-hours calls", "after-hours follow-up", "after-hours response"]
    if angle == "estimate_follow_up":
        if "quote" in obs_lower:
            return ["quote requests", "estimate follow-up", "quote follow-up"]
        return ["estimate follow-up", "estimate requests", "quote follow-up"]
    if angle == "service_requests":
        if "appointment" in obs_lower or "booking" in obs_lower:
            return ["appointment requests", "new bookings", "service requests"]
        if "scheduling" in obs_lower or "schedule" in obs_lower:
            return ["scheduling follow-up", "service requests", "new requests"]
        return ["service requests", "new requests", "service request follow-up"]
    if angle == "inquiry_routing":
        if "contact form" in obs_lower:
            return ["contact form follow-up", "form inquiries", "contact form inquiries"]
        if "text" in obs_lower or "chat" in obs_lower or "message" in obs_lower:
            return ["new messages", "incoming inquiries", "inquiry follow-up"]
        return ["new inquiries", "inquiry follow-up", "incoming inquiries"]
    if angle == "callback_recovery":
        if "voicemail" in obs_lower or "dispatch" in obs_lower:
            return ["missed calls", "voicemail follow-up", "callback follow-up"]
        return ["missed calls", "callback follow-up", "call follow-up"]
    if any(kw in obs_lower for kw in ("missed call", "callback", "voicemail", "phone")):
        return ["missed calls", "callback follow-up", "call follow-up"]
    if any(kw in obs_lower for kw in ("estimate", "quote", "proposal")):
        return ["estimate follow-up", "estimate requests", "quote follow-up"]
    if any(kw in obs_lower for kw in ("contact form", "inquiry", "message", "form")):
        return ["new inquiries", "inquiry follow-up", "contact follow-up"]
    return ["missed calls", "new inquiries", "follow-up timing"]


def _subject_from_observation(prospect: Dict[str, str], observation: str, angle: str) -> str:
    options = _subject_options_for_angle(angle, observation)
    pick = _component_variant_index(prospect, observation, angle, "subject", len(options))
    return options[pick]


def _build_first_touch_body(
    prospect: Dict[str, str],
    observation: str,
    *,
    channel: str,
) -> str:
    """
    Build the email body in Drew's voice: 4 short paragraphs, line-break separated.
    P1: My name is Drew. Saw [observation].
    P2: Consequence — hedged, specific to observation.
    P3: Offer — one on one, full picture, specific to their setup.
    P4: Real close question.
    """
    angle = _pick_offer_angle(prospect, observation)

    # Variant indices — deterministic per lead
    offer_v = _component_variant_index(prospect, observation, angle, "offer", 3, channel=channel)
    close_v = _component_variant_index(prospect, observation, angle, "close", 3, channel=channel)

    obs_sentence = _build_observation_opener(observation)
    consequence  = _build_consequence_sentence(observation, angle)
    offer        = _build_offer_sentence(observation, angle, offer_v)
    close        = _build_close_sentence(observation, angle, close_v, channel)

    if channel == "dm":
        p1 = f"Hey\n\nMy name is Drew. {obs_sentence}"
    else:
        p1 = f"My name is Drew. {obs_sentence}"

    return f"{p1}\n\n{consequence}\n\n{offer}\n\n{close}"


def _build_email_body(prospect: Dict[str, str], observation: str) -> str:
    return _build_first_touch_body(prospect, observation, channel="email")


def _build_dm_body(prospect: Dict[str, str], observation: str) -> str:
    return _build_first_touch_body(prospect, observation, channel="dm")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

_SUBJECT_OPTIONS = ["missed calls", "after-hours calls", "after-hours follow-up"]
_HIGH_FIT_INDUSTRIES = {
    "plumbing", "hvac", "electrical", "locksmith", "garage_door", "towing",
}


def draft_email(
    prospect: Dict[str, str],
    final_priority_score: int,
    observation: Optional[str] = None,
) -> Tuple[str, str]:
    business_name = (prospect.get("business_name") or "").strip()
    city = (prospect.get("city") or "").strip()
    if not business_name:
        raise ValueError("Cannot draft email without business_name.")
    if not city:
        raise ValueError(f"Cannot draft email for {business_name} without city.")

    raw_obs = observation or prospect.get("business_specific_observation") or ""
    obs_clean = raw_obs.strip()

    # No observation — use industry-keyed fallback draft
    if not obs_clean or _is_generic_observation(obs_clean):
        industry = detect_industry(
            prospect.get("business_name", ""),
            prospect.get("industry", ""),
        )
        name_hash = int(hashlib.md5(
            (prospect.get("business_name", "") + industry).encode()
        ).hexdigest(), 16)
        subject = _FALLBACK_SUBJECTS[name_hash % len(_FALLBACK_SUBJECTS)]
        body    = _build_no_obs_draft(prospect, channel="email")
        body    = enforce_human_style(body) + _SIGN_OFF
        validate_subject(subject)
        return subject, body

    obs = _require_observation(obs_clean)
    if _is_generic_observation(obs):
        raise ObservationMissingError(
            "Observation is too generic. Write something specific to this business."
        )

    angle   = _pick_offer_angle(prospect, obs)
    subject = _subject_from_observation(prospect, obs, angle)
    body    = _build_email_body(prospect, obs)
    body    = enforce_human_style(body)
    full_body = body + _SIGN_OFF

    validate_subject(subject)
    validate_draft(full_body, obs)
    return subject, full_body


def draft_email_json(
    prospect: Dict[str, str],
    final_priority_score: int,
    observation: Optional[str] = None,
) -> Dict:
    subject, body = draft_email(prospect, final_priority_score, observation=observation)
    return {"subject": subject, "email_body": body, "tone": "casual"}


def draft_social_messages(
    prospect: Dict[str, str],
    email_body: str,
    observation: Optional[str] = None,
) -> Tuple[str, str, str]:
    raw_obs = observation or prospect.get("business_specific_observation") or ""
    obs_clean = raw_obs.strip()

    # No observation — use industry-keyed fallback
    if not obs_clean or _is_generic_observation(obs_clean):
        dm_body = _build_no_obs_draft(prospect, channel="dm")
        dm_body = enforce_human_style(dm_body)
        return dm_body, dm_body, dm_body

    obs = _require_observation(obs_clean)
    if _is_generic_observation(obs):
        raise ObservationMissingError("Observation is too generic for DM generation.")
    dm_body = _build_dm_body(prospect, obs)
    dm_body = enforce_human_style(dm_body)
    validate_draft(dm_body, obs)
    return dm_body, dm_body, dm_body


# ---------------------------------------------------------------------------
# Pipeline compatibility shims
# ---------------------------------------------------------------------------

def pick_best_pitch_angle(likely_opportunity: str) -> str:
    return (likely_opportunity or "booking automation").strip() or "booking automation"
