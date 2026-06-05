"""Optional DeepEval checks for generated thesis proposal quality.

These tests are intentionally opt-in: normal CI should be deterministic and
must not depend on external LLM judges or API credentials.
"""

from __future__ import annotations

import os

import pytest

pytestmark = pytest.mark.eval

deepeval = pytest.importorskip("deepeval", reason="Install deepeval to run optional LLM evals")


@pytest.mark.skipif(os.getenv("RUN_DEEPEVAL") != "1", reason="Set RUN_DEEPEVAL=1 to run LLM quality evals")
@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="Set OPENAI_API_KEY to run DeepEval GEval checks")
def test_robotics_proposal_fixture_is_relevant_and_actionable() -> None:
    from deepeval.metrics import GEval
    from deepeval.test_case import LLMTestCase, SingleTurnParams

    test_case = LLMTestCase(
        input=(
            "Student profile: strong Python and machine learning coursework. "
            "Chair: Distributed Intelligence, reinforcement learning, robotics, planning. "
            "Requested direction: robust robot policy learning."
        ),
        actual_output=(
            "Title: Robust Robot Policy Learning under Distribution Shift\n"
            "Abstract: This thesis studies how reinforcement learning policies for mobile robots can remain reliable "
            "when sensor noise and environment layouts differ from training data. The student will compare domain "
            "randomization and uncertainty-aware policy evaluation in simulation, then report failure modes and "
            "practical recommendations for robust deployment.\n"
            "Difficulty: master\n"
            "Skills: Python, reinforcement learning, robotics simulation, uncertainty estimation."
        ),
    )
    metric = GEval(
        name="Proposal relevance and actionability",
        criteria=(
            "Score high only if the proposal is clearly aligned with the chair and requested direction, "
            "contains a concrete research question or method, and is feasible for a thesis."
        ),
        evaluation_params=[SingleTurnParams.INPUT, SingleTurnParams.ACTUAL_OUTPUT],
        threshold=0.7,
    )

    metric.measure(test_case)

    assert metric.score is not None
    assert metric.score >= metric.threshold
