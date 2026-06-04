# study-os-thesis
[![Code Quality](https://github.com/ValentinJSchmidt/study-os-thesis/actions/workflows/qa.yml/badge.svg?branch=main)](https://github.com/ValentinJSchmidt/study-os-thesis/actions/workflows/qa.yml)

An AI-powered thesis advisor for university students. Students upload their
transcript of records, the system analyses their course profile, and an LLM
agent recommends fitting research chairs and generates personalised thesis
proposals. Professors manage chairs and thesis proposals through an admin
interface.

## Stack

| Layer | Technology |
|---|---|
| **Backend** | FastAPI + async SQLAlchemy + Alembic, managed by `uv` |
| **Database** | PostgreSQL 16 + pgvector (Docker, host port **5433**) |
| **LLM (chat + generation)** | Ollama — `gemma4:26b` (or any model you configure) |
| **LLM (embeddings)** | Ollama — `qwen3-embedding:4b` (2560-dim vectors) |
| **Frontend** | React 18 + TypeScript + Vite + Tailwind CSS |

Everything runs locally — no cloud accounts or API keys required.

---

## Prerequisites

Install these once on each machine before cloning:

### 1. Docker

Used to run PostgreSQL + pgvector.

- **macOS / Windows**: Install [Docker Desktop](https://www.docker.com/products/docker-desktop/).
  On Windows, enable WSL 2 integration:
  Settings → Resources → WSL Integration → toggle your distro → Apply & Restart.
- **Linux**: Install the `docker` daemon and the `docker compose` plugin.

### 2. uv (Python package manager)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Restart your shell afterwards so `uv` is on PATH. Verify with `uv --version`.

### 3. Node.js ≥ 20

Download from [nodejs.org](https://nodejs.org/) or use a version manager such as
`nvm`:

```bash
nvm install 20 && nvm use 20
```

### 4. Ollama

Ollama must be reachable at the URL configured in `backend/.env`
(`OLLAMA_BASE_URL`). It can run:

- **Locally** on the same machine (`http://localhost:11434`)
- **Remotely** on another machine in the network (e.g. `http://192.168.x.x:11434`)

Install locally:

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh
```

Pull the required models (only needed on the machine running Ollama):

```bash
ollama pull gemma4:26b           # chat + proposal generation (~17 GB)
ollama pull qwen3-embedding:4b   # embeddings (~2.5 GB)
```

> If you use a remote Ollama server, make sure the models are already pulled
> there and set `OLLAMA_BASE_URL` in `.env` to the remote address.

---

## First-time setup

```bash
git clone <repo-url> study-os-thesis
cd study-os-thesis
```

### Configure the backend

```bash
cd backend
cp .env.example .env
```

Open `backend/.env` and edit the values:

| Variable | What to set |
|---|---|
| `JWT_SECRET` | Generate a random secret: `python -c "import secrets; print(secrets.token_urlsafe(32))"` |
| `OLLAMA_BASE_URL` | URL of your Ollama instance, e.g. `http://localhost:11434` or `http://192.0.2.10:11434` (remote) |
| `OLLAMA_CHAT_MODEL` | Chat model pulled in Ollama, default `gemma4:26b` |
| `OLLAMA_EXTRACT_MODEL` | Model used for transcript extraction. Leave empty to fall back to `OLLAMA_CHAT_MODEL` |
| `OLLAMA_EMBED_MODEL` | Embedding model, default `qwen3-embedding:4b` |
| `OLLAMA_EMBED_DIM` | Must match the embedding model output dimension. `qwen3-embedding:4b` = `2560` |

All other values can stay as-is for local development.

---

## Running the project

The `debug.sh` script in the repository root orchestrates everything.

### Commands

#### `./debug.sh up`

**Start from scratch** (or after `down`).

1. Starts the Docker database container and waits for it to be healthy.
2. Installs/updates backend Python dependencies (`uv sync`).
3. Installs/updates frontend Node dependencies (`npm install`).
4. Runs Alembic database migrations (`alembic upgrade head`).
5. Seeds the database with the 3 Tübingen research chairs (idempotent — skips
   if chairs already exist).
6. Starts the backend (uvicorn on port **8000**) and frontend (Vite on port
   **5173**) in parallel.

```bash
./debug.sh up
```

Use this the first time, and any time after `./debug.sh down`.

---

#### `./debug.sh` (no arguments)

**Resume a running setup.** Assumes the Docker container is already healthy
and skips container startup. Runs the same dependency, migration, and seed
steps, then starts the servers.

```bash
./debug.sh
```

Use this for day-to-day development after the container is already running.
Faster than `up` because it skips the Docker healthcheck wait.

---

#### `./debug.sh down`

**Stop the Docker containers** (database). Does not remove the data volume —
your data is preserved.

```bash
./debug.sh down
```

To **wipe all data** and start fresh, use Docker directly:

```bash
docker compose down -v   # -v removes the named volume (deletes all DB data)
docker compose up -d     # recreate the container
```

---

### Accessing the services

| Service | URL |
|---|---|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| Swagger docs | http://localhost:8000/docs |

---

## Project layout

```
study-os-thesis/
├── backend/
│   ├── app/
│   │   ├── api/            FastAPI routers (auth, theses, chat, chairs, students, proposals, admin)
│   │   ├── auth/           JWT + password hashing
│   │   ├── llm/            Ollama HTTP client
│   │   ├── models/         SQLAlchemy ORM models
│   │   ├── repositories/   Data-access layer (one per model group)
│   │   ├── schemas/        Pydantic request/response schemas
│   │   ├── services/       Business logic (auth, chat agent, chairs, students, theses)
│   │   └── tools/          Hybrid thesis search (pgvector + BM25 + RRF)
│   ├── alembic/            DB migrations (0001 → 0007)
│   ├── scripts/
│   │   └── seed.py         Idempotent DB seed (3 Tübingen chairs)
│   ├── log_config.json     Uvicorn logging config
│   ├── pyproject.toml      Python dependencies (Python ≥ 3.13)
│   └── .env.example        Environment variable template
├── frontend/
│   └── src/
│       ├── api/            Typed API clients (client, chairs, students, theses)
│       ├── auth/           React auth context + JWT storage
│       ├── components/     Shared UI components (SideNav, TopBar, SkillRadar, …)
│       └── pages/          Dashboard, Chat, ChairExplorer, Proposals, Admin, Login, Register
├── docker-compose.yml      PostgreSQL 16 + pgvector on host port 5433
└── debug.sh                All-in-one dev launcher (up / down / no-args)
```

---

## Key features

### Students
- **Transcript upload** — Upload a PDF transcript of records. The system extracts
  text with `pypdf`, sends it to the LLM for structured extraction (courses,
  grades, ECTS), and computes a credit-weighted GPA.
- **Competency profile** — Courses are mapped to skill axes (Programming,
  Statistics, Databases, Projects, Web, Versioning) and displayed as a radar
  chart. A course profile embedding is stored for semantic chair matching.
- **AI chat (Find Thesis)** — Chat with the agent. It can search research chairs
  by semantic similarity, search open thesis proposals, and — when explicitly
  asked — generate personalised thesis proposals saved under "Meine Vorschläge".

### Professors / Admins
- **Chair management** — Create research chairs with name, description, and
  professor. Ingest ArXiv papers by ID; the abstract is fetched, embedded, and
  stored as a chair document for semantic search.
- **Thesis proposals** — Submit open thesis proposals linked to a chair.

---

## Roles

| Role | Capabilities |
|---|---|
| `student` | Upload transcript, chat, view proposals, receive AI-generated proposals |
| `professor` | All student capabilities + submit thesis proposals |
| `admin` | All capabilities + manage chairs, manage users |

Register at `/register`. Admins cannot self-register — create an admin via the
Swagger docs (`POST /api/admin/users`) or directly in the DB.

> **Note:** The Swagger UI at `/docs` is enabled in development mode. Disable it
> in production by removing the `docs_url` from the FastAPI constructor or
> restricting access to trusted networks only.

---

## Environment variables reference

All variables live in `backend/.env` (copied from `backend/.env.example`).

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `postgresql+asyncpg://<user>:<password>@localhost:5433/<db>` | SQLAlchemy async DB URL. Credentials must match those in `docker-compose.yml` |
| `JWT_SECRET` | *(must be set)* | HMAC secret for signing JWTs. Generate with `python -c "import secrets; print(secrets.token_urlsafe(32))"` |
| `JWT_ALGORITHM` | `HS256` | JWT signing algorithm |
| `JWT_EXPIRES_MINUTES` | `60` | Token lifetime in minutes |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Base URL of the Ollama server |
| `OLLAMA_CHAT_MODEL` | `gemma4:26b` | Model for chat and proposal generation |
| `OLLAMA_EXTRACT_MODEL` | *(empty → falls back to chat model)* | Model for transcript extraction. Use a smaller model if you want faster parsing |
| `OLLAMA_EMBED_MODEL` | `qwen3-embedding:4b` | Embedding model |
| `OLLAMA_EMBED_DIM` | `2560` | Must match the embedding model output dimension |
| `CORS_ORIGINS` | `http://localhost:5173` | Comma-separated allowed CORS origins |

---

## Troubleshooting

### `[Errno 48] Address already in use` on port 8000

A previous uvicorn process is still running. Kill it:

```bash
lsof -ti :8000 | xargs kill -9
```

### `DB container is not running/healthy` when running `./debug.sh` (no args)

The container is not started. Use `./debug.sh up` instead to start it first.

### Transcript upload fails with "LLM could not parse"

The chat model returned non-JSON output. This can happen with smaller models.
Try setting `OLLAMA_EXTRACT_MODEL` to a model that follows JSON instructions
reliably (e.g. `gemma4:26b`, `qwen3.5:27b`).

### Embedding dimension mismatch error on startup

`OLLAMA_EMBED_DIM` in `.env` doesn't match what the model actually outputs.
The startup log shows the actual dimension:
```
Ollama embed dim check passed: model=qwen3-embedding:4b dim=2560
```
Update `OLLAMA_EMBED_DIM` to match, then restart.

### `password authentication failed for user "thesis"`

A local Postgres on port 5432 may be conflicting. Our Docker container uses
host port **5433** — verify `DATABASE_URL` in `.env` ends with `:5433/thesis`.

If the container was previously started with wrong credentials, wipe the volume:

```bash
docker compose down -v
docker compose up -d
```

### `ModuleNotFoundError: No module named 'app'` when running a script

Run scripts from the `backend/` directory with `PYTHONPATH` set:

```bash
cd backend
PYTHONPATH=. uv run python scripts/seed.py
```

### Docker credential error in WSL (`exec format error`)

Docker Desktop's credential helper is a Windows binary. Clear the credential
store for WSL:

```bash
echo '{}' > ~/.docker/config.json
```
