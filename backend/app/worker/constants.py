"""Constants for worker lifecycle events and Redis publishing."""

JOB_EVENTS_CHANNEL = "job_events"

TASK_STATUS_STARTED = "started"
TASK_STATUS_SUCCESS = "success"
TASK_STATUS_FAILURE = "failure"
TASK_STATUS_RETRY = "retry"

TASK_COMPLETE_EVENT = "task_complete"
TASK_FAILED_EVENT = "task_failed"
TASK_FAILURE_ERROR_MAX_CHARS = 500
TASK_TRACEBACK_MAX_CHARS = 1000
TASK_TIMEOUT_MESSAGE = "Processing timed out before it finished. Try a faster model or raise the task time limit."
