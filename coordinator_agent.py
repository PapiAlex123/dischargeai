# agents/coordinator_agent.py
"""
Master Discharge Planning Coordinator
Orchestrates 7 specialist agents and synthesizes a final Discharge Intelligence Plan.
"""
import os, time
from groq import Groq
from dotenv import load_dotenv
from typing import Optional, Callable

from agents.medication_agent  import MedicationAgent
from agents.warning_agent     import WarningAgent
from agents.followup_agent    import FollowupAgent
from agents.education_agent   import EducationAgent
from agents.facility_agent    import FacilityAgent
from agents.insurance_agent   import InsuranceAgent
from agents.risk_agent        import RiskAgent

load_dotenv()

SYNTHESIS_SYSTEM = """You are the Chief Discharge Planning AI Coordinator. You receive outputs 
from 7 specialist healthcare AI agents and synthesize them into one comprehensive, actionable 
Discharge Intelligence Plan. Prioritize patient safety above everything. Be concise but complete."""


class DischargePlanningCoordinator:

    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in .env file")
        self.client           = Groq(api_key=api_key)
        self.medication_agent = MedicationAgent()
        self.warning_agent    = WarningAgent()
        self.followup_agent   = FollowupAgent()
        self.education_agent  = EducationAgent()
        self.facility_agent   = FacilityAgent()
        self.insurance_agent  = InsuranceAgent()
        self.risk_agent       = RiskAgent()

    def run(
        self,
        discharge_note: str,
        patient_context: dict  = None,
        insurance_type: str    = "Medicare",
        progress_callback: Optional[Callable[[str, int], None]] = None,
    ) -> dict:
        ctx  = patient_context or {}
        name = ctx.get("name", "the patient")

        def step(label: str, pct: int):
            if progress_callback:
                progress_callback(label, pct)

        results = {}
        t0 = time.time()

        step("💊 Medication Agent — extracting all medications...", 8)
        results["medications"] = self.medication_agent.analyze(
            discharge_note, fhir_meds=ctx.get("active_medications", []))
        time.sleep(4)

        step("🚨 Warning Agent — identifying safety alerts...", 22)
        diag = (ctx.get("active_conditions") or [""])[0]
        results["warnings"] = self.warning_agent.analyze(discharge_note, diagnosis=diag)
        time.sleep(4)

        step("📅 Follow-Up Agent — building recovery schedule...", 36)
        results["followup"] = self.followup_agent.analyze(
            discharge_note, fhir_conditions=ctx.get("active_conditions", []))
        time.sleep(4)

        step("📚 Education Agent — creating caregiver guide...", 50)
        results["education"] = self.education_agent.analyze(discharge_note, patient_name=name)
        time.sleep(4)

        step("🏥 Facility Agent — finding placement options...", 63)
        results["facilities"] = self.facility_agent.analyze(discharge_note, patient_context=ctx)
        time.sleep(4)

        step("💳 Insurance Agent — checking coverage...", 76)
        results["insurance"] = self.insurance_agent.analyze(
            discharge_note, patient_context=ctx, insurance_type=insurance_type)
        time.sleep(4)

        step("📊 Risk Agent — assessing readmission risk...", 88)
        results["risk"] = self.risk_agent.analyze(discharge_note, patient_context=ctx)
        time.sleep(4)

        step("🧠 Coordinator — synthesizing final plan...", 95)
        results["final_plan"] = self._synthesize(discharge_note, ctx, results, name)

        results["metadata"] = {
            "patient_name":     name,
            "patient_id":       ctx.get("patient_id", "Manual input"),
            "dob":              ctx.get("date_of_birth", "N/A"),
            "gender":           ctx.get("gender", "N/A"),
            "insurance":        insurance_type,
            "fhir_source":      ctx.get("fhir_source", "Manual discharge note"),
            "conditions_count": len(ctx.get("conditions", [])),
            "meds_count":       len(ctx.get("medications", [])),
            "agents_run":       7,
            "processing_time":  f"{time.time() - t0:.0f}s",
        }

        step("✅ All agents complete!", 100)
        return results

    def _synthesize(self, note: str, ctx: dict, outputs: dict, name: str) -> str:
        def snip(key, n=600):
            return (outputs.get(key) or "Not available")[:n]

        prompt = f"""Synthesize these 7 specialist agent outputs into a unified Discharge Intelligence Plan for {name}.

[MEDICATIONS] {snip('medications')}
[WARNINGS] {snip('warnings')}
[FOLLOWUP] {snip('followup')}
[EDUCATION] {snip('education', 400)}
[FACILITIES] {snip('facilities', 400)}
[INSURANCE] {snip('insurance', 400)}
[RISK] {snip('risk')}

Create the final plan:

## 🏥 DISCHARGE INTELLIGENCE PLAN — {name.upper()}

### ⚡ EXECUTIVE SUMMARY — TOP 5 PRIORITY ACTIONS:
(The 5 most critical actions in the next 24 hours for the care team)
1. ...

### 🎯 CLINICAL SNAPSHOT:
(Patient, diagnosis, disposition, risk level in 3-4 lines)

### 🚨 SAFETY FLAGS:
(Any red flags, conflicts between agent outputs, or critical items the team must not miss)

### ✅ DISCHARGE READINESS CHECKLIST:
□ Medications reconciled and prescriptions filled
□ Transportation arranged  
□ Receiving facility confirmed and bed secured
□ Insurance prior authorization obtained
□ Patient and caregiver education completed
□ All follow-up appointments scheduled
□ Medical equipment ordered and delivered
□ Emergency contact plan documented

### 📋 CARE TRANSITION SUMMARY FOR RECEIVING TEAM:
(1-paragraph clinical handoff summary)

### 🗓️ 30-DAY MILESTONE CALENDAR:
Day 1-3: ...
Day 4-7: ...
Week 2: ...
Week 3-4: ...
Day 30: ..."""

        try:
            resp = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": SYNTHESIS_SYSTEM},
                    {"role": "user",   "content": prompt},
                ],
                max_tokens=1800,
                temperature=0.2,
            )
            return resp.choices[0].message.content
        except Exception as e:
            return f"[Synthesis error: {e}]\n\nAll individual agent outputs are available in the tabs above."
