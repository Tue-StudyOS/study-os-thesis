.PHONY: check check-skills evals multiturn-evals app-bundle

# The web-app backend was removed in the skill-architecture pivot. The old
# FastAPI/Celery/Postgres stack is archived on the legacy/web-app branch.

check: check-skills

check-skills:
	python -m pytest -q

evals:
	RUN_DEEPEVAL=1 python -m pytest -m eval -q

multiturn-evals:
	python scripts/run_codex_multiturn_eval.py --runner fixture

app-bundle:
	python -m scripts.build_app_bundle
