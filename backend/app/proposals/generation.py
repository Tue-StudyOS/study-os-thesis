"""LLM-backed proposal generation service."""

from __future__ import annotations

import logging

from pydantic import BaseModel, Field

from app.chairs.repository import ChairRepository
from app.config import Settings
from app.llm.port import LLMPort
from app.models import Thesis, ThesisSource
from app.students.repository import StudentRepository
from app.theses.repository import ThesisRepository
from app.theses.schemas import GeneratedProposalItem

_logger = logging.getLogger(__name__)


class GeneratedProposalList(BaseModel):
    proposals: list[GeneratedProposalItem] = Field(default_factory=list, min_length=1, max_length=3)


_PROPOSAL_GENERATION_PROMPT = """\
You are a research proposal writer for a German university. Generate {count} distinct \
thesis proposal(s) for a student based on the information below.

## Chair
Name: {chair_name}
Description: {chair_description}

## Student profile
GPA (German scale, lower=better): {gpa}
Semester: {semester}
Program: {program}
Courses: {courses}

## Requested research direction
{research_direction}

Return ONLY a JSON object with this schema:
{{
  "proposals": [
    {{
      "title": "<concise thesis title>",
      "abstract": "<2-4 sentence description>",
      "difficulty": "bachelor" | "master" | "phd",
      "skills_required": {{
        "programming": ["Python"],
        "math": [],
        "theory": [],
        "domain": [],
        "other": []
      }}
    }}
  ]
}}
"""


class ProposalGenerationService:
    def __init__(
        self,
        *,
        chair_repo: ChairRepository,
        thesis_repo: ThesisRepository,
        student_repo: StudentRepository | None,
        chat_client: LLMPort,
        embed_client: LLMPort,
        settings: Settings,
    ) -> None:
        self._chair_repo = chair_repo
        self._thesis_repo = thesis_repo
        self._student_repo = student_repo
        self._chat = chat_client
        self._embed = embed_client
        self._settings = settings

    async def generate_and_save(
        self,
        *,
        chair_id: int,
        research_direction: str,
        count: int,
        user_id: int,
        chat_session_id: int,
    ) -> dict:
        chair = await self._chair_repo.get_by_id(chair_id, load_documents=False)
        if chair is None:
            return {"error": f"Chair {chair_id} not found"}

        gpa = "N/A"
        semester = "N/A"
        program = "N/A"
        courses_str = "No courses available"
        if self._student_repo is not None:
            try:
                student = await self._student_repo.get_by_user_id(user_id)
                if student:
                    gpa = str(student.gpa) if student.gpa is not None else "N/A"
                    semester = str(student.semester) if student.semester else "N/A"
                    program = student.program or "N/A"
                    if student.courses:
                        courses_str = "; ".join(f"{c.course_name} ({c.credits} ECTS, {c.grade})" if c.credits and c.grade else c.course_name for c in student.courses)
            except Exception as exc:
                _logger.warning("Could not load student profile for proposal generation: %s", exc)

        prompt = _PROPOSAL_GENERATION_PROMPT.format(
            count=count,
            chair_name=chair.name,
            chair_description=chair.short_description,
            gpa=gpa,
            semester=semester,
            program=program,
            courses=courses_str,
            research_direction=research_direction,
        )

        try:
            output = await self._chat.chat_structured(
                model=self._settings.effective_extract_model,
                messages=[{"role": "user", "content": prompt}],
                output_schema=GeneratedProposalList,
            )
        except Exception as exc:
            _logger.error("Proposal generation failed: %s", exc)
            return {"error": f"LLM unavailable or returned invalid proposal format: {exc}"}

        saved = []
        for proposal in output.proposals[:count]:
            try:
                embedding = await self._embed.embed(
                    self._settings.ollama_embed_model,
                    f"{proposal.title}\n\n{proposal.abstract}",
                )
            except Exception:
                embedding = None

            thesis = Thesis(
                title=proposal.title,
                abstract=proposal.abstract,
                chair_id=chair_id,
                submitter_id=user_id,
                source=ThesisSource.student,
                difficulty=proposal.difficulty,
                skills_required=proposal.skills_required.model_dump(),
                generated_for_user_id=user_id,
                chat_session_id=chat_session_id,
                embedding=embedding,
            )
            self._thesis_repo.session.add(thesis)
            await self._thesis_repo.session.flush()
            await self._thesis_repo.session.refresh(thesis)
            saved.append({"id": thesis.id, "title": thesis.title, "difficulty": thesis.difficulty.value})

        await self._thesis_repo.commit()
        return {
            "generated": len(saved),
            "proposals": saved,
            "message": f"{len(saved)} proposal(s) saved to 'Meine Vorschläge'.",
        }
