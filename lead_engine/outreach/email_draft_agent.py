from __future__ import annotations

import hashlib
import re
from typing import Dict, List, Optional, Tuple

DRAFT_VERSION = "v15"

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
# Banned language - applies to all first-touch drafts
# ---------------------------------------------------------------------------

_BANNED_WORDS = [
    "optimize", "revolutionize", "leverage", "synergy", "streamline",
    "game-changer", "game changer", "cutting-edge", "cutting edge",
    "robust", "scalable", "seamlessly", "seamless",
    "ai-powered", "ai powered", "system integration", "platform",
    "solution", "lead capture", "lead gen", "automation", "automate",
    "book more", "book appointments", "booked appointments",
    "never miss a lead", "fill your calendar", "autopilot",
    "capture leads", "follow-up system", "follow up system",
    "business growth", "grow your business", "scale your",
    "schedule a call", "book a call", "let's hop on", "hop on a call",
    "free audit", "free consultation", "streamline operations",
    "maximize efficiency", "unlock growth", "transform your business",
]

_SUBJECT_BANNED_PHRASES = [
    "ai", "automation", "automate", "solution", "opportunity", "support",
    "checking in", "increase revenue", "grow your business", "urgent",
    "last chance", "free audit", "free consultation",
]

_VAGUE_POSITIONING_PHRASES = [
    "workflow gap",
    "from the business side",
    "not the agency side",
    "another set of eyes",
    "operational stuff",
    "compare notes sometime",
    "worth comparing notes",
    "site is pretty explicit about",
    "the mess shows up",
    "if that is a live issue there",
    "where i'd start",
    "what i'd look at first",
    "first place i'd look",
]

_FORMAL_OPENER_SUBS = [
    ("I noticed that ", ""),
    ("I wanted to reach out ", ""),
    ("I wanted to reach out", ""),
    ("my name is", ""),
    ("We are a leading", ""),
    ("we are a leading", ""),
    ("we help businesses like yours", ""),
    ("We help businesses like yours", ""),
    ("I help businesses ", ""),
    ("We offer ", ""),
    ("We offer", ""),
    ("AI-powered", "simple"),
    ("ai-powered", "simple"),
    ("streamline", "speed up"),
    ("optimize", "improve"),
    ("solution", "fix"),
    ("platform", "system"),
]


# ---------------------------------------------------------------------------
# Genericity detection - swappability test
# ---------------------------------------------------------------------------

_GENERIC_OBSERVATION_PHRASES = [
    "noticed you do ",
    "saw you're in ",
    "looks like you help homeowners",
    "noticed you offer ",
    "saw you do ",
    "you do landscaping",
    "you do roofing",
    "you do concrete",
    "you do plumbing",
    "you do hvac",
    "you do electrical",
]

_CONCRETE_SERVICE_SIGNALS = [
    "missed-call text back",
    "text-back",
    "missed calls",
    "after-hours response",
    "after-hours reply",
    "after-hours calls",
    "lead tracking",
    "contact form routing",
    "inquiry routing",
    "estimate follow-up",
    "quote follow-up",
    "callback recovery",
    "intake capture",
    "pipeline",
    "calls",
    "callbacks",
    "estimate requests",
    "quotes",
    "follow-up",
    "slow follow-up",
    "inquiries",
    "new leads",
    "new requests",
    "service requests",
    "getting back to people",
    "response side",
    "sit",
    "stack up",
    "pile up",
    "slip",
    "fall through",
]


# ---------------------------------------------------------------------------
# Observation validation
# ---------------------------------------------------------------------------

class ObservationMissingError(ValueError):
    """Raised when first-touch generation is attempted without an observation."""


class DraftInvalidError(ValueError):
    """Raised when a generated draft fails validation rules."""


def _require_observation(observation: Optional[str]) -> str:
    """Normalize and require a non-empty observation. Raises if absent."""
    obs = (observation or "").strip()
    if not obs:
        raise ObservationMissingError(
            "First-touch draft blocked: business_specific_observation is required. "
            "Add a concrete, business-specific detail before generating."
        )
    if len(obs) < 15:
        raise ObservationMissingError(
            "Observation too short to be meaningful. "
            "Write a specific detail about this business - not a category label."
        )
    return obs


