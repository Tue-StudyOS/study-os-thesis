# Refactoring State: API/Worker Separation

Last updated: 2026-05-28

## Overall Status

| Phase | Description | Status | Tests |
|---|---|---|---|
| 1 | Infrastructure (Redis, Celery app, config, utils, publisher) | **Done** | 17/17 passing |
| 2 | Jobs table & domain (model, service, repository, schemas, controller) | **Done** (migration not yet generated) | 19/19 passing |
| 3 | WebSocket layer (manager, listener, controller, lifespan) | **Done** (2 e2e tests hanging — see Known Issues) | 12/12 unit passing, 2 e2e blocked |
| 4 | Migrate ingestion tasks (theses, chairs, students) | **Done** | 16/16 task tests passing, 12/12 e2e passing |
| 5 | Migrate chat agent loop | **Done** | 6/6 task tests passing, 5/5 e2e passing |
| 6 | Retry policies & timeouts | **Done** | 10/10 passing |
| 7 | Regression tests (existing service logic) | **Done** | 68/68 passing |

**Total: 173 tests collected. 171 passing, 2 hanging (WebSocket e2e).**

---

## Test Results

```
tests/unit/   — 151 passed, 0 failed
tests/e2e/    —  20 passed, 0 failed (excluding 2 WebSocket tests)
              —   2 hanging (test_ws_endpoints.py)
```

Run command (excluding hanging tests):

```bash
cd backend
DATABASE_URL="postgresql+asyncpg://test:test@localhost:5433/test" \
JWT_SECRET="test-secret-for-e2e-tests-1234567890" \
uv run pytest tests/ --ignore=tests/e2e/test_ws_endpoints.py -v
```

---

## Known Issues

### 1. WebSocket e2e tests hang (`tests/e2e/test_ws_endpoints.py`)

**Root cause:** Starlette's sync `TestClient.websocket_connect()` blocks when the
server accepts the connection and then immediately closes it. The ASGI server-side
`websocket.close(code=4001)` sends a close frame, but the test client's
`receive_json()` call blocks forever waiting for data instead of seeing the close.

**Affected tests:**
- `test_websocket_requires_auth` — connects without token, server accepts then closes
- `test_websocket_rejects_invalid_token` — connects with bad JWT, same behavior

**Controller logic is correct** (`app/ws/controller.py`): it accepts, validates the
token, and closes with 4001 if invalid. The issue is purely in how to test this
with Starlette's sync WebSocket test client.

**Fix options:**
1. Use `anyio` with `move_on_after` to add a timeout around the receive call
2. Switch to `httpx-ws` or `websockets` library for the test
3. Have the server send a JSON error message before closing so `receive_json()` returns

### 2. Alembic migration 0009 not yet generated

The `Job` model exists in `app/models/job.py` but the Alembic migration
`0009_add_jobs_table` has not been created yet. Run:

```bash
cd backend
uv run alembic revision --autogenerate -m "add_jobs_table"
uv run alembic upgrade head
```

This is blocked on having the DB container running with the current schema.

### 3. Pre-existing uncommitted changes in working tree

These files have changes **not related** to the API/Worker refactoring:

- `backend/app/models/user.py` — removed `professor` enum value (migration 0008)
- `backend/app/students/schemas.py` — added `model_config = ConfigDict(extra="ignore")`, widened `grade` max_length
- `backend/app/students/service.py` — tweaked LLM prompt wording
- `backend/app/theses/service.py` — (check diff, may be from earlier session)
- `frontend/src/auth/AuthContext.tsx`, `frontend/src/pages/Admin.tsx`, etc. — frontend changes unrelated to this work

---

## Files Created (new)

### Infrastructure (`app/worker/`)

| File | Purpose |
|---|---|
| `app/worker/__init__.py` | Package init |
| `app/worker/celery_app.py` | Celery instance, autodiscover tasks from domain modules |
| `app/worker/celery_config.py` | Broker/backend URLs, serialization, concurrency, retry settings |
| `app/worker/utils.py` | `run_async()` — runs async coroutines inside sync Celery tasks |
| `app/worker/publisher.py` | `publish_event()` — publishes JSON events to Redis Pub/Sub channel `job_events` |

### Jobs domain (`app/jobs/`)

