"""Deterministic checks for Codex-native multi-turn eval scaffolding."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SIM_DIR = REPO_ROOT / "skills" / "tests" / "simulations"
RUNNER_PATH = REPO_ROOT / "scripts" / "run_codex_multiturn_eval.py"
PERSONAS = {"terse-user", "deep-user", "standard-user"}


def _load_runner():
    spec = importlib.util.spec_from_file_location("run_codex_multiturn_eval", RUNNER_PATH)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_multiturn_eval_resources_exist() -> None:
    for persona in PERSONAS:
        persona_path = SIM_DIR / "personas" / f"{persona}.md"
        assert persona_path.is_file()
        persona_text = persona_path.read_text(encoding="utf-8")
        assert "## Hidden Profile" in persona_text
        assert "## Disclosure Rules" in persona_text
        assert "## Response Style" in persona_text
        assert "## Anti-Behavior" in persona_text
        assert (SIM_DIR / "fixtures" / f"{persona}.json").is_file()

    assert (SIM_DIR / "scenarios" / "ml-master-thesis.md").is_file()
    assert (SIM_DIR / "rubrics" / "conversation-rubric.md").is_file()


def test_fixture_runs_have_valid_turns() -> None:
    for persona in PERSONAS:
        data = json.loads((SIM_DIR / "fixtures" / f"{persona}.json").read_text(encoding="utf-8"))
        assert data["persona_id"] == persona
        assert data["runner"] == "fixture"
        assert data["turns"]
        assert data["turns"][0]["role"] == "user"
        assert {turn["role"] for turn in data["turns"]} == {"user", "assistant"}
        for turn in data["turns"]:
            assert turn["role"] in {"user", "assistant"}
            assert turn["content"].strip()


def test_fixture_export_writes_markdown_and_json(tmp_path: Path) -> None:
    runner = _load_runner()
    run = runner.load_fixture_run("terse-user", max_turns=10)
    runner.write_run(run, tmp_path)

    run_json = tmp_path / "runs" / "terse-user.json"
    run_md = tmp_path / "runs" / "terse-user.md"
    assert run_json.is_file()
    assert run_md.is_file()

    exported = json.loads(run_json.read_text(encoding="utf-8"))
    assert exported["persona_id"] == "terse-user"
    assert exported["user_runner"] == "fixture"
    assert exported["simulator_metadata"]["user_response_mode"] == "scripted-fixture"
    markdown = run_md.read_text(encoding="utf-8")
    assert "## Metadata" in markdown
    assert "## Persona" in markdown
    assert "## Hidden Profile" in markdown
    assert "## Transcript" in markdown
    assert "### Turn 1: User" in markdown
    assert "### Turn 2: Assistant" in markdown


def test_deepeval_kwargs_are_conversation_level() -> None:
    runner = _load_runner()
    run = runner.load_fixture_run("deep-user", max_turns=10)
    kwargs = runner.deepeval_test_case_kwargs(run)

    assert kwargs["name"] == "deep-user-full-conversation"
    assert "machine learning master's student" in kwargs["scenario"]
    assert "profile" in kwargs["expected_outcome"].lower()
    assert "detailed" in kwargs["user_description"].lower()
    assert kwargs["turns"] == run["turns"]


def test_metric_specs_cover_required_eval_dimensions() -> None:
    runner = _load_runner()
    names = {spec["name"] for spec in runner.metric_specs()}
    assert {
        "workflow_compliance",
        "profile_depth",
        "shallow_profile_guardrail",
        "memory_retention",
        "question_quality",
        "evidence_discipline",
        "student_usefulness",
        "user_simulation_realism",
    } <= names


def test_user_simulator_prompt_is_student_only() -> None:
    runner = _load_runner()
    scenario = runner.load_scenario()
    persona = runner.load_persona("terse-user")
    turns = [
        {"role": "user", "content": scenario.initial_user_message},
        {"role": "assistant", "content": "Welche ML-Themen interessieren dich?"},
    ]

    prompt = runner.user_simulator_prompt(scenario, persona, turns, max_turns=6)

    assert "simulated student user" in prompt
    assert "not an assistant" in prompt
    assert "Do not explain the eval" in prompt
    assert "Hidden profile:" in prompt
    assert "Disclosure rules:" in prompt
    assert "Anti-behavior:" in prompt


def test_fixture_user_runner_preserves_scripted_turns() -> None:
    runner = _load_runner()
    fixture = runner.load_fixture_run("standard-user", max_turns=10)
    turns = fixture["turns"][:2]

    next_user = runner.next_user_response(
        "standard-user",
        "fixture",
        turns,
        max_turns=10,
        timeout=1,
    )

    assert next_user == fixture["turns"][2]["content"]
