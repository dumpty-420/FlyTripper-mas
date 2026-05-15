"""
ReactiveAgent — conversational ReAct (Reason + Act) agent with tools.

Uses LangChain's ``initialize_agent`` with DuckDuckGo search, Wikipedia,
a calculator, and a date/time tool.  Maintains conversation memory within
a single session.
"""

from __future__ import annotations

from langchain_classic.agents import initialize_agent, AgentType
from langchain_classic.memory import ConversationBufferMemory

from app.config import get_llm
from app.tools.search import get_ddg_search_tool
from app.tools.calculator import get_calculator_tool
from app.tools.datetime_tool import get_datetime_tool
from app.tools.wikipedia_tool import get_wikipedia_tool


class ReactiveAgent:
    """
    Conversational ReAct agent that reasons step-by-step and can
    search the web, look up Wikipedia, do math, and tell the time.
    """

    def __init__(self, verbose: bool = True) -> None:
        self.name = "Reactive Agent"
        self.llm = get_llm()

        self.tools = [
            get_ddg_search_tool(),
            get_wikipedia_tool(),
            get_calculator_tool(),
            get_datetime_tool(),
        ]

        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
        )

        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=verbose,
            handle_parsing_errors=True,
            max_iterations=5,
        )

    def run(self, message: str) -> str:
        """Send *message* to the agent and return the response."""
        return self.agent.run(message)

    def reset_memory(self) -> None:
        """Clear conversation history."""
        self.memory.clear()

    def __repr__(self) -> str:
        return f"<ReactiveAgent tools={[t.name for t in self.tools]}>"