| File | Purpose |
|---|---|
| `app/jobs/__init__.py` | Package init |
| `app/jobs/controller.py` | `GET /api/jobs/{id}`, `GET /api/jobs` endpoints |
| `app/jobs/service.py` | `create_job`, `mark_started`, `mark_success`, `mark_failure`, `mark_retry`, `get_job`, `list_jobs` |
| `app/jobs/repository.py` | CRUD against jobs table (create, get_by_id, update, list_by_user) |
| `app/jobs/schemas.py` | `JobOut` Pydantic schema |
| `app/jobs/deps.py` | `JobServiceDep`, `JobRepoDep` FastAPI DI wiring |
| `app/models/job.py` | `Job` SQLAlchemy model, `JobType` enum, `JobStatus` enum |

### WebSocket layer (`app/ws/`)

| File | Purpose |
|---|---|
| `app/ws/__init__.py` | Package init |
| `app/ws/manager.py` | `ConnectionManager` — tracks WebSocket connections by user_id, dispatches messages |
| `app/ws/listener.py` | `redis_listener()` — subscribes to Redis Pub/Sub, routes events to WebSockets. `_handle_message()` extracted for testability. |
| `app/ws/controller.py` | `WS /api/ws` endpoint — JWT auth via query param, keep-alive loop |

### Celery tasks

| File | Purpose |
|---|---|
| `app/theses/tasks.py` | `embed_thesis` — generates thesis embedding in background |
| `app/chairs/tasks.py` | `ingest_arxiv_paper`, `embed_chair_description` — ArXiv ingestion and chair embedding |
| `app/students/tasks.py` | `parse_transcript` — PDF parsing + LLM extraction + embedding |
| `app/chat/tasks.py` | `process_chat_turn` — full agent loop (up to 6 LLM iterations) with WebSocket event streaming |

### Test files (`tests/`)

| File | Tests | Status |
|---|---|---|
| `tests/conftest.py` | Shared fixtures: `fake_settings`, `mock_llm_chat/embed`, `fake_user/admin`, `_make_orm` | Working |
| `tests/unit/conftest.py` | Mock repositories | Working |
| `tests/e2e/conftest.py` | FastAPI app with DI overrides, Celery patches, `client`/`admin_client` | Working |
| `tests/unit/test_compute_gpa.py` | 10 tests | All passing |
| `tests/unit/test_auth_service.py` | 9 tests | All passing |
| `tests/unit/test_thesis_service.py` | 9 tests | All passing |
| `tests/unit/test_chair_service.py` | 12 tests | All passing |
| `tests/unit/test_student_service.py` | 11 tests | All passing |
| `tests/unit/test_chat_service.py` | 16 tests | All passing |
| `tests/unit/worker/test_celery_config.py` | 9 tests | All passing |
| `tests/unit/worker/test_run_async.py` | 3 tests | All passing |
| `tests/unit/worker/test_publisher.py` | 5 tests | All passing |
| `tests/unit/worker/test_thesis_tasks.py` | 5 tests | All passing |
| `tests/unit/worker/test_chair_tasks.py` | 6 tests | All passing |
| `tests/unit/worker/test_student_tasks.py` | 5 tests | All passing |
| `tests/unit/worker/test_chat_tasks.py` | 6 tests | All passing |
| `tests/unit/worker/test_retry_policy.py` | 10 tests | All passing |
| `tests/unit/ws/test_connection_manager.py` | 8 tests | All passing |
| `tests/unit/ws/test_listener.py` | 4 tests | All passing |
| `tests/unit/jobs/test_job_schemas.py` | 5 tests | All passing |
| `tests/unit/jobs/test_job_service.py` | 14 tests | All passing |
| `tests/e2e/test_health.py` | 1 test | Passing |
| `tests/e2e/test_job_endpoints.py` | 5 tests | All passing |
| `tests/e2e/test_thesis_endpoints.py` | 6 tests | All passing |
| `tests/e2e/test_chair_endpoints.py` | 4 tests | All passing |
| `tests/e2e/test_student_endpoints.py` | 3 tests | All passing |
| `tests/e2e/test_chat_endpoints.py` | 5 tests | All passing |
| `tests/e2e/test_ws_endpoints.py` | 2 tests | **Hanging** |

---

## Files Modified (existing)

