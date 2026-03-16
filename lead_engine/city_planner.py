"""
city_planner.py — City discovery tracking and revisit scheduling.

Stores a JSON list of cities the operator has searched, when they were last
searched, how many leads were found, and when to search again.

Revisit tiers (rules-based, no external API needed):
  large  — population-equivalent cities / metro areas: revisit every 14 days
  mid    — suburban cities / large towns:              revisit every 30 days
  small  — small towns / neighbourhoods:               revisit every 75 days

Cities are promoted to a higher tier if cumulative leads_found > threshold.
"""
from __future__ import annotations

import json
import logging
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Optional

log = logging.getLogger("copperline")

# ---------------------------------------------------------------------------
# Tier config
# ---------------------------------------------------------------------------
_TIERS = {
    "large": {"revisit_days": 14,  "label": "Large / Metro"},
    "mid":   {"revisit_days": 30,  "label": "Mid-size"},
    "small": {"revisit_days": 75,  "label": "Small / Neighbourhood"},
}

# Known large metros — anything else defaults to "mid" unless overridden
_LARGE_CITIES = {
    "chicago", "new york", "los angeles", "houston", "phoenix", "philadelphia",
    "san antonio", "san diego", "dallas", "san jose", "austin", "jacksonville",
    "fort worth", "columbus", "charlotte", "indianapolis", "san francisco",
    "seattle", "denver", "nashville", "oklahoma city", "el paso", "washington",
    "las vegas", "louisville", "baltimore", "milwaukee", "albuquerque", "tucson",
    "fresno", "sacramento", "mesa", "atlanta", "kansas city", "omaha",
    "colorado springs", "raleigh", "long beach", "virginia beach", "minneapolis",
    "tampa", "new orleans", "arlington", "bakersfield", "wichita", "aurora",
    "cleveland", "anaheim", "honolulu", "orlando", "lexington", "pittsburgh",
    "stockton", "riverside", "cincinnati", "st. louis", "st louis",
}


