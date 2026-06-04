"""Skill taxonomy: normalize raw tag strings to canonical SkillTag entries.

Resolution order:
  1. Exact name match in skill_tags.name
  2. Alias match via JSONB containment on skill_tags.aliases
  3. Fuzzy match (token sort ratio >= 0.90 via rapidfuzz) against all tag names
  4. No match → create a new SkillTag row

The taxonomy grows organically as new module entries are processed; the seed
data in the migration covers the most common CS/engineering skills.
"""

from __future__ import annotations

import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.skill import SkillTag

_logger = logging.getLogger(__name__)


def _normalize_raw(tag: str) -> str:
    """Lowercase, strip surrounding whitespace."""
    return tag.lower().strip()


class SkillTaxonomy:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        # In-process cache: canonical name -> SkillTag.  Valid only for the
        # lifetime of one Celery task (a fresh session is created per task).
        self._cache: dict[str, SkillTag] = {}

    async def normalize(self, raw_tag: str) -> str:
        """Return the canonical lowercase name for *raw_tag*."""
        lower = _normalize_raw(raw_tag)
        tag = await self._resolve(lower)
        return tag.name if tag else lower

    async def get_or_create(self, raw_tag: str, category: str | None = None) -> SkillTag:
        """Resolve *raw_tag* to an existing SkillTag or create a new one."""
        lower = _normalize_raw(raw_tag)
        tag = await self._resolve(lower)
        if tag:
            return tag

        # Create a new tag.
        new_tag = SkillTag(name=lower, category=category, aliases=[lower] if lower != raw_tag.lower() else [])
        self._session.add(new_tag)
        await self._session.flush()
        self._cache[lower] = new_tag
        _logger.debug("SkillTaxonomy: created new tag %r (category=%s)", lower, category)
        return new_tag

    # ------------------------------------------------------------------
    # Internal resolution helpers
    # ------------------------------------------------------------------

    async def _resolve(self, lower: str) -> SkillTag | None:
        # 1. Cache hit
        if lower in self._cache:
            return self._cache[lower]

        # 2. Exact name match
        tag = await self._find_by_name(lower)
        if tag:
            self._cache[lower] = tag
            return tag

        # 3. Alias containment match (PostgreSQL JSONB @> operator via cast)
        tag = await self._find_by_alias(lower)
        if tag:
            self._cache[lower] = tag
            return tag

        # 4. Fuzzy match
        tag = await self._find_by_fuzzy(lower)
        if tag:
            self._cache[lower] = tag
            return tag

        return None

    async def _find_by_name(self, name: str) -> SkillTag | None:
        return await self._session.scalar(
            select(SkillTag).where(SkillTag.name == name).limit(1)
        )

    async def _find_by_alias(self, alias: str) -> SkillTag | None:
        from sqlalchemy import type_coerce
        from sqlalchemy.dialects.postgresql import JSONB

        # aliases @> '["<alias>"]'  — JSONB containment
        return await self._session.scalar(
            select(SkillTag)
            .where(
                SkillTag.aliases.cast(JSONB).contains(  # type: ignore[union-attr]
                    type_coerce([alias], JSONB)
                )
            )
            .limit(1)
        )

    async def _find_by_fuzzy(self, lower: str, threshold: float = 0.90) -> SkillTag | None:
        try:
            from rapidfuzz import fuzz, process
        except ImportError:
            return None

        # Load all tag names (the taxonomy is bounded to ~200-500 entries).
        all_tags_result = await self._session.scalars(select(SkillTag))
        all_tags = list(all_tags_result.all())
        if not all_tags:
            return None

        names = [t.name for t in all_tags]
        match = process.extractOne(
            lower,
            names,
            scorer=fuzz.token_sort_ratio,
            score_cutoff=threshold * 100,
        )
        if match:
            _matched_name, _score, idx = match
            return all_tags[idx]

        return None
