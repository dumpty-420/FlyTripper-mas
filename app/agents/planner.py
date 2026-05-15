"""
PlannerAgent — transforms research into a day-by-day itinerary.
"""

from __future__ import annotations

from app.agents.base import BaseAgent


class PlannerAgent(BaseAgent):
    """Creates a structured day-by-day travel plan from research data."""

    def __init__(self, **kwargs) -> None:
        instructions = [
            "You are the **Planner Agent**. Your responsibility is to transform "
            "research results into a clear travel plan.",
            "",
            "🔹 Instructions:",
            "1. Create a day-by-day itinerary for the trip.",
            "2. Each day should include a balance of attractions, food options, and rest time.",
            "3. Ensure logical sequencing (minimize travel time, group nearby spots together).",
            "4. Respect the number of days requested by the user.",
            "5. Do not invent new information — only use the research provided.",
            "6. Ensure each day has a clear theme or highlight (morning, afternoon, evening activities).",
            "7. Write in an engaging but professional tone.",
            "",
            "🔹 Format Requirement:",
            "Wrap the final response in this format:",
            "Final Answer:",
            "Day 1: ...",
            "Day 2: ...",
            "Day 3: ...",
            "...",
            "",
            "Only provide the itinerary, nothing else.",
        ]

        super().__init__(
            name="Planner Agent",
            instructions=instructions,
            **kwargs,
        )

    def plan(self, research: str, num_days: int) -> str:
        """Generate a *num_days*-day itinerary from *research*."""
        prompt = (
            f"Create a {num_days}-day itinerary from this research:\n{research}"
        )
        return self.run(prompt)
