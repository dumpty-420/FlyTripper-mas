"""Web search tools — SerpAPI and DuckDuckGo wrappers."""

from langchain_classic.agents import Tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import SerpAPIWrapper

from app.config import SERP_API_KEY


def get_serp_search_tool() -> Tool:
    """Return a SerpAPI-based web search tool (requires SERP_API_KEY)."""
    if not SERP_API_KEY:
        raise EnvironmentError(
            "SERP_API_KEY not found. Add it to your .env file."
        )
    search = SerpAPIWrapper(serpapi_api_key=SERP_API_KEY)
    return Tool(
        name="SearchGoogle",
        func=search.run,
        description=(
            "Search the web for travel activities, hotels, restaurants, "
            "attractions, and current information."
        ),
    )


def get_ddg_search_tool() -> Tool:
    """Return a free DuckDuckGo search tool (no API key needed)."""
    search = DuckDuckGoSearchRun()
    return Tool(
        name="WebSearch",
        func=search.run,
        description=(
            "Search the web for current information, news, or general "
            "queries. Input should be a search query string."
        ),
    )
