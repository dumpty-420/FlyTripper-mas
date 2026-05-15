"""
TravelOrchestrator — coordinates the multi-agent pipeline.

Pipeline:  Researcher → Planner → Optimizer → QA

Each stage feeds its output into the next, producing a verified
day-by-day itinerary plus an ICS calendar file.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from app.agents.researcher import ResearcherAgent
from app.agents.planner import PlannerAgent
from app.agents.optimizer import OptimizerAgent
from app.agents.qa import QAAgent
from app.utils.ics_generator import generate_ics_content, clean_response


@dataclass
class TravelResult:
    """Container for orchestrator output."""

    destination: str
    num_days: int
    raw_itinerary: str
    itinerary: str          # cleaned (Final Answer prefix removed)
    ics_bytes: bytes


class TravelOrchestrator:
    """
    Runs the 4-agent travel planning pipeline and returns a
    ``TravelResult`` with the verified itinerary and ICS file.
    """

    def __init__(
        self,
        on_stage: Callable[[str], None] | None = None,
    ) -> None:
        """
        Parameters
        ----------
        on_stage : callable, optional
            A callback invoked with the current stage name so the UI
            can show progress (e.g. ``st.status``).
        """
        self._on_stage = on_stage or (lambda _stage: None)

        # Lazy-init agents on first run to avoid slow import-time LLM calls
        self._researcher: ResearcherAgent | None = None
        self._planner: PlannerAgent | None = None
        self._optimizer: OptimizerAgent | None = None
        self._qa: QAAgent | None = None

    # ── Private helpers ──────────────────────────────────────────────
    def _init_agents(self) -> None:
        if self._researcher is None:
            self._researcher = ResearcherAgent()
            self._planner = PlannerAgent()
            self._optimizer = OptimizerAgent()
            self._qa = QAAgent()

    def _notify(self, stage: str) -> None:
        self._on_stage(stage)

    # ── Public API ───────────────────────────────────────────────────
    def run(
        self,
        destination: str,
        num_days: int,
        preferences: str = "",
    ) -> TravelResult:
        """Execute the full pipeline and return a ``TravelResult``."""
        self._init_agents()

        # Stage 1 — Research
        self._notify("🔍 Researching destination…")
        research = self._researcher.research(destination, num_days)

        # Stage 2 — Planning
        self._notify("🗓️ Building itinerary…")
        itinerary = self._planner.plan(research, num_days)

        # Stage 3 — Optimization
        self._notify("⚡ Optimizing for preferences…")
        optimized = self._optimizer.optimize(itinerary, preferences)

        # Stage 4 — QA
        self._notify("✅ Running quality checks…")
        verified = self._qa.verify(optimized)

        # Generate ICS
        ics_bytes = generate_ics_content(verified)

        return TravelResult(
            destination=destination,
            num_days=num_days,
            raw_itinerary=verified,
            itinerary=clean_response(verified),
            ics_bytes=ics_bytes,
        )
