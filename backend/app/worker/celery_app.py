"""Celery application instance for study-os-thesis."""

from celery import Celery

celery_app = Celery("study_os_thesis")
celery_app.config_from_object("app.worker.celery_config")
celery_app.autodiscover_tasks([
    "app.theses",
    "app.chairs",
    "app.students",
    "app.chat",
])
