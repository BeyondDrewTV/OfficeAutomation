from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

import lead_memory as _lm

ANGLE_OBSERVATION_CONTINUATION = "observation_continuation"
ANGLE_OPERATIONAL_NUDGE = "operational_nudge"
ANGLE_NOTE_REFRAME = "note_reframe"
ANGLE_TIMELINE_REFRAME = "timeline_reframe"
ANGLE_LOW_PRESSURE_CLOSEOUT = "low_pressure_closeout"

_SIGN_OFF = "\n\n- Drew"
_MAX_WORDS = 65
_STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "been", "but", "by", "for",
    "from", "had", "has", "have", "if", "in", "into", "is", "it", "its",
    "just", "me", "my", "no", "not", "of", "on", "or", "our", "so", "still",
    "that", "the", "their", "them", "there", "this", "to", "up", "was", "we",
    "were", "with", "you", "your",
}
_GENERIC_CONTEXT_TOKENS = {
    "business", "businesses", "calls", "call", "service", "services",
    "workflow", "operator", "owner", "owners", "local", "question",
    "quick", "note", "email", "emails", "follow", "followup", "follow-up",
    "text", "texts", "thread", "timing", "example", "busy", "days",
}
_CONTINUATION_MARKERS = (
    "following up",
    "circling back",
    "last note",
    "leaving one follow-up",
    "closing the loop",
)
_BANNED_PHRASES = {
    "automation", "automated", "lead gen", "lead-gen", "agency",
    "agencies", "free audit", "free consultation", "schedule a call",
    "book a call", "book a meeting", "hop on a call", "let's hop on",
    "click here", "pricing", "per month", "/mo", "monthly", "roi",
    "growth", "scale your", "platform", "solution", "streamline",
    "optimize", "just bumping this up", "bumping this up", "checking in",
    "touching base", "happy to show you", "happy to send a quick example",
    "worth a quick look", "curious?", "free trial",
}
_SWAPPABLE_PATTERNS = {
    "just following up on my note from last week",
    "one more note before i move on",
    "last one from me",
    "if the timing isn't right, no worries at all",
    "if the timing's off",
}
_FIRST_TOUCH_PHRASES = {
    "came across your business",
    "came across your page",
    "had a quick question",
    "figured i'd reach out",
    "wanted to reach out",
    "noticed you do",
    "noticed you offer",
    "saw you do",
}
_BLOCKED_REASON_MESSAGES = {
    "insufficient_context": "Follow-up blocked: no lead-specific continuation context is on file.",
    "generic_context": "Follow-up blocked: the available context is too generic to justify a grounded follow-up.",
    "contact_path_not_email": "Follow-up blocked: this lead is not on an email follow-up path.",
    "invalid_banned_language": "Follow-up blocked: generated copy used banned language.",
    "invalid_hard_cta": "Follow-up blocked: generated copy used a hard CTA.",
    "invalid_generic_copy": "Follow-up blocked: generated copy still reads like swappable sequence language.",
    "invalid_missing_context_overlap": "Follow-up blocked: generated copy does not materially reflect lead-specific context.",
    "invalid_not_continuation": "Follow-up blocked: generated copy reads like a first-touch instead of a continuation.",
    "invalid_too_long": "Follow-up blocked: generated copy is too long for a follow-up.",
}

_OPERATIONAL_IMPLICATIONS: List[Tuple[Tuple[str, ...], str]] = [
    (("voicemail", "after-hours", "after hours", "missed call", "missed calls", "callback", "callbacks"),
     "That felt like the kind of thing that turns into missed callbacks once the day runs long."),
    (("form", "contact form", "contact page", "no email"),
     "That usually means extra back-and-forth when someone is ready to reach you."),
    (("schedule", "booking", "bookings", "appointment", "appointments", "quote", "quotes", "estimate", "estimates"),
     "That tends to create a lag between interest and the next step when things get busy."),
    (("juggling", "mixing", "split", "splitting", "seasonal", "overlap", "lineup"),
     "That looked like the kind of operational overlap that gets messy when the week fills up."),
    (("review", "reviews", "photos", "hours", "page", "site", "website"),
     "It felt like one of those details that can quietly shape how follow-through lands."),
]


