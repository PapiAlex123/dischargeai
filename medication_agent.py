# agents/medication_agent.py
from agents.base_agent import BaseAgent

SYSTEM = """You are a clinical pharmacist AI expert. Extract all medications from hospital 
discharge notes and explain each one clearly for patients and caregivers.
Use plain English. Be precise about dosing, timing, purpose, and safety warnings."""


class MedicationAgent(BaseAgent):
    def __init__(self):
        super().__init__(system_prompt=SYSTEM)

    def analyze(self, discharge_note: str, fhir_meds: list = None) -> str:
        fhir_ctx = ""
        if fhir_meds:
            names = [m["name"] for m in fhir_meds if m.get("status") == "active"]
            if names:
                fhir_ctx = f"\n\nFHIR Active Medications on file: {', '.join(names)}"

        prompt = f"""Analyze this hospital discharge note and extract ALL medications.

DISCHARGE NOTE:
{discharge_note}
{fhir_ctx}

For EACH medication provide:
💊 **[Medication Name & Dose]**
- ⏰ Schedule: how often and when to take it
- 🎯 Purpose: what it treats (plain language)
- ⚠️ Warnings: key side effects or things to watch
- 🍎 Interactions: food or drug interactions

At the end add a **🔴 HIGH-ALERT MEDICATIONS** section flagging any blood thinners, 
insulin, opioids, heart medications, or diuretics with special handling instructions.

Then add **✅ MEDICATION SAFETY TIPS** — 5 bullet points for safe medication management at home."""

        return self.run(prompt, max_tokens=1800)
