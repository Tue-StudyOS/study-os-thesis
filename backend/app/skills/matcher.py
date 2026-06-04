"""Module matching: map a student course to a handbook entry.

Cascade order (stops at first result meeting its confidence threshold):
  1. Exact module code match          confidence = 1.0
  2. Normalized title exact match     confidence = 0.95
  3. Fuzzy title match (rapidfuzz)    confidence = 0.70-0.90
  4. Semantic match (embedding cos.)  confidence = 0.50-0.80
"""

from __future__ import annotations

import logging
import re
import unicodedata
from dataclasses import dataclass

from app.config import Settings
from app.llm.port import LLMPort
from app.models.handbook import ModuleHandbookEntry
from app.models.student import StudentCourse

_logger = logging.getLogger(__name__)


@dataclass
class ModuleMatch:
    handbook_entry: ModuleHandbookEntry
    method: str        # "exact_code" | "title_exact" | "title_fuzzy" | "semantic"
    confidence: float  # 0.0-1.0


def _normalize_title(title: str) -> str:
    """Lowercase, transliterate German umlauts, strip module codes and extra whitespace."""
    t = title.lower().strip()
    # Transliterate umlauts
    replacements = [("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")]
    for de, en in replacements:
        t = t.replace(de, en)
    # Normalize unicode (e.g. accents)
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode("ascii")
    # Strip parenthetical module codes like "(IN0001)"
    t = re.sub(r"\s*\([^)]*\)\s*", " ", t)
    # Strip Roman numerals at end (I, II, III, IV, V)
    t = re.sub(r"\s+(?:i{1,3}|iv|v|vi{1,3}|ix|x)\s*$", "", t)
    # Collapse whitespace
    return re.sub(r"\s+", " ", t).strip()


class CascadeModuleMatcher:
    """Match student courses to handbook entries using a cascade of strategies."""

    def __init__(
        self,
        embed_client: LLMPort,
        settings: Settings,
        min_confidence: float = 0.5,
    ) -> None:
        self._embed = embed_client
        self._settings = settings
        self._min_confidence = min_confidence
        # Cache of (normalized course name, entry.id) -> best match for the run
        self._match_cache: dict[str, ModuleMatch | None] = {}

    async def match(
        self,
        course: StudentCourse,
        handbook_entries: list[ModuleHandbookEntry],
    ) -> list[ModuleMatch]:
        """Return a list of ModuleMatch sorted by confidence descending.

        Only matches above ``min_confidence`` are returned.
        """
        normalized_name = _normalize_title(course.course_name)

        if normalized_name in self._match_cache:
            cached = self._match_cache[normalized_name]
            return [cached] if cached else []

        best = await self._find_best(course, normalized_name, handbook_entries)
        self._match_cache[normalized_name] = best
        return [best] if best else []

    # ------------------------------------------------------------------
    # Cascade steps
    # ------------------------------------------------------------------

    async def _find_best(
        self,
        course: StudentCourse,
        normalized_name: str,
        entries: list[ModuleHandbookEntry],
    ) -> ModuleMatch | None:
        # Step 1: exact module code
        if hasattr(course, "module_code") and course.module_code:  # type: ignore[attr-defined]
            for entry in entries:
                if entry.module_code and entry.module_code.strip().upper() == course.module_code.strip().upper():  # type: ignore[attr-defined]
                    return ModuleMatch(entry, "exact_code", 1.0)

        # Step 2: normalized title exact match
        for entry in entries:
            if _normalize_title(entry.module_title) == normalized_name:
                return ModuleMatch(entry, "title_exact", 0.95)
            if entry.module_title_en and _normalize_title(entry.module_title_en) == normalized_name:
                return ModuleMatch(entry, "title_exact", 0.95)

        # Step 3: fuzzy title match
        best_fuzzy = self._fuzzy_match(normalized_name, entries)
        if best_fuzzy and best_fuzzy.confidence >= self._min_confidence:
            return best_fuzzy

        # Step 4: semantic match
        best_semantic = await self._semantic_match(course.course_name, entries)
        if best_semantic and best_semantic.confidence >= self._min_confidence:
            return best_semantic

        _logger.debug(
            "Matcher: no match for course %r (normalized=%r)", course.course_name, normalized_name
        )
        return None

    def _fuzzy_match(
        self,
        normalized_name: str,
        entries: list[ModuleHandbookEntry],
    ) -> ModuleMatch | None:
        try:
            from rapidfuzz import fuzz
        except ImportError:
            return None

        best_ratio = 0.0
        best_entry: ModuleHandbookEntry | None = None

        for entry in entries:
            norm_de = _normalize_title(entry.module_title)
            ratio_de = fuzz.token_sort_ratio(normalized_name, norm_de) / 100.0

            ratio_en = 0.0
            if entry.module_title_en:
                norm_en = _normalize_title(entry.module_title_en)
                ratio_en = fuzz.token_sort_ratio(normalized_name, norm_en) / 100.0

            ratio = max(ratio_de, ratio_en)
            if ratio > best_ratio:
                best_ratio = ratio
                best_entry = entry

        if best_entry is None or best_ratio < 0.80:
            return None

        # Map [0.80, 1.0] → [0.70, 0.90]
        confidence = 0.70 + (best_ratio - 0.80) * 1.0
        return ModuleMatch(best_entry, "title_fuzzy", min(0.90, confidence))

    async def _semantic_match(
        self,
        course_name: str,
        entries: list[ModuleHandbookEntry],
    ) -> ModuleMatch | None:
        """Embed course name and compare with handbook title embeddings."""
        try:
            course_vec = await self._embed.embed(
                self._settings.ollama_embed_model, course_name
            )
        except Exception as exc:
            _logger.debug("Matcher: embedding failed for %r: %s", course_name, exc)
            return None

        best_sim = 0.0
        best_entry: ModuleHandbookEntry | None = None

        for entry in entries:
            title_text = entry.module_title
            if entry.module_title_en:
                title_text = f"{entry.module_title} / {entry.module_title_en}"
            try:
                entry_vec = await self._embed.embed(
                    self._settings.ollama_embed_model, title_text
                )
            except Exception:
                continue

            sim = _cosine_similarity(course_vec, entry_vec)
            if sim > best_sim:
                best_sim = sim
                best_entry = entry

        if best_entry is None or best_sim < 0.75:
            return None

        # Map [0.75, 1.0] → [0.50, 0.80]
        confidence = 0.50 + (best_sim - 0.75) * 1.2
        return ModuleMatch(best_entry, "semantic", min(0.80, confidence))


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    if len(a) != len(b) or not a:
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)
