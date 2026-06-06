"""Unit tests for scraper API schemas."""

import pytest
from pydantic import ValidationError

from app.scraper.schemas import ScrapeChairRequest


@pytest.mark.unit
def test_scrape_request_rejects_numeric_strings():
    with pytest.raises(ValidationError):
        ScrapeChairRequest.model_validate({"max_results": "250", "since_days": 3650})

    with pytest.raises(ValidationError):
        ScrapeChairRequest.model_validate({"max_results": 250, "since_days": "3650"})


@pytest.mark.unit
def test_scrape_request_rejects_float_values():
    with pytest.raises(ValidationError):
        ScrapeChairRequest.model_validate({"max_results": 250.5, "since_days": 3650})


@pytest.mark.unit
def test_scrape_request_accepts_bounded_integers():
    request = ScrapeChairRequest.model_validate({"max_results": 250, "since_days": 3650})

    assert request.max_results == 250
    assert request.since_days == 3650
