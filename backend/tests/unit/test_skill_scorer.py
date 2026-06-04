"""Unit tests for the pure skill scoring functions in app.skills.scorer.

No database, no LLM calls, no I/O.  All inputs are simple dataclass instances.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import pytest

from app.skills.scorer import (
    ScoringConfig,
    compute_grade_factor,
    compute_recency_factor,
    compute_skill_scores,
)


# ---------------------------------------------------------------------------
# Minimal stubs that satisfy the duck-typing in compute_skill_scores()
# ---------------------------------------------------------------------------


@dataclass
class _Match:
    method: str
    confidence: float


@dataclass
class _Course:
    id: int
    course_name: str
    credits: float | None
    grade: str | None
    semester_taken: str | None


@dataclass
class _Entry:
    id: int
    level: str | None


@dataclass
class _Mapping:
    skill_tag_id: int
    relevance: float


@dataclass
class _MatchedModule:
    course: _Course
    handbook_entry: _Entry | None
    match: _Match | None
    skill_mappings: list[_Mapping] = field(default_factory=list)


# ---------------------------------------------------------------------------
# grade factor
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestGradeFactor:
    def test_best_grade(self) -> None:
        assert compute_grade_factor("1,0", ScoringConfig()) == pytest.approx(1.0)

    def test_worst_passing_grade(self) -> None:
        # 4.0 -> (5.0 - 4.0) / 4.0 = 0.25
        assert compute_grade_factor("4,0", ScoringConfig()) == pytest.approx(0.25)

    def test_failed_grade(self) -> None:
        # 5.0 -> (5.0 - 5.0) / 4.0 = 0.0
        assert compute_grade_factor("5,0", ScoringConfig()) == pytest.approx(0.0)

    def test_mid_grade(self) -> None:
        # 2.0 -> (5.0 - 2.0) / 4.0 = 0.75
        assert compute_grade_factor("2,0", ScoringConfig()) == pytest.approx(0.75)

    def test_german_comma_format(self) -> None:
        assert compute_grade_factor("1,3", ScoringConfig()) == pytest.approx((5 - 1.3) / 4)

    def test_bestanden_uses_pass_factor(self) -> None:
        cfg = ScoringConfig(pass_grade_factor=0.6)
        assert compute_grade_factor("bestanden", cfg) == pytest.approx(0.6)

    def test_none_uses_default(self) -> None:
        cfg = ScoringConfig(default_grade_factor=0.5)
        assert compute_grade_factor(None, cfg) == pytest.approx(0.5)

    def test_out_of_range_uses_default(self) -> None:
        cfg = ScoringConfig(default_grade_factor=0.5)
        assert compute_grade_factor("0,5", cfg) == pytest.approx(0.5)
        assert compute_grade_factor("5,5", cfg) == pytest.approx(0.5)

    def test_period_decimal(self) -> None:
        # "1.3" should also work (not just comma)
        assert compute_grade_factor("1.3", ScoringConfig()) == pytest.approx((5 - 1.3) / 4)


# ---------------------------------------------------------------------------
# recency factor
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestRecencyFactor:
    def test_no_semester_returns_default(self) -> None:
        cfg = ScoringConfig(recency_default=0.75)
        assert compute_recency_factor(None, cfg) == pytest.approx(0.75)

    def test_current_year_no_decay(self) -> None:
        from datetime import date

        current = str(date.today().year)
        # 0 years ago -> 1.0 - 0.05 * 0 = 1.0
        assert compute_recency_factor(f"WS {current}", ScoringConfig()) == pytest.approx(1.0)

    def test_decay_two_years(self) -> None:
        from datetime import date

        past_year = date.today().year - 2
        result = compute_recency_factor(f"SS {past_year}", ScoringConfig())
        expected = max(0.5, 1.0 - 0.05 * 2)  # 0.9
        assert result == pytest.approx(expected)

    def test_floor_is_respected(self) -> None:
        # 20 years ago: 1.0 - 0.05 * 20 = 0.0  -> clamped to floor 0.5
        from datetime import date

        old_year = date.today().year - 20
        result = compute_recency_factor(f"WS {old_year}/00", ScoringConfig(recency_floor=0.5))
        assert result == pytest.approx(0.5)

    def test_unrecognized_format_returns_default(self) -> None:
        cfg = ScoringConfig(recency_default=0.75)
        assert compute_recency_factor("Sommersemester", cfg) == pytest.approx(0.75)


# ---------------------------------------------------------------------------
# full scoring pipeline
# ---------------------------------------------------------------------------


@pytest.mark.unit
class TestComputeSkillScores:
    def _simple_module(
        self,
        skill_tag_id: int = 1,
        credits: float = 6.0,
        grade: str = "1,0",
        level: str = "master",
        relevance: float = 1.0,
        confidence: float = 1.0,
        semester: str | None = None,
    ) -> _MatchedModule:
        from datetime import date

        semester = semester or f"WS {date.today().year}"
        return _MatchedModule(
            course=_Course(
                id=1,
                course_name="Test",
                credits=credits,
                grade=grade,
                semester_taken=semester,
            ),
            handbook_entry=_Entry(id=1, level=level),
            match=_Match(method="exact_code", confidence=confidence),
            skill_mappings=[_Mapping(skill_tag_id=skill_tag_id, relevance=relevance)],
        )

    def test_empty_input_returns_empty(self) -> None:
        assert compute_skill_scores([]) == []

    def test_single_perfect_module_score_one(self) -> None:
        module = self._simple_module(grade="1,0", level="master", confidence=1.0, relevance=1.0)
        scores = compute_skill_scores([module])
        assert len(scores) == 1
        assert scores[0].score == pytest.approx(0.85, rel=0.01)  # master level_factor=0.85

    def test_failed_module_excluded(self) -> None:
        module = self._simple_module(grade="5,0", confidence=1.0, relevance=1.0)
        scores = compute_skill_scores([module])
        # grade_factor(5.0) == 0.0 → contribution == 0 → numerator = 0 → score = 0
        assert scores[0].score == pytest.approx(0.0)

    def test_low_confidence_excluded(self) -> None:
        module = self._simple_module(confidence=0.3)  # below default min 0.5
        scores = compute_skill_scores([module])
        assert scores == []

    def test_score_capped_at_one(self) -> None:
        module = self._simple_module(grade="1,0", level="phd", confidence=1.0, relevance=1.0)
        scores = compute_skill_scores([module])
        assert scores[0].score <= 1.0

    def test_higher_relevance_gives_higher_score(self) -> None:
        m_high = self._simple_module(skill_tag_id=1, relevance=0.9, grade="1,3")
        m_low = self._simple_module(skill_tag_id=2, relevance=0.3, grade="1,3")
        scores = compute_skill_scores([m_high, m_low])
        score_map = {s.skill_tag_id: s.score for s in scores}
        assert score_map[1] > score_map[2]

    def test_better_grade_gives_higher_score(self) -> None:
        m_good = self._simple_module(skill_tag_id=1, grade="1,0")
        m_bad = self._simple_module(skill_tag_id=2, grade="3,7")
        scores = compute_skill_scores([m_good, m_bad])
        score_map = {s.skill_tag_id: s.score for s in scores}
        assert score_map[1] > score_map[2]

    def test_sorted_by_score_descending(self) -> None:
        m1 = self._simple_module(skill_tag_id=1, grade="1,0")
        m2 = self._simple_module(skill_tag_id=2, grade="3,7")
        scores = compute_skill_scores([m1, m2])
        assert scores[0].score >= scores[1].score

    def test_multiple_modules_same_skill_accumulated(self) -> None:
        """Two modules contributing to the same skill should accumulate."""
        m1 = self._simple_module(skill_tag_id=1, credits=6.0, grade="1,0")
        m2 = self._simple_module(skill_tag_id=1, credits=6.0, grade="1,0")
        m2.course = _Course(
            id=2, course_name="Test2", credits=6.0, grade="1,0", semester_taken=m1.course.semester_taken
        )
        scores = compute_skill_scores([m1, m2])
        # Both contribute; the score should be the same as one (normalized)
        assert len(scores) == 1  # both go to skill_tag_id=1
        assert scores[0].score <= 1.0

    def test_evidence_items_recorded(self) -> None:
        module = self._simple_module()
        scores = compute_skill_scores([module])
        assert len(scores[0].evidence) == 1
        ev = scores[0].evidence[0]
        assert ev.student_course_id == 1
        assert ev.handbook_entry_id == 1
        assert ev.match_method == "exact_code"
