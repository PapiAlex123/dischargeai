# agents/facility_agent.py
import os, json
from agents.base_agent import BaseAgent

SYSTEM = """You are a healthcare placement specialist AI. Recommend appropriate post-acute 
care facilities based on the patient's clinical needs, insurance, and location.
Always explain WHY each facility matches this specific patient's needs."""

FACILITIES = [
    {"name":"The Plaza at Edgemere",         "type":"SNF",  "city":"Dallas",    "rating":5,"medicare":True, "medicaid":True, "phone":"(214)388-0400","specialties":["Cardiac","Orthopedic","Wound Care","Memory Care"]},
    {"name":"Walnut Place",                  "type":"SNF",  "city":"Dallas",    "rating":4,"medicare":True, "medicaid":True, "phone":"(214)696-2400","specialties":["Memory Care","General Rehab","Long-Term"]},
    {"name":"Baylor Scott & White IRF",      "type":"IRF",  "city":"Dallas",    "rating":5,"medicare":True, "medicaid":False,"phone":"(214)820-3151","specialties":["Stroke","Brain Injury","Orthopedic","Cardiac"]},
    {"name":"Select Specialty Hospital",     "type":"LTACH","city":"Dallas",    "rating":4,"medicare":True, "medicaid":True, "phone":"(214)345-0300","specialties":["Ventilator Weaning","Complex Medical","Wound Care"]},
    {"name":"Encompass Health Rehab Plano",  "type":"IRF",  "city":"Plano",     "rating":5,"medicare":True, "medicaid":False,"phone":"(972)612-9000","specialties":["Hip Fracture","Joint Replacement","Stroke","Cardiac"]},
    {"name":"Carrollton Springs SNF",        "type":"SNF",  "city":"Carrollton","rating":4,"medicare":True, "medicaid":True, "phone":"(972)395-1400","specialties":["Cardiac Rehab","Orthopedic","Short-Term Rehab"]},
    {"name":"LHC Home Health Dallas",        "type":"HHA",  "city":"Dallas",    "rating":5,"medicare":True, "medicaid":True, "phone":"(214)369-2699","specialties":["Wound Care","IV Therapy","PT/OT","Cardiac"]},
    {"name":"Amedisys Home Health Dallas",   "type":"HHA",  "city":"Dallas",    "rating":4,"medicare":True, "medicaid":True, "phone":"(214)630-0900","specialties":["Cardiac","Post-Surgical","PT/OT","Diabetes"]},
    {"name":"Kindred at Home Dallas",        "type":"HHA",  "city":"Dallas",    "rating":4,"medicare":True, "medicaid":False,"phone":"(214)956-3700","specialties":["COPD","CHF","Diabetes Management","Infusion"]},
    {"name":"Autumn Leaves North Dallas",    "type":"SNF",  "city":"Dallas",    "rating":4,"medicare":True, "medicaid":True, "phone":"(214)696-6000","specialties":["Memory Care","Alzheimer's","Dementia"]},
    {"name":"Signature Healthcare Rowlett",  "type":"SNF",  "city":"Rowlett",   "rating":4,"medicare":True, "medicaid":True, "phone":"(972)475-5900","specialties":["Short-Term Rehab","Cardiac","Orthopedic"]},
]


class FacilityAgent(BaseAgent):
    def __init__(self):
        super().__init__(system_prompt=SYSTEM)
        data_path = os.path.join(os.path.dirname(__file__), "..", "data", "dallas_snf.json")
        try:
            with open(data_path) as f:
                self.facilities = json.load(f)
        except Exception:
            self.facilities = FACILITIES

    def analyze(self, discharge_note: str, patient_context: dict = None) -> str:
        ctx       = patient_context or {}
        zip_code  = ctx.get("zip_code", "75201")
        city      = ctx.get("city", "Dallas")
        conditions = ctx.get("active_conditions", [])

        fac_list = "\n".join([
            f"• {f['name']} | {f['type']} | {'⭐'*f['rating']} | "
            f"Medicare:{'✓' if f['medicare'] else '✗'} Medicaid:{'✓' if f['medicaid'] else '✗'} | "
            f"Tel:{f.get('phone','N/A')} | Specialties: {', '.join(f['specialties'])}"
            for f in self.facilities
        ])

        prompt = f"""A patient is being discharged and needs post-acute care placement.

DISCHARGE NOTE:
{discharge_note}

PATIENT LOCATION: {city}, ZIP {zip_code}
KNOWN CONDITIONS: {', '.join(conditions) if conditions else 'See discharge note'}

AVAILABLE FACILITIES:
{fac_list}

## 🏥 WHAT LEVEL OF CARE DOES THIS PATIENT NEED?
(SNF / IRF / HHA / LTACH — explain the clinical reasoning)

## 🥇 TOP 3 RECOMMENDED FACILITIES:
For each:
**[Facility Name]** — [Type] — [Star Rating]
- ✅ Why it's right for THIS patient specifically
- 📋 Medicare/Medicaid status + phone number
- ❓ What to ask when you call

## 📞 HOW TO ARRANGE PLACEMENT — STEP BY STEP:
(who calls, what to say, documents needed, typical timeline)

## ⏰ PLACEMENT TIMELINE:
(realistic expectations: how long placement takes, what delays are common)

## 🔗 VERIFY ON CMS CARE COMPARE:
https://www.medicare.gov/care-compare/ (paste facility name to check real-time ratings)"""

        return self.run(prompt, max_tokens=1600)
