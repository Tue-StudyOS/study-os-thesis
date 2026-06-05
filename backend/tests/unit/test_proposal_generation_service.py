"""Unit tests for typed LLM proposal generation."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from app.models import ThesisDifficulty
from app.proposals.generation import GeneratedProposalList, ProposalGenerationService
from app.theses.schemas import GeneratedProposalItem, SkillsRequired


@pytest.mark.unit
@pytest.mark.asyncio
async def test_generate_and_save_uses_structured_output_and_persists_thesis():
    chair_repo = AsyncMock()
    chair_repo.get_by_id.return_value = SimpleNamespace(
        id=6,
        name="Distributed Intelligence",
        short_description="Robotics and learning",
    )
    student_repo = AsyncMock()
    student_repo.get_by_user_id.return_value = None
    session = MagicMock()
    session.flush = AsyncMock()
    session.refresh = AsyncMock()
    thesis_repo = AsyncMock(session=session)
    chat = AsyncMock()
    chat.chat_structured.return_value = GeneratedProposalList(
        proposals=[
            GeneratedProposalItem(
                title="Learning Robust Robot Policies",
                abstract="A thesis about robust robot learning methods.",
                difficulty=ThesisDifficulty.master,
                skills_required=SkillsRequired(programming=["Python"]),
            )
        ]
    )
    embed = AsyncMock()
    embed.embed.return_value = [0.1, 0.2]
    settings = SimpleNamespace(effective_extract_model="chat-model", ollama_embed_model="embed-model")

    async def refresh(thesis):
        thesis.id = 42

    session.refresh.side_effect = refresh

    service = ProposalGenerationService(
        chair_repo=chair_repo,
        thesis_repo=thesis_repo,
        student_repo=student_repo,
        chat_client=chat,
        embed_client=embed,
        settings=settings,
    )

    result = await service.generate_and_save(
        chair_id=6,
        research_direction="robot learning",
        count=1,
        user_id=7,
        chat_session_id=8,
    )

    chat.chat_structured.assert_awaited_once()
    assert chat.chat_structured.call_args.kwargs["output_schema"] is GeneratedProposalList
    session.add.assert_called_once()
    thesis = session.add.call_args.args[0]
    assert thesis.title == "Learning Robust Robot Policies"
    assert thesis.embedding == [0.1, 0.2]
    thesis_repo.commit.assert_awaited_once()
    assert result["generated"] == 1
    assert result["proposals"] == [{"id": 42, "title": "Learning Robust Robot Policies", "difficulty": "master"}]
