# Basic Cleanup — Bundle Scope Matrix
Version: v1 | Kit: basic_cleanup_v1

**Dependency note:** Basic Cleanup uses the Presence Refresh kit as its operational backbone. See `lead_engine/delivery_kits/presence_refresh/` for the component kit files.

---

## Scope Comparison

| Item | Basic Cleanup | Full Presence Refresh |
|---|---|---|
| GBP: name, phone, hours, address | ✓ In scope | ✓ In scope |
| GBP: description refresh | ✓ In scope | ✓ In scope |
| GBP: services list update | ✓ In scope | ✓ In scope |
| GBP: photo review + 1 update | ✓ In scope | ✓ In scope |
| GBP: full photo refresh / upload | ✗ Not in scope | ✓ In scope |
| GBP: Q&A cleanup | ✗ Not in scope | ✓ In scope |
| Facebook: full refresh | ✗ Not in scope | ✓ In scope |
| Facebook: basic consistency check | ✓ In scope (read only, flag only) | ✓ In scope |
| Cross-platform consistency | Flagged only (not fixed) | Fixed in scope |
| Trust copy rewrite | ✗ Not in scope | ✓ In scope |

---

## Scope Ceiling

Basic Cleanup covers only GBP core fields and one photo update. Anything beyond this table is a change order or an upgrade to full Presence Refresh.

---

## Revision Window

One pass within the sold scope. Revision requests that expand the scope are change orders.

---

## Pricing Note

Basic Cleanup is priced below full Presence Refresh — the narrower scope is the reason.

---

## Dependency

Presence Refresh kit files must be active before running a Basic Cleanup engagement. Do not run a Basic Cleanup without the `lead_engine/delivery_kits/presence_refresh/` kit files present and understood.
