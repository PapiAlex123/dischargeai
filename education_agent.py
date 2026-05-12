# agents/education_agent.py
from agents.base_agent import BaseAgent

SYSTEM = """You are a patient education specialist. Translate clinical discharge instructions 
into warm, simple, caregiver-friendly language at a 6th-grade reading level.
Include teach-back questions to verify understanding. Be compassionate and supportive."""


class EducationAgent(BaseAgent):
    def __init__(self):
        super().__init__(system_prompt=SYSTEM)

    def analyze(self, discharge_note: str, patient_name: str = "your loved one") -> str:
        prompt = f"""Create a complete caregiver education guide for the family of {patient_name}.

DISCHARGE NOTE:
{discharge_note}

## 👋 WELCOME HOME — WHAT HAPPENED & WHAT TO EXPECT
(2 paragraphs — warm, plain language explanation of what happened and what recovery looks like)

## 🏠 BEFORE THEY ARRIVE HOME — CHECKLIST:
(what to prepare: remove rugs, set up bedroom, get medications, arrange transport, etc.)

## 🗓️ SAMPLE DAILY ROUTINE:
**Morning:** (specific tasks)
**Afternoon:** (specific tasks)  
**Evening:** (specific tasks)
**Bedtime:** (specific tasks)

## 💬 HOW TO COMMUNICATE & HELP:
(practical tips for supporting the patient emotionally and physically)

## 🧘 CAREGIVER SELF-CARE REMINDER:
(brief — caregiver burnout is real, here's how to avoid it)

## ❓ TEACH-BACK VERIFICATION QUESTIONS:
(5 questions the caregiver must be able to answer before leaving the hospital)
Q1: When should you call 911?
Q2: How often does [patient] take their medications?
Q3: What are the daily weight/monitoring goals?
Q4: When is the first follow-up appointment?
Q5: What is the most important dietary restriction?

## 📞 IMPORTANT PHONE NUMBERS TEMPLATE:
(template with slots for: PCP, specialist, pharmacy, facility, emergency contact)"""

        return self.run(prompt, max_tokens=1600)
