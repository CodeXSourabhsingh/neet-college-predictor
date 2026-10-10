import requests

SHEET_URL = "https://script.google.com/macros/s/AKfycbxgUGQ3vWcJ20Tzu8TEu--sUtVDniGg0BI-d52R0wC4kEfezrOOVdWDf7n0_dHF0xY/exec"

_phone_cache = set()


def phone_exists(phone):
    """Check if phone is already in the sheet (cached per session)."""
    global _phone_cache
    if not _phone_cache:
        r = requests.get(SHEET_URL + "?action=phones", timeout=5)
        if r.status_code == 200:
            _phone_cache = set(str(p) for p in r.json().get("phones", []))
    return str(phone) in _phone_cache


def save_lead(name, phone, score, category, state, air,
              utm_source="", utm_medium="", utm_campaign=""):
    try:
        requests.post(SHEET_URL, json={
            "name": name,
            "phone": phone,
            "score": score,
            "category": category,
            "state": state,
            "predicted_air": air,
            "utm_source": utm_source,
            "utm_medium": utm_medium,
            "utm_campaign": utm_campaign,
        }, timeout=5)
        _phone_cache.add(str(phone))
    except Exception:
        pass


def send_event(event_name, score="", category="", state="",
               safe_count="", moderate_count="", reach_count="",
               utm_source="", device=""):
    try:
        requests.post(SHEET_URL, json={
            "type": "event",
            "event": event_name,
            "score": score,
            "category": category,
            "state": state,
            "safe_count": safe_count,
            "moderate_count": moderate_count,
            "reach_count": reach_count,
            "utm_source": utm_source,
            "device": device,
        }, timeout=5)
    except Exception:
        pass