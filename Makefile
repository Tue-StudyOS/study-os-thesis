.PHONY: audit audit-backend audit-frontend check check-backend check-frontend format

RUFF := backend/.venv/bin/ruff

check: check-backend check-frontend

audit: audit-backend audit-frontend

audit-backend:
	cd backend && reqfile=$$(mktemp /tmp/study-os-req.XXXXXX) && uv export --frozen --no-hashes --no-emit-project --group dev --group audit --output-file "$$reqfile" >/dev/null && .venv/bin/pip-audit -r "$$reqfile" --progress-spinner off; code=$$?; rm -f "$$reqfile"; exit $$code

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
