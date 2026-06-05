"""LLM-based paper enricher: generates summaries and canonical tags.

Uses the existing LLMPort interface so it is provider-agnostic.
A dedicated enrichment model (LLM_ENRICHMENT_MODEL) is used instead of the
chat model, allowing a smaller/faster model for this batch workload.
"""

from __future__ import annotations

import logging

from pydantic import BaseModel, Field
from thefuzz import process as fuzz_process  # type: ignore[import-untyped]

from app.llm.port import LLMPort
from app.scraper.interfaces import LLMEnricher
from app.scraper.tags import CANONICAL_TAGS

_logger = logging.getLogger(__name__)

# Fuzzy-match threshold: a returned tag must have this similarity to a
# canonical tag to be accepted (0-100 scale).
_FUZZY_THRESHOLD = 80


class PaperTagSelection(BaseModel):
    tags: list[str] = Field(default_factory=list, min_length=0, max_length=5)


class PaperSummaryOutput(BaseModel):
    summary: str = Field(min_length=1, max_length=1800)


class LLMPaperEnricher(LLMEnricher):
    """Generates a 2-3 sentence summary and 2-5 canonical tags for a paper.

    The tag generation uses a closed-vocabulary prompt to keep tags consistent
    across the corpus.  Raw LLM output is parsed, then fuzzy-matched against
    the canonical tag set so minor phrasing variations are normalised.
    """

    def __init__(self, llm_client: LLMPort, model_name: str) -> None:
        self._llm = llm_client
        self._model = model_name

    async def summarize(self, title: str, abstract: str) -> str:
        prompt = (
            "Summarize this research paper in 2-3 sentences for a graduate student. "
            "Focus on the main contribution and methodology. "
            'Be concise and avoid jargon where possible. Return ONLY a valid JSON object like {"summary": "..."}.\n\n'
            f"Title: {title}\n\nAbstract: {abstract}"
        )
        try:
            result = await self._llm.chat_structured(
                self._model,
                [{"role": "user", "content": prompt}],
                output_schema=PaperSummaryOutput,
                options={"temperature": 0.3, "num_predict": 250},
            )
            return result.summary.strip()
        except Exception as exc:
            _logger.warning("LLM summarize failed for %r: %s", title[:60], exc)
            return ""

    async def generate_tags(self, title: str, abstract: str) -> list[str]:
        tag_list = ", ".join(f'"{t}"' for t in sorted(CANONICAL_TAGS))
        prompt = (
            "Given this research paper, select 2 to 5 topic tags from the list below. "
            'Return ONLY a valid JSON object like {"tags": ["machine learning", "optimization"]} — no explanation, no markdown. '
            f"Available tags: [{tag_list}]\n\n"
            f"Title: {title}\n\nAbstract: {abstract}"
        )
        try:
            result = await self._llm.chat_structured(
                self._model,
                [{"role": "user", "content": prompt}],
                output_schema=PaperTagSelection,
                options={"temperature": 0.1, "num_predict": 150},
            )
        except Exception as exc:
            _logger.warning("LLM tag generation failed for %r: %s", title[:60], exc)
            return []

        return self._normalize(result.tags, title)

    def _normalize(self, tags: list[str], title: str) -> list[str]:
        normalized: list[str] = []
        for tag in tags:
            tag_lower = tag.strip().lower()
            if tag_lower in CANONICAL_TAGS:
                normalized.append(tag_lower)
                continue
            # Fuzzy match against the canonical set
            match = fuzz_process.extractOne(tag_lower, CANONICAL_TAGS)
            if match and match[1] >= _FUZZY_THRESHOLD:
                normalized.append(match[0])
            else:
                _logger.debug("Unrecognized tag discarded: %r (best match: %s)", tag, match)

        # Deduplicate while preserving order
        seen: set[str] = set()
        result: list[str] = []
        for t in normalized:
            if t not in seen:
                seen.add(t)
                result.append(t)
        return result