class FollowupBlockedError(ValueError):
    def __init__(self, reason: str, message: Optional[str] = None):
        self.reason = reason
        super().__init__(message or _BLOCKED_REASON_MESSAGES.get(reason, reason))


def _parse_dt(value: str) -> Optional[datetime]:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if not dt.tzinfo:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except Exception:
        return None


def _clean_context_text(text: str) -> str:
    cleaned = re.sub(r"\s+", " ", (text or "").strip())
    cleaned = cleaned.strip(" -,.")
    return cleaned


def _meaningful_tokens(text: str) -> set[str]:
    tokens = {
        tok.lower()
        for tok in re.findall(r"[A-Za-z0-9']+", (text or "").lower())
        if len(tok) > 3
    }
    return {
        tok for tok in tokens
        if tok not in _STOPWORDS and tok not in _GENERIC_CONTEXT_TOKENS
    }


def _context_grade(text: str) -> dict:
    return _lm.grade_observation(_clean_context_text(text))


def _is_specific_context(text: str) -> bool:
    cleaned = _clean_context_text(text)
    if not cleaned:
        return False
    grade = _context_grade(cleaned).get("grade")
    if grade in {"empty", "too_short", "generic"}:
        return False
    if grade in {"specific", "tied_to_workflow"}:
        return True
    tokens = _meaningful_tokens(cleaned)
    return grade == "category_only" and len(tokens) >= 4


