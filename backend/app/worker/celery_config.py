"""Celery configuration for study-os-thesis workers."""

import os
from celery.schedules import crontab as _crontab

broker_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
result_backend: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Serialization
task_serializer: str = "json"
result_serializer: str = "json"
accept_content: list[str] = ["json"]

# Time
timezone: str = "UTC"
enable_utc: bool = True

# Task behaviour
task_track_started: bool = True
task_acks_late: bool = True
worker_prefetch_multiplier: int = 1
task_reject_on_worker_lost: bool = True

# Results
result_expires: int = 86400  # 24 hours
result_extended: bool = True

# Redis transport
broker_transport_options: dict = {
    "visibility_timeout": 3600,
}

# Concurrency
worker_concurrency: int = 4

# ---------------------------------------------------------------------------
# Celery Beat: periodic tasks
# ---------------------------------------------------------------------------
# Scrape all chairs weekly (every Monday at 02:00 UTC).
# Override the schedule by setting SCRAPER_BEAT_SCHEDULE env var:
#   "interval"  → run every N seconds (useful for dev/testing)
#   "weekly"    → every Monday at 02:00 UTC (default)
#   "daily"     → every day at 02:00 UTC
#   "disabled"  → do not schedule automatically

_beat_mode = os.getenv("SCRAPER_BEAT_SCHEDULE", "weekly").lower()

if _beat_mode == "disabled":
    beat_schedule: dict = {}
elif _beat_mode == "daily":
    beat_schedule = {
        "scrape-all-chairs-daily": {
            "task": "app.scraper.tasks.scrape_all_chairs",
            "schedule": _crontab(hour=2, minute=0),
        }
    }
elif _beat_mode == "interval":
    # For development: run every SCRAPER_BEAT_INTERVAL_SECONDS seconds (default 3600)
    _interval = int(os.getenv("SCRAPER_BEAT_INTERVAL_SECONDS", "3600"))
    beat_schedule = {
        "scrape-all-chairs-interval": {
            "task": "app.scraper.tasks.scrape_all_chairs",
            "schedule": float(_interval),
        }
    }
else:
    # Default: weekly on Monday at 02:00 UTC
    beat_schedule = {
        "scrape-all-chairs-weekly": {
            "task": "app.scraper.tasks.scrape_all_chairs",
            "schedule": _crontab(hour=2, minute=0, day_of_week=1),
        }
    }
