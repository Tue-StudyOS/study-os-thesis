# study-os-thesis — Claude Project Kontext
**Generiert:** 2026-06-09 | **Branch:** `feat/i18n-settings-page`

---

## Was das Projekt ist
KI-gestützter Thesis-Advisor für Universitätsstudenten. Studenten laden ihr
Transcript of Records hoch, das System analysiert ihr Kurseprofil, und ein
LLM-Agent empfiehlt passende Lehrstühle und generiert personalisierte
Thesisvorschläge. Professoren und Admins verwalten Lehrstühle und Proposals
über ein Admin-Interface.

GitHub: https://github.com/ValentinJSchmidt/study-os-thesis

---

## Stack

| Schicht | Technologie |
|---|---|
| Backend | FastAPI + async SQLAlchemy + Alembic, gemanagt mit `uv` |
| Datenbank | PostgreSQL 16 + pgvector (Docker, Host-Port **5433**) |
| LLM Chat | Ollama — gemma4:26b (Standard) |
| LLM Embeddings | Ollama — qwen3-embedding:4b (2560-dim Vektoren) |
| Frontend | React 18 + TypeScript + Vite + Tailwind CSS v4 |
| Task Queue | Celery + Redis |

---

## Projekt-Layout

```
study-os-thesis/
├── backend/
│   ├── app/
│   │   ├── api/            FastAPI Routers (auth, theses, chat, chairs, students, proposals, admin)
│   │   ├── auth/ auth_core/ JWT + Password Hashing
│   │   ├── chairs/         Chair-Domain (Service, Repository, Schemas)
│   │   ├── chat/           ChatService = ReAct-Agent-Loop (max 6 Iterationen)
│   │   ├── jobs/           Job-Status-Tracking
│   │   ├── llm/            LLMPort Protocol + OllamaClient + LiteLLMAdapter
│   │   ├── models/         SQLAlchemy ORM: user, chair, chat, student, thesis, paper, job, researcher
│   │   ├── papers/         Papers-Domain
│   │   ├── proposals/      Proposals-Domain
│   │   ├── repositories/   Data-Access-Layer (ein Repo pro Domain)
│   │   ├── researchers/    Researcher-Domain
│   │   ├── schemas/        Pydantic Request/Response Schemas
│   │   ├── scraper/        OpenAlex-Scraper
│   │   ├── services/       Business Logic
│   │   ├── students/       Student-Domain
│   │   ├── theses/         Thesis-Domain
│   │   ├── tools/          Hybrid Thesis Search (pgvector + BM25 + RRF)
│   │   ├── worker/         Celery Worker
│   │   └── ws/             WebSocket (Redis Pub/Sub)
│   ├── alembic/versions/   12 Migrationen, aktuell: 0012_openalex_only_cleanup
│   └── tests/              unit/ | integration/ | e2e/ | evals/
├── frontend/src/
│   ├── api/                Typed API Clients
│   ├── auth/               React Auth Context + JWT Storage
│   ├── components/         SideNav, TopBar, SkillRadar, …
│   └── pages/              Dashboard, Chat, ChairExplorer, Proposals, Admin, Login, Register
├── docker-compose.yml      PostgreSQL 16 + pgvector + Redis
├── debug.sh                All-in-one Dev-Launcher (up / down / kein Arg)
└── Makefile                make check | make audit | make format
```

---

## Architektur-Kernprinzipien

1. **Port-Adapter für LLM** — `LLMPort` Protocol entkoppelt Business-Logik vom Provider. Zwei Singletons: `llm_chat_client` + `llm_embed_client` (erlaubt Mischen von Providern).
2. **ReAct-Agent-Loop** — `ChatService` macht Reason→Act→Observe, max. 6 Iterationen. Tools: `search_chairs`, `search_theses`, `generate_proposal`.
3. **Hybrid Search** — pgvector (cosine) + PostgreSQL tsvector/GIN (BM25), fusioniert mit RRF. Beide Legs laufen parallel via `asyncio.gather`. Fallback: nur BM25 wenn Ollama offline.
4. **Kein HNSW** — 2560-dim Vektoren übersteigen pgvectors Limit (2000) → Sequential Scan. Bei Forschungsprojekt-Scale ok.
5. **Atomare Message-Commits** — Alle Nachrichten eines Agent-Turns werden geflusht, aber erst am Ende committed. Verhindert partielle Turns bei Fehler.
6. **Celery für schwere Ops** — LLM-Calls, PDF-Parsing, Embedding-Generation laufen über Worker. HTTP-Controller dispatcht und antwortet sofort.

---

## Datenbankschema (Kerntabellen)

