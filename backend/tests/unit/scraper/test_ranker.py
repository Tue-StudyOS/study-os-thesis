"""Unit tests for RecencyPaperRanker."""

from datetime import datetime, timedelta, timezone
from itertools import pairwise
from types import SimpleNamespace

import pytest

from app.scraper.adapters.ranker import RecencyPaperRanker


@pytest.mark.unit
class TestRecencyScore:
    def setup_method(self):
        self.ranker = RecencyPaperRanker(half_life_days=180)

    def test_today_scores_close_to_one(self):
        score = self.ranker.compute_recency_score(datetime.now(timezone.utc))
        assert score > 0.99

    def test_half_life_date_scores_approximately_half(self):
        date = datetime.now(timezone.utc) - timedelta(days=180)
        score = self.ranker.compute_recency_score(date)
        assert abs(score - 0.5) < 0.01

    def test_one_year_ago_scores_quarter(self):
        date = datetime.now(timezone.utc) - timedelta(days=365)
        score = self.ranker.compute_recency_score(date)
        # exp(-ln2/180 * 365) ≈ 0.249
        assert abs(score - 0.25) < 0.01

    def test_two_years_ago_is_much_lower(self):
        date = datetime.now(timezone.utc) - timedelta(days=730)
        score = self.ranker.compute_recency_score(date)
        assert score < 0.1

    def test_none_date_returns_low_sentinel(self):
        score = self.ranker.compute_recency_score(None)
        assert score == 0.1

    def test_future_date_does_not_exceed_one(self):
        # age_days = max(0, ...) clamps to 0 for future dates
        future = datetime.now(timezone.utc) + timedelta(days=365)
        score = self.ranker.compute_recency_score(future)
        assert score <= 1.0
        assert score > 0.99

    def test_timezone_naive_date_does_not_crash(self):
        naive = datetime.now() - timedelta(days=90)
        score = self.ranker.compute_recency_score(naive)
        assert 0 < score <= 1.0

    def test_score_is_monotonically_decreasing_with_age(self):
        dates = [datetime.now(timezone.utc) - timedelta(days=d) for d in [0, 30, 90, 180, 365, 730]]
        scores = [self.ranker.compute_recency_score(d) for d in dates]
        for earlier, later in pairwise(scores):
            assert earlier > later

    def test_custom_half_life_respected(self):
        ranker_365 = RecencyPaperRanker(half_life_days=365)
        date = datetime.now(timezone.utc) - timedelta(days=365)
        score = ranker_365.compute_recency_score(date)
        assert abs(score - 0.5) < 0.01

    def test_score_always_positive(self):
        ancient = datetime(1900, 1, 1, tzinfo=timezone.utc)
        score = self.ranker.compute_recency_score(ancient)
        assert score > 0


@pytest.mark.unit
class TestRelevanceScore:
    def test_relevance_mirrors_recency_in_mvp(self):
        ranker = RecencyPaperRanker()
        paper = SimpleNamespace(recency_score=0.73)
        assert ranker.compute_relevance_score(paper) == 0.73

    def test_relevance_zero_paper(self):
        ranker = RecencyPaperRanker()
        paper = SimpleNamespace(recency_score=0.0)
        assert ranker.compute_relevance_score(paper) == 0.0
