from __future__ import annotations

import re
from typing import Dict, List, Optional

from discovery.auto_prospect_agent import (
    classify_contactability,
    extract_contact_details_from_website,
    find_business_website_fallback,
)
from intelligence.website_scan_agent import scan_website


_GENERIC_TEMPLATE_PHRASES = [
    "customer satisfaction",
    "quality service",
    "call today",
    "learn more",
    "family owned",
    "family-owned",
    "licensed and insured",
    "professional service",
    "our team",
    "contact us",
]

_SERVICE_PATTERNS = [
    ("water heater work", ("water heater", "tankless water heater", "tankless")),
    ("drain and sewer work", ("drain cleaning", "sewer cleaning", "sewer line", "hydro jet", "camera inspection")),
    ("ductless mini-split work", ("mini split", "mini-split", "ductless")),
    ("heat pump work", ("heat pump",)),
    ("commercial service", ("commercial hvac", "light commercial", "commercial refrigeration", "commercial service")),
    ("garage door opener work", ("garage door opener", "opener repair")),
    ("spring repair", ("spring replacement", "broken spring", "garage door spring")),
    ("panel upgrade work", ("panel upgrade", "electrical panel", "breaker panel")),
    ("ev charger installs", ("ev charger", "electric vehicle charger")),
    ("flat roofing work", ("flat roof", "metal roof", "rubber roof", "tpo roofing")),
    ("rekey and lockout work", ("rekey", "lockout", "car lockout", "house lockout")),
    ("brake work", ("brake repair", "brake service", "brakes")),
    ("transmission work", ("transmission repair", "transmission service")),
    ("towing support", ("towing", "tow truck", "roadside assistance")),
]

_AVAILABILITY_PATTERNS = [
    ("emergency service", ("emergency service", "emergency repair", "24/7", "24 hour", "24-hour")),
    ("after-hours coverage", ("after hours", "after-hours", "after hour")),
    ("weekend coverage", ("weekend service", "weekend availability", "weekends")),
    ("same-day service", ("same day service", "same-day service", "same day appointments")),
]

_CTA_PATTERNS = [
    ("free estimates", ("free estimate", "free estimates")),
    ("quote requests", ("request quote", "get quote", "request estimate", "get estimate")),
    ("online booking", ("book now", "online booking", "schedule appointment")),
    ("service scheduling", ("schedule service", "request service", "request appointment")),
    ("financing", ("financing", "payment plans")),
]


def refresh_observation_evidence(
    row: Dict[str, str],
    *,
    prospect_row: Optional[Dict[str, str]] = None,
) -> dict:
    business_name = (row.get("business_name") or "").strip()
    city = (row.get("city") or prospect_row.get("city") or "").strip() if prospect_row else (row.get("city") or "").strip()
    existing_website = (row.get("website") or prospect_row.get("website") or "").strip() if prospect_row else (row.get("website") or "").strip()
    website = existing_website
    website_source = "existing_website" if website else ""

    if not website and business_name:
        fallback_website, _ = find_business_website_fallback(business_name, city)
        website = (fallback_website or "").strip()
        if website:
            website_source = "search_fallback"

    base_result = {
        "ok": True,
        "website": website,
        "website_source": website_source,
        "row_updates": {},
        "prospect_updates": {},
        "updated_fields": [],
        "prospect_updated_fields": [],
        "summary": "",
        "evidence": [],
        "source_labels": [],
        "blocked": False,
        "blocked_reason": "",
        "blocked_message": "",
    }

    if not website:
        base_result.update({
            "blocked": True,
            "blocked_reason": "no_retrievable_source",
            "blocked_message": "No website is on file for this lead, and refresh could not find a retrievable source.",
            "summary": "No retrievable website source was available for a live evidence refresh.",
            "source_labels": ["website_lookup"],
        })
        return base_result

    contact_details = extract_contact_details_from_website(website)
    scan_result = scan_website(website)

    row_updates, prospect_updates = _build_contact_updates(row, prospect_row, website, contact_details)
    base_result["row_updates"] = row_updates
    base_result["prospect_updates"] = prospect_updates
    base_result["updated_fields"] = sorted(row_updates.keys())
    base_result["prospect_updated_fields"] = sorted(prospect_updates.keys())

    if not scan_result.get("website_reachable") and not contact_details.get("site_reachable"):
        base_result.update({
            "blocked": True,
            "blocked_reason": "fetch_failed",
            "blocked_message": "The website could not be retrieved right now, so no fresh observation evidence was added.",
            "summary": "Website refresh failed before any fresh business-specific evidence could be confirmed.",
            "evidence": _contact_update_evidence(contact_details, row_updates),
            "source_labels": ["website_refresh", "contact_refresh"],
        })
        return base_result

    derived = _derive_site_evidence(scan_result, city=city)
    evidence = []
    evidence.extend(derived.get("evidence") or [])
    evidence.extend(_contact_update_evidence(contact_details, row_updates))
    source_labels = ["website_refresh"]
    if row_updates:
        source_labels.append("contact_refresh")

    if derived.get("ok"):
        refresh_signals = _merge_refresh_signals(
            derived.get("signals") or [],
            row_updates=row_updates,
        )
        row_updates["lead_insight_sentence"] = derived["sentence"]
        row_updates["lead_insight_signals"] = "|".join(refresh_signals)
        base_result.update({
            "row_updates": row_updates,
            "updated_fields": sorted(row_updates.keys()),
            "summary": f"Fresh site evidence was retrieved from {_website_source_label(website_source)} and saved on this lead.",
            "evidence": evidence,
            "source_labels": source_labels,
        })
        return base_result

    base_result.update({
        "blocked": True,
        "blocked_reason": derived.get("blocked_reason") or "no_concrete_business_signal",
        "blocked_message": derived.get("blocked_message") or "No concrete business-specific site signal was confirmed.",
        "summary": "Refresh updated what it could, but it still did not uncover enough grounded evidence for an observation candidate.",
        "evidence": evidence,
        "source_labels": source_labels,
    })
    return base_result


