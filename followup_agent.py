# agents/followup_agent.py
from agents.base_agent import BaseAgent

SYSTEM = """You are a care coordination AI specialist. Extract follow-up care instructions 
and turn them into a clear, specific, calendar-style action plan. 
Be precise with timeframes. Think like a care coordinator, not a doctor."""


class FollowupAgent(BaseAgent):
    def __init__(self):
        super().__init__(system_prompt=SYSTEM)

    def analyze(self, discharge_note: str, fhir_conditions: list = None) -> str:
        ctx = ""
        if fhir_conditions:
            ctx = f"\nKnown conditions: {', '.join(fhir_conditions[:5])}"

        prompt = f"""Create a complete follow-up care plan from this discharge note.

DISCHARGE NOTE:
{discharge_note}
{ctx}

## 📅 APPOINTMENT SCHEDULE:
(every follow-up appointment — who, when, why, phone number placeholder)

## 🧪 LABS & TESTS NEEDED:
(specific tests with exact timing — e.g. "BMP in 5 days to check potassium")

## 💪 ACTIVITY INSTRUCTIONS:
(what patient CAN and CANNOT do — with timeframes for when restrictions lift)

## 🍽️ DIET & FLUID INSTRUCTIONS:
(specific restrictions — sodium limits, fluid limits, foods to avoid)

## 🏠 HOME CARE INSTRUCTIONS:
(wound care, equipment, positioning, hygiene)

## 📆 WEEK-BY-WEEK RECOVERY GUIDE:
**Week 1:** what to expect + key tasks
**Week 2:** milestones + what changes
**Week 3-4:** recovery goals
**Month 2+:** long-term management

## ⏰ DO THESE TODAY (first 24 hours home):
(numbered list — 5 most important immediate actions)"""

        return self.run(prompt, max_tokens=1600)
