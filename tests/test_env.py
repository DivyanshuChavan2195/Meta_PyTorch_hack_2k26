import pytest
from app.env import TrustTriageEnv
from app.models import Action
from app.graders import grade_episode
from app.tasks import TASKS


# ----------------------------
# BASIC TASK FLOW TESTS
# ----------------------------

def test_easy_reject_flow():
    env = TrustTriageEnv()
    obs = env.reset("easy_1")
    assert obs.claim_id == "easy_1"
    assert obs.done is False

    result = env.step(Action(action="VERIFY"))
    assert result.reward > 0
    assert result.done is False

    result = env.step(Action(action="REJECT"))
    assert result.done is True
    assert result.info["final_score"] >= 0.8


def test_medium_escalate_flow():
    env = TrustTriageEnv()
    obs = env.reset("medium_1")
    assert obs.claim_id == "medium_1"

    result = env.step(Action(action="ESCALATE"))
    assert result.done is True
    assert 0.0 <= result.info["final_score"] <= 1.0


def test_hard_escalate_flow():
    env = TrustTriageEnv()
    obs = env.reset("hard_1")
    assert obs.claim_id == "hard_1"

    result = env.step(Action(action="ESCALATE"))
    assert result.done is True
    assert result.info["final_score"] == 1.0


# ----------------------------
# STATE TRANSITION TESTS
# ----------------------------

def test_verify_changes_observation():
    env = TrustTriageEnv()
    obs = env.reset("easy_1")

    old_evidence = obs.evidence_count
    old_confidence = obs.verifier_confidence

    result = env.step(Action(action="VERIFY"))
    new_obs = result.observation

    assert new_obs.evidence_count != old_evidence
    assert new_obs.verifier_confidence != old_confidence
    assert "VERIFY" in new_obs.history


def test_max_steps_ends_episode():
    env = TrustTriageEnv()
    env.reset("hard_1")

    env.step(Action(action="DEFER"))
    env.step(Action(action="VERIFY"))
    result = env.step(Action(action="DEFER"))

    assert result.done is True
    assert "final_score" in result.info


# ----------------------------
# GRADER TESTS
# ----------------------------

def test_grader_false_claim_reject():
    task = TASKS["easy_1"]
    score = grade_episode(task, "REJECT", 2)
    assert score == 1.0


def test_grader_uncertain_claim_escalate():
    task = TASKS["hard_1"]
    score = grade_episode(task, "ESCALATE", 1)
    assert score == 1.0


def test_grader_score_range():
    for task_id, task in TASKS.items():
        for action in ["ACCEPT", "REJECT", "VERIFY", "DEFER", "ESCALATE"]:
            score = grade_episode(task, action, 2)
            assert 0.0 <= score <= 1.0


# ----------------------------
# ERROR HANDLING TESTS
# ----------------------------

def test_invalid_task_raises():
    env = TrustTriageEnv()
    with pytest.raises(ValueError):
        env.reset("not_a_real_task")


def test_step_before_reset_raises():
    env = TrustTriageEnv()
    with pytest.raises(ValueError):
        env.step(Action(action="VERIFY"))