def _is_generic_observation(obs: str) -> bool:
    obs_lower = obs.lower()
    return any(phrase in obs_lower for phrase in _GENERIC_OBSERVATION_PHRASES)


def validate_draft(body: str, observation: str) -> None:
    """
    Deterministic validation for first-touch drafts.
    Raises DraftInvalidError with a specific reason on any failure.
    """
    body_lower = body.lower()

    hits = [w for w in _BANNED_WORDS if w in body_lower]
    if hits:
        raise DraftInvalidError(f"Banned word(s) in draft: {hits}")

    filler_openers = [
        "i wanted to reach out",
        "my name is",
        "we are a leading",
        "we help businesses like yours",
        "i help businesses like",
    ]
    for filler in filler_openers:
        if body_lower.startswith(filler):
            raise DraftInvalidError(f"Draft opens with sender-centered filler: '{filler}'")

    vague_hits = [phrase for phrase in _VAGUE_POSITIONING_PHRASES if phrase in body_lower]
    if vague_hits:
        raise DraftInvalidError(f"Vague positioning found in draft: {vague_hits}")

    hard_cta = [
        "schedule a call", "book a call", "book a meeting",
        "let's hop on", "hop on a call", "set up a call",
        "click here", "visit our website", "check out our",
    ]
    for cta in hard_cta:
        if cta in body_lower:
            raise DraftInvalidError(f"Hard CTA found in first-touch draft: '{cta}'")

    if re.search(r"https?://", body):
        raise DraftInvalidError("First-touch draft must not contain links.")

    if re.search(r"\$\d+|\bper month\b|\b/mo\b|\bmonthly\b", body_lower):
        raise DraftInvalidError("First-touch draft must not mention pricing.")

    stop_words = {
        "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for", "of",
        "with", "is", "are", "was", "were", "you", "your", "i", "it", "its",
        "that", "this", "they", "them", "their", "have", "has", "be", "been",
        "not", "do", "does", "did", "from", "by", "as", "so", "if", "we", "my",
    }
    obs_tokens = {
        w.lower().strip(".,;:!?\"'()")
        for w in observation.split()
        if w.lower().strip(".,;:!?\"'()") not in stop_words and len(w) > 3
    }
    body_text = re.sub(r"\n\n-\s*\w+\s*$", "", body, flags=re.IGNORECASE)
    body_tokens = {w.lower().strip(".,;:!?\"'()") for w in body_text.split()}
    overlap = obs_tokens & body_tokens
    if not overlap:
        raise DraftInvalidError(
            "Draft does not materially reflect the observation. "
            "The observation must meaningfully appear in the message."
        )

    if not any(signal in body_lower for signal in _CONCRETE_SERVICE_SIGNALS):
        raise DraftInvalidError(
            "Draft does not mention a concrete service-business bottleneck or fix."
        )


def validate_subject(subject: str) -> None:
    subj = (subject or "").strip().lower()
    if not subj:
        raise DraftInvalidError("First-touch subject must not be empty.")
    if len(subj) > 48:
        raise DraftInvalidError("First-touch subject is too long.")
    if len(subj.split()) > 6:
        raise DraftInvalidError("First-touch subject uses too many words.")
    if "!" in subj:
        raise DraftInvalidError("First-touch subject must not use hype punctuation.")
    hits = [phrase for phrase in _SUBJECT_BANNED_PHRASES if phrase in subj]
    if hits:
        raise DraftInvalidError(f"Banned phrase(s) in subject: {hits}")


# ---------------------------------------------------------------------------
# Post-processing: human style enforcement
# ---------------------------------------------------------------------------

_WORD_TARGET_MAX = 86
_SIGN_OFF = "\n\n- Drew"


