# agents/warning_agent.py
from agents.base_agent import BaseAgent

SYSTEM = """You are an emergency medicine AI specialist focused on patient safety after hospital discharge.
Identify warning signs clearly. Be specific with numbers and thresholds.
Your output can save lives — never be vague."""


class WarningAgent(BaseAgent):
    def __init__(self):
        super().__init__(system_prompt=SYSTEM)

    def analyze(self, discharge_note: str, diagnosis: str = "") -> str:
        diag = f"Primary Diagnosis: {diagnosis}\n" if diagnosis else ""

        prompt = f"""Analyze this discharge note and identify ALL warning signs.

{diag}DISCHARGE NOTE:
{discharge_note}

Organize your response EXACTLY as:

## 🚨 CALL 911 / GO TO ER IMMEDIATELY IF:
(list specific symptoms requiring emergency care — be very specific with numbers)

## 📞 CALL YOUR DOCTOR WITHIN 24 HOURS IF:
(symptoms needing prompt but non-emergency attention)

## 👀 MONITOR DAILY FOR THESE CHANGES:
(gradual changes to watch — trends, not emergencies)

## 📋 DAILY MONITORING CHECKLIST:
(specific measurable things to check each day — weight, BP, O2 sat, glucose, etc.)

## 📅 FIRST WEEK DANGER ZONES:
(when is the patient at highest risk and what to watch for day-by-day)

Use specific thresholds (e.g. "weight gain MORE than 2 lbs overnight" not just "weight gain")."""

        return self.run(prompt, max_tokens=1500)