def _build_contact_updates(
    row: Dict[str, str],
    prospect_row: Optional[Dict[str, str]],
    website: str,
    contact_details: Dict[str, object],
) -> tuple[dict, dict]:
    row_updates: Dict[str, str] = {}
    prospect_updates: Dict[str, str] = {}

    email = (contact_details.get("email") or "").strip()
    contact_form_url = (contact_details.get("contact_form_url") or "").strip()
    facebook_url = (contact_details.get("facebook_url") or "").strip()
    instagram_url = (contact_details.get("instagram_url") or "").strip()
    site_reachable = bool(contact_details.get("site_reachable"))

    if email and email != (row.get("to_email") or "").strip():
        row_updates["to_email"] = email
    if contact_form_url and contact_form_url != (row.get("contact_form_url") or "").strip():
        row_updates["contact_form_url"] = contact_form_url
    if facebook_url and facebook_url != (row.get("facebook_url") or "").strip():
        row_updates["facebook_url"] = facebook_url
    if instagram_url and instagram_url != (row.get("instagram_url") or "").strip():
        row_updates["instagram_url"] = instagram_url

    if prospect_row is not None:
        if email and email != (prospect_row.get("to_email") or "").strip():
            prospect_updates["to_email"] = email
        if contact_form_url and contact_form_url != (prospect_row.get("contact_form_url") or "").strip():
            prospect_updates["contact_form_url"] = contact_form_url
        if facebook_url and facebook_url != (prospect_row.get("facebook_url") or "").strip():
            prospect_updates["facebook_url"] = facebook_url
        if instagram_url and instagram_url != (prospect_row.get("instagram_url") or "").strip():
            prospect_updates["instagram_url"] = instagram_url

        contactability = classify_contactability(
            email=email or (prospect_row.get("to_email") or "").strip(),
            website=website,
            website_reachable=site_reachable,
            is_directory=False,
            is_ambiguous=False,
        )
        if contactability and contactability != (prospect_row.get("contactability") or "").strip():
            prospect_updates["contactability"] = contactability

    return row_updates, prospect_updates


