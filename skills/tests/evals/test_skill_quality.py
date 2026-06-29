"""Optional LLM-as-judge checks for the portable thesis-finder skills.

These tests are opt-in because they require an external judge model and are
not deterministic enough for the normal local quality gate.
"""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path

import pytest


SKILLS_DIR = Path(__file__).resolve().parents[2]


def _skill_context(skill_name: str) -> str:
    skill_dir = SKILLS_DIR / skill_name
    parts = [(skill_dir / "SKILL.md").read_text(encoding="utf-8")]
    references_dir = skill_dir / "references"
    if references_dir.exists():
        for reference in sorted(references_dir.glob("*.md")):
            parts.append(f"\n# Reference: {reference.name}\n{reference.read_text(encoding='utf-8')}")
    return "\n\n".join(parts)


pytestmark = [
    pytest.mark.eval,
    pytest.mark.skipif(os.getenv("RUN_DEEPEVAL") != "1", reason="Set RUN_DEEPEVAL=1 to run LLM quality evals"),
    pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Set OPENAI_API_KEY to run DeepEval GEval checks"),
    pytest.mark.skipif(importlib.util.find_spec("deepeval") is None, reason="Install deepeval to run optional LLM evals"),
]


@pytest.mark.parametrize(
    ("skill_name", "user_prompt", "actual_output", "criteria"),
    [
        (
            "build-student-profile",
            "I liked ML, statistics, and neural data analysis courses. I can code Python and want a master thesis with real data.",
            (
                "Student thesis profile:\n"
                "- Thesis level: master, inferred from the prompt.\n"
                "- Interests: machine learning, statistics, neural data analysis, real-data projects.\n"
                "- Skills: Python programming, ML/statistics coursework.\n"
                "- Matching keywords: neural data analysis; machine learning; statistical modeling; real-world datasets.\n"
                "- Missing information: preferred chairs, time constraints, and whether the student wants theory, modeling, or applied analysis. "
                "This profile should stay in the current conversation only and should not be written to bundled skill resources."
            ),
            (
                "Score high only if the answer extracts interests, skills, constraints, and matching keywords, marks inferred facts, "
                "asks only material follow-ups, and explicitly avoids persisting private student data."
            ),
        ),
        (
            "design-agent-skill",
            "Create a portable skill for reviewing thesis proposal drafts.",
            (
                "Skill package: `review-thesis-proposal`.\n"
                "Frontmatter:\n"
                "---\n"
                "name: review-thesis-proposal\n"
                "description: Review thesis proposal drafts for clarity, feasibility, research fit, and evidence. Use when asked to critique, improve, or score a bachelor or master thesis proposal draft.\n"
                "---\n"
                "Body outline: identify thesis level and field, check research question, methods, scope, evidence, supervision fit, and risks. Put detailed scoring rubrics in `references/proposal-review-rubric.md`. Avoid client-specific metadata and do not store private student data in bundled resources."
            ),
            (
                "Score high only if the output follows the design-agent-skill workflow: proposes a portable skill with valid name and trigger-rich description, "
                "separates core instructions from references, avoids client-specific assumptions, and explicitly protects private student data."
            ),
        ),
        (
            "find-recent-papers",
            "I'm interested in differentiable robotics and reinforcement learning. Find recent papers that could inspire a master thesis.",
            (
                "1. Diffusion Policy: Visuomotor Policy Learning via Action Diffusion (2023), Chi et al., Robotics: Science and Systems / project and arXiv pages. "
                "Why it matters: it connects modern generative modeling with robot manipulation and suggests thesis angles around robustness, data efficiency, or sim-to-real evaluation.\n"
                "2. RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control (2023), Brohan et al., arXiv / Google DeepMind. "
                "Why it matters: useful for a thesis conversation about foundation models for robotics; a local project could narrow this to evaluation or failure analysis.\n"
                "3. Learning Fine-Grained Bimanual Manipulation with Low-Cost Hardware (ALOHA, 2023), Zhao et al., arXiv / project page. "
                "Why it matters: a practical thesis angle could compare imitation-learning data collection strategies for manipulation. These leads should be verified against primary pages before citing final venue or acceptance status."
            ),
            (
                "Score high only if the answer behaves like find-recent-papers: it recommends recent traceable papers, includes dates/authors/sources, "
                "explains thesis relevance, labels uncertainty, and avoids fabricated citation counts, venues, affiliations, or guarantees."
            ),
        ),
        (
            "find-university-chairs",
            "Which university chairs might fit a thesis on neural data analysis and machine learning?",
            (
                "Potential matches to investigate:\n"
                "1. Machine Learning / probabilistic modeling groups: strong fit if their recent publications mention neural data, representation learning, or Bayesian inference. Conversation starter: ask whether a thesis could evaluate ML models on neural recordings.\n"
                "2. Computational neuroscience or neural data science groups: strong fit for the application area, especially if current lab pages or recent papers discuss spike trains, calcium imaging, or brain-computer interfaces.\n"
                "3. Biomedical data analysis groups: possible fit when they combine statistical learning with biological signals.\n"
                "Before contacting anyone, verify each chair's official university page and recent publications, then write a short email linking your coursework, ML experience, and one specific paper. Public pages can be stale, so do not assume openings or supervision capacity."
            ),
            (
                "Score high only if the answer behaves like find-university-chairs: it ranks plausible chair types or supervisors by research fit, "
                "uses evidence-aware caveats, prepares high-signal contact, distinguishes research areas from fixed thesis openings, and does not invent quotas, team sizes, citation counts, or willingness to supervise."
            ),
        ),
        (
            "generate-thesis-directions",
            "Generate thesis directions from a match to a neural data analysis chair and recent ML papers.",
            (
                "Possible direction: Robust representation learning for neural recordings.\n"
                "Research question: How stable are learned neural representations across sessions or subjects?\n"
                "Method: compare baseline statistical models with a modern representation-learning approach on a public neural dataset, if the supervisor confirms data access.\n"
                "Fit: relevant for a chair working on neural data analysis and ML.\n"
                "Prerequisites: Python, statistics, ML evaluation, and careful experiment design.\n"
                "Meeting question: Which datasets and evaluation protocols would make this feasible for a master thesis? This is a conversation starter, not an advertised topic."
            ),
            (
                "Score high only if the answer creates a concrete but tentative thesis direction grounded in profile/paper/chair evidence, "
                "states methods and prerequisites, and avoids pretending the topic is officially available."
            ),
        ),
        (
            "draft-thesis-contact",
            "Draft an email to a possible supervisor for a neural data analysis master thesis.",
            (
                "Subject: Master thesis inquiry on ML methods for neural data analysis\n\n"
                "Dear Dr. Example,\n\n"
                "I am a master's student interested in machine learning for neural data analysis. My strongest preparation is Python, statistics, and ML coursework, and I was particularly interested in your group's recent work on data-driven analysis of neural recordings. I would like to ask whether there might be room to discuss a possible thesis direction around robust evaluation of ML models on neural datasets.\n\n"
                "If this is broadly aligned with your current supervision interests, I would be grateful for a short meeting or a pointer to someone in the group who works on this topic.\n\n"
                "Best regards,\n"
                "Student\n\n"
                "Rationale: the email names a concrete area, connects it to the student's background, and asks for a conversation rather than assuming an open topic."
            ),
            (
                "Score high only if the answer is concise, specific, polite, grounded in profile and chair evidence, avoids spam-like generic phrasing, "
                "and does not invent openings, funding, or supervision promises."
            ),
        ),
        (
            "thesis-finder",
            "I want to find where to write my master's thesis. I'm interested in machine learning and neuroscience, prefer empirical work, want to work in Germany, and don't want pure theory.",
            (
                "Based on your profile, you have two paths:\n"
                "(a) University at Tübingen — machine learning and neuroscience groups across all faculties, live discovery of active chairs.\n"
                "(b) Company in Baden-Württemberg (BW-region only) — ML/AI R&D teams and labs.\n\n"
                "Answer: Which path fits better, or do you want to explore both? I can then run the full discovery for your chosen path(s) and match you to specific supervisors, labs, and companies with concrete evidence."
            ),
            (
                "Score high only if the answer behaves like thesis-finder: routes to one or both discovery skills, "
                "asks the student to choose rather than deciding unilaterally, and does not attempt to produce a full option map itself."
            ),
        ),
        (
            "find-company-thesis-options",
            "I want to find companies in Baden-Württemberg for a master's thesis in machine learning applied to automotive systems. I have Python, PyTorch, and want a structured environment.",
            (
                "Candidate companies:\n"
                "1. Daimler / Mercedes-Benz AI Research — automotive AI, large structured program.\n"
                "2. Bosch Center for AI — automotive and robotics AI, competitive, apply via careers.\n"
                "3. Zeiss — optical systems + ML, smaller team, unclear thesis signal.\n\n"
                "For each, the output includes: company size, R&D focus, thesis signal (explicit opening / active program / unclear), contact path, and evidence date. All marked with verification caveats and sources."
            ),
            (
                "Score high only if the answer behaves like find-company-thesis-options: filters from BW backbone, "
                "enriches with live web evidence, marks thesis signal clearly (never invents availability), links all URLs to company pages, and includes the map-level coverage caveat."
            ),
        ),
    ],
)
def test_skill_fixture_output_matches_skill_rubric(skill_name: str, user_prompt: str, actual_output: str, criteria: str) -> None:
    from deepeval.metrics import GEval
    from deepeval.test_case import LLMTestCase, SingleTurnParams

    test_case = LLMTestCase(
        input=f"Skill under test:\n{_skill_context(skill_name)}\n\nUser prompt:\n{user_prompt}",
        actual_output=actual_output,
    )
    metric = GEval(
        name=f"{skill_name} behavior",
        criteria=criteria,
        evaluation_params=[SingleTurnParams.INPUT, SingleTurnParams.ACTUAL_OUTPUT],
        threshold=0.7,
    )

    metric.measure(test_case)

    assert metric.score is not None
    assert metric.score >= metric.threshold
