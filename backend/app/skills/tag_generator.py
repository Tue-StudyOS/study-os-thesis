"""LLM-based skill tag generation for module handbook entries.

Tags are generated once per (handbook_entry, llm_prompt_version, content_hash)
and cached in the ``module_skill_mappings`` table.  Subsequent calls for the
same entry are fully served from the DB with no LLM call.
"""

from __future__ import annotations

import hashlib
import json
import logging
from typing import Any

from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import Settings
from app.llm.port import LLMPort
from app.models.handbook import ModuleHandbookEntry, ModuleSkillMapping
from app.models.skill import SkillTag
from app.skills.taxonomy import SkillTaxonomy

_logger = logging.getLogger(__name__)

_PROMPT_VERSION = "v1"

_TAG_GENERATION_PROMPT = """\
Given the following university module, extract 3-8 skill tags that describe
the competencies a student gains by completing it.

Module title: {title}
Description: {description}
Learning outcomes: {learning_outcomes}
Contents: {contents}
Prerequisites: {prerequisites}
ECTS: {ects}

Return a JSON array:
[
  {{"tag": "machine learning", "relevance": 0.9, "category": "theory"}}
]

Rules:
- Tags must be lowercase English canonical names.
- "relevance" is 0.0-1.0: how central this skill is to the module.
- "category" is one of: programming, mathematics, theory, systems, data, engineering, research.
- Prefer specific but not overly narrow tags.
  Good: "machine learning". Bad: "gradient descent for logistic regression".
- Do not include generic academic soft skills (critical thinking, teamwork, etc.).
- Return ONLY the JSON array, no markdown, no explanation.
"""


class _RawTag(BaseModel):
    tag: str = Field(min_length=2, max_length=100)
    relevance: float = Field(ge=0.0, le=1.0)
    category: str = Field(default="other")


def _input_hash(entry: ModuleHandbookEntry) -> str:
    text = " | ".join(
        filter(
            None,
            [
                entry.module_title,
                entry.description,
                entry.learning_outcomes,
                entry.contents,
                entry.prerequisites,
            ],
        )
    )
    return hashlib.sha256(text.encode()).hexdigest()


class LLMSkillTagGenerator:
    """Generate and cache skill mappings for a handbook entry."""

    VALID_CATEGORIES = frozenset(
        ("programming", "mathematics", "theory", "systems", "data", "engineering", "research")
    )

    def __init__(
        self,
        session: AsyncSession,
        llm_client: LLMPort,
        settings: Settings,
        taxonomy: SkillTaxonomy,
    ) -> None:
        self._session = session
        self._llm = llm_client
        self._settings = settings
        self._taxonomy = taxonomy

    async def ensure_mappings(
        self, entry: ModuleHandbookEntry
    ) -> list[ModuleSkillMapping]:
        """Return cached mappings or generate new ones via LLM."""
        # Reload with skill_mappings eagerly loaded
        fresh = await self._session.get(
            ModuleHandbookEntry,
            entry.id,
        )
        if fresh is None:
            return []

        # Refresh skill_mappings relationship
        await self._session.refresh(fresh, ["skill_mappings"])

        if fresh.skill_mappings:
            cached_hash = fresh.skill_mappings[0].llm_input_hash if fresh.skill_mappings else None
            current_hash = _input_hash(entry)
            if cached_hash == current_hash:
                _logger.debug(
                    "TagGenerator: using cached mappings for entry_id=%d", entry.id
                )
                return list(fresh.skill_mappings)
            # Content changed — delete stale mappings and regenerate.
            for m in fresh.skill_mappings:
                await self._session.delete(m)
            await self._session.flush()

        raw_tags = await self._call_llm(entry)
        mappings: list[ModuleSkillMapping] = []
        ih = _input_hash(entry)
        model_name = self._settings.effective_extract_model

        for raw in raw_tags:
            category = raw.category if raw.category in self.VALID_CATEGORIES else "other"
            skill_tag = await self._taxonomy.get_or_create(raw.tag, category)
            mapping = ModuleSkillMapping(
                handbook_entry_id=entry.id,
                skill_tag_id=skill_tag.id,
                relevance=min(1.0, max(0.0, raw.relevance)),
                source="llm_generated",
                llm_prompt_version=_PROMPT_VERSION,
                llm_model=model_name,
                llm_input_hash=ih,
            )
            self._session.add(mapping)
            mappings.append(mapping)

        await self._session.flush()

        # Re-attach skill_tag for callers that need it immediately.
        for m in mappings:
            tag = await self._session.get(SkillTag, m.skill_tag_id)
            m.skill_tag = tag  # type: ignore[assignment]

        return mappings

    async def _call_llm(self, entry: ModuleHandbookEntry, retries: int = 2) -> list[_RawTag]:
        prompt = _TAG_GENERATION_PROMPT.format(
            title=entry.module_title or "",
            description=(entry.description or "")[:800],
            learning_outcomes=(entry.learning_outcomes or "")[:600],
            contents=(entry.contents or "")[:600],
            prerequisites=(entry.prerequisites or "")[:300],
            ects=entry.ects or "unknown",
        )
        for attempt in range(retries + 1):
            try:
                response = await self._llm.chat(
                    model=self._settings.effective_extract_model,
                    messages=[{"role": "user", "content": prompt}],
                    options={"temperature": 0},
                )
                content: str = (response.get("message", {}) or {}).get("content", "") or ""
                content = content.strip()
                if content.startswith("```"):
                    content = content.split("```")[1]
                    if content.startswith("json"):
                        content = content[4:]
                content = content.strip()

                raw_list: Any = json.loads(content)
                if not isinstance(raw_list, list):
                    raw_list = [raw_list]

                return [_RawTag.model_validate(item) for item in raw_list[:10]]
            except Exception as exc:
                _logger.warning(
                    "TagGenerator: attempt %d/%d failed for entry_id=%d: %s",
                    attempt + 1,
                    retries + 1,
                    entry.id,
                    exc,
                )
                if attempt == retries:
                    _logger.error(
                        "TagGenerator: all retries exhausted for entry_id=%d — no tags generated",
                        entry.id,
                    )
                    return []
        return []
