#!/usr/bin/env python3
"""Compare thesis simulation command performance across before/after runs.

This harness is intentionally thin: it discovers the repo-local simulation
commands, checks that Claude commands and Codex prompts stay synchronized, parses
rating artifacts produced by the simulation workflow, and reports gate results.
It does not reimplement thesis-discovery skill logic.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CLAUDE_COMMANDS_DIR = REPO_ROOT / ".claude" / "commands"
CODEX_PROMPTS_DIR = REPO_ROOT / ".codex" / "prompts"
COMMAND_PATTERN = "thesis-sim-*.md"
REQUIRED_COMMANDS = {
    "thesis-sim-jan",
    "thesis-sim-maja",
    "thesis-sim-marvin",
    "thesis-sim-simon",
    "thesis-sim-simone",
    "thesis-sim-lilly",
    "thesis-sim-tina",
    "thesis-sim-timo",
}
BASELINE_REQUIRED_COMMANDS = {
    "thesis-sim-jan",
    "thesis-sim-maja",
    "thesis-sim-simon",
    "thesis-sim-tina",
}
BASELINE_OPTIONAL_COMMANDS = REQUIRED_COMMANDS - BASELINE_REQUIRED_COMMANDS
MISROUTING_GUARDRAIL_COMMANDS = {
    "thesis-sim-jan",
    "thesis-sim-simon",
    "thesis-sim-maja",
}
TINAS_REQUIRED_GUARDRAIL = "both tracks or structural company limit"
TOPIC_MENU_GUARDRAIL = "Topic menus / possible thesis angles present"
SESSION_PERSISTENCE_GUARDRAIL = "Session persistence avoided"
RUBRIC_DIMENSIONS = {
    "workflow compliance",
    "profile depth",
    "department routing",
    "evidence discipline",
    "recommendation quality",
    "persona realism",
    "conversation usefulness",
}


@dataclass(frozen=True)
class CommandSync:
    slugs: list[str]
    missing_in_claude: list[str]
    missing_in_codex: list[str]
    content_mismatches: list[str]
    unexpected_commands: list[str]

    @property
    def ok(self) -> bool:
        return (
            not self.missing_in_claude
            and not self.missing_in_codex
            and not self.content_mismatches
            and not self.unexpected_commands
        )


@dataclass(frozen=True)
class Rating:
    slug: str
    path: str
    total_score: int
    evidence_score: int | None
    verified_urls: int | None
    unconfirmed_claims: int | None
    wall_clock_seconds: float | None
    topic_menus_present: bool | None
    session_persistence_avoided: bool | None
    guardrail_failures: list[str]


def command_slug(path: Path) -> str:
    return path.stem


def discover_command_files(directory: Path) -> dict[str, Path]:
    return {command_slug(path): path for path in sorted(directory.glob(COMMAND_PATTERN))}


def check_command_sync(
    claude_dir: Path = CLAUDE_COMMANDS_DIR,
    codex_dir: Path = CODEX_PROMPTS_DIR,
) -> CommandSync:
    claude = discover_command_files(claude_dir)
    codex = discover_command_files(codex_dir)
    slugs = sorted(set(claude) | set(codex))
    mismatches = [
        slug
        for slug in slugs
        if slug in claude
        and slug in codex
        and claude[slug].read_text(encoding="utf-8") != codex[slug].read_text(encoding="utf-8")
    ]
    return CommandSync(
        slugs=slugs,
        missing_in_claude=sorted((set(codex) - set(claude)) | (REQUIRED_COMMANDS - set(claude))),
        missing_in_codex=sorted((set(claude) - set(codex)) | (REQUIRED_COMMANDS - set(codex))),
        content_mismatches=mismatches,
        unexpected_commands=sorted((set(claude) | set(codex)) - REQUIRED_COMMANDS),
    )


def _extract_int(pattern: str, text: str) -> int | None:
    match = re.search(pattern, text, flags=re.IGNORECASE)
    return int(match.group(1)) if match else None


def _extract_float(pattern: str, text: str) -> float | None:
    match = re.search(pattern, text, flags=re.IGNORECASE)
    return float(match.group(1)) if match else None


def student_slug_for_command(slug: str) -> str:
    return slug.removeprefix("thesis-sim-")


def _extract_yes_no(label: str, text: str) -> bool | None:
    match = re.search(
        rf"^\s*(?:[-*+]\s*)?(?:\d+\.\s*)?{re.escape(label)}\s*:\s*(yes|no)\s*$",
        text,
        flags=re.IGNORECASE | re.MULTILINE,
    )
    if not match:
        return None
    return match.group(1).lower() == "yes"


def evaluate_guardrails(command_slug_value: str, text: str) -> list[str]:
    failures: list[str] = []
    topic_menus_present = _extract_yes_no(TOPIC_MENU_GUARDRAIL, text)
    if topic_menus_present is None:
        failures.append("missing_topic_menus")
    elif not topic_menus_present:
        failures.append("topic_menus_missing")

    session_persistence_avoided = _extract_yes_no(SESSION_PERSISTENCE_GUARDRAIL, text)
    if session_persistence_avoided is None:
        failures.append("missing_session_persistence_check")
    elif not session_persistence_avoided:
        failures.append("session_persistence_used")

    if command_slug_value in MISROUTING_GUARDRAIL_COMMANDS:
        misrouting = _extract_yes_no("Company/CS misrouting", text)
        if misrouting is None:
            failures.append("missing_company_cs_misrouting")
        elif misrouting:
            failures.append("company_cs_misrouting")
    if command_slug_value == "thesis-sim-tina":
        tracks_or_limit = _extract_yes_no(TINAS_REQUIRED_GUARDRAIL, text)
        if tracks_or_limit is None:
            failures.append("missing_tina_tracks_or_limit_honesty")
        elif not tracks_or_limit:
            failures.append("tina_tracks_or_limit_honesty_failed")
    return failures


def parse_rating(path: Path) -> Rating:
    text = path.read_text(encoding="utf-8")
    scores: dict[str, int] = {}
    for line in text.splitlines():
        cells = [cell.strip(" `*").lower() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        dimension = cells[0]
        if dimension in RUBRIC_DIMENSIONS and re.fullmatch(r"[0-3]", cells[1]):
            scores[dimension] = int(cells[1])

    total = _extract_int(r"total(?: score)?:\s*(\d+)", text)
    if total is None:
        total = sum(scores.values())

    parsed_slug = path.stem.split("_rating_")[0]
    command_slug_value = parsed_slug if parsed_slug.startswith("thesis-sim-") else f"thesis-sim-{parsed_slug}"

    return Rating(
        slug=command_slug_value,
        path=str(path),
        total_score=total,
        evidence_score=scores.get("evidence discipline"),
        verified_urls=_extract_int(r"verified urls?:\s*(\d+)", text),
        unconfirmed_claims=_extract_int(r"unconfirmed claims?:\s*(\d+)", text),
        wall_clock_seconds=_extract_float(r"wall[-_ ]clock seconds?:\s*([0-9]+(?:\.[0-9]+)?)", text),
        topic_menus_present=_extract_yes_no(TOPIC_MENU_GUARDRAIL, text),
        session_persistence_avoided=_extract_yes_no(SESSION_PERSISTENCE_GUARDRAIL, text),
        guardrail_failures=evaluate_guardrails(command_slug_value, text),
    )


def latest_rating_for_slug(root: Path, slug: str) -> Path:
    student_slug = student_slug_for_command(slug)
    candidates = [
        *(root / "rating").glob(f"{slug}_rating_*.md"),
        *(root / "rating").glob(f"{student_slug}_rating_*.md"),
        *root.glob(f"{slug}.md"),
        *root.glob(f"{student_slug}.md"),
    ]
    if not candidates:
        raise FileNotFoundError(f"No rating artifact found for {slug!r} under {root}")
    return max(candidates, key=_rating_recency_key)


def _rating_recency_key(path: Path) -> tuple[int, datetime, int, str]:
    match = re.search(r"_rating_(\d{2})\.(\d{2})\.(\d{4})-(\d{2})-(\d{2})-(\d{2})\.md$", path.name)
    if match:
        day, month, year, hour, minute, second = map(int, match.groups())
        return (1, datetime(year, month, day, hour, minute, second), path.stat().st_mtime_ns, path.name)
    return (0, datetime.min, path.stat().st_mtime_ns, path.name)


def load_ratings(root: Path, slugs: list[str]) -> dict[str, Rating]:
    return {slug: parse_rating(latest_rating_for_slug(root, slug)) for slug in slugs}


def load_optional_ratings(root: Path, slugs: list[str]) -> tuple[dict[str, Rating], list[str]]:
    ratings: dict[str, Rating] = {}
    missing: list[str] = []
    for slug in slugs:
        try:
            ratings[slug] = parse_rating(latest_rating_for_slug(root, slug))
        except FileNotFoundError:
            missing.append(slug)
    return ratings, missing


def compare_runs(baseline_dir: Path, candidate_dir: Path) -> dict[str, object]:
    sync = check_command_sync()
    slugs = sorted(REQUIRED_COMMANDS)
    baseline, missing_baseline_ratings = load_optional_ratings(baseline_dir, slugs)
    candidate = load_ratings(candidate_dir, slugs)
    comparable_slugs = [slug for slug in slugs if slug in baseline and slug in candidate]
    rows = []
    for slug in slugs:
        after = candidate[slug]
        before = baseline.get(slug)
        rows.append(
            {
                "slug": slug,
                "baseline_total": None if before is None else before.total_score,
                "candidate_total": after.total_score,
                "delta": None if before is None else after.total_score - before.total_score,
                "candidate_evidence_score": after.evidence_score,
                "verified_urls_delta": None
                if before is None or before.verified_urls is None or after.verified_urls is None
                else after.verified_urls - before.verified_urls,
                "unconfirmed_claims_delta": None
                if before is None or before.unconfirmed_claims is None or after.unconfirmed_claims is None
                else after.unconfirmed_claims - before.unconfirmed_claims,
                "wall_clock_seconds_delta": None
                if before is None or before.wall_clock_seconds is None or after.wall_clock_seconds is None
                else round(after.wall_clock_seconds - before.wall_clock_seconds, 3),
                "topic_menus_present": after.topic_menus_present,
                "session_persistence_avoided": after.session_persistence_avoided,
                "guardrail_failures": after.guardrail_failures,
            }
        )

    baseline_mean = (
        sum(baseline[slug].total_score for slug in comparable_slugs) / len(comparable_slugs)
        if comparable_slugs
        else None
    )
    candidate_mean = (
        sum(candidate[slug].total_score for slug in comparable_slugs) / len(comparable_slugs)
        if comparable_slugs
        else None
    )
    candidate_mean_all = sum(r.total_score for r in candidate.values()) / len(slugs)
    missing_required_baseline_ratings = sorted(set(missing_baseline_ratings) & BASELINE_REQUIRED_COMMANDS)
    candidate_only_commands = sorted(set(missing_baseline_ratings) & BASELINE_OPTIONAL_COMMANDS)
    gates = {
        "commands_synced": sync.ok and set(sync.slugs) == REQUIRED_COMMANDS,
        "required_baseline_ratings_present": not missing_required_baseline_ratings,
        "mean_score_not_lower": baseline_mean is not None and candidate_mean is not None and candidate_mean >= baseline_mean,
        "all_commands_at_least_14": all(r.total_score >= 14 for r in candidate.values()),
        "all_evidence_at_least_2": all((r.evidence_score or 0) >= 2 for r in candidate.values()),
        "no_guardrail_failures": all(not r.guardrail_failures for r in candidate.values()),
    }
    return {
        "baseline_dir": str(baseline_dir),
        "candidate_dir": str(candidate_dir),
        "command_sync": asdict(sync),
        "baseline_mean": None if baseline_mean is None else round(baseline_mean, 3),
        "candidate_mean": None if candidate_mean is None else round(candidate_mean, 3),
        "candidate_mean_all": round(candidate_mean_all, 3),
        "comparable_commands": comparable_slugs,
        "missing_baseline_ratings": missing_baseline_ratings,
        "missing_required_baseline_ratings": missing_required_baseline_ratings,
        "candidate_only_commands": candidate_only_commands,
        "rows": rows,
        "gates": gates,
        "passed": all(gates.values()),
    }


def _format_optional(value: object, *, signed: bool = False) -> str:
    if value is None:
        return "n/a"
    if signed and isinstance(value, int):
        return f"{value:+d}"
    return str(value)


def write_markdown(result: dict[str, object], path: Path) -> None:
    lines = [
        "# Command Simulation Performance Comparison",
        "",
        f"Baseline: `{result['baseline_dir']}`",
        f"Candidate: `{result['candidate_dir']}`",
        f"Baseline mean over comparable commands: **{_format_optional(result['baseline_mean'])}**",
        f"Candidate mean over comparable commands: **{_format_optional(result['candidate_mean'])}**",
        f"Candidate mean over all current commands: **{result['candidate_mean_all']}**",
        f"Passed: **{result['passed']}**",
        "",
        "## Per Command",
        "",
        "| Command | Baseline | Candidate | Delta | Evidence | Guardrails |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for row in result["rows"]:  # type: ignore[index]
        failures = ", ".join(row["guardrail_failures"]) or "none"
        lines.append(
            f"| {row['slug']} | {_format_optional(row['baseline_total'])} | {row['candidate_total']} | "
            f"{_format_optional(row['delta'], signed=True)} | {row['candidate_evidence_score']} | {failures} |"
        )
    candidate_only = result.get("candidate_only_commands") or []
    if candidate_only:
        lines += [
            "",
            "## Candidate-Only Commands",
            "",
            "These commands were present in the candidate run but absent from the baseline run, so they are excluded from delta and mean-regression gates while still counting toward absolute score, evidence, and guardrail gates.",
            "",
            ", ".join(f"`{slug}`" for slug in candidate_only),
        ]
    missing_required = result.get("missing_required_baseline_ratings") or []
    if missing_required:
        lines += [
            "",
            "## Missing Required Baseline Ratings",
            "",
            ", ".join(f"`{slug}`" for slug in missing_required),
        ]
    lines += [
        "",
        "## Gates",
        "",
        "| Gate | Passed |",
        "|---|---|",
    ]
    for name, passed in result["gates"].items():  # type: ignore[union-attr]
        lines.append(f"| {name} | {passed} |")
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline-dir", type=Path, required=True)
    parser.add_argument("--candidate-dir", type=Path, required=True)
    parser.add_argument("--output-json", type=Path)
    parser.add_argument("--output-md", type=Path)
    args = parser.parse_args()

    result = compare_runs(args.baseline_dir, args.candidate_dir)
    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.output_md:
        args.output_md.parent.mkdir(parents=True, exist_ok=True)
        write_markdown(result, args.output_md)
    if not args.output_json and not args.output_md:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
