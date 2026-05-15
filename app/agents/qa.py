"""
QAAgent — validates factual accuracy, consistency, and formatting
of the final itinerary.
"""

from __future__ import annotations

from app.agents.base import BaseAgent


class QAAgent(BaseAgent):
    """Quality-assurance pass on a travel itinerary."""

    def __init__(self, **kwargs) -> None:
        instructions = [
            "You are the **Quality Assurance Agent** for travel itineraries.",
            "Your responsibility is to **validate and correct** the final plan "
            "before presenting it to the user.",
            "",
            "🔹 Instructions:",
            "1. Check factual accuracy: remove hallucinations, unrealistic claims, or non-existent places.",
            "2. Verify consistency: ensure attractions match the destination and sequence makes sense.",
            "3. Ensure clarity: rewrite vague items (e.g., 'visit museum' → 'Visit the Louvre Museum').",
            "4. Confirm that each day is feasible (not overloaded, includes travel time).",
            "5. Keep output user-friendly and safe (avoid unsafe areas or misleading advice).",
            "",
            "🔹 Format Requirement:",
            "Output the final verified itinerary, preserving the format:",
            "Final Answer:",
            "Day 1: ...",
            "Day 2: ...",
            "...",
        ]

        super().__init__(
            name="QA Agent",
            instructions=instructions,
            **kwargs,
        )

    def verify(self, itinerary: str) -> str:
        """Validate and correct the *itinerary*."""
        prompt = f"Verify and correct this itinerary:\n{itinerary}"
        return self.run(prompt)
