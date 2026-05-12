# agents/base_agent.py
"""
Base Groq Agent — all specialist agents inherit from this.
Uses llama-3.3-70b-versatile via Groq's ultra-fast inference API.
Free tier: 30 requests/minute, 14,400 requests/day.
"""
import os
import time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

MODEL = "llama-3.3-70b-versatile"


class BaseAgent:
    """Base class for all discharge planning specialist agents."""

    def __init__(self, system_prompt: str = "You are a helpful healthcare AI assistant."):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found. Add it to your .env file.")
        self.client        = Groq(api_key=api_key)
        self.system_prompt = system_prompt

    def run(self, user_prompt: str, max_tokens: int = 1500, retries: int = 3) -> str:
        """Call Groq LLM and return the text response."""
        for attempt in range(retries):
            try:
                response = self.client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {"role": "system",  "content": self.system_prompt},
                        {"role": "user",    "content": user_prompt},
                    ],
                    max_tokens=max_tokens,
                    temperature=0.3,
                )
                return response.choices[0].message.content
            except Exception as e:
                err = str(e)
                if attempt < retries - 1:
                    wait = 6 * (attempt + 1)
                    time.sleep(wait)
                else:
                    return f"[Agent error: {err}]"
        return "[Agent failed to respond]"
