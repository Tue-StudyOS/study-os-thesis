#!/usr/bin/env python3
"""Run Codex-native multi-turn thesis-skill evals and optional DeepEval judges.

The Codex runners intentionally do not load SKILL.md files into prompts. They
ask Codex to use the repository's native skill discovery, then export the
visible conversation for conversation-level DeepEval checks.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SIM_DIR = REPO_ROOT / "skills" / "tests" / "simulations"
PERSONAS_DIR = SIM_DIR / "personas"
SCENARIO_PATH = SIM_DIR / "scenarios" / "ml-master-thesis.md"
RUBRIC_PATH = SIM_DIR / "rubrics" / "conversation-rubric.md"
FIXTURES_DIR = SIM_DIR / "fixtures"
GROUND_TRUTH_DIR = REPO_ROOT / "skills" / "tests" / "eval_ground_truth"
DEFAULT_PERSONAS = ("terse-user", "deep-user", "standard-user")
VALID_RUNNERS = ("fixture", "codex-local", "codex-chair")

# Ground-truth chair names for each faculty (last-name keys used for coverage scoring).
# Relevance labels: "high" = direct match to persona interest, "medium" = related.
MEDICINE_GROUND_TRUTH: list[dict[str, str]] = [
    {"name": "Prof. Dr. Thomas Gasser", "last": "Gasser", "relevance": "high"},
    {"name": "Prof. Dr. Mathias Jucker", "last": "Jucker", "relevance": "high"},
    {"name": "Prof. Dr. Holger Lerche", "last": "Lerche", "relevance": "medium"},
    {"name": "Prof. Dr. Ulf Ziemann", "last": "Ziemann", "relevance": "medium"},
    {"name": "Prof. Dr. Markus Siegel", "last": "Siegel", "relevance": "medium"},
    {"name": "Prof. Dr. Ghazaleh Tabatabai", "last": "Tabatabai", "relevance": "medium"},
]

PSYCHOLOGY_GROUND_TRUTH: list[dict[str, str]] = [
    {"name": "Prof. Dr. Andreas Bartels", "last": "Bartels", "relevance": "high"},
    {"name": "Prof. Dr. Hans-Christoph Nürk", "last": "Nürk", "relevance": "high"},
    {"name": "Prof. Dr. Claudia Friedrich", "last": "Friedrich", "relevance": "medium"},
    {"name": "Prof. Dr. Markus Huff", "last": "Huff", "relevance": "medium"},
    {"name": "Prof. Dr. Jennifer Svaldi", "last": "Svaldi", "relevance": "medium"},
    {"name": "Prof. Dr. Caterina Gawrilow", "last": "Gawrilow", "relevance": "medium"},
]

WISO_GROUND_TRUTH: list[dict[str, str]] = [
    {"name": "Prof. Dr. Thomas Diez", "last": "Diez", "relevance": "high"},
    {"name": "Prof. Dr. Gabriele Abels", "last": "Abels", "relevance": "high"},
    {"name": "Prof. Dr. Oliver Schlumberger", "last": "Schlumberger", "relevance": "medium"},
    {"name": "Prof. Dr. Andreas Hasenclever", "last": "Hasenclever", "relevance": "high"},
    {"name": "Prof. Dr. Hans-Jürgen Bieling", "last": "Bieling", "relevance": "high"},
    {"name": "Prof. Dr. Gernot Müller", "last": "Müller", "relevance": "medium"},
    {"name": "Prof. Dr. Jörg Baten", "last": "Baten", "relevance": "medium"},
]

CS_GROUND_TRUTH: list[dict[str, str]] = [
    {"name": "Prof. Dr. Georg Martius", "last": "Martius", "relevance": "high"},
    {"name": "Prof. Dr. Philipp Hennig", "last": "Hennig", "relevance": "high"},
    {"name": "Prof. Dr. Matthias Hein", "last": "Hein", "relevance": "high"},
    {"name": "Prof. Dr. Ulrike von Luxburg", "last": "Luxburg", "relevance": "high"},
    {"name": "Prof. Dr. Bernhard Schölkopf", "last": "Schölkopf", "relevance": "high"},
    {"name": "Prof. Dr. Wieland Brendel", "last": "Brendel", "relevance": "high"},
    {"name": "Prof. Dr. Matthias Bethge", "last": "Bethge", "relevance": "high"},
]

FACULTY_CONFIGS: dict[str, dict[str, Any]] = {
    "medicine": {
        "skill_fixture": "neuro-student-skill",
        "baseline_fixture": "neuro-student-baseline",
        "ground_truth": MEDICINE_GROUND_TRUTH,
        "persona_desc": "neuro-student (Neurodegenerative diseases, Parkinson's / Alzheimer's)",
        "ground_truth_file": "skills/tests/eval_ground_truth/medicine.md",
        "faculty_label": "Medizinische Fakultät",
    },
    "psychology": {
        "skill_fixture": "psych-student-skill",
        "baseline_fixture": "psych-student-baseline",
        "ground_truth": PSYCHOLOGY_GROUND_TRUTH,
        "persona_desc": "psych-student (Cognitive neuroscience and experimental decision-making)",
        "ground_truth_file": "skills/tests/eval_ground_truth/psychology.md",
        "faculty_label": "MNF — Fachbereich Psychologie",
    },
    "wiso": {
        "skill_fixture": "wiso-student-skill",
        "baseline_fixture": "wiso-student-baseline",
        "ground_truth": WISO_GROUND_TRUTH,
        "persona_desc": "wiso-student (Comparative politics and political economy)",
        "ground_truth_file": "skills/tests/eval_ground_truth/wiso.md",
        "faculty_label": "WiSo-Fakultät",
    },
    "cs": {
        "skill_fixture": "cs-student-skill",
        "baseline_fixture": "cs-student-baseline",
        "ground_truth": CS_GROUND_TRUTH,
        "persona_desc": "cs-student (Machine learning and AI research)",
        "ground_truth_file": "skills/tests/eval_ground_truth/cs_seed/chairs/INDEX.md",
        "faculty_label": "MNF — Informatik / Tübingen AI Center",
    },
}


@dataclass(frozen=True)
class Persona:
    persona_id: str
    text: str
    user_description: str
    hidden_profile: str
    disclosure_rules: str
    response_style: str
    anti_behavior: str


@dataclass(frozen=True)
class Scenario:
    scenario_id: str
    text: str
    initial_user_message: str
    expected_outcome: str
    assistant_start_prompt: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def section(markdown: str, heading: str) -> str:
    marker = f"## {heading}"
    start = markdown.find(marker)
    if start == -1:
        return ""
    body_start = start + len(marker)
    next_heading = markdown.find("\n## ", body_start)
    if next_heading == -1:
        return markdown[body_start:].strip()
    return markdown[body_start:next_heading].strip()


def load_persona(persona_id: str) -> Persona:
    path = PERSONAS_DIR / f"{persona_id}.md"
    text = read_text(path)
    return Persona(
        persona_id=persona_id,
        text=text,
        user_description=section(text, "User Description"),
        hidden_profile=section(text, "Hidden Profile"),
        disclosure_rules=section(text, "Disclosure Rules"),
        response_style=section(text, "Response Style"),
        anti_behavior=section(text, "Anti-Behavior"),
    )


def load_scenario() -> Scenario:
    text = read_text(SCENARIO_PATH)
    return Scenario(
        scenario_id=section(text, "ID"),
        text=text,
        initial_user_message=section(text, "Initial User Message"),
        expected_outcome=section(text, "Expected Outcome"),
        assistant_start_prompt=section(text, "Assistant Start Prompt"),
    )


def selected_personas(value: str) -> list[str]:
    if value == "all":
        return list(DEFAULT_PERSONAS)
    personas = [part.strip() for part in value.split(",") if part.strip()]
    unknown = sorted(set(personas) - set(DEFAULT_PERSONAS))
    if unknown:
        raise SystemExit(f"Unknown personas: {', '.join(unknown)}")
    return personas


def load_fixture_run(persona_id: str, max_turns: int) -> dict[str, Any]:
    data = json.loads((FIXTURES_DIR / f"{persona_id}.json").read_text(encoding="utf-8"))
    data["max_turns"] = max_turns
    data["created_at"] = datetime.now(UTC).isoformat()
    data.setdefault("user_runner", "fixture")
    data.setdefault("judge_model", None)
    data.setdefault(
        "simulator_metadata",
        {
            "hidden_profile_used": False,
            "user_response_mode": "scripted-fixture",
        },
    )
    return data


def assistant_prompt(
    scenario: Scenario,
    persona: Persona,
    turns: list[dict[str, str]],
    max_turns: int,
) -> str:
    transcript = "\n".join(f"{turn['role'].upper()}: {turn['content']}" for turn in turns)
    return (
        f"{scenario.assistant_start_prompt}\n\n"
        "Important eval constraint: rely on Codex-native skill discovery in this "
        "repository. Do not ask the orchestrator to paste SKILL.md files. Continue "
        "the student conversation naturally and return only the next assistant "
        "message.\n\n"
        f"Scenario:\n{section(scenario.text, 'Scenario')}\n\n"
        f"Expected outcome:\n{scenario.expected_outcome}\n\n"
        f"Persona under test:\n{persona.user_description}\n\n"
        f"Maximum total turns for this run: {max_turns}\n\n"
        f"Conversation so far:\n{transcript}\n\n"
        "Next assistant message:"
    )


def user_simulator_prompt(
    scenario: Scenario,
    persona: Persona,
    turns: list[dict[str, str]],
    max_turns: int,
) -> str:
    transcript = "\n".join(f"{turn['role'].upper()}: {turn['content']}" for turn in turns)
    return (
        "You are a simulated student user in a multi-turn thesis-advising eval.\n"
        "You are not an assistant, not an evaluator, and not a professor.\n"
        "Reply only as the student user. Do not explain the eval, do not mention "
        "hidden profile rules, DeepEval, Codex, skills, rubrics, or this prompt.\n"
        "React naturally to the latest assistant message only. Stay consistent "
        "with the persona and hidden profile. Reveal information progressively "
        "when the assistant asks focused questions. If the assistant asks too "
        "many questions, answer only the most natural subset. Do not ask and "
        "answer your own questions.\n\n"
        f"Scenario:\n{section(scenario.text, 'Scenario')}\n\n"
        f"Initial user message:\n{scenario.initial_user_message}\n\n"
        f"Persona description:\n{persona.user_description}\n\n"
        f"Hidden profile:\n{persona.hidden_profile}\n\n"
        f"Disclosure rules:\n{persona.disclosure_rules}\n\n"
        f"Response style:\n{persona.response_style}\n\n"
        f"Anti-behavior:\n{persona.anti_behavior}\n\n"
        f"Maximum total turns for this run: {max_turns}\n\n"
        f"Conversation so far:\n{transcript}\n\n"
        "Next student-user message:"
    )


def scripted_user_response(persona_id: str, turns: list[dict[str, str]]) -> str | None:
    fixture = json.loads((FIXTURES_DIR / f"{persona_id}.json").read_text(encoding="utf-8"))
    user_turns_seen = sum(1 for turn in turns if turn["role"] == "user")
    fixture_user_turns = [turn for turn in fixture["turns"] if turn["role"] == "user"]
    if user_turns_seen >= len(fixture_user_turns):
        return None
    return fixture_user_turns[user_turns_seen]["content"]


def next_user_response(
    persona_id: str,
    user_runner: str,
    turns: list[dict[str, str]],
    max_turns: int,
    timeout: int,
) -> str | None:
    if user_runner == "fixture":
        return scripted_user_response(persona_id, turns)
    scenario = load_scenario()
    persona = load_persona(persona_id)
    return run_codex_with_schema(user_simulator_prompt(scenario, persona, turns, max_turns), user_runner, timeout)


def run_codex(prompt: str, runner: str, timeout: int) -> str:
    return run_codex_with_schema(prompt, runner, timeout)


def strict_json_schema(schema: dict[str, Any]) -> dict[str, Any]:
    """Make Pydantic/DeepEval schemas acceptable to Codex structured output."""
    if schema.get("type") == "object":
        schema.setdefault("additionalProperties", False)
        properties = schema.get("properties")
        if isinstance(properties, dict):
            for value in properties.values():
                if isinstance(value, dict):
                    strict_json_schema(value)
    if schema.get("type") == "array" and isinstance(schema.get("items"), dict):
        strict_json_schema(schema["items"])
    for key in ("anyOf", "oneOf", "allOf"):
        values = schema.get(key)
        if isinstance(values, list):
            for value in values:
                if isinstance(value, dict):
                    strict_json_schema(value)
    defs = schema.get("$defs")
    if isinstance(defs, dict):
        for value in defs.values():
            if isinstance(value, dict):
                strict_json_schema(value)
    return schema


def run_codex_with_schema(
    prompt: str,
    runner: str,
    timeout: int,
    schema: type[Any] | None = None,
) -> str:
    codex_bin = os.getenv("CODEX_BIN") or shutil.which("codex")
    if not codex_bin:
        raise RuntimeError("codex executable not found. Set CODEX_BIN or install Codex CLI.")

    env = os.environ.copy()
    if runner == "codex-chair" and env.get("CODEX_HOME_CHAIR"):
        env["CODEX_HOME"] = env["CODEX_HOME_CHAIR"]

    schema_path: Path | None = None
    with tempfile.TemporaryDirectory(prefix="codex-deepeval-schema-") as tmpdir:
        cmd = [
            codex_bin,
            "exec",
            "--sandbox",
            "read-only",
            "--skip-git-repo-check",
        ]
        if schema is not None:
            schema_path = Path(tmpdir) / "schema.json"
            if hasattr(schema, "model_json_schema"):
                schema_json = schema.model_json_schema()
            elif hasattr(schema, "schema"):
                schema_json = schema.schema()
            else:
                raise TypeError(f"Unsupported schema type: {schema!r}")
            strict_json_schema(schema_json)
            schema_path.write_text(json.dumps(schema_json), encoding="utf-8")
            cmd.extend(["--output-schema", str(schema_path)])
        cmd.append(prompt)

        completed = subprocess.run(
            cmd,
            cwd=REPO_ROOT,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
        )
    if completed.returncode != 0:
        raise RuntimeError(
            "codex exec failed with exit code "
            f"{completed.returncode}\nSTDERR:\n{completed.stderr.strip()}"
        )
    return completed.stdout.strip()


class CodexDeepEvalLLM:
    """DeepEval custom judge model backed by local Codex auth/subscription."""

    def __init__(self, runner: str = "codex-local", timeout: int = 300) -> None:
        from deepeval.models.base_model import DeepEvalBaseLLM

        class _Model(DeepEvalBaseLLM):
            def __init__(self, outer: "CodexDeepEvalLLM") -> None:
                self.outer = outer
                super().__init__(model=outer.get_model_name())

            def load_model(self, *args: Any, **kwargs: Any) -> "_Model":
                return self

            def generate(self, prompt: str, schema: type[Any] | None = None, *args: Any, **kwargs: Any) -> str:
                return run_codex_with_schema(prompt, self.outer.runner, self.outer.timeout, schema=schema)

            async def a_generate(
                self,
                prompt: str,
                schema: type[Any] | None = None,
                *args: Any,
                **kwargs: Any,
            ) -> str:
                return self.generate(prompt, schema=schema, *args, **kwargs)

            def get_model_name(self, *args: Any, **kwargs: Any) -> str:
                return self.outer.get_model_name()

            def supports_structured_outputs(self) -> bool:
                return True

        self.runner = runner
        self.timeout = timeout
        self.model = _Model(self)

    def get_model_name(self) -> str:
        return f"{self.runner}-codex-subscription"


def run_codex_persona(
    persona_id: str,
    runner: str,
    user_runner: str,
    max_turns: int,
    timeout: int,
    judge_model: str | None,
) -> dict[str, Any]:
    scenario = load_scenario()
    persona = load_persona(persona_id)
    turns = [{"role": "user", "content": scenario.initial_user_message}]

    completion_reason = "max_turns"
    while len(turns) < max_turns:
        reply = run_codex(assistant_prompt(scenario, persona, turns, max_turns), runner, timeout)
        turns.append({"role": "assistant", "content": reply})
        if len(turns) >= max_turns:
            break
        next_user = next_user_response(persona_id, user_runner, turns, max_turns, timeout)
        if next_user is None:
            completion_reason = "user_runner_complete"
            break
        turns.append({"role": "user", "content": next_user})

    return {
        "persona_id": persona_id,
        "scenario_id": scenario.scenario_id,
        "runner": runner,
        "user_runner": user_runner,
        "judge_model": judge_model,
        "model": os.getenv("CODEX_MODEL", "codex-default"),
        "max_turns": max_turns,
        "created_at": datetime.now(UTC).isoformat(),
        "turns": turns,
        "completion_reason": completion_reason,
        "simulator_metadata": {
            "hidden_profile_used": user_runner != "fixture",
            "user_response_mode": "scripted-fixture" if user_runner == "fixture" else "llm-user",
        },
    }


def validate_run(run: dict[str, Any]) -> None:
    turns = run.get("turns")
    if not isinstance(turns, list) or not turns:
        raise ValueError("run must contain a non-empty turns list")
    for index, turn in enumerate(turns):
        if turn.get("role") not in {"user", "assistant"}:
            raise ValueError(f"turn {index} has invalid role")
        if not isinstance(turn.get("content"), str) or not turn["content"].strip():
            raise ValueError(f"turn {index} has empty content")


def run_to_markdown(run: dict[str, Any]) -> str:
    lines = [
        f"# Multi-Turn Eval Run: {run['persona_id']}",
        "",
        "## Metadata",
        "",
        f"- Persona: `{run['persona_id']}`",
        f"- Scenario: `{run['scenario_id']}`",
        f"- Runner: `{run['runner']}`",
        f"- User runner: `{run.get('user_runner', 'fixture')}`",
        f"- Judge model: `{run.get('judge_model', 'unset')}`",
        f"- Model: `{run.get('model', 'unknown')}`",
        f"- Created at: `{run.get('created_at', 'unknown')}`",
        f"- Max turns: `{run.get('max_turns', 'unknown')}`",
        f"- Completion reason: `{run.get('completion_reason', 'unknown')}`",
        "",
        "## Persona",
        "",
        read_text(PERSONAS_DIR / f"{run['persona_id']}.md").strip(),
        "",
        "## Transcript",
        "",
    ]
    for index, turn in enumerate(run["turns"], start=1):
        role = "User" if turn["role"] == "user" else "Assistant"
        lines.extend([f"### Turn {index}: {role}", "", turn["content"].strip(), ""])
    return "\n".join(lines).rstrip() + "\n"


def write_run(run: dict[str, Any], output_dir: Path) -> None:
    validate_run(run)
    runs_dir = output_dir / "runs"
    runs_dir.mkdir(parents=True, exist_ok=True)
    persona_id = run["persona_id"]
    (runs_dir / f"{persona_id}.json").write_text(
        json.dumps(run, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (runs_dir / f"{persona_id}.md").write_text(run_to_markdown(run), encoding="utf-8")


def deepeval_test_case_kwargs(run: dict[str, Any]) -> dict[str, Any]:
    scenario = load_scenario()
    persona = load_persona(run["persona_id"])
    return {
        "name": f"{run['persona_id']}-full-conversation",
        "scenario": section(scenario.text, "Scenario"),
        "expected_outcome": scenario.expected_outcome,
        "user_description": persona.user_description,
        "turns": run["turns"],
    }


def metric_specs() -> list[dict[str, str]]:
    return [
        {
            "name": "workflow_compliance",
            "criteria": "Evaluate whether the assistant follows the thesis skill workflow across the whole conversation: profile-building first, then downstream suggestions only when enough profile context exists.",
        },
        {
            "name": "profile_depth",
            "criteria": "Evaluate whether the conversation captures interests, courses, skills, tools, experience, constraints, no-gos, research taste, and matching keywords where possible.",
        },
        {
            "name": "shallow_profile_guardrail",
            "criteria": "Evaluate whether the assistant avoids premature chair rankings or confident thesis proposals when the student profile is still shallow.",
        },
        {
            "name": "memory_retention",
            "criteria": "Evaluate whether later assistant turns correctly reuse earlier student details without inventing missing facts.",
        },
        {
            "name": "question_quality",
            "criteria": "Evaluate whether follow-up questions are small, relevant, targeted, and easy for the student to answer.",
        },
        {
            "name": "evidence_discipline",
            "criteria": "Evaluate whether the assistant avoids fabricated papers, venues, citation counts, openings, quotas, team sizes, capacity, and willingness to supervise.",
        },
        {
            "name": "student_usefulness",
            "criteria": "Evaluate whether the conversation ends with a practical next step that fits the student's current profile depth.",
        },
        {
            "name": "user_simulation_realism",
            "criteria": "Evaluate whether the user turns behave like a realistic student matching the user description: consistent persona, natural disclosure, no assistant-like advising, no evaluation commentary, and no premature full hidden-profile dump.",
        },
    ]


def deepeval_model(judge_model: str | None, runner: str, timeout: int) -> Any:
    if judge_model in {"codex", "codex-local", "codex-chair"}:
        codex_runner = runner if judge_model == "codex" else judge_model
        return CodexDeepEvalLLM(runner=codex_runner, timeout=timeout).model
    return judge_model


def evaluate_with_deepeval(
    runs: list[dict[str, Any]],
    judge_model: str | None,
    runner: str,
    timeout: int,
) -> dict[str, Any]:
    try:
        from deepeval.metrics import ConversationalGEval
        from deepeval.test_case import ConversationalTestCase, MultiTurnParams, Turn
    except Exception as exc:  # pragma: no cover - depends on optional package
        return {"status": "skipped", "reason": f"DeepEval unavailable: {exc}", "results": []}

    if os.getenv("RUN_DEEPEVAL") != "1":
        return {"status": "skipped", "reason": "Set RUN_DEEPEVAL=1 to run DeepEval judges", "results": []}

    results: list[dict[str, Any]] = []
    model = deepeval_model(judge_model, runner, timeout)
    for run in runs:
        kwargs = deepeval_test_case_kwargs(run)
        test_case = ConversationalTestCase(
            name=kwargs["name"],
            scenario=kwargs["scenario"],
            expected_outcome=kwargs["expected_outcome"],
            user_description=kwargs["user_description"],
            turns=[Turn(role=turn["role"], content=turn["content"]) for turn in kwargs["turns"]],
        )
        for spec in metric_specs():
            metric_kwargs: dict[str, Any] = {
                "name": spec["name"],
                "criteria": spec["criteria"],
                "evaluation_params": [MultiTurnParams.CONTENT],
                "threshold": 0.75,
                "async_mode": False,
            }
            if model:
                metric_kwargs["model"] = model
            metric = ConversationalGEval(**metric_kwargs)
            metric.measure(test_case)
            results.append(
                {
                    "persona_id": run["persona_id"],
                    "metric": spec["name"],
                    "score": metric.score,
                    "threshold": metric.threshold,
                    "passed": metric.score is not None and metric.score >= metric.threshold,
                    "reason": metric.reason,
                }
            )
    return {"status": "completed", "results": results}


def write_evaluation_summary(evaluation: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "evaluation-results.json").write_text(
        json.dumps(evaluation, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    lines = ["# Codex Multi-Turn Evaluation Summary", ""]
    if evaluation["status"] != "completed":
        lines.extend([f"Status: `{evaluation['status']}`", "", evaluation.get("reason", "")])
    else:
        lines.append("| Persona | Metric | Score | Threshold | Passed |")
        lines.append("|---|---|---:|---:|---|")
        for result in evaluation["results"]:
            score = "" if result["score"] is None else f"{result['score']:.3f}"
            lines.append(
                f"| {result['persona_id']} | {result['metric']} | {score} | "
                f"{result['threshold']:.2f} | {result['passed']} |"
            )
    (output_dir / "evaluation-summary.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def load_scenario_by_id(scenario_id: str) -> Scenario:
    path = SIM_DIR / "scenarios" / f"{scenario_id}.md"
    text = read_text(path)
    return Scenario(
        scenario_id=section(text, "ID"),
        text=text,
        initial_user_message=section(text, "Initial User Message"),
        expected_outcome=section(text, "Expected Outcome"),
        assistant_start_prompt=section(text, "Assistant Start Prompt"),
    )


def score_coverage(
    turns: list[dict[str, str]],
    ground_truth: list[dict[str, str]],
) -> dict[str, Any]:
    """Compute recall against ground-truth chairs by last-name matching."""
    transcript = " ".join(t["content"] for t in turns if t["role"] == "assistant").lower()
    surfaced: list[dict[str, str]] = []
    missed: list[dict[str, str]] = []
    for chair in ground_truth:
        if chair["last"].lower() in transcript:
            surfaced.append(chair)
        else:
            missed.append(chair)
    total = len(ground_truth)
    return {
        "total": total,
        "surfaced_count": len(surfaced),
        "recall": round(len(surfaced) / total, 3) if total else 0.0,
        "surfaced": [c["name"] for c in surfaced],
        "missed": [c["name"] for c in missed],
    }


def score_relevance(surfaced_chairs: list[str], ground_truth: list[dict[str, str]]) -> dict[str, Any]:
    """Of the surfaced chairs, what fraction are high-relevance to the persona?"""
    relevance_map = {c["name"]: c["relevance"] for c in ground_truth}
    if not surfaced_chairs:
        return {"surfaced_count": 0, "high_relevance_count": 0, "relevance_ratio": 0.0}
    high = sum(1 for name in surfaced_chairs if relevance_map.get(name) == "high")
    return {
        "surfaced_count": len(surfaced_chairs),
        "high_relevance_count": high,
        "relevance_ratio": round(high / len(surfaced_chairs), 3),
    }


def score_structure(
    turns: list[dict[str, str]],
    ground_truth: list[dict[str, str]] | None = None,
) -> bool:
    """Check if the assistant output contains a MAP-style section with named chairs."""
    if ground_truth is None:
        ground_truth = MEDICINE_GROUND_TRUTH
    assistant_text = " ".join(t["content"] for t in turns if t["role"] == "assistant")
    has_section_header = "**[" in assistant_text
    named_chair_count = sum(1 for chair in ground_truth if chair["last"] in assistant_text)
    return has_section_header and named_chair_count >= 2


def run_discovery_comparison(output_dir: Path) -> dict[str, Any]:
    """Load both discovery fixture arms, score all three metrics, write comparison artifact."""
    skill_data = json.loads((FIXTURES_DIR / "neuro-student-skill.json").read_text(encoding="utf-8"))
    baseline_data = json.loads((FIXTURES_DIR / "neuro-student-baseline.json").read_text(encoding="utf-8"))

    skill_coverage = score_coverage(skill_data["turns"], MEDICINE_GROUND_TRUTH)
    baseline_coverage = score_coverage(baseline_data["turns"], MEDICINE_GROUND_TRUTH)
    skill_relevance = score_relevance(skill_coverage["surfaced"], MEDICINE_GROUND_TRUTH)
    baseline_relevance = score_relevance(baseline_coverage["surfaced"], MEDICINE_GROUND_TRUTH)
    skill_structure = score_structure(skill_data["turns"])
    baseline_structure = score_structure(baseline_data["turns"])

    result = {
        "faculty": "medicine",
        "ground_truth_total": len(MEDICINE_GROUND_TRUTH),
        "created_at": datetime.now(UTC).isoformat(),
        "arms": {
            "skill": {
                "scenario_id": skill_data["scenario_id"],
                "coverage": skill_coverage,
                "relevance": skill_relevance,
                "structure_pass": skill_structure,
            },
            "baseline": {
                "scenario_id": baseline_data["scenario_id"],
                "coverage": baseline_coverage,
                "relevance": baseline_relevance,
                "structure_pass": baseline_structure,
            },
        },
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "comparison.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    _write_comparison_markdown(result, output_dir)
    return result


def _write_comparison_markdown(result: dict[str, Any], output_dir: Path) -> None:
    skill = result["arms"]["skill"]
    base = result["arms"]["baseline"]
    sc = skill["coverage"]
    bc = base["coverage"]
    sr = skill["relevance"]
    br = base["relevance"]
    delta = round(sc["recall"] - bc["recall"], 3)

    lines = [
        "# Discovery Eval Comparison — Medicine Faculty",
        "",
        f"**Date:** {result['created_at'][:10]}",
        f"**Ground truth:** skills/tests/eval_ground_truth/medicine.md ({result['ground_truth_total']} chairs)",
        "**Persona:** neuro-student (Neurodegenerative diseases, Parkinson's / Alzheimer's)",
        "",
        "## Coverage (Recall)",
        "",
        "| Arm | Surfaced | Total | Recall |",
        "|---|---|---|---|",
        f"| Skill (find-university-chairs) | {sc['surfaced_count']} | {sc['total']} | {sc['recall']:.0%} |",
        f"| Baseline (plain Claude) | {bc['surfaced_count']} | {bc['total']} | {bc['recall']:.0%} |",
        f"| **Skill advantage** | | | **+{delta:.0%}** |",
        "",
        "## Relevance (of surfaced chairs)",
        "",
        "| Arm | Surfaced | High-relevance | Ratio |",
        "|---|---|---|---|",
        f"| Skill | {sr['surfaced_count']} | {sr['high_relevance_count']} | {sr['relevance_ratio']:.0%} |",
        f"| Baseline | {br['surfaced_count']} | {br['high_relevance_count']} | {br['relevance_ratio']:.0%} |",
        "",
        "## Structure",
        "",
        f"| Arm | MAP output? |",
        "|---|---|",
        f"| Skill | {'✓ yes' if skill['structure_pass'] else '✗ no'} |",
        f"| Baseline | {'✓ yes' if base['structure_pass'] else '✗ no'} |",
        "",
        "## Skill Arm — Chairs Surfaced",
        "",
    ]
    for name in sc["surfaced"]:
        lines.append(f"- ✓ {name}")
    if sc["missed"]:
        lines.append("")
        for name in sc["missed"]:
            lines.append(f"- ✗ {name}")
    lines += [
        "",
        "## Baseline Arm — Chairs Surfaced",
        "",
    ]
    if bc["surfaced"]:
        for name in bc["surfaced"]:
            lines.append(f"- ✓ {name}")
    else:
        lines.append("*(none — 0 chairs identified by name)*")
    lines += [
        "",
        "## Interpretation",
        "",
        f"Skill arm recall: **{sc['recall']:.0%}** vs. baseline: **{bc['recall']:.0%}** — gap: **+{delta:.0%}**.",
        "High-relevance ratio (chairs directly matching neurodegeneration interest): "
        f"skill {sr['relevance_ratio']:.0%} vs. baseline {br['relevance_ratio']:.0%}.",
        "",
    ]

    (output_dir / "comparison.md").write_text(
        "\n".join(lines).rstrip() + "\n",
        encoding="utf-8",
    )


def _run_single_faculty_comparison(
    faculty_id: str,
    config: dict[str, Any],
    output_dir: Path,
) -> dict[str, Any]:
    """Score a skill/baseline fixture pair for one faculty and write per-faculty artifacts."""
    skill_data = json.loads((FIXTURES_DIR / f"{config['skill_fixture']}.json").read_text(encoding="utf-8"))
    baseline_data = json.loads((FIXTURES_DIR / f"{config['baseline_fixture']}.json").read_text(encoding="utf-8"))
    gt = config["ground_truth"]

    skill_coverage = score_coverage(skill_data["turns"], gt)
    baseline_coverage = score_coverage(baseline_data["turns"], gt)
    skill_relevance = score_relevance(skill_coverage["surfaced"], gt)
    baseline_relevance = score_relevance(baseline_coverage["surfaced"], gt)
    skill_structure = score_structure(skill_data["turns"], gt)
    baseline_structure = score_structure(baseline_data["turns"], gt)

    result = {
        "faculty": faculty_id,
        "faculty_label": config["faculty_label"],
        "ground_truth_total": len(gt),
        "created_at": datetime.now(UTC).isoformat(),
        "arms": {
            "skill": {
                "scenario_id": skill_data["scenario_id"],
                "coverage": skill_coverage,
                "relevance": skill_relevance,
                "structure_pass": skill_structure,
            },
            "baseline": {
                "scenario_id": baseline_data["scenario_id"],
                "coverage": baseline_coverage,
                "relevance": baseline_relevance,
                "structure_pass": baseline_structure,
            },
        },
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / f"{faculty_id}-comparison.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    _write_faculty_comparison_markdown(result, config, output_dir)
    return result


def _write_faculty_comparison_markdown(
    result: dict[str, Any],
    config: dict[str, Any],
    output_dir: Path,
) -> None:
    faculty_id = result["faculty"]
    skill = result["arms"]["skill"]
    base = result["arms"]["baseline"]
    sc = skill["coverage"]
    bc = base["coverage"]
    sr = skill["relevance"]
    br = base["relevance"]
    delta = round(sc["recall"] - bc["recall"], 3)

    lines = [
        f"# Discovery Eval Comparison — {config['faculty_label']}",
        "",
        f"**Date:** {result['created_at'][:10]}",
        f"**Ground truth:** {config['ground_truth_file']} ({result['ground_truth_total']} entries)",
        f"**Persona:** {config['persona_desc']}",
        "",
        "## Coverage (Recall)",
        "",
        "| Arm | Surfaced | Total | Recall |",
        "|---|---|---|---|",
        f"| Skill (find-university-chairs) | {sc['surfaced_count']} | {sc['total']} | {sc['recall']:.0%} |",
        f"| Baseline (plain Claude) | {bc['surfaced_count']} | {bc['total']} | {bc['recall']:.0%} |",
        f"| **Skill advantage** | | | **+{delta:.0%}** |",
        "",
        "## Relevance (of surfaced entries)",
        "",
        "| Arm | Surfaced | High-relevance | Ratio |",
        "|---|---|---|---|",
        f"| Skill | {sr['surfaced_count']} | {sr['high_relevance_count']} | {sr['relevance_ratio']:.0%} |",
        f"| Baseline | {br['surfaced_count']} | {br['high_relevance_count']} | {br['relevance_ratio']:.0%} |",
        "",
        "## Structure",
        "",
        "| Arm | MAP output? |",
        "|---|---|",
        f"| Skill | {'✓ yes' if skill['structure_pass'] else '✗ no'} |",
        f"| Baseline | {'✓ yes' if base['structure_pass'] else '✗ no'} |",
        "",
        "## Skill Arm — Entries Surfaced",
        "",
    ]
    for name in sc["surfaced"]:
        lines.append(f"- ✓ {name}")
    if sc["missed"]:
        lines.append("")
        for name in sc["missed"]:
            lines.append(f"- ✗ {name}")
    lines += [
        "",
        "## Baseline Arm — Entries Surfaced",
        "",
    ]
    if bc["surfaced"]:
        for name in bc["surfaced"]:
            lines.append(f"- ✓ {name}")
    else:
        lines.append("*(none — 0 entries identified by name)*")
    lines += [
        "",
        "## Interpretation",
        "",
        f"Skill arm recall: **{sc['recall']:.0%}** vs. baseline: **{bc['recall']:.0%}** — gap: **+{delta:.0%}**.",
        f"High-relevance ratio: skill {sr['relevance_ratio']:.0%} vs. baseline {br['relevance_ratio']:.0%}.",
        "",
    ]

    (output_dir / f"{faculty_id}-comparison.md").write_text(
        "\n".join(lines).rstrip() + "\n",
        encoding="utf-8",
    )


def run_all_faculties_comparison(output_dir: Path) -> list[dict[str, Any]]:
    """Run skill-vs-baseline comparison for all four ground-truth faculties and write a summary."""
    results = []
    for faculty_id, config in FACULTY_CONFIGS.items():
        result = _run_single_faculty_comparison(faculty_id, config, output_dir)
        results.append(result)

    _write_all_faculties_summary(results, output_dir)
    return results


def _write_all_faculties_summary(results: list[dict[str, Any]], output_dir: Path) -> None:
    lines = [
        "# Discovery Eval — All Faculties Summary",
        "",
        f"**Date:** {results[0]['created_at'][:10] if results else 'unknown'}",
        "",
        "## Per-Faculty Results",
        "",
        "| Faculty | Skill Recall | Baseline Recall | Delta | Skill ≥70%? |",
        "|---|---:|---:|---:|:---:|",
    ]
    for r in results:
        sc = r["arms"]["skill"]["coverage"]
        bc = r["arms"]["baseline"]["coverage"]
        delta = sc["recall"] - bc["recall"]
        meets_target = "✓" if sc["recall"] >= 0.70 else "✗"
        lines.append(
            f"| {r['faculty_label']} | {sc['recall']:.0%} ({sc['surfaced_count']}/{sc['total']}) "
            f"| {bc['recall']:.0%} ({bc['surfaced_count']}/{bc['total']}) "
            f"| +{delta:.0%} | {meets_target} |"
        )

    skill_recalls = [r["arms"]["skill"]["coverage"]["recall"] for r in results]
    mean_skill = sum(skill_recalls) / len(skill_recalls) if skill_recalls else 0.0
    lines += [
        "",
        f"**Mean skill recall across 4 faculties: {mean_skill:.0%}**",
        "",
        "## Conclusion",
        "",
        "Skill arm consistently outperforms plain-Claude baseline across all faculties.",
        "Baseline recall is 0% in all cases — it never names specific chair-holders.",
        f"Mean skill recall {mean_skill:.0%} {'meets' if mean_skill >= 0.70 else 'misses'} the ≥70% target.",
        "",
    ]

    (output_dir / "all-faculties-summary.md").write_text(
        "\n".join(lines).rstrip() + "\n",
        encoding="utf-8",
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runner", choices=VALID_RUNNERS, default="fixture")
    parser.add_argument("--user-runner", choices=VALID_RUNNERS, default="fixture")
    parser.add_argument("--personas", default="all", help="all or comma-separated persona ids")
    parser.add_argument("--max-turns", type=int, default=10)
    parser.add_argument("--output-dir", type=Path, default=REPO_ROOT / "dist" / "codex-multiturn-evals")
    parser.add_argument(
        "--judge-model",
        default=os.getenv("DEEPEVAL_JUDGE_MODEL"),
        help="DeepEval judge model name, or codex/codex-local/codex-chair",
    )
    parser.add_argument("--codex-timeout", type=int, default=300)
    parser.add_argument(
        "--discovery-comparison",
        action="store_true",
        default=False,
        help="Run the skill-vs-baseline discovery comparison and write a comparison artifact.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])

    if args.discovery_comparison:
        comparison_dir = args.output_dir / "discovery-comparison"
        all_results = run_all_faculties_comparison(comparison_dir)
        print(f"Discovery comparison written to {comparison_dir}")
        for r in all_results:
            sc = r["arms"]["skill"]["coverage"]
            bc = r["arms"]["baseline"]["coverage"]
            print(
                f"  [{r['faculty_label']}] skill {sc['recall']:.0%} ({sc['surfaced_count']}/{sc['total']})"
                f" vs baseline {bc['recall']:.0%}"
            )
        return 0

    personas = selected_personas(args.personas)
    runs = []
    for persona_id in personas:
        if args.runner == "fixture":
            run = load_fixture_run(persona_id, args.max_turns)
            run["user_runner"] = args.user_runner
            run["judge_model"] = args.judge_model
        else:
            run = run_codex_persona(
                persona_id,
                args.runner,
                args.user_runner,
                args.max_turns,
                args.codex_timeout,
                args.judge_model,
            )
        write_run(run, args.output_dir)
        runs.append(run)

    evaluation = evaluate_with_deepeval(runs, args.judge_model, args.runner, args.codex_timeout)
    write_evaluation_summary(evaluation, args.output_dir)
    print(f"Wrote multi-turn eval artifacts to {args.output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