def enforce_human_style(body_text: str) -> str:
    if not body_text:
        return body_text

    for pattern, replacement in _FORMAL_OPENER_SUBS:
        if pattern in body_text:
            body_text = body_text.replace(pattern, replacement)

    body_text = body_text.replace("\n\n", " ").replace("\n", " ")
    body_text = re.sub(r"\s+", " ", body_text).strip()
    body_text = re.sub(r"\s+([,.?!])", r"\1", body_text)
    body_text = re.sub(r"([?!.,]){2,}", r"\1", body_text)

    words = body_text.split()
    if len(words) > _WORD_TARGET_MAX:
        trimmed = " ".join(words[:_WORD_TARGET_MAX]).rstrip(",;:-")
        last_punct = max(trimmed.rfind("."), trimmed.rfind("?"), trimmed.rfind("!"))
        body_text = trimmed[: last_punct + 1] if last_punct > 0 else trimmed

    body_text = body_text.rstrip(" ,;-")
    if body_text and body_text[-1] not in ".?!":
        body_text += "."
    return body_text


# ---------------------------------------------------------------------------
# Deterministic first-touch offer framing
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


def _variant_index(business_name: str, n: int = 3) -> int:
    digest = hashlib.sha256(business_name.strip().lower().encode()).hexdigest()
    return int(digest[:8], 16) % n


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


def _normalize_observation_sentence(observation: str) -> str:
    obs = observation.strip().rstrip(".")
    obs = re.sub(
        r"^(saw|noticed|looks like|came across|saw that|noticed that)\s+",
        "",
        obs,
        flags=re.IGNORECASE,
    ).strip()
    obs_lower = obs.lower()
    replacements = [
        ("site is pretty explicit about ", "you put a lot of emphasis on "),
        ("site is explicit about ", "you put a lot of emphasis on "),
        ("site is clear about ", "you put a lot of emphasis on "),
        ("they are pushing ", "you put a lot of emphasis on "),
        ("they're pushing ", "you put a lot of emphasis on "),
        ("your site leans hard on ", "you put a lot of emphasis on "),
        ("your site pushes ", "you put a lot of emphasis on "),
        ("your site keeps ", "you keep "),
        ("your site splits ", "you split "),
        ("they are ", "you're "),
        ("they're ", "you're "),
        ("their ", "your "),
        ("contact form ", "your contact form "),
        ("phone number ", "your phone number "),
        ("site ", "your site "),
    ]
    for old, new in replacements:
        if obs_lower.startswith(old):
            obs = new + obs[len(old):]
            break
    obs = obs.replace(" pretty hard on the homepage", " on the homepage")
    if obs and obs[0].isalpha():
        obs = obs[0].lower() + obs[1:]
    return obs


def _pick_offer_angle(prospect: Dict[str, str], observation: str) -> str:
    obs_lower = observation.lower()
    for angle, keywords in _ANGLE_KEYWORDS:
        if any(keyword in obs_lower for keyword in keywords):
            return angle

    likely = (prospect.get("likely_opportunity") or "").lower()
    if "after" in likely or "missed" in likely or "call" in likely:
        return "callback_recovery"
    if "estimate" in likely or "quote" in likely or "follow" in likely:
        return "estimate_follow_up"
    return "owner_workflow"


