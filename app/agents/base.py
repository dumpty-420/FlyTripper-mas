"""
BaseAgent — abstract foundation for all specialized agents.

Every agent has a *name*, a list of *instructions*, optional *tools*,
and a ``run(message)`` method that invokes the LLM.
"""

from __future__ import annotations

from typing import Any

from langchain_google_genai import ChatGoogleGenerativeAI

from app.config import get_llm


class BaseAgent:
    """Lightweight agent that sends a structured prompt to a Gemini LLM."""

    def __init__(
        self,
        name: str,
        instructions: list[str] | None = None,
        tools: list[dict[str, Any]] | None = None,
        llm: ChatGoogleGenerativeAI | None = None,
    ) -> None:
        self.name = name
        self.instructions = instructions or []
        self.tools = tools or []
        self.llm = llm or get_llm()

    # ── Core execution ───────────────────────────────────────────────
    def run(self, message: str, **kwargs: Any) -> str:
        """Build a prompt from instructions + tools + message, then invoke."""
        parts: list[str] = []

        # System instructions
        if self.instructions:
            parts.append("\n".join(self.instructions))

        # Tool descriptions (simple text injection — the LLM doesn't
        # actually call tools here; tool calling is done by the
        # orchestrator or by LangChain-based agents like ReactiveAgent)
        if self.tools:
            tool_block = "You have access to these tools:\n"
            for tool in self.tools:
                tool_block += f"- {tool['name']}: {tool['description']}\n"
            parts.append(tool_block)

        parts.append(f"\nMessage:\n{message}")

        full_prompt = "\n".join(parts)
        response = self.llm.invoke(full_prompt)
        return response.content

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name={self.name!r}>"
