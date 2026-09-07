import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

try:
    import streamlit as st
except ImportError:
    st = None


def get_secret(name: str, default: str = "") -> str:
    """Read a secret from Streamlit Secrets first, then environment variables."""

    # Streamlit Cloud / local Streamlit secrets
    if st is not None:
        try:
            value = st.secrets.get(name)
            if value:
                return str(value)
        except Exception:
            pass

    # .env / system environment
    return os.getenv(name, default)


@dataclass(frozen=True)
class Settings:
    gemini_api_key: str = get_secret("GEMINI_API_KEY")
    gemini_model: str = get_secret(
        "GEMINI_MODEL",
        "gemini-2.0-flash"
    )

    tavily_api_key: str = get_secret("TAVILY_API_KEY")

    max_search_results: int = int(
        get_secret("MAX_SEARCH_RESULTS", "5")
    )

    max_queries_per_round: int = int(
        get_secret("MAX_QUERIES_PER_ROUND", "4")
    )

    max_research_rounds: int = int(
        get_secret("MAX_RESEARCH_ROUNDS", "2")
    )


settings = Settings()
