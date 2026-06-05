"""Unit tests for pure helper functions in scholar_scraper.py.

These test the parsing logic without requiring Playwright.
"""

import datetime

import pytest

from app.scraper.adapters.scholar_scraper import (
    _parse_authors_from_meta,
    _parse_year_from_meta,
    _strip_leading_titles_for_search,
    _year_cutoff,
)


@pytest.mark.unit
class TestParseYearFromMeta:
    @pytest.mark.parametrize(
        "meta,expected",
        [
            # Standard Scholar meta line
            ("A Author, B Author - Nature, 2023 - Publisher", 2023),
            # Year at end without publisher
            ("Alice Smith - Journal of ML, 2021", 2021),
            # Year only (minimal)
            ("2019", 2019),
            # Older paper
            ("G Martius - Old Journal, 1998 - Publisher", 1998),
            # No year at all
            ("A Author - Journal without year", None),
            ("", None),
            # Multiple years — should return first
            ("2020 work extended in 2023", 2020),
            # Year embedded in a DOI-like string — must still work
            ("A Author - Proc. ICML 2022, pages 100", 2022),
        ],
    )
    def test_parse_year(self, meta, expected):
        assert _parse_year_from_meta(meta) == expected

    def test_does_not_match_partial_numbers(self):
        # "123" is not a 4-digit year
        assert _parse_year_from_meta("A Author - volume 123, issue 4") is None

    def test_current_year_is_valid(self):
        current = datetime.datetime.now().year
        meta = f"G Martius - arXiv, {current}"
        assert _parse_year_from_meta(meta) == current


@pytest.mark.unit
class TestParseAuthorsFromMeta:
    @pytest.mark.parametrize(
        "meta,expected",
        [
            # Standard case
            ("Alice Smith, Bob Jones - Nature, 2023 - Publisher", ["Alice Smith", "Bob Jones"]),
            # Single author
            ("Georg Martius - ICML, 2022", ["Georg Martius"]),
            # No dash at all — entire string treated as author part
            ("Alice Smith, Bob Jones", ["Alice Smith", "Bob Jones"]),
            # Trailing ellipsis from Scholar abbreviation
            ("A Author, B Author… - Journal, 2023", ["A Author", "B Author"]),
            # Three authors
            ("X One, Y Two, Z Three - Venue, 2020", ["X One", "Y Two", "Z Three"]),
        ],
    )
    def test_parse_authors(self, meta, expected):
        assert _parse_authors_from_meta(meta) == expected

    def test_empty_string_returns_empty(self):
        assert _parse_authors_from_meta("") == []

    def test_only_dash_returns_empty_like(self):
        # " - 2023" has no author part before the dash
        result = _parse_authors_from_meta(" - 2023")
        # After split on " - ", first part is " " which strips to ""
        assert result == []

    def test_strips_whitespace_from_each_author(self):
        result = _parse_authors_from_meta("  Alice  ,  Bob  - Journal")
        assert result == ["Alice", "Bob"]

    def test_initialised_names_preserved(self):
        # Scholar often abbreviates to "G Martius" or "AB Author"
        result = _parse_authors_from_meta("G Martius, AB Author - Venue")
        assert result == ["G Martius", "AB Author"]


@pytest.mark.unit
class TestYearCutoff:
    def test_ten_years_cutoff(self):
        current = datetime.datetime.now().year
        assert _year_cutoff(3650) == current - 10

    def test_one_year_cutoff(self):
        current = datetime.datetime.now().year
        assert _year_cutoff(365) == current - 1

    def test_five_year_cutoff(self):
        current = datetime.datetime.now().year
        assert _year_cutoff(1825) == current - 5

    def test_partial_year_rounds_down(self):
        # 400 days // 365 = 1
        current = datetime.datetime.now().year
        assert _year_cutoff(400) == current - 1


@pytest.mark.unit
class TestStripTitlesForSearch:
    @pytest.mark.parametrize(
        "raw,expected",
        [
            ("Prof. Dr. Georg Martius", "Georg Martius"),
            ("Professor Dr.-Ing. Alice Smith", "Alice Smith"),
            ("Dr. Bob", "Bob"),
            ("Georg Martius", "Georg Martius"),
        ],
    )
    def test_strips_only_leading_titles(self, raw, expected):
        assert _strip_leading_titles_for_search(raw) == expected
