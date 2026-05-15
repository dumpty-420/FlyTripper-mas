"""
Centralized configuration — single source of truth for API keys, model
settings, and shared LLM instances.
"""

import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# ── Load .env once at import time ────────────────────────────────────
load_dotenv()

# ── API keys ─────────────────────────────────────────────────────────
GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
SERP_API_KEY: str = os.getenv("SERP_API_KEY", "")

# ── Model defaults ───────────────────────────────────────────────────
DEFAULT_MODEL = "gemini-2.5-flash"
DEFAULT_TEMPERATURE = 0.3


def get_llm(
    model: str = DEFAULT_MODEL,
    temperature: float = DEFAULT_TEMPERATURE,
    **kwargs,
) -> ChatGoogleGenerativeAI:
    """Return a configured Gemini LLM instance."""
    if not GOOGLE_API_KEY:
        raise EnvironmentError(
            "GOOGLE_API_KEY not found. "
            "Create a .env file with:\n  GOOGLE_API_KEY=your-key-here"
        )
    return ChatGoogleGenerativeAI(
        model=model,
        google_api_key=GOOGLE_API_KEY,
        temperature=temperature,
        **kwargs,
    )
