"""
OptimizerAgent — refines the draft itinerary for efficiency and user preferences.
"""

from __future__ import annotations

from app.agents.base import BaseAgent


class OptimizerAgent(BaseAgent):
    """Optimizes itineraries for realistic timing, preferences, and hidden gems."""

    def __init__(self, **kwargs) -> None:
        instructions = [
            "You are the **Optimizer Agent**. Your task is to refine "
            "the draft itinerary for maximum usability.",
            "",
            "🔹 Instructions:",
            "1. Improve the itinerary for efficiency (minimize unnecessary travel).",
            "2. Adjust based on user preferences (e.g., prefers museums over nightlife).",
            "3. Ensure realistic timings (no overpacked days, allow travel/rest time).",
            "4. Add small enhancements (hidden gems, local experiences) where appropriate.",
            "5. Keep it feasible and enjoyable for a real traveler.",
            "",
            "🔹 Format Requirement:",
            "Output the refined itinerary in the same day-by-day format, preserving:",
            "Final Answer:",
            "Day 1: ...",
            "Day 2: ...",
            "...",
        ]

        super().__init__(
            name="Optimizer Agent",
            instructions=instructions,
            **kwargs,
        )

    def optimize(self, itinerary: str, preferences: str = "") -> str:
        """Optimize *itinerary* according to optional *preferences*."""
        prompt = (
            f"Optimize this itinerary for user preferences: {preferences}\n"
            f"{itinerary}"
        )
        return self.run(prompt)
