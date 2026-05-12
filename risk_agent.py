# agents/risk_agent.py
from agents.base_agent import BaseAgent

SYSTEM = """You are a clinical AI specializing in hospital readmission risk assessment.
Use evidence-based risk factors (LACE index, HOSPITAL score) to estimate 30-day readmission risk.
Always explain your reasoning and give SPECIFIC, actionable interventions.
This is the core AI factor that traditional rule-based software cannot replicate."""


class RiskAgent(BaseAgent):
    def __init__(self):
        super().__init__(system_prompt=SYSTEM)

    def analyze(self, discharge_note: str, patient_context: dict = None) -> str:
        ctx        = patient_context or {}
        conditions = ctx.get("active_conditions", [])
        meds       = ctx.get("active_medications", [])

        fhir_ctx = ""
        if conditions:
            fhir_ctx = f"\nFHIR Conditions: {', '.join(conditions[:5])}"
            fhir_ctx += f"\nActive Medications: {len(meds)} on file"

        prompt = f"""Perform a 30-day hospital readmission risk assessment.

DISCHARGE NOTE:
{discharge_note}
{fhir_ctx}

## 📊 READMISSION RISK ASSESSMENT

### 🎯 RISK LEVEL: [LOW / MEDIUM / HIGH / VERY HIGH]
### 📈 ESTIMATED 30-DAY READMISSION PROBABILITY: [X%]

### 🔴 RISK FACTORS IDENTIFIED:
(list each factor with its contribution to overall risk — be specific)
• **[Factor]** — [why it increases readmission risk]

### 🟢 PROTECTIVE FACTORS:
(factors that REDUCE readmission risk for this patient)

### ⚡ TOP 5 INTERVENTIONS TO REDUCE READMISSION (ordered by impact):
1. [Most impactful — who does it, when, how]
2. ...

### 📞 PROACTIVE OUTREACH SCHEDULE:
(who should call the patient and when — day 1, day 3, day 7, day 14, day 30)

### 🏠 SOCIAL DETERMINANTS OF HEALTH RISKS:
(housing, food security, transportation, social support — flag any concerns from the note)

### 📅 HIGHEST RISK WINDOW:
(when exactly in the first 30 days is this patient at greatest risk — and why)

### 🏆 LACE SCORE ESTIMATE:
L (Length of stay): [estimate] 
A (Acuity of admission): [estimate]
C (Comorbidities): [estimate]
E (ED visits in past 6 months): [estimate]
Total: [X/19] — [interpretation]"""

        return self.run(prompt, max_tokens=1600)
