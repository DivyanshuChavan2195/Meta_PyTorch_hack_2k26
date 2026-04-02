import random
from app.models import Observation, Action, StepResult, EnvState
from app.tasks import TASKS
from app.reward import compute_reward
from app.graders import grade_episode


# Action costs mapping
ACTION_COSTS = {
    "VERIFY": 1.0,
    "DEFER": 0.5,
    "ESCALATE": 2.0,
    "ACCEPT": 0.2,
    "REJECT": 0.2,
}


def add_noise(value: float, noise_range: float = 0.1) -> float:
    """Add random noise to a value and clip to [0, 1]."""
    noise = random.uniform(-noise_range, noise_range)
    noisy_value = value + noise
    return max(0.0, min(1.0, noisy_value))


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
            budget_remaining=3.0,
            total_cost=0.0,
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

        # Get action cost
        action_cost = ACTION_COSTS.get(action.action, 0.0)

        # Apply noise if action is VERIFY
        if action.action == "VERIFY" and not self.verified:
            obs.source_reliability = add_noise(obs.source_reliability)
            obs.contradiction_score = add_noise(obs.contradiction_score)
            obs.verifier_confidence = add_noise(obs.verifier_confidence)
            
            update = self.task["verify_update"]
            obs.source_reliability = update["source_reliability"]
            obs.evidence_count = update["evidence_count"]
            obs.contradiction_score = update["contradiction_score"]
            obs.verifier_confidence = update["verifier_confidence"]
            self.verified = True

        # Deduct cost from budget and track total cost
        obs.budget_remaining -= action_cost
        obs.total_cost += action_cost

        reward, reason = compute_reward(self.task, obs, action.action, action_cost)

        # Generate explanation
        explanation = f"Action: {action.action} | Cost: {action_cost:.1f} | Budget remaining: {obs.budget_remaining:.1f} | {reason}"

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
            },
            explanation=explanation
        )

    def state(self):
        return self.state_data