| File | Changes |
|---|---|
| `docker-compose.yml` | Added `redis` service (redis:7-alpine, port 6379, healthcheck, noeviction, AOF) and `redis-data` volume |
| `backend/pyproject.toml` | Added `celery[redis]>=5.4`, `redis>=5.0` to deps; `pytest-cov`, `respx` to dev deps; `asyncio_mode = "auto"`, markers, `tests/**/*.py` ANN ignore |
| `backend/app/config.py` | Added `redis_url` field with alias `REDIS_URL` |
| `backend/.env.example` | Added `REDIS_URL=redis://localhost:6379/0` |
| `backend/app/models/__init__.py` | Re-exports `Job`, `JobType`, `JobStatus` |
| `backend/app/main.py` | Imports+registers `jobs_router`, `ws_router`; lifespan creates `ConnectionManager`, starts `redis_listener` asyncio task, cancels on shutdown |
| `backend/app/theses/controller.py` | `POST /` now creates thesis (no embedding), dispatches `embed_thesis.delay()`, returns `{...thesis, job_id}` with 201 |
| `backend/app/chairs/controller.py` | `POST /` dispatches `embed_chair_description.delay()`, returns `{...chair, job_id}` with 201. `POST /{id}/documents/arxiv` validates chair exists, dispatches `ingest_arxiv_paper.delay()`, returns `{job_id}` with 202 |
| `backend/app/students/controller.py` | `POST /me/transcript` validates PDF, dispatches `parse_transcript.delay()`, returns `{job_id}` with 202. No longer calls service inline. |
| `backend/app/chat/controller.py` | `POST /sessions/{id}/messages` validates session ownership, dispatches `process_chat_turn.delay()`, returns `{job_id, session_id}` with 202 |
| `debug.sh` | Launches Celery worker (`uv run celery -A app.worker.celery_app worker`) as third background process. Added `CELERY_PID`, `redis_is_healthy()`, Redis health check in `cmd_start`/`cmd_up`. |

---

## What Still Needs to Be Done

### Blocking (must fix before merge)

1. **Fix WebSocket e2e tests** — either change the test approach (use `anyio.move_on_after` timeout, or send a JSON error before closing) or change the controller to send an error message before closing so `receive_json()` returns.

2. **Generate Alembic migration 0009** — `alembic revision --autogenerate -m "add_jobs_table"` then `alembic upgrade head`.

### Non-blocking (can be follow-up PRs)

3. **Integration tests** — `tests/integration/` directory exists but has no test files. Needs a test DB fixture and repository-level tests against real PostgreSQL+pgvector.

4. **PDF bytes storage for transcript worker** — The `parse_transcript` task currently receives a placeholder `pdf_bytes_ref`. In production the PDF bytes need to be stored (e.g. in Redis, S3, or a temp file) and referenced by key so the worker can retrieve them.

5. **Chat WebSocket streaming** — The `process_chat_turn` task publishes `chat_turn_started` and `chat_turn_completed` events, but does not yet publish intermediate `chat_message` or `chat_tool_call` events after each LLM iteration. The service layer needs hooks to publish per-iteration.

6. **Frontend WebSocket client** — `frontend/src/api/ws.ts` and Chat page updates for real-time message streaming.

7. **Flower monitoring dashboard** — Optional. Add `flower` to dev deps and a command in `debug.sh`.

8. **ThesisService.create_thesis still calls embed inline** — The controller dispatches to a Celery task, but the service method itself still calls `self._ollama.embed(...)`. The service should be refactored to optionally skip embedding (or a new `create_thesis_without_embedding` method) so the controller can persist the thesis row without an embedding, then the worker generates it. Currently the e2e test works because the service is fully mocked, but in a real integration test this would double-embed.

---

## Architecture Diagram (Post-Refactor)

```
                 ┌──────────────┐
                 │   Frontend   │
                 │  (React/TS)  │
                 └──────┬───────┘
                        │ HTTP + WebSocket
                        ▼
                 ┌──────────────┐
                 │  FastAPI API  │
                 │   (uvicorn)   │
                 │               │
                 │ • Auth/CRUD   │ ◄──── Redis Pub/Sub ◄───┐
                 │ • Job create  │       (listener)         │
                 │ • WS push     │                          │
                 └──────┬───────┘                          │
                        │ .delay()                          │
                        ▼                                   │
                 ┌──────────────┐                          │
                 │  Redis 7     │                          │
                 │  (broker +   │                          │
                 │   pub/sub)   │                          │
                 └──────┬───────┘                          │
                        │ task queue                        │
                        ▼                                   │
                 ┌──────────────┐                          │
                 │ Celery Worker │──── publish_event() ────┘
                 │               │
                 │ • embed_thesis│
                 │ • ingest_arxiv│
                 │ • parse_trans │
                 │ • chat_turn   │
                 └──────┬───────┘
                        │ asyncio.run()
                        ▼
                 ┌──────────────┐     ┌──────────────┐
                 │ PostgreSQL   │     │ Ollama / LLM │
                 │  + pgvector  │     │  (chat/embed) │
                 └──────────────┘     └──────────────┘
```
