"""Skill computation orchestration service."""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass

from app.config import Settings
from app.handbook.repository import HandbookRepository
from app.llm.port import LLMPort
from app.models.skill import SkillComputationRun
from app.skills.matcher import CascadeModuleMatcher, ModuleMatch
from app.skills.repository import SkillRepository
from app.skills.scorer import ScoringConfig, compute_skill_scores
from app.skills.tag_generator import LLMSkillTagGenerator
from app.skills.taxonomy import SkillTaxonomy
from app.students.repository import StudentRepository

_logger = logging.getLogger(__name__)


@dataclass
class _MatchedModule:
    """Adapter to satisfy compute_skill_scores() duck-typing."""

    course: object
    handbook_entry: object | None
    match: ModuleMatch | None
    skill_mappings: list


@dataclass
class SkillComputationResult:
    status: str
    computation_run_id: uuid.UUID | None
    skills_count: int
    matched_courses: int
    unmatched_courses: list[str]
    warnings: list[str]


class SkillComputationService:
    """Orchestrates the full skill computation pipeline for one user."""

    def __init__(
        self,
        skill_repo: SkillRepository,
        handbook_repo: HandbookRepository,
        student_repo: StudentRepository,
        embed_client: LLMPort,
        llm_client: LLMPort,
        settings: Settings,
    ) -> None:
        self._skill_repo = skill_repo
        self._handbook_repo = handbook_repo
        self._student_repo = student_repo
        self._embed = embed_client
        self._llm = llm_client
        self._settings = settings

    async def compute_skills(
        self,
        user_id: int,
        run: SkillComputationRun,
        config: ScoringConfig | None = None,
    ) -> SkillComputationResult:
        config = config or ScoringConfig()
        warnings: list[str] = []

        # ---- Step 1: Load student courses ----
        _logger.info("Step 1/5 — Loading student courses (user_id=%d)", user_id)
        student = await self._student_repo.get_by_user_id(user_id)
        if not student or not student.courses:
            await self._skill_repo.fail_run(run, "No courses found for user")
            return SkillComputationResult(
                status="no_courses",
                computation_run_id=run.id,
                skills_count=0,
                matched_courses=0,
                unmatched_courses=[],
                warnings=["No courses found. Please upload a transcript first."],
            )

        courses = list(student.courses)
        _logger.info("Step 1/5 — Found %d courses (user_id=%d)", len(courses), user_id)

        # ---- Step 2: Load handbook entries ----
        _logger.info("Step 2/5 — Loading module handbook entries")
        handbook_entries = await self._handbook_repo.get_latest_entries()
        if not handbook_entries:
            warnings.append("No module handbook has been ingested yet. Skills could not be computed.")
            await self._skill_repo.complete_run(
                run,
                total_courses=len(courses),
                matched_courses=0,
                unmatched_courses=[c.course_name for c in courses],
                warnings=warnings,
                config=_config_to_dict(config),
            )
            return SkillComputationResult(
                status="no_handbook",
                computation_run_id=run.id,
                skills_count=0,
                matched_courses=0,
                unmatched_courses=[c.course_name for c in courses],
                warnings=warnings,
            )
        _logger.info(
            "Step 2/5 — Loaded %d handbook entries from %d universities",
            len(handbook_entries),
            len({e.university_id for e in handbook_entries}),
        )

        # ---- Step 3: Match courses ----
        _logger.info(
            "Step 3/5 — Matching %d courses against %d handbook entries",
            len(courses),
            len(handbook_entries),
        )
        matcher = CascadeModuleMatcher(
            embed_client=self._embed,
            settings=self._settings,
            min_confidence=config.min_match_confidence,
        )

        # Build session-scoped helpers for tag generation
        from sqlalchemy.inspection import inspect as sa_inspect

        session = sa_inspect(
            next(iter(handbook_entries))
        ).session if handbook_entries else None

        # We need the session from the repository — access via private attr pattern
        session = self._skill_repo._session  # type: ignore[attr-defined]
        taxonomy = SkillTaxonomy(session)
        tag_gen = LLMSkillTagGenerator(session, self._llm, self._settings, taxonomy)

        matched_modules: list[_MatchedModule] = []
        unmatched: list[str] = []

        for course in courses:
            matches = await matcher.match(course, handbook_entries)
            if not matches:
                unmatched.append(course.course_name)
                _logger.debug("Matcher: no match for %r", course.course_name)
                continue

            best = matches[0]
            entry = best.handbook_entry

            # ---- Step 3a: Ensure skill tags for this entry ----
            mappings = await tag_gen.ensure_mappings(entry)
            if not mappings:
                warnings.append(
                    f"No skill tags could be generated for handbook entry '{entry.module_title}'."
                )

            matched_modules.append(
                _MatchedModule(
                    course=course,
                    handbook_entry=entry,
                    match=best,
                    skill_mappings=mappings,
                )
            )

        _logger.info(
            "Step 3/5 — Matched %d/%d courses (%d unmatched)",
            len(matched_modules),
            len(courses),
            len(unmatched),
        )
        if unmatched:
            _logger.info("Unmatched courses: %s", unmatched)

        # Warn about courses without ECTS or grades
        for mm in matched_modules:
            if mm.course.credits is None:
                warnings.append(
                    f"Course '{mm.course.course_name}' has no ECTS; assumed {config.default_ects}."
                )

        # ---- Step 4: Compute scores ----
        _logger.info("Step 4/5 — Computing skill scores")
        computed = compute_skill_scores(matched_modules, config)
        _logger.info(
            "Step 4/5 — Computed %d skill scores from %d matched modules",
            len(computed),
            len(matched_modules),
        )

        # ---- Step 5: Persist ----
        _logger.info("Step 5/5 — Persisting %d user skills (user_id=%d)", len(computed), user_id)
        await self._skill_repo.replace_user_skills(user_id, run, computed)

        handbook_version = handbook_entries[0].handbook_version if handbook_entries else None
        university_id = handbook_entries[0].university_id if handbook_entries else None

        await self._skill_repo.complete_run(
            run,
            total_courses=len(courses),
            matched_courses=len(matched_modules),
            unmatched_courses=unmatched,
            warnings=warnings,
            config=_config_to_dict(config),
            handbook_version=handbook_version,
            university_id=university_id,
        )
        _logger.info("Step 5/5 — Skills committed (user_id=%d)", user_id)

        return SkillComputationResult(
            status="completed",
            computation_run_id=run.id,
            skills_count=len(computed),
            matched_courses=len(matched_modules),
            unmatched_courses=unmatched,
            warnings=warnings,
        )


def _config_to_dict(config: ScoringConfig) -> dict:
    return {
        "default_ects": config.default_ects,
        "default_grade_factor": config.default_grade_factor,
        "pass_grade_factor": config.pass_grade_factor,
        "level_weights": dict(config.level_weights),
        "recency_decay_per_year": config.recency_decay_per_year,
        "recency_floor": config.recency_floor,
        "recency_default": config.recency_default,
        "min_match_confidence": config.min_match_confidence,
    }
