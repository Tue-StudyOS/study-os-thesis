"""Regression tests for domain constants modules."""

from app.admin import constants as admin_constants
from app.auth import constants as auth_constants
from app.chat import constants as chat_constants
from app.chairs import constants as chair_constants
from app.jobs import constants as job_constants
from app.papers import constants as papers_constants
from app.proposals import constants as proposals_constants
from app.researchers import constants as researchers_constants
from app.scraper.constants import api as scraper_api
from app.scraper.constants import tasks as scraper_tasks
from app.students import constants as students_constants
from app.theses import constants as theses_constants
from app.tools import constants as tools_constants
from app.worker import constants as worker_constants
from app.ws import constants as ws_constants


def test_domain_route_prefixes_remain_api_scoped():
    assert admin_constants.ADMIN_API_PREFIX == "/api/admin"
    assert auth_constants.AUTH_API_PREFIX == "/api/auth"
    assert chair_constants.CHAIRS_API_PREFIX == "/api/chairs"
    assert chat_constants.CHAT_API_PREFIX == "/api/chat"
    assert job_constants.JOBS_API_PREFIX == "/api/jobs"
    assert papers_constants.PAPERS_API_PREFIX == "/api/papers"
    assert proposals_constants.PROPOSALS_API_PREFIX == "/api/proposals"
    assert researchers_constants.RESEARCHERS_API_PREFIX == "/api/researchers"
    assert scraper_api.SCRAPER_API_PREFIX == "/api/scraper"
    assert students_constants.STUDENTS_API_PREFIX == "/api/students"
    assert theses_constants.THESES_API_PREFIX == "/api/theses"
    assert ws_constants.WS_JOB_UPDATES_PATH == "/api/ws"


def test_worker_pubsub_channel_is_stable():
    assert worker_constants.JOB_EVENTS_CHANNEL == "job_events"


def test_tool_search_bounds_are_ordered():
    assert tools_constants.THESIS_SEARCH_MIN_K <= tools_constants.THESIS_SEARCH_DEFAULT_K <= tools_constants.THESIS_SEARCH_MAX_K
    assert tools_constants.THESIS_SEARCH_FETCH_MULTIPLIER > 1


def test_admin_pagination_constants_are_ordered():
    assert admin_constants.ADMIN_USER_LIST_MIN_LIMIT <= admin_constants.ADMIN_USER_LIST_DEFAULT_LIMIT <= admin_constants.ADMIN_USER_LIST_MAX_LIMIT


def test_task_time_limits_are_ordered():
    assert scraper_tasks.SCRAPE_CHAIR_SOFT_TIME_LIMIT_SECONDS < scraper_tasks.SCRAPE_CHAIR_TIME_LIMIT_SECONDS
    assert scraper_tasks.SCRAPE_RESEARCHER_SOFT_TIME_LIMIT_SECONDS < scraper_tasks.SCRAPE_RESEARCHER_TIME_LIMIT_SECONDS
    assert theses_constants.EMBED_THESIS_SOFT_TIME_LIMIT_SECONDS < theses_constants.EMBED_THESIS_TIME_LIMIT_SECONDS
    assert students_constants.TRANSCRIPT_SOFT_TIME_LIMIT_DEFAULT_SECONDS < students_constants.TRANSCRIPT_HARD_TIME_LIMIT_DEFAULT_SECONDS
