import json
import re
from typing import Any

import google.generativeai as genai

from config import settings
from prompts import (
    SYSTEM_PROMPT,
    PLANNER_PROMPT,
    GAP_ANALYSIS_PROMPT,
    SYNTHESIS_PROMPT,
)
from search_tool import SearchTool
from source_manager import deduplicate_sources, source_context


class ResearchAgent:
    """LLM-driven research agent that explicitly uses a web-search tool."""

    def __init__(self) -> None:
        if not settings.gemini_api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is missing. Add it to your .env file or Streamlit secrets."
            )

        genai.configure(api_key=settings.gemini_api_key)

        # System instruction belongs here for google-generativeai.
        self.client = genai.GenerativeModel(
            model_name=settings.gemini_model,
            system_instruction=SYSTEM_PROMPT,
        )

        self.search_tool = SearchTool()

    def _json_call(self, prompt: str) -> dict[str, Any]:
        response = self.client.generate_content(
            contents=[
                {
                    "role": "user",
                    "parts": [{"text": prompt}],
                }
            ],
        )

        text = response.text.strip()

        # Handle accidental markdown fences.
        text = re.sub(r"^```json\s*", "", text)
        text = re.sub(r"\s*```$", "", text)

        return json.loads(text)

    def create_plan(self, question: str) -> dict[str, Any]:
        return self._json_call(
            f"{PLANNER_PROMPT}\n\nUSER QUESTION:\n{question}"
        )

    def analyze_gaps(
        self,
        question: str,
        sources: list[dict],
    ) -> dict[str, Any]:
        prompt = (
            f"{GAP_ANALYSIS_PROMPT}\n\n"
            f"USER QUESTION:\n{question}\n\n"
            f"CURRENT SOURCES:\n{source_context(sources)}"
        )

        return self._json_call(prompt)

    def synthesize(
        self,
        question: str,
        sources: list[dict],
    ) -> str:
        prompt = (
            f"{SYNTHESIS_PROMPT}\n\n"
            f"USER QUESTION:\n{question}\n\n"
            f"EVIDENCE:\n{source_context(sources)}"
        )

        response = self.client.generate_content(
            contents=[
                {
                    "role": "user",
                    "parts": [{"text": prompt}],
                }
            ],
        )

        return response.text.strip()

    def research(self, question: str) -> dict[str, Any]:
        question = question.strip()

        if len(question) < 10:
            raise ValueError("Please enter a meaningful research question.")

        plan = self.create_plan(question)

        queries = plan.get("queries", [])[
            : settings.max_queries_per_round
        ]

        raw_sources: list[dict] = []
        trace: list[dict] = []

        for round_number in range(
            1,
            settings.max_research_rounds + 1,
        ):
            round_queries = queries[
                : settings.max_queries_per_round
            ]

            for query in round_queries:
                results = self.search_tool.search(query)

                raw_sources.extend(results)

                trace.append(
                    {
                        "round": round_number,
                        "query": query,
                        "results": len(results),
                    }
                )

            sources = deduplicate_sources(raw_sources)

            if round_number >= settings.max_research_rounds:
                break

            gap = self.analyze_gaps(
                question,
                sources,
            )

            if not gap.get("need_more_search"):
                break

            queries = gap.get("queries", [])[
                : settings.max_queries_per_round
            ]

            if not queries:
                break

        sources = deduplicate_sources(raw_sources)

        if not sources:
            raise RuntimeError(
                "The search tool returned no usable sources."
            )

        report = self.synthesize(
            question,
            sources,
        )

        report = self._validate_citations(
            report,
            sources,
        )

        return {
            "question": question,
            "research_goal": plan.get("research_goal", ""),
            "focus_areas": plan.get("focus_areas", []),
            "report": report,
            "sources": sources,
            "trace": trace,
        }

    @staticmethod
    def _validate_citations(
        report: str,
        sources: list[dict],
    ) -> str:
        valid_ids = {s["id"] for s in sources}

        def replace_invalid(match: re.Match) -> str:
            citation = match.group(1)

            return (
                f"[{citation}]"
                if citation in valid_ids
                else ""
            )

        return re.sub(
            r"\[(S\d+)\]",
            replace_invalid,
            report,
        )