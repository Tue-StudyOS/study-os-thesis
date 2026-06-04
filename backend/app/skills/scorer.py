"""Pure skill scoring functions — no I/O, no LLM calls, no DB access.

Formula for each skill S:

    score(S) = sum_m( W(m) * G(m) * R(m,S) * L(m) * T(m) * C(m) )
               / normalization_divisor

    normalization_divisor = max( sum_m( W(m) * C(m) ), 1.0 )

where m iterates over all completed modules matched to skill S.

Factor definitions:
  W(m): credits_weight  = ects / max_ects_in_transcript
  G(m): grade_factor    = (5.0 - grade) / 4.0  (German scale)
  R(m,S): skill_relevance = module_skill_mappings.relevance
  L(m): level_factor    = bachelor:0.6, master:0.85, phd:1.0, unknown:0.7
  T(m): recency_factor  = max(0.5, 1.0 - 0.05 * years_ago)
  C(m): match_confidence from ModuleMatch

Score is clamped to [0.0, 1.0].
"""

from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date
from typing import Any


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ScoringConfig:
    default_ects: float = 5.0
    default_grade_factor: float = 0.5
    pass_grade_factor: float = 0.6  # "bestanden" — ungraded pass
    level_weights: dict[str, float] = field(
        default_factory=lambda: {
            "bachelor": 0.6,
            "master": 0.85,
            "phd": 1.0,
            "unknown": 0.7,
        }
    )
    recency_decay_per_year: float = 0.05
    recency_floor: float = 0.5
    recency_default: float = 0.75   # when semester_taken is absent
    min_match_confidence: float = 0.5


# ---------------------------------------------------------------------------
# Evidence item (serializable)
# ---------------------------------------------------------------------------


@dataclass
class EvidenceItem:
    student_course_id: int
    handbook_entry_id: int | None
    match_method: str
    match_confidence: float
    module_skill_relevance: float
    credits_used: float | None
    grade_factor: float | None
    level_factor: float
    recency_factor: float
    raw_contribution: float


@dataclass
class ComputedSkill:
    skill_tag_id: int
    score: float                    # 0.0-1.0
    evidence: list[EvidenceItem]


# ---------------------------------------------------------------------------
# Factor helpers
# ---------------------------------------------------------------------------


def compute_grade_factor(grade: str | None, config: ScoringConfig) -> float:
    """Convert a raw grade string to a 0.0-1.0 factor."""
    if grade is None:
        return config.default_grade_factor
    normalized = grade.replace(",", ".").strip()
    try:
        val = float(normalized)
    except ValueError:
        lower = grade.lower()
        if "bestanden" in lower or "passed" in lower:
            return config.pass_grade_factor
        return config.default_grade_factor
    # German grade scale: 1.0 (best) → 5.0 (fail)
    if not (1.0 <= val <= 5.0):
        return config.default_grade_factor
    return (5.0 - val) / 4.0


def compute_recency_factor(semester_taken: str | None, config: ScoringConfig) -> float:
    """Compute temporal decay based on the semester string."""
    if not semester_taken:
        return config.recency_default
    years_ago = _parse_years_ago(semester_taken)
    if years_ago is None:
        return config.recency_default
    return max(config.recency_floor, 1.0 - config.recency_decay_per_year * years_ago)


def _parse_years_ago(semester_taken: str) -> float | None:
    """Extract a year from a semester string and return how many years ago.

    Handles formats like:
      "WS 2023/24", "SS 2024", "SoSe 2022", "WiSe 2022/23", "2023"
    """
    # Try to find a 4-digit year
    m = re.search(r"(\d{4})", semester_taken)
    if not m:
        return None
    year = int(m.group(1))
    current_year = date.today().year
    return max(0.0, float(current_year - year))


# ---------------------------------------------------------------------------
# Main scoring function
# ---------------------------------------------------------------------------


def compute_skill_scores(
    matched_modules: list[Any],  # list[MatchedModule] — avoids circular import
    config: ScoringConfig | None = None,
) -> list[ComputedSkill]:
    """Pure function: compute weighted skill scores from matched modules.

    ``matched_modules`` must be objects with attributes:
      .course       — StudentCourse-like (id, credits, grade, semester_taken)
      .handbook_entry — ModuleHandbookEntry-like or None
      .match        — object with .confidence and .method, or None
      .skill_mappings — list of ModuleSkillMapping-like (skill_tag_id, relevance)
    """
    config = config or ScoringConfig()

    if not matched_modules:
        return []

    # Max ECTS across transcript for credits normalization
    max_ects = max(
        (float(m.course.credits or config.default_ects) for m in matched_modules),
        default=config.default_ects,
    )
    max_ects = max(max_ects, 1.0)  # guard against zero division

    skill_evidence: dict[int, list[EvidenceItem]] = defaultdict(list)

    for mm in matched_modules:
        if mm.match is None or mm.match.confidence < config.min_match_confidence:
            continue

        ects = float(mm.course.credits or config.default_ects)
        credits_w = ects / max_ects
        grade_f = compute_grade_factor(mm.course.grade, config)
        level = (mm.handbook_entry.level or "unknown") if mm.handbook_entry else "unknown"
        level_f = config.level_weights.get(level, config.level_weights["unknown"])
        recency_f = compute_recency_factor(mm.course.semester_taken, config)
        conf = mm.match.confidence

        for mapping in mm.skill_mappings:
            relevance = float(mapping.relevance)
            contribution = credits_w * grade_f * relevance * level_f * recency_f * conf
            skill_evidence[mapping.skill_tag_id].append(
                EvidenceItem(
                    student_course_id=mm.course.id,
                    handbook_entry_id=mm.handbook_entry.id if mm.handbook_entry else None,
                    match_method=mm.match.method,
                    match_confidence=conf,
                    module_skill_relevance=relevance,
                    credits_used=ects,
                    grade_factor=grade_f,
                    level_factor=level_f,
                    recency_factor=recency_f,
                    raw_contribution=contribution,
                )
            )

    results: list[ComputedSkill] = []
    for skill_tag_id, items in skill_evidence.items():
        numerator = sum(i.raw_contribution for i in items)
        denominator = max(
            sum(
                (i.credits_used or config.default_ects) / max_ects * i.match_confidence
                for i in items
            ),
            1.0,
        )
        score = min(1.0, numerator / denominator)
        results.append(ComputedSkill(skill_tag_id=skill_tag_id, score=score, evidence=items))

    return sorted(results, key=lambda s: s.score, reverse=True)
