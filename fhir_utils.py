# fhir_utils.py
"""
FHIR R4 Client — fetches real patient clinical data.
Default: public HAPI FHIR sandbox (no auth needed for demo).
Browse test patients at: https://hapi.fhir.org/baseR4/Patient
"""
import httpx
from typing import Optional, List, Dict

DEFAULT_FHIR_BASE = "https://hapi.fhir.org/baseR4"
TIMEOUT = 30.0


def _headers(token: Optional[str] = None) -> Dict:
    h = {"Accept": "application/fhir+json"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def _get(url: str, params: dict = None, token: str = None) -> dict:
    with httpx.Client(timeout=TIMEOUT) as c:
        r = c.get(url, params=params or {}, headers=_headers(token))
        r.raise_for_status()
        return r.json()


def build_patient_context(patient_id: str, base_url: str = DEFAULT_FHIR_BASE,
                           token: Optional[str] = None) -> Dict:
    ctx = {"patient_id": patient_id, "fhir_source": base_url}

    # Demographics
    try:
        pt = _get(f"{base_url}/Patient/{patient_id}", token=token)
        name_obj = (pt.get("name") or [{}])[0]
        given  = " ".join(name_obj.get("given", []))
        family = name_obj.get("family", "")
        ctx["name"]          = f"{given} {family}".strip() or "Unknown"
        ctx["date_of_birth"] = pt.get("birthDate", "Unknown")
        ctx["gender"]        = pt.get("gender", "Unknown")
        for addr in pt.get("address", []):
            ctx["zip_code"] = addr.get("postalCode", "75201")
            ctx["city"]     = addr.get("city", "")
            break
    except Exception as e:
        ctx["name"] = "Unknown"
        ctx["fhir_error"] = str(e)

    # Conditions
    try:
        bundle = _get(f"{base_url}/Condition", {"patient": patient_id, "_count": 30}, token)
        conds  = [e["resource"] for e in bundle.get("entry", [])]
        ctx["conditions"] = [_cond_text(c) for c in conds][:10]
        ctx["active_conditions"] = [
            _cond_text(c) for c in conds
            if c.get("clinicalStatus", {}).get("coding", [{}])[0].get("code") == "active"
        ][:6]
    except Exception:
        ctx["conditions"] = []
        ctx["active_conditions"] = []

    # Medications
    try:
        bundle = _get(f"{base_url}/MedicationRequest", {"patient": patient_id, "_count": 30}, token)
        meds   = [e["resource"] for e in bundle.get("entry", [])]
        ctx["medications"] = [
            {"name": _med_name(m), "status": m.get("status", "unknown"),
             "dosage": (m.get("dosageInstruction") or [{}])[0].get("text", "")}
            for m in meds
        ][:12]
        ctx["active_medications"] = [m for m in ctx["medications"] if m["status"] == "active"]
    except Exception:
        ctx["medications"] = []
        ctx["active_medications"] = []

    # Allergies
    try:
        bundle   = _get(f"{base_url}/AllergyIntolerance", {"patient": patient_id}, token)
        allergies = [e["resource"] for e in bundle.get("entry", [])]
        ctx["allergies"] = [a.get("code", {}).get("text", "Unknown") for a in allergies][:6]
    except Exception:
        ctx["allergies"] = []

    return ctx


def _cond_text(c: dict) -> str:
    code = c.get("code", {})
    if code.get("text"):
        return code["text"]
    for co in code.get("coding", []):
        if co.get("display"):
            return co["display"]
    return "Unknown condition"


def _med_name(m: dict) -> str:
    med = m.get("medicationCodeableConcept", {})
    if med.get("text"):
        return med["text"]
    for co in med.get("coding", []):
        if co.get("display"):
            return co["display"]
    return m.get("medicationReference", {}).get("display", "Unknown medication")