def _infer_tier(city: str) -> str:
    return "large" if city.strip().lower() in _LARGE_CITIES else "mid"


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _next_check(tier: str, last_checked: str) -> str:
    days = _TIERS.get(tier, _TIERS["mid"])["revisit_days"]
    try:
        base = datetime.fromisoformat(last_checked.replace("Z", "+00:00"))
    except Exception:
        base = datetime.now(timezone.utc)
    return (base + timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")


def _is_due(entry: Dict) -> bool:
    nxt = entry.get("next_check_at", "")
    if not nxt:
        return True
    try:
        return datetime.now(timezone.utc) >= datetime.fromisoformat(nxt.replace("Z", "+00:00"))
    except Exception:
        return True


# ---------------------------------------------------------------------------
# State city seeds — nearby/local city suggestions per state
# Focused on mid-size service-trade markets (not just capitals/metros)
# ---------------------------------------------------------------------------
_STATE_CITY_SEEDS: Dict[str, List[str]] = {
    "IL": ["Rockford","Chicago","Aurora","Joliet","Naperville","Springfield","Peoria",
           "Elgin","Waukegan","Champaign","Bloomington","Decatur","Evanston","Bolingbrook",
           "Palatine","Schaumburg","Wicker Park","Pilsen","Oak Park","Evanston",
           "Cicero","Berwyn","Des Plaines","Orland Park","Tinley Park","Skokie",
           "Moline","Rock Island","Galesburg","Belleville","Quincy","DeKalb","Freeport",
           "Crystal Lake","Carpentersville","Romeoville","Plainfield","Downers Grove"],
    "WI": ["Milwaukee","Madison","Green Bay","Kenosha","Racine","Appleton","Waukesha",
           "Oshkosh","Eau Claire","Janesville","West Allis","La Crosse","Sheboygan",
           "Wauwatosa","Fond du Lac","New Berlin","Beloit","Wausau","Greenfield",
           "Franklin","Oak Creek","Manitowoc","West Bend","Sun Prairie","Superior"],
    "IN": ["Indianapolis","Fort Wayne","Evansville","South Bend","Carmel","Fishers",
           "Bloomington","Hammond","Gary","Lafayette","Muncie","Terre Haute","Kokomo",
           "Anderson","Noblesville","Greenwood","Elkhart","Mishawaka","Lawrence",
           "Jeffersonville","Columbus","Portage","New Albany","Richmond","Westfield"],
    "OH": ["Columbus","Cleveland","Cincinnati","Toledo","Akron","Dayton","Parma",
           "Canton","Youngstown","Lorain","Hamilton","Springfield","Kettering",
           "Elyria","Lakewood","Cuyahoga Falls","Middletown","Euclid","Newark",
           "Mansfield","Mentor","Beavercreek","Dublin","Strongsville","Fairfield"],
    "MI": ["Detroit","Grand Rapids","Warren","Sterling Heights","Ann Arbor","Lansing",
           "Flint","Dearborn","Livonia","Westland","Troy","Farmington Hills","Kalamazoo",
           "Wyoming","Southfield","Rochester Hills","Taylor","Pontiac","St Clair Shores",
           "Royal Oak","Novi","Dearborn Heights","Battle Creek","Saginaw","Muskegon"],
    "TX": ["Houston","San Antonio","Dallas","Austin","Fort Worth","El Paso","Arlington",
           "Corpus Christi","Plano","Laredo","Lubbock","Garland","Irving","Amarillo",
           "Grand Prairie","Brownsville","McKinney","Frisco","Pasadena","Killeen",
           "McAllen","Mesquite","Midland","Denton","Waco","Carrollton","Round Rock"],
    "FL": ["Jacksonville","Miami","Tampa","Orlando","St Petersburg","Hialeah","Tallahassee",
           "Fort Lauderdale","Port St Lucie","Cape Coral","Pembroke Pines","Hollywood",
           "Gainesville","Miramar","Coral Springs","Palm Bay","West Palm Beach","Clearwater",
           "Lakeland","Pompano Beach","Davie","Deltona","Boca Raton","Plantation","Sunrise"],
    "GA": ["Atlanta","Augusta","Columbus","Macon","Savannah","Athens","Sandy Springs",
           "Roswell","South Fulton","Johns Creek","Albany","Warner Robins","Alpharetta",
           "Marietta","Smyrna","Valdosta","Brookhaven","Dunwoody","Gainesville","Rome"],
    "PA": ["Philadelphia","Pittsburgh","Allentown","Erie","Reading","Scranton","Bethlehem",
           "Lancaster","Harrisburg","York","Altoona","Wilkes-Barre","Chester","Easton",
           "Norristown","State College","Hazleton","New Castle","McKeesport","Johnstown"],
    "NY": ["New York","Buffalo","Rochester","Yonkers","Syracuse","Albany","New Rochelle",
           "Mount Vernon","Schenectady","Utica","White Plains","Hempstead","Troy","Niagara Falls",
           "Binghamton","Freeport","Valley Stream","Long Beach","Spring Valley","Rome"],
    "CA": ["Los Angeles","San Diego","San Jose","San Francisco","Fresno","Sacramento",
           "Long Beach","Oakland","Bakersfield","Anaheim","Santa Ana","Riverside","Stockton",
           "Chula Vista","Fremont","San Bernardino","Modesto","Fontana","Moreno Valley",
           "Glendale","Huntington Beach","Santa Clarita","Garden Grove","Oceanside","Rancho Cucamonga"],
    "AZ": ["Phoenix","Tucson","Mesa","Chandler","Scottsdale","Glendale","Gilbert","Tempe",
           "Peoria","Surprise","Yuma","Avondale","Goodyear","Flagstaff","Buckeye","Casa Grande"],
    "CO": ["Denver","Colorado Springs","Aurora","Fort Collins","Lakewood","Thornton",
           "Arvada","Westminster","Pueblo","Centennial","Boulder","Highlands Ranch",
           "Greeley","Longmont","Loveland","Broomfield","Castle Rock","Commerce City"],
    "WA": ["Seattle","Spokane","Tacoma","Vancouver","Bellevue","Everett","Kent","Renton",
           "Kirkland","Bellingham","Kennewick","Yakima","Redmond","Marysville","Pasco"],
    "NC": ["Charlotte","Raleigh","Greensboro","Durham","Winston-Salem","Fayetteville",
           "Cary","Wilmington","High Point","Concord","Asheville","Gastonia","Jacksonville",
           "Chapel Hill","Huntersville","Rocky Mount","Burlington","Wilson","Kannapolis"],
    "TN": ["Nashville","Memphis","Knoxville","Chattanooga","Clarksville","Murfreesboro",
           "Franklin","Jackson","Johnson City","Bartlett","Hendersonville","Kingsport",
           "Smyrna","Cleveland","Collierville","Brentwood","Germantown","Spring Hill"],
    "MO": ["Kansas City","St Louis","Springfield","Columbia","Independence","Lee's Summit",
           "O'Fallon","St Joseph","St Charles","Blue Springs","Joplin","Florissant",
           "Chesterfield","Jefferson City","Cape Girardeau","St Peters","Kirkwood"],
    "MN": ["Minneapolis","Saint Paul","Rochester","Duluth","Bloomington","Brooklyn Park",
           "Plymouth","St Cloud","Eagan","Woodbury","Coon Rapids","Burnsville","Eden Prairie",
           "Apple Valley","Edina","Lakeville","Minnetonka","Maple Grove","Maplewood"],
    "NV": ["Las Vegas","Henderson","Reno","North Las Vegas","Sparks","Carson City",
           "Enterprise","Whitney","Paradise","Sunrise Manor","Spring Valley","Summerlin"],
    "VA": ["Virginia Beach","Norfolk","Chesapeake","Richmond","Newport News","Alexandria",
           "Hampton","Roanoke","Portsmouth","Suffolk","Lynchburg","Harrisonburg",
           "Charlottesville","Danville","Manassas","Fredericksburg","Petersburg"],
}


# ---------------------------------------------------------------------------
# Storage helpers
# ---------------------------------------------------------------------------

class CityPlanner:
    def __init__(self, store_path: Path) -> None:
        self._path = store_path
        self._data: List[Dict] = []
        self._load()

    def _load(self) -> None:
        if self._path.exists():
            try:
                with self._path.open(encoding="utf-8") as f:
                    self._data = json.load(f)
            except Exception as exc:
                log.warning("city_planner: could not load %s: %s", self._path, exc)
                self._data = []
        else:
            self._data = []

    def _save(self) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._path.open("w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2)

    def _key(self, city: str, state: str) -> str:
        return f"{city.strip().lower()}|{state.strip().lower()}"

    def _find(self, city: str, state: str) -> Optional[Dict]:
        k = self._key(city, state)
        for entry in self._data:
            if self._key(entry["city"], entry["state"]) == k:
                return entry
        return None

    # ── Public API ────────────────────────────────────────────────────────

    def all_cities(self) -> List[Dict]:
        """Return all tracked cities, sorted: due first, then by city name."""
        def sort_key(e):
            due = 0 if _is_due(e) else 1
            never = 0 if not e.get("last_checked_at") else 1
            return (due, never, e.get("city", "").lower())
        return sorted(self._data, key=sort_key)

    def ensure_city(self, city: str, state: str, tier: Optional[str] = None) -> Dict:
        """Add a city if not already tracked. Returns the entry."""
        entry = self._find(city, state)
        if entry is None:
            t = tier or _infer_tier(city)
            entry = {
                "city": city.strip(),
                "state": state.strip().upper(),
                "tier": t,
                "last_checked_at": None,
                "leads_found": 0,
                "new_leads_last_run": 0,
                "status": "never_checked",
                "next_check_at": None,
            }
            self._data.append(entry)
            self._save()
        return entry

    def record_discovery(self, city: str, state: str, new_leads: int,
                          industry: Optional[str] = None) -> Dict:
        """
        Called after a successful Discover run.
        Updates city-level totals and, when industry is given, per-industry tracking.
        Auto-promotes tier if leads are coming in frequently.
        """
        entry = self.ensure_city(city, state)
        now = _now_iso()
        entry["last_checked_at"] = now
        entry["leads_found"] = entry.get("leads_found", 0) + new_leads
        entry["new_leads_last_run"] = new_leads

        # ── Per-industry tracking ─────────────────────────────────────────
        if industry:
            if "industries" not in entry:
                entry["industries"] = {}
            ind = entry["industries"].setdefault(industry, {
                "leads_found": 0,
                "last_checked_at": None,
                "new_leads_last_run": 0,
                "status": "never_checked",
            })
            ind["leads_found"] = ind.get("leads_found", 0) + new_leads
            ind["new_leads_last_run"] = new_leads
            ind["last_checked_at"] = now
            ind["status"] = "checked"

        # Auto-promote tier
        if entry["tier"] == "small" and entry["leads_found"] > 10:
            entry["tier"] = "mid"
        elif entry["tier"] == "mid" and entry["leads_found"] > 30:
            entry["tier"] = "large"

        entry["status"] = "done" if new_leads == 0 else "checked"
        entry["next_check_at"] = _next_check(entry["tier"], entry["last_checked_at"])
        self._save()
        return entry

    def get_industry_matrix(self, industries: List[str]) -> List[Dict]:
        """
        Return all tracked cities enriched with per-industry coverage data.
        Each entry includes an `industries` map keyed by industry name with
        status, leads_found, last_checked_at for that combination.
        Missing industries are returned with status='never_checked'.
        Sorted: cities with most uncovered industries first, then by city name.
        """
        result = []
        for entry in self._data:
            city_industries: Dict[str, Dict] = entry.get("industries", {})
            ind_rows = []
            never_count = 0
            due_count = 0
            for ind in industries:
                rec = city_industries.get(ind)
                if rec:
                    # check if this industry is due for revisit based on city tier
                    days = _TIERS.get(entry["tier"], _TIERS["mid"])["revisit_days"]
                    last = rec.get("last_checked_at", "")
                    ind_due = False
                    if last:
                        try:
                            base = datetime.fromisoformat(last.replace("Z", "+00:00"))
                            ind_due = datetime.now(timezone.utc) >= base + timedelta(days=days)
                        except Exception:
                            ind_due = True
                    status = "due" if ind_due else rec.get("status", "checked")
                    if ind_due:
                        due_count += 1
                    ind_rows.append({
                        "industry": ind,
                        "status": status,
                        "leads_found": rec.get("leads_found", 0),
                        "new_leads_last_run": rec.get("new_leads_last_run", 0),
                        "last_checked_at": rec.get("last_checked_at"),
                    })
                else:
                    never_count += 1
                    ind_rows.append({
                        "industry": ind,
                        "status": "never_checked",
                        "leads_found": 0,
                        "new_leads_last_run": 0,
                        "last_checked_at": None,
                    })

            covered = len(industries) - never_count
            city_due = _is_due(entry)
            result.append({
                **entry,
                "industry_rows": ind_rows,
                "covered_count": covered,
                "total_industries": len(industries),
                "never_count": never_count,
                "due_count": due_count,
                "city_is_due": city_due,
            })

        # Sort: most uncovered first, then due, then by city name
        result.sort(key=lambda e: (
            -e["never_count"],
            0 if e["city_is_due"] else 1,
            e["city"].lower()
        ))
        return result

    def set_tier(self, city: str, state: str, tier: str) -> None:
        entry = self.ensure_city(city, state)
        if tier in _TIERS:
            entry["tier"] = tier
            if entry.get("last_checked_at"):
                entry["next_check_at"] = _next_check(tier, entry["last_checked_at"])
            self._save()

    def skip_city(self, city: str, state: str) -> None:
        """Mark city as skipped — hides it from 'due' list until next_check_at."""
        entry = self.ensure_city(city, state)
        # Push next check out by full tier cadence from now
        entry["last_checked_at"] = entry.get("last_checked_at") or _now_iso()
        entry["next_check_at"] = _next_check(entry["tier"], _now_iso())
        entry["status"] = "skipped"
        self._save()

    def tiers_info(self) -> Dict:
        return {k: v for k, v in _TIERS.items()}

    # ── City suggestions for autocomplete ────────────────────────────────

    def suggest(self, state: str, query: str = "", limit: int = 30) -> List[Dict]:
        """
        Return city suggestions for autocomplete, merging:
          1. Already-tracked cities (with their status)
          2. Seed cities for the given state not yet tracked

        Each entry: { city, state, status, tier, tracked, leads_found, next_check_at }
        Sorted: tracked+due first, tracked+never second, seeds last.
        Filtered by query prefix if provided.
        """
        state_up = state.strip().upper()
        query_lc = query.strip().lower()

        # Build tracked set with status
        tracked = {}
        for entry in self._data:
            if entry.get("state", "").upper() != state_up:
                continue
            city_lc = entry["city"].strip().lower()
            due = _is_due(entry)
            never = not entry.get("last_checked_at")
            if never:
                status = "never_checked"
            elif entry.get("status") == "skipped":
                status = "skipped"
            elif due:
                status = "due"
            else:
                status = "checked"
            tracked[city_lc] = {
                "city": entry["city"],
                "state": state_up,
                "status": status,
                "tier": entry.get("tier", "mid"),
                "tracked": True,
                "leads_found": entry.get("leads_found", 0),
                "next_check_at": entry.get("next_check_at", ""),
            }

        # Seed cities for state
        seeds = _STATE_CITY_SEEDS.get(state_up, [])

        results = []
        seen = set()

        # Tracked cities first
        for city_lc, info in tracked.items():
            if query_lc and query_lc not in city_lc:
                continue
            seen.add(city_lc)
            results.append(info)

        # Seed cities not yet tracked
        for city_name in seeds:
            city_lc = city_name.lower()
            if city_lc in seen:
                continue
            if query_lc and query_lc not in city_lc:
                continue
            seen.add(city_lc)
            results.append({
                "city": city_name,
                "state": state_up,
                "status": "never_checked",
                "tier": _infer_tier(city_name),
                "tracked": False,
                "leads_found": 0,
                "next_check_at": "",
            })

        # Sort: due/never+tracked → never_checked+tracked → skipped → seeds
        def _sort_key(e):
            if e["tracked"]:
                order = {"due": 0, "never_checked": 1, "checked": 2, "skipped": 3}.get(e["status"], 4)
            else:
                order = 5
            return (order, e["city"].lower())

        results.sort(key=_sort_key)
        return results[:limit]