def _derive_site_evidence(scan_result: Dict[str, object], *, city: str = "") -> dict:
    text = re.sub(r"\s+", " ", str(scan_result.get("text_corpus") or "").lower()).strip()
    if not text:
        return {
            "ok": False,
            "blocked_reason": "no_concrete_business_signal",
            "blocked_message": "The website loaded, but it did not expose enough readable text for a safe observation.",
            "evidence": [],
            "signals": [],
        }

    services = _match_labels(text, _SERVICE_PATTERNS, limit=2)
    availability = _match_labels(text, _AVAILABILITY_PATTERNS, limit=1)
    ctas = _match_labels(text, _CTA_PATTERNS, limit=2)
    area_phrase = _city_area_signal(text, city)

    evidence: List[str] = []
    signals: List[str] = ["fresh site evidence"]
    if services:
        signals.extend(services)
        evidence.append("Site explicitly mentions " + ", ".join(services) + ".")
    if availability:
        signals.extend(availability)
        evidence.append("Site explicitly mentions " + ", ".join(availability) + ".")
    if ctas:
        signals.extend(ctas)
        evidence.append("Site explicitly mentions " + ", ".join(ctas) + ".")
    if area_phrase:
        signals.append(area_phrase)
        evidence.append("Site spells out " + area_phrase + ".")

    if services or availability or ctas or area_phrase:
        return {
            "ok": True,
            "sentence": _build_observation_sentence(
                services=services,
                availability=availability,
                ctas=ctas,
                area_phrase=area_phrase,
            ),
            "signals": signals,
            "evidence": evidence,
        }

    generic_hits = [phrase for phrase in _GENERIC_TEMPLATE_PHRASES if phrase in text]
    if len(generic_hits) >= 2:
        return {
            "ok": False,
            "blocked_reason": "generic_template_language",
            "blocked_message": "The website mostly surfaced generic template language, not business-specific operational detail.",
            "evidence": ["Generic site copy dominated the scan: " + ", ".join(generic_hits[:3]) + "."],
            "signals": ["fresh site evidence"],
        }

    return {
        "ok": False,
        "blocked_reason": "no_concrete_business_signal",
        "blocked_message": "The website refreshed successfully, but it still did not reveal a concrete business-specific signal.",
        "evidence": [],
        "signals": ["fresh site evidence"],
    }


def _match_labels(text: str, patterns: List[tuple[str, tuple[str, ...]]], *, limit: int) -> List[str]:
    labels: List[str] = []
    for label, tokens in patterns:
        if any(token in text for token in tokens):
            labels.append(label)
        if len(labels) >= limit:
            break
    return labels


def _city_area_signal(text: str, city: str) -> str:
    city_name = (city or "").strip().lower()
    if not city_name:
        return ""
    service_area_patterns = [
        rf"(serving|service area|proudly serving|surrounding areas).{{0,50}}{re.escape(city_name)}",
        rf"{re.escape(city_name)}.{{0,40}}(service area|surrounding areas|and surrounding)",
    ]
    if any(re.search(pattern, text) for pattern in service_area_patterns):
        return f"{city_name}-area coverage"
    return ""


def _build_observation_sentence(
    *,
    services: List[str],
    availability: List[str],
    ctas: List[str],
    area_phrase: str,
) -> str:
    parts: List[str] = []
    if services:
        parts.append(services[0])
    if availability:
        parts.append(availability[0])
    elif ctas:
        parts.append(ctas[0])
    elif area_phrase:
        parts.append(area_phrase)

    if len(parts) >= 2:
        return f"site is pretty explicit about {parts[0]} and {parts[1]}."
    if parts:
        return f"site is pretty explicit about {parts[0]}."
    return "site refresh did not uncover a concrete business-specific signal."


def _contact_update_evidence(contact_details: Dict[str, object], row_updates: Dict[str, str]) -> List[str]:
    evidence: List[str] = []
    if row_updates.get("to_email"):
        evidence.append("Refresh found a visible email address.")
    if row_updates.get("contact_form_url"):
        evidence.append("Refresh confirmed a contact form path.")
    if row_updates.get("facebook_url"):
        evidence.append("Refresh confirmed a Facebook route.")
    if row_updates.get("instagram_url"):
        evidence.append("Refresh confirmed an Instagram route.")
    if not evidence and contact_details.get("site_reachable"):
        evidence.append("Website was reachable during refresh.")
    return evidence


def _merge_refresh_signals(base_signals: List[str], *, row_updates: Dict[str, str]) -> List[str]:
    signals: List[str] = []
    for label in base_signals:
        clean = (label or "").strip().lower()
        if clean and clean not in signals:
            signals.append(clean)
    if row_updates.get("to_email") and "email available" not in signals:
        signals.append("email available")
    if row_updates.get("contact_form_url") and "contact form" not in signals:
        signals.append("contact form")
    if row_updates.get("facebook_url") and "facebook" not in signals:
        signals.append("facebook")
    if row_updates.get("instagram_url") and "instagram" not in signals:
        signals.append("instagram")
    return signals[:6]


def _website_source_label(source: str) -> str:
    if source == "search_fallback":
        return "search fallback"
    if source == "existing_website":
        return "the website already on file"
    return "website refresh"
