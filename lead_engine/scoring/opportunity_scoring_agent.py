from __future__ import annotations

from typing import Dict, Tuple
from urllib.request import urlopen, Request
from urllib.error import URLError

# ---------------------------------------------------------------------------
# Known large chains — scored down as low-opportunity targets
# ---------------------------------------------------------------------------
_KNOWN_CHAINS = {
    "mcdonald's", "mcdonalds", "subway", "starbucks", "dunkin", "dunkin donuts",
    "burger king", "wendy's", "wendys", "taco bell", "chick-fil-a", "chickfila",
    "domino's", "dominoes", "pizza hut", "little caesars",
    "jiffy lube", "midas", "meineke", "firestone", "pep boys",
    "anytime fitness", "planet fitness", "la fitness",
    "h&r block", "hr block", "jackson hewitt",
    "great clips", "sport clips", "supercuts",
    "servpro", "servicemaster", "molly maid",
}

# ---------------------------------------------------------------------------
# Score → human label
# ---------------------------------------------------------------------------
_LABELS: Dict[int, str] = {
    5: "High Opportunity",
    4: "Good Fit",
    3: "Possible",
    2: "Weak",
    1: "Skip",
}


def _website_reachable(url: str, timeout: int = 5) -> bool:
    """HEAD request; falls back to GET. Never raises."""
    if not url or not url.startswith(("http://", "https://")):
        return False
    try:
        req = Request(url, method="HEAD", headers={"User-Agent": "LeadBot/1.0"})
        with urlopen(req, timeout=timeout) as r:
            return r.status < 400
    except Exception:
        pass
    try:
        req = Request(url, headers={"User-Agent": "LeadBot/1.0"})
        with urlopen(req, timeout=timeout) as r:
            return r.status < 400
    except Exception:
        return False


def score_opportunity(
    prospect: Dict[str, str],
    website_scan: Dict[str, object],
) -> Tuple[int, str]:
    """
    Deterministic 1-5 lead score.

    Scoring model
    -------------
    Start at 0, then:
      +2  website exists
      +2  business email exists
      +1  review_count < 200  (sparse reviews → less competition-aware)
      +1  rating < 4.6        (room for improvement → pain point exists)
      +1  not a known chain
      -1  business name matches a known chain
      -1  website unreachable
      -1  no email found
    Clamped to [1, 5].
    """
    reasons: list[str] = []
    score = 0

    website  = (prospect.get("website") or "").strip()
    email    = (prospect.get("to_email") or "").strip()
    name_lc  = (prospect.get("business_name") or "").strip().lower()

    # --- positive signals ---
    if website:
        score += 2
        reasons.append("has website")
    if email:
        score += 2
        reasons.append("has email")

    try:
        review_count = int(prospect.get("review_count") or 0)
    except (ValueError, TypeError):
        review_count = 0
    if 0 < review_count < 200:
        score += 1
        reasons.append(f"low review count ({review_count})")

    try:
        rating = float(prospect.get("rating") or 0)
    except (ValueError, TypeError):
        rating = 0.0
    if 0 < rating < 4.6:
        score += 1
        reasons.append(f"rating {rating} < 4.6")

    is_chain = any(chain in name_lc for chain in _KNOWN_CHAINS)
    if not is_chain:
        score += 1
        reasons.append("independent business")

    # --- negative signals ---
    if is_chain:
        score -= 1
        reasons.append("known chain")

    if website and not _website_reachable(website):
        score -= 1
        reasons.append("website unreachable")

    if not email:
        score -= 1
        reasons.append("no email")

    final_score = max(1, min(5, score))
    label = _LABELS[final_score]
    reason_str = "; ".join(reasons) if reasons else "no signals"

    return final_score, f"{label} — {reason_str}"


def score_label(score: int) -> str:
    """Return the human-readable label for a numeric score."""
    return _LABELS.get(max(1, min(5, score)), "Unknown")
