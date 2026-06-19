.PHONY: audit audit-backend check check-backend check-skills format

RUFF := backend/.venv/bin/ruff

check: check-backend check-skills

audit: audit-backend

audit-backend:
	cd backend && uv run --group audit pip-audit --local --progress-spinner off

check-backend:
	$(RUFF) check backend
	$(RUFF) format --check backend

check-skills:
	backend/.venv/bin/python -m pytest -q

format:
	$(RUFF) format backend