def _extract_prior_anchor(body: str) -> str:
    if not body:
        return ""
    patterns = [
        r"after noticing ([^.]+)",
        r"noticed ([^.]+)",
        r"saw ([^.]+)",
        r"came across your (?:business|page)\s*[-,:]\s*([^.]+)",
        r"about ([^.]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, body, flags=re.IGNORECASE)
        if not match:
            continue
        candidate = _clean_context_text(match.group(1))
        candidate = re.split(r"\n|[-–—]\s*Drew\b", candidate, maxsplit=1, flags=re.IGNORECASE)[0]
        candidate = _clean_context_text(candidate)
        if _context_grade(candidate).get("grade") in {"specific", "tied_to_workflow"}:
            return candidate
    return ""


def _extract_timeline_anchor(timeline: List[dict]) -> str:
    for entry in reversed(timeline or []):
        event_type = (entry.get("event_type") or "").strip()
        detail = _clean_context_text(entry.get("detail") or "")
        if not detail:
            continue
        if event_type == _lm.EVT_DRAFT_REGENERATED and detail.lower().startswith("obs="):
            detail = _clean_context_text(detail[4:])
        if event_type in {_lm.EVT_OBSERVATION_ADDED, _lm.EVT_DRAFT_REGENERATED, _lm.EVT_NOTE_ADDED} and _is_specific_context(detail):
            return detail
    return ""


def _time_phrase(days_since_sent: Optional[int]) -> str:
    if days_since_sent is None:
        return "a bit back"
    if days_since_sent < 7:
        return "earlier this week"
    if days_since_sent < 15:
        return "last week"
    if days_since_sent < 31:
        return "earlier this month"
    return "a while back"


def _contact_path(row: Dict[str, str]) -> str:
    if (row.get("do_not_contact") or "").strip().lower() == "true":
        return "suppress"
    if (row.get("replied") or "").strip().lower() == "true":
        return "conversation"
    if (row.get("last_contact_channel") or "").strip() in {"facebook", "instagram", "contact_form"} and not (row.get("message_id") or "").strip():
        return "social"
    if (row.get("to_email") or "").strip():
        return "email"
    if (row.get("facebook_url") or "").strip() or (row.get("instagram_url") or "").strip() or (row.get("contact_form_url") or "").strip():
        return "social"
    return "enrich"


def _select_anchor(row: Dict[str, str], timeline: List[dict], obs_history: List[dict], record: dict) -> Tuple[str, str]:
    candidates = [
        ("current_observation", row.get("business_specific_observation") or record.get("current_observation") or ""),
        ("obs_history", (obs_history[-1] or {}).get("text") if obs_history else ""),
        ("timeline_observation", _extract_timeline_anchor(timeline)),
        ("conversation_next_step", row.get("conversation_next_step") or ""),
        ("conversation_notes", row.get("conversation_notes") or ""),
    ]
    generic_fallback = ""
    for source, raw_text in candidates:
        text = _clean_context_text(raw_text or "")
        if not text:
            continue
        if _is_specific_context(text):
            return source, text
        if not generic_fallback:
            generic_fallback = text
    if generic_fallback:
        raise FollowupBlockedError("generic_context")
    raise FollowupBlockedError("insufficient_context")


def _angle_label(angle_family: str) -> str:
    labels = {
        ANGLE_OBSERVATION_CONTINUATION: "Observation continuation",
        ANGLE_OPERATIONAL_NUDGE: "Operational nudge",
        ANGLE_NOTE_REFRAME: "Note reframe",
        ANGLE_TIMELINE_REFRAME: "Timeline-aware reframe",
        ANGLE_LOW_PRESSURE_CLOSEOUT: "Low-pressure closeout",
    }
    return labels.get(angle_family, angle_family.replace("_", " "))


def _operational_implication(anchor_text: str) -> str:
    lower = anchor_text.lower()
    for keywords, line in _OPERATIONAL_IMPLICATIONS:
        if any(keyword in lower for keyword in keywords):
            return line
    return ""


def _build_subject(row: Dict[str, str]) -> str:
    prior = _clean_context_text(row.get("subject") or "")
    if not prior:
        return "Re: quick question"
    prior = re.sub(r"^\s*re:\s*", "", prior, flags=re.IGNORECASE).strip()
    return f"Re: {prior}" if prior else "Re: quick question"


def _select_angle_family(anchor_source: str, anchor_text: str, touch_num: int) -> str:
    if touch_num >= 3:
        return ANGLE_LOW_PRESSURE_CLOSEOUT
    if anchor_source in {"conversation_next_step", "conversation_notes"}:
        return ANGLE_NOTE_REFRAME
    if touch_num >= 2:
        return ANGLE_TIMELINE_REFRAME
    if _operational_implication(anchor_text):
        return ANGLE_OPERATIONAL_NUDGE
    return ANGLE_OBSERVATION_CONTINUATION


def _build_body(row: Dict[str, str], context: dict) -> str:
    business_name = _clean_context_text(row.get("business_name") or "there")
    anchor = context["anchor_text"]
    angle_family = context["angle_family"]
    implication = context["operational_implication"]
    when = context["time_phrase"]

    if angle_family == ANGLE_OPERATIONAL_NUDGE:
        lines = [
            f"Hi {business_name},",
            "",
            f"Following up on the note I sent about {anchor}.",
            implication,
            "If it is already handled on your end, all good.",
        ]
    elif angle_family == ANGLE_NOTE_REFRAME:
        lines = [
            f"Hi {business_name},",
            "",
            f"Leaving one follow-up here on {anchor}.",
            "It still felt like the next thing worth tightening up if it is on your radar.",
            "If not, no problem at all.",
        ]
    elif angle_family == ANGLE_TIMELINE_REFRAME:
        lines = [
            f"Hi {business_name},",
            "",
            f"Circling back on the note I sent {when} about {anchor}.",
            "Could just be timing, but it still felt relevant enough to leave one more note.",
            "If it is not a fit right now, all good.",
        ]
    elif angle_family == ANGLE_LOW_PRESSURE_CLOSEOUT:
        lines = [
            f"Hi {business_name},",
            "",
            f"Last note from me on {anchor}.",
            "It still felt relevant, but I do not want to crowd your inbox.",
            "If it ever becomes a pain point, this thread is here.",
        ]
    else:
        lines = [
            f"Hi {business_name},",
            "",
            f"Following up on the note I sent about {anchor}.",
            "It still felt like one of those things that can quietly get harder once the day fills up.",
            "If it is already covered, all good.",
        ]

    return "\n".join(lines).strip() + _SIGN_OFF


def _validate_followup(body: str, context: dict) -> None:
    body_lower = body.lower()
    for phrase in _BANNED_PHRASES:
        if phrase in body_lower:
            if any(cta in phrase for cta in ("call", "show you", "example", "click here")):
                raise FollowupBlockedError("invalid_hard_cta")
            raise FollowupBlockedError("invalid_banned_language")
    for pattern in _SWAPPABLE_PATTERNS:
        if pattern in body_lower:
            raise FollowupBlockedError("invalid_generic_copy")

    if re.search(r"https?://", body, flags=re.IGNORECASE):
        raise FollowupBlockedError("invalid_hard_cta")
    if re.search(r"\$\d+|\bper month\b|\b/mo\b|\bmonthly\b", body_lower):
        raise FollowupBlockedError("invalid_banned_language")

    if any(marker in body_lower for marker in _FIRST_TOUCH_PHRASES):
        raise FollowupBlockedError("invalid_not_continuation")
    if not any(marker in body_lower for marker in _CONTINUATION_MARKERS):
        raise FollowupBlockedError("invalid_not_continuation")

    non_signature = re.sub(r"\n\n-\s*Drew\s*$", "", body, flags=re.IGNORECASE).strip()
    if len(non_signature.split()) > _MAX_WORDS:
        raise FollowupBlockedError("invalid_too_long")

    anchor_tokens = _meaningful_tokens(context.get("anchor_text") or "")
    body_tokens = _meaningful_tokens(non_signature)
    if not anchor_tokens or not (anchor_tokens & body_tokens):
        raise FollowupBlockedError("invalid_missing_context_overlap")

    generic_body = body_lower.replace((context.get("anchor_text") or "").lower(), "")
    if not _meaningful_tokens(generic_body):
        raise FollowupBlockedError("invalid_generic_copy")


def build_followup_plan(row: Dict[str, str], touch_num: int) -> Dict[str, object]:
    record = _lm.get_record(row) or {}
    timeline = _lm.get_timeline(row) or []
    obs_history = _lm.get_obs_history(row) or []
    sent_dt = _parse_dt(row.get("sent_at") or "")
    days_since_sent = None
    if sent_dt:
        days_since_sent = max(0, int((datetime.now(timezone.utc) - sent_dt).days))

    if _contact_path(row) != "email":
        raise FollowupBlockedError("contact_path_not_email")

    anchor_source, anchor_text = _select_anchor(row, timeline, obs_history, record)
    angle_family = _select_angle_family(anchor_source, anchor_text, touch_num)
    context = {
        "touch_num": touch_num,
        "anchor_source": anchor_source,
        "anchor_text": anchor_text,
        "angle_family": angle_family,
        "angle_label": _angle_label(angle_family),
        "operational_implication": _operational_implication(anchor_text) or "It still looked like one of those small operational gaps that gets harder to stay on top of once the day fills up.",
        "time_phrase": _time_phrase(days_since_sent),
        "timeline_event_count": len(timeline),
        "obs_history_count": len(obs_history),
        "days_since_sent": days_since_sent,
        "contact_path": "email",
        "last_contact_channel": _clean_context_text(row.get("last_contact_channel") or ""),
        "last_contacted_at": _clean_context_text(row.get("last_contacted_at") or ""),
    }
    subject = _build_subject(row)
    body = _build_body(row, context)
    _validate_followup(body, context)
    return {
        "ok": True,
        "subject": subject,
        "body": body,
        "angle_family": angle_family,
        "angle_label": context["angle_label"],
        "context": context,
    }
