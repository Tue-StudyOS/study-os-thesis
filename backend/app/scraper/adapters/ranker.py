"""Recency-based paper ranker using exponential decay."""

from __future__ import annotations

import math
from datetime import datetime, timezone

from app.papers.domain import EnrichedPaper
from app.scraper.interfaces import PaperRanker


class RecencyPaperRanker(PaperRanker):
    """Scores papers by how recently they were published.

    Uses exponential decay:  score = exp(-ln(2) / half_life * age_days)

    With half_life_days=180:
        today     → 1.000
        3 months  → 0.707
        6 months  → 0.500
        1 year    → 0.250
        2 years   → 0.063

    relevance_score mirrors recency_score in the MVP.
    Future: add citation count and embedding similarity to chair description.
    """

    def __init__(self, half_life_days: int = 180) -> None:
        self._decay = math.log(2) / half_life_days

    def compute_recency_score(self, publication_date: datetime | None) -> float:
        if publication_date is None:
            return 0.1  # unknown date → low but non-zero score

        # Normalise to UTC-aware for safe subtraction
        if publication_date.tzinfo is None:
            publication_date = publication_date.replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)
        age_days = max((now - publication_date).days, 0)
        return math.exp(-self._decay * age_days)

    def compute_relevance_score(self, paper: EnrichedPaper) -> float:
        # MVP: relevance equals recency.
        # Extension points: += 0.3 * citation_score + 0.2 * chair_similarity
        return paper.recency_score
