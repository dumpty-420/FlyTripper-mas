"""Wikipedia lookup tool."""

from langchain_classic.agents import Tool
from langchain_community.utilities import WikipediaAPIWrapper


def get_wikipedia_tool(
    top_k_results: int = 2,
    doc_content_chars_max: int = 1000,
) -> Tool:
    """Return a LangChain Tool wrapping Wikipedia search."""
    wiki = WikipediaAPIWrapper(
        top_k_results=top_k_results,
        doc_content_chars_max=doc_content_chars_max,
    )
    return Tool(
        name="Wikipedia",
        func=wiki.run,
        description=(
            "Look up factual information on Wikipedia. "
            "Best for historical facts, science, geography, and people. "
            "Input should be a topic name."
        ),
    )
