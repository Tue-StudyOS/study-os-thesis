# Initial Project Memories für study-os-thesis

Speichere diese in Ruflo Memory für zukünftige SPARC-Tasks:

## 1. Projekt Stack

```bash
claude-flow memory store \
  --key "projekt/stack" \
  --value "Backend: FastAPI + SQLAlchemy 2.0 + Alembic Migrations + pytest. Frontend: React 19 + TypeScript + Vite + Tailwind CSS. Database: PostgreSQL. Auth: JWT (TBD). Tests: pytest (Backend), Vitest (Frontend)" \
  --namespace uni-projekt
```

## 2. Coding Konventionen

```bash
claude-flow memory store \
  --key "projekt/conventions" \
  --value "Backend: Python 3.10+, Type hints everywhere, SQLAlchemy models with pydantic schemas, pytest with fixtures. Frontend: Functional components, TypeScript strict mode, Tailwind utility classes. Git: Conventional commits (feat:, fix:, etc). Branch naming: feat/N-description, fix/N-description" \
  --namespace uni-projekt
```

## 3. Architektur-Entscheidungen

```bash
claude-flow memory store \
  --key "projekt/architecture" \
  --value "Monorepo mit /backend (FastAPI) und /frontend (React). DB: PostgreSQL mit Alembic migrations in backend/alembic/versions/. Models in backend/app/models/. API routes in backend/app/api/. Frontend components in frontend/src/components/. State management: React Query (server) + local useState (client)." \
  --namespace uni-projekt
```

## 4. Aktuelle Domain (Chair Discovery)

```bash
claude-flow memory store \
  --key "feature/chair-discovery" \
  --value "Schema: Universities 1:N Departments, Departments 1:N Chairs, Chairs 1:N Employees. Feature extends researchers as university-employee for chair discovery. Status: In development on feat/22-chair-employees-schema. Migrations: 0013 entity shape. Tests: integration tests for entity relationships." \
  --namespace uni-projekt
```

## 5. Testing Strategie

```bash
claude-flow memory store \
  --key "projekt/testing" \
  --value "Backend: Unit tests for business logic, integration tests for API endpoints with real DB (pytest fixtures). Frontend: Unit tests for components, integration tests for flows. TDD approach: write failing tests first, then implement. Aim for >80% coverage on new code." \
  --namespace uni-projekt
```

## 6. Wichtige Module

```bash
claude-flow memory store \
  --key "projekt/modules" \
  --value "Backend modules: models/ (SQLAlchemy entities), schemas/ (Pydantic validation), services/ (business logic), api/ (route handlers). Frontend modules: components/ (React components), pages/ (page-level components), hooks/ (custom hooks), api/ (API client calls), types/ (TypeScript types)." \
  --namespace uni-projekt
```

## Quick Setup für neue Session

Kopiere-Paste diese Befehle zu Sitzungsbeginn:

```bash
# 1. Load context
npx ts-node .claude-flow/project-context.ts

# 2. Recall all memories
claude-flow memory recall "projekt/*" --namespace uni-projekt

# 3. Get recommended SPARC command
npx ts-node scripts/suggest-sparc.ts

# 4. (Optional) Check what's currently open
git status
```

## Pro Tipps

### Nach Schema-/Migration-Work

```bash
claude-flow memory store \
  --key "migration/[name]" \
  --value "Migration 001X: [Was wurde geändert]. Changed tables: []. New tables: []. Backwards compatible: [ja/nein]" \
  --namespace uni-projekt
```

### Nach neuer Feature

```bash
claude-flow memory store \
  --key "feature/[name]" \
  --value "Feature [name]: Implemented [what]. Files changed: []. Tests: [number]. Status: [ready|in-progress|blocked]" \
  --namespace uni-projekt
```

### Issues/Blockers

```bash
claude-flow memory store \
  --key "blocker/[name]" \
  --value "Issue: [description]. Root cause: []. Workaround: []. Solution in progress: [link]" \
  --namespace uni-projekt
```

---

**Hinweis:** Diese Memories solltest du in den nächsten 30 Minuten eingeben. Sie sind die Grundlage für optimale SPARC-Befehle in allen zukünftigen Tasks!