- `users` — id, email, password_hash, role (student|professor|admin)
- `students` — user_id FK, program, gpa, **profile_embedding vector(2560)**
- `student_courses` — student_id, course_name, credits, grade
- `chairs` — id, name, short_description, professor_name, professor_user_id FK
- `chair_documents` — chair_id FK, kind, title, content, **embedding vector(2560)**
- `theses` — id, title, abstract, chair_id FK, source, **embedding vector(2560)**, **search_vec TSVECTOR GENERATED**
- `chat_sessions` + `chat_messages` — role, content, tool_calls jsonb, tool_call_id, tool_name
- `papers` — chair_id, title, abstract, doi, source=openalex
- `researchers` — chair_id FK, name, university employee fields (seit Migration 0013)
- `jobs` — Status-Tracking für async Celery Tasks

---

## Dev-Workflow

```bash
# Starten (erstmalig oder nach down)
./debug.sh up

# Starten (täglich, Container läuft bereits)
./debug.sh

# Qualitätsgates vor PR
make check         # Ruff lint/format + Vitest + Frontend Build
make audit         # pip-audit + npm audit

# Tests
cd backend && uv run pytest                         # alle
cd backend && uv run pytest -m unit                 # nur unit
cd backend && uv run pytest -m integration          # braucht DB

# LLM Evals (optional, braucht DeepEval-Config)
cd backend && uv sync --group eval
RUN_DEEPEVAL=1 uv run pytest tests/evals -m eval -p no:rerunfailures

# Ruff formatieren
make format

# CI-Status nach PR-Push
gh pr checks
```

---

## Services

| Service | URL |
|---|---|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| Swagger Docs | http://localhost:8000/docs |

---

## Rollen

| Rolle | Fähigkeiten |
|---|---|
| `student` | Transcript upload, Chat, Proposals ansehen, KI-Proposals erhalten |
| `professor` | Alles von student + Thesis-Proposals einreichen |
| `admin` | Alles + Lehrstühle/User verwalten |

Admin anlegen: `POST /api/admin/users` via Swagger oder direkt in DB.

---

## Konventionen

- **Branch-Naming**: `feat/…`, `fix/…`, `docs/…`, `ci/…`, `chore/…`
- **Commit-Format**: Conventional Commits (`feat:`, `fix:`, `ci:`, `docs:`, `chore:`), Imperativ, kein Punkt
- **PR-Template**: Summary + Motivation + What Changed + Known Issues + How to Test, `Closes #N`
- **CI grün** vor Review-Request: `gh pr checks`
- Keine Abstraktion für Einzel-Verwendung, keine spekulativen Features
- Python: Ruff, line-length 180, Python 3.13 strikt

---

## Umgebungsvariablen (backend/.env)

| Variable | Standard |
|---|---|
| `DATABASE_URL` | `postgresql+asyncpg://thesis:thesis@localhost:5433/thesis` |
| `JWT_SECRET` | *(muss gesetzt werden)* |
| `OLLAMA_BASE_URL` | `http://localhost:11434` |
| `OLLAMA_CHAT_MODEL` | `gemma4:26b` |
| `OLLAMA_EMBED_MODEL` | `qwen3-embedding:4b` |
| `OLLAMA_EMBED_DIM` | `2560` |
| `CORS_ORIGINS` | `http://localhost:5173` |

---

## Aktueller Stand

### Branch
```
feat/i18n-settings-page
```

### Letzte Commits
```
9919dcb feat: enhance settings with profile fields and remove /help link
a23b0b5 feat: complete settings and help page (issue #29)
00dcec9 feat: translate all pages to support full i18n in German and English
096d85f feat: add full i18n translations to all pages
28209a4 feat: implement i18n with language switching and localStorage persistence
ea6c9da chore: ignore local workflow files (WORKFLOW.md, script changes)
0f2049f Merge pull request #30 from ValentinJSchmidt/fix/migration-0012-enum-single-tx
ce10ca4 fix: make 0012 enum cleanup safe in single-transaction upgrade
```

### Offene Issues
- #36 backend: implement chair-discovery scraping agent
- #33 When using deepseek you get duplicates for the first two papers
- #32 add tag for the papers
- #29 Implementation of the help and settings page
- #25 Have markdown rendering for nice formating
- #23 Make language both available in english and german and well
- #22 Implement an intelligent agent, which automatically fetches all the chair information from the university page
- #18 Weird loading bug with the icon when you start up the app
- #16 Replace the dummy skill computation with a real one
- #15 UI does has some weird formatting error
- #14 Change the starting prompt
- #13 test the app with deepseek
- #7 Optimize RAG capabilities for better results
- #6 Add deepeval
- #5 Implement Port-Adapter Pattern for Model Providers
- #4 Implement OCR engine instead of plain local LLM