def _build_reactive_consequence(obs: str, angle: str) -> str:
    """
    Build a consequence sentence that logically extends the specific observation
    rather than pulling from a generic angle-keyed pool.

    Reads observation signals in priority order. Falls back to a short
    angle-keyed sentence only when no specific signal is detected.
    No randomness. One output per observation.
    """
    o = obs.lower()

    # --- No confirmation / no response after submission ---
    if any(p in o for p in (
        "no confirmation", "no immediate confirmation", "no response",
        "nothing back", "no follow", "unclear", "no next step",
        "no idea if it went", "no acknowledgment",
    )):
        if any(p in o for p in ("contact form", "form", "submit", "inquiry")):
            return "someone fills that out and gets nothing back — no confirmation, no idea if it went anywhere"
        return "when there's no confirmation after someone reaches out, a lot of those just slip through"

    # --- Voicemail / dispatch number ---
    if any(p in o for p in ("voicemail", "dispatch number", "dispatch line")):
        return "requests that go to voicemail often don't get followed up until the next morning at the earliest"

    # --- Phone as only or primary contact path ---
    if any(p in o for p in (
        "only contact", "primary contact", "only way to reach",
        "no other contact", "just a phone", "single phone",
        "phone number prominently", "phone is the main",
    )):
        return "if someone calls and you're mid-job, that goes to voicemail and may not get returned same day"

    # --- Estimate / quote form as primary CTA ---
    if any(p in o for p in (
        "estimate request form", "quote request form", "estimate form",
        "request form as the primary", "free estimate as the primary",
        "free quote as the primary", "primary call to action",
    )):
        return "the gap is usually after someone submits — those tend to sit until someone has time to get back to them"

    # --- Pushes quotes / estimates on every page ---
    if any(p in o for p in (
        "push free quote", "pushes free quote", "quote on every page",
        "quote button", "quote requests on every",
    )):
        return "quote requests tend to sit until someone gets around to following up, especially once the schedule fills"

    # --- 24/7 or emergency / same-day claims ---
    if any(p in o for p in ("24/7", "24 7", "emergency service", "same-day response", "same day response")):
        return "that works when someone picks up, but after-hours calls and same-day requests can stack up between jobs"

    # --- After-hours or weekend availability ---
    if any(p in o for p in (
        "after-hours", "after hours", "weekend availability",
        "weekend and evening", "nights and weekend", "nights and week",
    )):
        return "nights and weekends are when people actually need help, and that's also when follow-up tends to slip"

    # --- Multiple contact channels / chat widget / text-back ---
    if any(p in o for p in (
        "chat widget", "text-back", "text back",
        "couple different places", "few different places",
        "multiple contact", "more than one way",
    )):
        return "the tricky part is staying on top of messages coming from a couple different places at the same time"

    # --- Online booking / scheduling widget ---
    if any(p in o for p in (
        "online booking", "booking widget", "scheduling widget",
        "book online", "book appointments online",
    )):
        return "the booking side is covered, but requests that come in outside the widget tend to sit"

    # --- Estimate / proposal request (general, no form specifics) ---
    if any(p in o for p in ("proposal request", "proposal form", "free in-home")):
        return "the gap is usually after someone requests — those tend to sit until someone circles back"

    # --- Angle-keyed fallbacks (short, plain, no template feel) ---
    fallbacks = {
        "after_hours_response":
            "after-hours calls and follow-up tend to slip once the day gets busy",
        "estimate_follow_up":
            "estimate requests tend to sit longer than they should once the schedule fills up",
        "service_requests":
            "new requests pile up faster than it looks, especially once the schedule is full",
        "inquiry_routing":
            "inquiries coming in from different places tend to get missed or handled late",
        "callback_recovery":
            "a lot of those calls don't get returned until the next opening in the schedule",
        "owner_workflow":
            "calls and requests tend to sit longer than they should once the job load picks up",
    }
    return fallbacks.get(angle, fallbacks["owner_workflow"])


def _subject_options_for_angle(angle: str, observation: str) -> List[str]:
    """
    Return a tight pool of subject options matched to the angle and observation.
    Deterministic pick happens in _subject_from_observation.
    """
    obs_lower = observation.lower()
    if angle == "after_hours_response":
        if "emergency" in obs_lower or "urgent" in obs_lower:
            return ["emergency calls", "after-hours calls", "after-hours follow-up"]
        if "weekend" in obs_lower or "nights" in obs_lower:
            return ["after-hours calls", "after-hours follow-up", "weekend calls"]
        return ["after-hours calls", "after-hours follow-up", "after-hours response"]
    if angle == "estimate_follow_up":
        if "quote" in obs_lower or "quotes" in obs_lower:
            return ["quote requests", "estimate follow-up", "quote follow-up"]
        return ["estimate follow-up", "estimate requests", "quote follow-up"]
    if angle == "service_requests":
        if "appointment" in obs_lower or "booking" in obs_lower:
            return ["appointment requests", "new bookings", "service requests"]
        if "scheduling" in obs_lower or "schedule" in obs_lower:
            return ["scheduling follow-up", "service requests", "new requests"]
        return ["service requests", "new requests", "service request follow-up"]
    if angle == "inquiry_routing":
        if "contact form" in obs_lower or "contact-form" in obs_lower:
            return ["contact form follow-up", "form inquiries", "contact form inquiries"]
        if "text" in obs_lower or "chat" in obs_lower or "message" in obs_lower:
            return ["new messages", "incoming inquiries", "inquiry follow-up"]
        return ["new inquiries", "inquiry follow-up", "incoming inquiries"]
    if angle == "callback_recovery":
        if "voicemail" in obs_lower or "dispatch" in obs_lower:
            return ["missed calls", "voicemail follow-up", "callback follow-up"]
        return ["missed calls", "callback follow-up", "call follow-up"]
    if any(kw in obs_lower for kw in ("missed call", "missed-call", "callback", "voicemail", "phone")):
        return ["missed calls", "callback follow-up", "call follow-up"]
    if any(kw in obs_lower for kw in ("estimate", "quote", "proposal")):
        return ["estimate follow-up", "estimate requests", "quote follow-up"]
    if any(kw in obs_lower for kw in ("contact form", "inquiry", "inquiries", "message", "form")):
        return ["new inquiries", "inquiry follow-up", "contact follow-up"]
    return ["missed calls", "new inquiries", "follow-up timing"]


