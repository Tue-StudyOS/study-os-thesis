"""Deduplication service for the scraper pipeline.

Two-tier lookup strategy:
  1. doi       — canonical identifier when available
  2. (title_normalized, first_author) — fallback for papers without DOI

When a duplicate is found, the service merges any missing fields from the
incoming candidate into the existing DB row.
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
        # Tier 1: exact DOI
        if candidate.doi:
            existing = await self._repo.get_by_doi(candidate.doi)
            if existing:
                return existing

        # Tier 2: normalised title + first author.
        # When the candidate has no DOI we must match an existing row even if
        # that row *has* a DOI — otherwise a DOI-less re-scrape of a paper that
        # was first stored with a DOI is treated as new and duplicated. When the
        # candidate has a DOI, restrict to DOI-less existing rows so distinct
        # versions sharing a title+author (different DOIs) are not merged.
        title_norm = self.normalize_title(candidate.title)
        first_author = candidate.authors[0] if candidate.authors else None
        if first_author:
            existing = await self._repo.get_by_title_author(
                title_norm,
                first_author,
                require_null_doi=bool(candidate.doi),
            )
            if existing:
                return existing

        return None

    async def merge_metadata(self, existing: Paper, candidate: PaperCandidate) -> Paper:
        """Fill NULL fields on *existing* with data from *candidate* if better."""
        updates: dict[str, object] = {}

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
