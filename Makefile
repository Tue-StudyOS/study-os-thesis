.PHONY: check format

RUFF := backend/.venv/bin/ruff

check:
	$(RUFF) check backend
	$(RUFF) format --check backend

format:
	$(RUFF) format backend