def _subject_from_observation(prospect: Dict[str, str], observation: str, angle: str) -> str:
    options = _subject_options_for_angle(angle, observation)
    pick = _component_variant_index(prospect, observation, angle, "subject", len(options))
    return options[pick]


def _offer_options(angle: str) -> List[str]:
    """
    Short, plain offer sentences. Varied openers so the same skeleton
    does not repeat across a batch. All stay first-person, direct, no hype.
    """
    if angle == "after_hours_response":
        return [
            "i help owners tighten the response side so after-hours calls don't just sit",
            "worth a look at how the after-hours handoff is set up — usually a small fix makes a big difference",
            "i work directly with owners on the callback and after-hours side, one-on-one",
        ]
    if angle == "estimate_follow_up":
        return [
            "i help owners close that gap between an incoming request and an actual follow-up",
            "worth looking at how the estimate follow-up side is set up — usually pretty fixable",
            "i work directly with owners on the follow-up side, specifically around requests that go cold",
        ]
    if angle == "inquiry_routing":
        return [
            "i help owners make the follow-up side more consistent when inquiries come in from a few places",
            "worth a look at how that intake path is set up — usually not a big lift to tighten",
            "i work directly with owners on the gap between an inquiry coming in and someone actually getting back to it",
        ]
    if angle == "service_requests":
        return [
            "i help owners make the response side easier to stay on top of when new requests come in",
            "worth looking at how new requests are being handled — usually there's a simple fix in there",
            "i work directly with owners on the handoff between the first inquiry and the first real follow-up",
        ]
    if angle == "callback_recovery":
        return [
            "i help owners tighten the missed-call and callback side so good leads don't just sit",
            "worth a look at how callbacks are being handled — usually pretty straightforward to fix",
            "i work directly with owners on the part after the phone rings, especially when callbacks start getting pushed",
        ]
    return [
        "i help owners clean up the response side so new leads don't depend on someone remembering to follow up",
        "worth a look at how the follow-up side is set up — usually a small fix covers most of the gap",
        "i work directly with owners on missed calls, slow follow-up, and requests that sit too long",
    ]


def _close_options(channel: str) -> List[str]:
    if channel == "dm":
        return [
            "happy to share a couple ideas if useful",
            "if useful, i can send a few thoughts based on what i saw",
            "if you'd like, i can send over a couple ideas that might fit your setup",
        ]
    return [
        "happy to share a few ideas specific to your setup if useful",
        "if useful, i'm happy to send a couple thoughts based on what i saw",
        "if you'd like, i can send over a few ideas that might fit the way you already run things",
    ]


def _soft_close(channel: str, variant: int) -> str:
    closers = _close_options(channel)
    return closers[variant % len(closers)]


