.PHONY: audit audit-backend audit-frontend check check-backend check-frontend format

RUFF := backend/.venv/bin/ruff

check: check-backend check-frontend

audit: audit-backend audit-frontend

audit-backend:
	cd backend && uv run --group audit pip-audit --local --progress-spinner off

audit-frontend:
	cd frontend && npm audit --audit-level=moderate

check-backend:
	$(RUFF) check backend
	$(RUFF) format --check backend

check-frontend:
	cd frontend && npm run test
	cd frontend && npm run build

format:
	$(RUFF) format backend
