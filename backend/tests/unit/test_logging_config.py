"""Tests for shared backend logging configuration."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

LOG_FORMAT = "%(log_color)s%(asctime)8s | %(levelname)-8s | %(name)-28.28s | %(filename)-24.24s:%(lineno)4d | %(message)s%(reset)s"
PLAIN_LOG_FORMAT = "%(asctime)8s | %(levelname)-8s | %(name)-28.28s | %(filename)-24.24s:%(lineno)4d | %(message)s"


@pytest.fixture
def log_config() -> dict:
    config_path = Path(__file__).resolve().parents[2] / "log_config.json"
    with config_path.open(encoding="utf-8") as config_file:
        return json.load(config_file)


@pytest.mark.unit
def test_console_formatter_is_colored_and_uses_standard_format(log_config: dict) -> None:
    formatter = log_config["formatters"]["console"]

    assert formatter["()"] == "colorlog.ColoredFormatter"
    assert formatter["format"] == LOG_FORMAT
    assert formatter["force_color"] is True


@pytest.mark.unit
def test_file_formatter_uses_matching_plain_format(log_config: dict) -> None:
    formatter = log_config["formatters"]["file"]

    assert formatter["format"] == PLAIN_LOG_FORMAT


@pytest.mark.unit
def test_core_logger_families_use_shared_handlers(log_config: dict) -> None:
    expected_handlers = ["console", "file"]

    assert log_config["root"]["handlers"] == expected_handlers
    for logger_name in (
        "app",
        "uvicorn",
        "uvicorn.error",
        "uvicorn.access",
        "watchfiles",
        "watchfiles.main",
        "celery",
        "celery.app.trace",
        "kombu",
        "billiard",
        "sqlalchemy.engine",
        "httpx",
    ):
        assert log_config["loggers"][logger_name]["handlers"] == expected_handlers
