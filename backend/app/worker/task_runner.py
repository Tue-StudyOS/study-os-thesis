"""Shared lifecycle wrapper for Celery tasks.

Centralises the job-status transitions, WebSocket event publishing, and the
retry / dead-letter policy so every task behaves identically. A task body just
provides the actual unit of work as an async callable.
"""

from __future__ import annotations

import logging
import traceback
from collections.abc import Awaitable, Callable
from typing import Any

from celery.exceptions import MaxRetriesExceededError, SoftTimeLimitExceeded

from app.exceptions import NotFoundException
from app.worker.constants import (
    TASK_COMPLETE_EVENT,
    TASK_FAILED_EVENT,
    TASK_FAILURE_ERROR_MAX_CHARS,
    TASK_STATUS_FAILURE,
    TASK_STATUS_RETRY,
    TASK_STATUS_STARTED,
    TASK_STATUS_SUCCESS,
    TASK_TIMEOUT_MESSAGE,
    TASK_TRACEBACK_MAX_CHARS,
)
from app.worker.job_status import mark_failure, mark_retry, mark_started, mark_success
from app.worker.publisher import publish_event
from app.worker.utils import run_async

logger = logging.getLogger(__name__)

_RETRYABLE: tuple[type[BaseException], ...] = (ConnectionError, TimeoutError, OSError)
_PERMANENT: tuple[type[BaseException], ...] = (NotFoundException,)


def execute_task(
    task: Any,
    *,
    job_id: str,
    user_id: int,
    redis_url: str,
    work: Callable[[], Awaitable[dict]],
    success_event: str = TASK_COMPLETE_EVENT,
    started_event: str | None = None,
    started_data: dict | None = None,
    permanent_exceptions: tuple[type[BaseException], ...] = _PERMANENT,
    retryable_exceptions: tuple[type[BaseException], ...] = _RETRYABLE,
) -> dict:
    """Run ``work`` with full job-lifecycle bookkeeping.

    Transitions the job row pending -> started -> success/failure/retry, mirrors
    each transition onto the ``job_events`` Redis channel, and applies the retry
    policy. On exhausted retries the job is marked ``failure`` (dead letter).
    """
    mark_started(job_id)
    if started_event is not None:
        publish_event(
            redis_url,
            event_type=started_event,
            job_id=job_id,
            user_id=user_id,
            status=TASK_STATUS_STARTED,
            data=started_data or {},
        )

    try:
        result = run_async(work())
    except SoftTimeLimitExceeded:
        # The task hit its soft time limit (e.g. a slow local LLM). Record a
        # clean, human-readable reason instead of a truncated traceback so the
        # frontend can surface it directly.
        _fail(
            redis_url,
            job_id,
            user_id,
            TASK_TIMEOUT_MESSAGE,
        )
        raise
    except permanent_exceptions as exc:
        _fail(redis_url, job_id, user_id, str(exc))
        raise
    except retryable_exceptions as exc:
        mark_retry(job_id)
        publish_event(
            redis_url,
            event_type=TASK_FAILED_EVENT,
            job_id=job_id,
            user_id=user_id,
            status=TASK_STATUS_RETRY,
            data={"error": str(exc)},
        )
        try:
            raise task.retry(exc=exc)
        except MaxRetriesExceededError:
            _fail(redis_url, job_id, user_id, f"Exhausted retries: {exc}")
            raise
    except Exception:
        _fail(redis_url, job_id, user_id, traceback.format_exc()[:TASK_TRACEBACK_MAX_CHARS])
        raise

    mark_success(job_id, result)
    publish_event(
        redis_url,
        event_type=success_event,
        job_id=job_id,
        user_id=user_id,
        status=TASK_STATUS_SUCCESS,
        data=result,
    )
    return result


def _fail(redis_url: str, job_id: str, user_id: int, error: str) -> None:
    mark_failure(job_id, error)
    publish_event(
        redis_url,
        event_type=TASK_FAILED_EVENT,
        job_id=job_id,
        user_id=user_id,
        status=TASK_STATUS_FAILURE,
        data={"error": error[:TASK_FAILURE_ERROR_MAX_CHARS]},
    )
