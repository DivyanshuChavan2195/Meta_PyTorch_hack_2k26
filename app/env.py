from app.models import Observation, Action, StepResult, EnvState
from app.tasks import TASKS
from app.reward import compute_reward
from app.graders import grade_episode


class TrustTriageEnv:
    def __init__(self):
        self.task = None
        self.state_data = None
        self.verified = False

    def reset(self, task_id: str = "easy_1") -> Observation:
        if task_id not in TASKS:
            raise ValueError(f"Unknown task_id: {task_id}")

        self.task = TASKS[task_id]
        self.verified = False

        obs = Observation(
            claim_id=self.task["id"],
            claim_text=self.task["claim_text"],
            source_reliability=self.task["initial_signals"]["source_reliability"],
            evidence_count=self.task["initial_signals"]["evidence_count"],
            contradiction_score=self.task["initial_signals"]["contradiction_score"],
            verifier_confidence=self.task["initial_signals"]["verifier_confidence"],
            risk_level=self.task["risk_level"],
            time_step=0,
            history=[],
            done=False,
            last_action_error=False,
        )

        self.state_data = EnvState(
            task_id=task_id,
            ground_truth=self.task["ground_truth"],
            current_observation=obs,
            steps_taken=0,
            max_steps=3,
            final_action=None,
        )

        return obs

    def step(self, action: Action) -> StepResult:
        if self.state_data is None:
            raise ValueError("Environment not initialized. Call reset() first.")

        obs = self.state_data.current_observation
        self.state_data.steps_taken += 1
        done = False
        info = {}

        obs.history.append(action.action)

        # VERIFY changes the world state
        if action.action == "VERIFY" and not self.verified:
            update = self.task["verify_update"]
            obs.source_reliability = update["source_reliability"]
            obs.evidence_count = update["evidence_count"]
            obs.contradiction_score = update["contradiction_score"]
            obs.verifier_confidence = update["verifier_confidence"]
            self.verified = True

        reward, reason = compute_reward(self.task, obs, action.action)

        # Terminal actions
        if action.action in ["ACCEPT", "REJECT", "ESCALATE"]:
            done = True
            self.state_data.final_action = action.action
            info["final_score"] = grade_episode(
                self.task,
                action.action,
                self.state_data.steps_taken
            )

        if self.state_data.steps_taken >= self.state_data.max_steps:
            done = True
            if not self.state_data.final_action:
                self.state_data.final_action = action.action
            info["final_score"] = grade_episode(
                self.task,
                self.state_data.final_action,
                self.state_data.steps_taken
            )

        obs.time_step = self.state_data.steps_taken
        obs.done = done

        self.state_data.current_observation = obs

        return StepResult(
            observation=obs,
            reward=reward,
            done=done,
            info={
                "reason": reason,
                **info
            }
        )

    def state(self):
        return self.state_data