# agents/insurance_agent.py
from agents.base_agent import BaseAgent

SYSTEM = """You are a healthcare insurance specialist AI. Explain insurance coverage in plain 
language. Be specific with dollar amounts. Always tell patients what they need to DO to protect 
their coverage. Never use insurance jargon without explaining it."""

MEDICARE_RULES = """
SKILLED NURSING (SNF): Days 1-20 = $0 copay | Days 21-100 = ~$200/day copay | Day 101+ = NOT covered
  Requires: 3-night qualifying inpatient hospital stay | Prior authorization required
INPATIENT REHAB (IRF): Medicare Part A covers 100% after ~$1,632 deductible/benefit period
  Requires: 3-night hospital stay | Must tolerate 3+ hours therapy/day | Prior auth required
HOME HEALTH (HHA): Medicare covers 100% | Patient must be homebound | No prior auth needed
  Requires: Physician order | Part-time/intermittent skilled services only
OUTPATIENT THERAPY: Medicare Part B covers 80% | Patient pays 20% coinsurance after deductible
LONG-TERM CARE: Medicare does NOT cover custodial care | Medicaid or private pay required
"""


class InsuranceAgent(BaseAgent):
    def __init__(self):
        super().__init__(system_prompt=SYSTEM)

    def analyze(self, discharge_note: str, patient_context: dict = None,
                insurance_type: str = "Medicare") -> str:
        conditions = (patient_context or {}).get("active_conditions", [])

        prompt = f"""Explain insurance coverage for this patient's discharge needs.

DISCHARGE NOTE:
{discharge_note}

PATIENT INSURANCE: {insurance_type}
KNOWN CONDITIONS: {', '.join(conditions) if conditions else 'See discharge note'}

MEDICARE REFERENCE RULES:
{MEDICARE_RULES}

## 💳 WHAT {insurance_type.upper()} COVERS FOR THIS PATIENT:
(be specific about what service is needed and exactly what is covered)

## 💰 WHAT THE PATIENT WILL PAY:
(specific dollar amounts — no vague language)

## ✅ PRE-AUTHORIZATION CHECKLIST:
(step-by-step actions to complete BEFORE discharge)
□ Step 1...
□ Step 2...

## 📋 DOCUMENTS TO GATHER:
(insurance cards, referrals, auth numbers, etc.)

## ❌ COVERAGE GAPS TO KNOW:
(honest about what is NOT covered)

## 🔍 CALL YOUR INSURANCE — ASK THESE 5 QUESTIONS:
Q1: ...
Q2: ...

## 💡 3 WAYS TO LOWER YOUR OUT-OF-POCKET COSTS:"""

        return self.run(prompt, max_tokens=1400)