def _build_first_touch_body(
    prospect: Dict[str, str],
    observation: str,
    *,
    channel: str,
) -> str:
    obs_norm = _normalize_observation_sentence(observation)
    angle = _pick_offer_angle(prospect, observation)

    if obs_norm.startswith("your site "):
        email_openers = [
            f"i noticed {obs_norm}.",
            f"saw that {obs_norm}.",
            f"noticed that {obs_norm}.",
        ]
        dm_openers = [
            f"hey - i noticed {obs_norm}.",
            f"hey - saw that {obs_norm}.",
            f"hey - noticed that {obs_norm}.",
        ]
    else:
        email_openers = [
            f"i was checking out your site and noticed {obs_norm}.",
            f"saw on your site that {obs_norm}.",
            f"noticed on your site that {obs_norm}.",
        ]
        dm_openers = [
            f"hey - i was checking out your site and noticed {obs_norm}.",
            f"hey - saw on your site that {obs_norm}.",
            f"hey - noticed on your site that {obs_norm}.",
        ]

    opener_pool = email_openers if channel == "email" else dm_openers
    opener_pick = _component_variant_index(
        prospect, observation, angle, "opener", len(opener_pool), channel=channel,
    )
    opener_text = opener_pool[opener_pick]

    # Consequence: observation-reactive, not angle-pooled
    consequence = _build_reactive_consequence(observation, angle)

    offer_options = _offer_options(angle)
    close_options = _close_options(channel)

    offer_pick = _component_variant_index(
        prospect, observation, angle, "offer", len(offer_options), channel=channel,
    )
    close_pick = _component_variant_index(
        prospect, observation, angle, "close", len(close_options), channel=channel,
    )

    offer = offer_options[offer_pick]
    close = close_options[close_pick]

    body = f"{opener_text} {consequence}. {offer}. {close}."
    if len(body.split()) <= _WORD_TARGET_MAX:
        return body

    # Body-fit fallback: shorten close, then offer
    shortest_close = min(close_options, key=lambda x: (len(x.split()), len(x)))
    body = f"{opener_text} {consequence}. {offer}. {shortest_close}."
    if len(body.split()) <= _WORD_TARGET_MAX:
        return body

    shortest_offer = min(offer_options, key=lambda x: (len(x.split()), len(x)))
    return f"{opener_text} {consequence}. {shortest_offer}. {shortest_close}."


def _build_email_body(prospect: Dict[str, str], observation: str) -> str:
    return _build_first_touch_body(prospect, observation, channel="email")


def _build_dm_body(prospect: Dict[str, str], observation: str) -> str:
    return _build_first_touch_body(prospect, observation, channel="dm")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

_SUBJECT_OPTIONS = [
    "quick question",
    "missed calls",
    "after-hours follow-up",
]

_HIGH_FIT_INDUSTRIES = {
    "plumbing", "hvac", "electrical", "locksmith", "garage_door", "towing",
}


def draft_email(
    prospect: Dict[str, str],
    final_priority_score: int,
    observation: Optional[str] = None,
) -> Tuple[str, str]:
    """
    Generate a first-touch email draft.
    Requires observation. Raises ObservationMissingError if absent.
    Raises DraftInvalidError if the generated draft fails validation.
    """
    business_name = (prospect.get("business_name") or "").strip()
    city = (prospect.get("city") or "").strip()

    if not business_name:
        raise ValueError("Cannot draft email without business_name.")
    if not city:
        raise ValueError(f"Cannot draft email for {business_name} without city.")

    raw_obs = observation or prospect.get("business_specific_observation") or ""
    obs = _require_observation(raw_obs)

    if _is_generic_observation(obs):
        raise ObservationMissingError(
            "Observation is too generic - it could apply to most businesses in this category. "
            "Write something specific to this business."
        )

    angle = _pick_offer_angle(prospect, obs)
    subject = _subject_from_observation(prospect, obs, angle)
    body_text = _build_email_body(prospect, obs)
    body_text = enforce_human_style(body_text)

    full_body = body_text + _SIGN_OFF
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
    """
    Return short companion drafts for Facebook DM, Instagram DM, and contact-form use.
    Requires observation. Raises ObservationMissingError if absent.
    """
    raw_obs = observation or prospect.get("business_specific_observation") or ""
    obs = _require_observation(raw_obs)

    if _is_generic_observation(obs):
        raise ObservationMissingError(
            "Observation is too generic for DM generation. "
            "Write something specific to this business."
        )

    dm_body = _build_dm_body(prospect, obs)
    dm_body = enforce_human_style(dm_body)
    validate_draft(dm_body, obs)

    return dm_body, dm_body, dm_body


# ---------------------------------------------------------------------------
# Pipeline compatibility shims (unchanged signatures)
# ---------------------------------------------------------------------------

def pick_best_pitch_angle(likely_opportunity: str) -> str:
    return (likely_opportunity or "booking automation").strip() or "booking automation"
