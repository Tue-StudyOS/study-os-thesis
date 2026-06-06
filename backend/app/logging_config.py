"""Shared logging configuration helpers."""

from __future__ import annotations

import json
import logging.config
from pathlib import Path
from typing import Any

_BACKEND_DIR = Path(__file__).resolve().parents[1]
_LOG_CONFIG_PATH = _BACKEND_DIR / "log_config.json"


def configure_logging(config_path: Path = _LOG_CONFIG_PATH) -> None:
    """Apply the shared logging configuration used by Uvicorn and Celery."""

    (_BACKEND_DIR / "logs").mkdir(exist_ok=True)
    with config_path.open(encoding="utf-8") as config_file:
        config: dict[str, Any] = json.load(config_file)
    logging.config.dictConfig(config)
