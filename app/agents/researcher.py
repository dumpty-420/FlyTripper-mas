"""
ResearcherAgent — gathers travel information from the web.

This agent uses the search tool to find attractions, hotels,
restaurants, and transport tips for a given destination.
"""

from __future__ import annotations

from app.agents.base import BaseAgent
from app.tools.search import get_serp_search_tool


class ResearcherAgent(BaseAgent):
    """Searches the web and returns a structured research summary."""

    def __init__(self, **kwargs) -> None:
        search_tool = get_serp_search_tool()
        tool_desc = {
            "name": search_tool.name,
            "description": search_tool.description,
        }

        instructions = [
            "You are the **Researcher Agent** for a travel planning system.",
            "Your goal is to collect **reliable, up-to-date travel information** for the user's trip.",
            "",
            "You have access to the following tool(s):",
            "- Search tool: find attractions, hotels, restaurants, transportation options, and local insights.",
            "",
            "🔹 Instructions:",
            "1. Use the search tool where necessary (do not invent information).",
            "2. Focus on high-quality, verified results (official websites, top review sources, reliable blogs).",
            "3. Summarize findings in a structured way:",
            "   - Attractions (with highlights)",
            "   - Hotels/Accommodations",
            "   - Restaurants/Food options",
            "   - Travel/Transport tips",
            "4. Keep descriptions concise but informative (2–4 sentences per item).",
            "5. Avoid adding your own opinions; base all output on retrieved sources.",
            "",
            "Output must be a clear **research summary**. Do NOT create an itinerary.",
        ]

        super().__init__(
            name="Researcher Agent",
            instructions=instructions,
            tools=[tool_desc],
            **kwargs,
        )

    def research(self, destination: str, num_days: int) -> str:
        """Run a research query for *destination* over *num_days*."""
        prompt = (
            f"Research {destination} for a {num_days}-day trip. "
            "Include attractions, hotels, restaurants, and transport tips."
        )
        return self.run(prompt)
