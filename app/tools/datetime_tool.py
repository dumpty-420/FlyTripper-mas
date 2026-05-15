"""DateTime tool — returns the current date and time."""

from datetime import datetime

from langchain_classic.agents import Tool


def get_current_datetime(_input: str = "") -> str:
    """Return the current date and time as a human-readable string."""
    return datetime.now().strftime("%A, %B %d, %Y  %I:%M %p")


def get_datetime_tool() -> Tool:
    """Return a LangChain Tool wrapping the datetime function."""
    return Tool(
        name="DateTime",
        func=get_current_datetime,
        description="Get the current date and time. No input required.",
    )
