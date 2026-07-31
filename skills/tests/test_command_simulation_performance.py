"""Checks for /commands-based simulation performance comparison."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / "scripts" / "compare_command_simulation_performance.py"


def _load_script():
    spec = importlib.util.spec_from_file_location("compare_command_simulation_performance", SCRIPT_PATH)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def test_thesis_sim_commands_are_synced_between_clients() -> None:
    script = _load_script()
    sync = script.check_command_sync()
    assert sync.ok
    assert set(sync.slugs) == script.REQUIRED_COMMANDS
    assert sync.unexpected_commands == []


def test_rating_parser_extracts_scores_and_diagnostics(tmp_path: Path) -> None:
    script = _load_script()
    rating = tmp_path / "jan_rating_30.07.2026-12-00-00.md"
    rating.write_text(
        "\n".join(
            [
                "# Rating",
                "| Dimension | Score | Notes |",
                "|---|---:|---|",
                "| Workflow compliance | 3 | ok |",
                "| Profile depth | 3 | ok |",
                "| Department routing | 2 | ok |",
                "| Evidence discipline | 2 | ok |",
                "| Recommendation quality | 3 | ok |",
                "| Persona realism | 3 | ok |",
                "| Conversation usefulness | 3 | ok |",
                "",
                "Verified URLs: 7",
                "Unconfirmed claims: 0",
                "Wall-clock seconds: 42.5",
                "Company/CS misrouting: no",
            ]
        ),
        encoding="utf-8",
    )

    parsed = script.parse_rating(rating)

    assert parsed.slug == "thesis-sim-jan"
    assert parsed.total_score == 19
    assert parsed.evidence_score == 2
    assert parsed.verified_urls == 7
    assert parsed.unconfirmed_claims == 0
    assert parsed.wall_clock_seconds == 42.5
    assert parsed.guardrail_failures == []


def test_rating_parser_accepts_bulleted_guardrail_diagnostics(tmp_path: Path) -> None:
    script = _load_script()
    rating = tmp_path / "maja_rating_30.07.2026-12-00-00.md"
    rating.write_text(
        "\n".join(
            [
                "# Rating",
                "| Dimension | Score | Notes |",
                "|---|---:|---|",
                "| Evidence discipline | 2 | ok |",
                "Total: 16",
                "- Company/CS misrouting: no",
            ]
        ),
        encoding="utf-8",
    )

    parsed = script.parse_rating(rating)

    assert parsed.guardrail_failures == []


def test_latest_rating_uses_parsed_timestamp_not_lexical_filename_order(tmp_path: Path) -> None:
    script = _load_script()
    rating_dir = tmp_path / "rating"
    rating_dir.mkdir()
    older = rating_dir / "jan_rating_31.07.2026-12-00-00.md"
    newer = rating_dir / "jan_rating_01.08.2026-12-00-00.md"
    for path in (older, newer):
        path.write_text(
            "\n".join(
                [
                    "# Rating",
                    "| Dimension | Score | Notes |",
                    "|---|---:|---|",
                    "| Evidence discipline | 2 | ok |",
                    "Total: 16",
                    "Company/CS misrouting: no",
                ]
            ),
            encoding="utf-8",
        )

    selected = script.latest_rating_for_slug(tmp_path, "thesis-sim-jan")

    assert selected == newer


def test_comparison_applies_acceptance_gates(tmp_path: Path) -> None:
    script = _load_script()
    baseline = tmp_path / "baseline"
    candidate = tmp_path / "rules-only"
    (baseline / "rating").mkdir(parents=True)
    (candidate / "rating").mkdir(parents=True)

    for slug in sorted(script.REQUIRED_COMMANDS):
        student_slug = script.student_slug_for_command(slug)
        for root, total in ((baseline, 15), (candidate, 16)):
            guardrail = (
                "Both tracks or structural company limit: yes"
                if slug == "thesis-sim-tina"
                else "Company/CS misrouting: no"
            )
            (root / "rating" / f"{student_slug}_rating_30.07.2026-12-00-00.md").write_text(
                "\n".join(
                    [
                        "# Rating",
                        "| Dimension | Score | Notes |",
                        "|---|---:|---|",
                        "| Workflow compliance | 2 | ok |",
                        "| Profile depth | 2 | ok |",
                        "| Department routing | 2 | ok |",
                        "| Evidence discipline | 2 | ok |",
                        "| Recommendation quality | 2 | ok |",
                        "| Persona realism | 3 | ok |",
                        "| Conversation usefulness | 3 | ok |",
                        f"Total: {total}",
                        guardrail,
                    ]
                ),
                encoding="utf-8",
            )

    result = script.compare_runs(baseline, candidate)

    assert result["passed"] is True
    assert result["gates"]["mean_score_not_lower"] is True
    assert result["gates"]["all_commands_at_least_14"] is True


def test_comparison_allows_candidate_only_new_commands(tmp_path: Path) -> None:
    script = _load_script()
    baseline = tmp_path / "baseline"
    candidate = tmp_path / "rules-only"
    (baseline / "rating").mkdir(parents=True)
    (candidate / "rating").mkdir(parents=True)
    baseline_slugs = {
        "thesis-sim-jan",
        "thesis-sim-maja",
        "thesis-sim-simon",
        "thesis-sim-tina",
    }

    for slug in sorted(script.REQUIRED_COMMANDS):
        student_slug = script.student_slug_for_command(slug)
        guardrail = (
            "Both tracks or structural company limit: yes"
            if slug == "thesis-sim-tina"
            else "Company/CS misrouting: no"
        )
        (candidate / "rating" / f"{student_slug}_rating_30.07.2026-12-00-00.md").write_text(
            "\n".join(
                [
                    "# Rating",
                    "| Dimension | Score | Notes |",
                    "|---|---:|---|",
                    "| Workflow compliance | 2 | ok |",
                    "| Profile depth | 2 | ok |",
                    "| Department routing | 2 | ok |",
                    "| Evidence discipline | 2 | ok |",
                    "| Recommendation quality | 2 | ok |",
                    "| Persona realism | 3 | ok |",
                    "| Conversation usefulness | 3 | ok |",
                    "Total: 16",
                    guardrail,
                ]
            ),
            encoding="utf-8",
        )
        if slug in baseline_slugs:
            (baseline / "rating" / f"{student_slug}_rating_30.07.2026-12-00-00.md").write_text(
                "\n".join(
                    [
                        "# Rating",
                        "| Dimension | Score | Notes |",
                        "|---|---:|---|",
                        "| Workflow compliance | 2 | ok |",
                        "| Profile depth | 2 | ok |",
                        "| Department routing | 2 | ok |",
                        "| Evidence discipline | 2 | ok |",
                        "| Recommendation quality | 2 | ok |",
                        "| Persona realism | 3 | ok |",
                        "| Conversation usefulness | 3 | ok |",
                        "Total: 15",
                        guardrail,
                    ]
                ),
                encoding="utf-8",
            )

    result = script.compare_runs(baseline, candidate)

    assert result["passed"] is True
    assert result["comparable_commands"] == sorted(baseline_slugs)
    assert set(result["missing_baseline_ratings"]) == script.REQUIRED_COMMANDS - baseline_slugs
    assert result["missing_required_baseline_ratings"] == []
    assert set(result["candidate_only_commands"]) == script.REQUIRED_COMMANDS - script.BASELINE_REQUIRED_COMMANDS
    assert result["baseline_mean"] == 15
    assert result["candidate_mean"] == 16
    assert result["candidate_mean_all"] == 16
    marvin_row = next(row for row in result["rows"] if row["slug"] == "thesis-sim-marvin")
    assert marvin_row["baseline_total"] is None
    assert marvin_row["delta"] is None


def test_comparison_fails_when_original_baseline_command_is_missing(tmp_path: Path) -> None:
    script = _load_script()
    baseline = tmp_path / "baseline"
    candidate = tmp_path / "rules-only"
    (baseline / "rating").mkdir(parents=True)
    (candidate / "rating").mkdir(parents=True)
    intentionally_missing = "thesis-sim-jan"

    for slug in sorted(script.REQUIRED_COMMANDS):
        student_slug = script.student_slug_for_command(slug)
        guardrail = (
            "Both tracks or structural company limit: yes"
            if slug == "thesis-sim-tina"
            else "Company/CS misrouting: no"
        )
        rating_text = "\n".join(
            [
                "# Rating",
                "| Dimension | Score | Notes |",
                "|---|---:|---|",
                "| Workflow compliance | 2 | ok |",
                "| Profile depth | 2 | ok |",
                "| Department routing | 2 | ok |",
                "| Evidence discipline | 2 | ok |",
                "| Recommendation quality | 2 | ok |",
                "| Persona realism | 3 | ok |",
                "| Conversation usefulness | 3 | ok |",
                "Total: 16",
                guardrail,
            ]
        )
        (candidate / "rating" / f"{student_slug}_rating_30.07.2026-12-00-00.md").write_text(
            rating_text,
            encoding="utf-8",
        )
        if slug in script.BASELINE_REQUIRED_COMMANDS and slug != intentionally_missing:
            (baseline / "rating" / f"{student_slug}_rating_30.07.2026-12-00-00.md").write_text(
                rating_text,
                encoding="utf-8",
            )

    result = script.compare_runs(baseline, candidate)

    assert result["passed"] is False
    assert result["gates"]["required_baseline_ratings_present"] is False
    assert result["missing_required_baseline_ratings"] == [intentionally_missing]


def test_comparison_fails_when_required_guardrail_diagnostic_is_missing(tmp_path: Path) -> None:
    script = _load_script()
    baseline = tmp_path / "baseline"
    candidate = tmp_path / "rules-only"
    (baseline / "rating").mkdir(parents=True)
    (candidate / "rating").mkdir(parents=True)

    for slug in sorted(script.REQUIRED_COMMANDS):
        student_slug = script.student_slug_for_command(slug)
        for root in (baseline, candidate):
            lines = [
                "# Rating",
                "| Dimension | Score | Notes |",
                "|---|---:|---|",
                "| Workflow compliance | 2 | ok |",
                "| Profile depth | 2 | ok |",
                "| Department routing | 2 | ok |",
                "| Evidence discipline | 2 | ok |",
                "| Recommendation quality | 2 | ok |",
                "| Persona realism | 3 | ok |",
                "| Conversation usefulness | 3 | ok |",
                "Total: 16",
            ]
            if slug != "thesis-sim-jan":
                lines.append(
                    "Both tracks or structural company limit: yes"
                    if slug == "thesis-sim-tina"
                    else "Company/CS misrouting: no"
                )
            (root / "rating" / f"{student_slug}_rating_30.07.2026-12-00-00.md").write_text(
                "\n".join(lines),
                encoding="utf-8",
            )

    result = script.compare_runs(baseline, candidate)

    assert result["passed"] is False
    assert result["gates"]["no_guardrail_failures"] is False
    jan_row = next(row for row in result["rows"] if row["slug"] == "thesis-sim-jan")
    assert jan_row["guardrail_failures"] == ["missing_company_cs_misrouting"]
