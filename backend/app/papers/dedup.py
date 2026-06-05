"""Deduplication service for the scraper pipeline.

Three-tier lookup strategy:
  1. arxiv_id  — most reliable; unique worldwide
  2. doi       — also a canonical identifier
  3. (title_normalized, first_author) — fallback for non-arXiv papers

When a duplicate is found, the service merges any missing fields from the
incoming candidate into the existing DB row (e.g. fills in arxiv_id once
we discover it from arXiv, updates the abstract if we now have a better one).
"""

from __future__ import annotations

import re

from app.models.paper import Paper
from app.papers.domain import PaperCandidate
from app.papers.repository import PaperRepository


class DeduplicationService:
    def __init__(self, paper_repo: PaperRepository) -> None:
        self._repo = paper_repo

    async def find_duplicate(self, candidate: PaperCandidate) -> Paper | None:
        """Return an existing Paper that matches *candidate*, or None."""
        # Tier 1: exact arxiv_id
        if candidate.arxiv_id:
            existing = await self._repo.get_by_arxiv_id(candidate.arxiv_id)
            if existing:
                return existing

        # Tier 2: exact DOI
        if candidate.doi:
            existing = await self._repo.get_by_doi(candidate.doi)
            if existing:
                return existing

        # Tier 3: normalised title + first author
        title_norm = self.normalize_title(candidate.title)
        first_author = candidate.authors[0] if candidate.authors else None
        if first_author:
            existing = await self._repo.get_by_title_author(title_norm, first_author)
            if existing:
                return existing

        return None

    async def merge_metadata(self, existing: Paper, candidate: PaperCandidate) -> Paper:
        """Fill NULL fields on *existing* with data from *candidate* if better."""
        updates: dict[str, object] = {}

        if existing.arxiv_id is None and candidate.arxiv_id:
            updates["arxiv_id"] = candidate.arxiv_id
        if existing.doi is None and candidate.doi:
            updates["doi"] = candidate.doi
        if existing.abstract is None and candidate.abstract:
            updates["abstract"] = candidate.abstract
        if existing.publication_date is None and candidate.publication_date:
            updates["publication_date"] = candidate.publication_date
        if (not existing.authors) and candidate.authors:
            updates["authors"] = candidate.authors

        if updates:
            existing = await self._repo.update(existing, **updates)

        return existing

    @staticmethod
    def normalize_title(title: str) -> str:
        """Lowercase, strip punctuation, collapse whitespace."""
        t = title.lower().strip()
        t = re.sub(r"[^\w\s]", "", t)
        t = re.sub(r"\s+", " ", t)
        return t
