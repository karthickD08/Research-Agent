from typing import Any
from tavily import TavilyClient
from config import settings


class SearchTool:
    """Web-search tool used by the research agent."""

    name = "web_search"

    def __init__(self) -> None:
        if not settings.tavily_api_key:
            raise RuntimeError(
                "TAVILY_API_KEY is missing. Add it to your .env file or Streamlit secrets."
            )
        self.client = TavilyClient(api_key=settings.tavily_api_key)

    def search(self, query: str, max_results: int | None = None) -> list[dict[str, Any]]:
        response = self.client.search(
            query=query,
            search_depth="advanced",
            max_results=max_results or settings.max_search_results,
            include_answer=False,
            include_raw_content=False,
        )

        results = []
        for item in response.get("results", []):
            results.append(
                {
                    "title": item.get("title", "").strip(),
                    "url": item.get("url", "").strip(),
                    "content": item.get("content", "").strip(),
                    "score": float(item.get("score", 0.0) or 0.0),
                }
            )
        return results
