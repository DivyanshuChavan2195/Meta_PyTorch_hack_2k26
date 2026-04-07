import os
import json
import requests
from typing import List, Optional
from openai import OpenAI


# =========================
# ENV CONFIG
# =========================

API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY") or ""
API_BASE_URL = os.getenv("API_BASE_URL") or "https://router.huggingface.co/v1"
MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"
BENCHMARK = os.getenv("TRUST_TRIAGE_BENCHMARK", "trust_triage_env")
ENV_BASE_URL = os.getenv("ENV_BASE_URL") or "https://sarthugg-trust-triage-env.hf.space"

MAX_STEPS = 5
SUCCESS_SCORE_THRESHOLD = 0.10

ALLOWED_ACTIONS = {"ACCEPT", "REJECT", "VERIFY", "DEFER", "ESCALATE"}

# Add enough tasks so evaluator can enumerate them
TASKS = [
    "easy_1", "easy_2", "easy_3", "easy_4",
    "medium_1", "medium_2", "medium_3", "medium_4", "medium_5",
    "hard_1", "hard_2", "hard_3", "hard_4"
]


# =========================
# OPENAI CLIENT
# =========================

client = None
if API_KEY:
    try:
        client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
    except Exception:
        client = None


# =========================
# STRICT LOGGING FORMAT
# =========================

def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    error_val = error if error else "null"
    done_val = str(done).lower()
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True,
    )


def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}",
        flush=True,
    )


# =========================
# ENV API HELPERS
# =========================

def reset_env(task_id: str) -> dict:
    response = requests.post(
        f"{ENV_BASE_URL}/reset",
        params={"task_id": task_id},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def step_env(action: str) -> dict:
    response = requests.post(
        f"{ENV_BASE_URL}/step",
        json={"action": action},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


# =========================
# HEURISTIC POLICY
# =========================

def heuristic_policy(obs: dict) -> str:
    contradiction = obs.get("contradiction_score", 0.0)
    verifier = obs.get("verifier_confidence", 0.0)
    source = obs.get("source_reliability", 0.0)
    risk = obs.get("risk_level", "medium")
    step = obs.get("time_step", 0)

    if step == 0:
        if risk == "high" and verifier < 0.4:
            return "VERIFY"
        if contradiction > 0.7:
            return "REJECT"
        if verifier > 0.8 and source > 0.7:
            return "ACCEPT"
        return "VERIFY"

    if contradiction > 0.8:
        return "REJECT"
    if verifier > 0.85 and source > 0.7:
        return "ACCEPT"
    if risk == "high":
        return "ESCALATE"

    return "DEFER"


# =========================
# OPTIONAL LLM POLICY
# =========================

def llm_policy(obs: dict) -> str:
    if client is None:
        return heuristic_policy(obs)

    prompt = f"""
You are a trust and safety decision agent.

Choose exactly one action from:
ACCEPT, REJECT, VERIFY, DEFER, ESCALATE

Observation:
{json.dumps(obs, indent=2)}

Return only the action name.
""".strip()

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a careful trust and safety evaluator."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
            max_tokens=10,
            stream=False,
        )

        action = (completion.choices[0].message.content or "").strip().upper()

        if action in ALLOWED_ACTIONS:
            return action

        return heuristic_policy(obs)

    except Exception:
        return heuristic_policy(obs)


# =========================
# SCORE NORMALIZATION
# =========================

def normalize_score(rewards: List[float]) -> float:
    if not rewards:
        return 0.001

    avg = sum(rewards) / len(rewards)

    # Force score to be strictly inside (0,1)
    score = max(0.001, min(0.999, avg))
    return round(score, 3)


# =========================
# RUN ONE TASK
# =========================

def run_task(task_name: str) -> None:
    rewards: List[float] = []
    steps_taken = 0
    success = False
    score = 0.001

    log_start(task=task_name, env=BENCHMARK, model=MODEL_NAME)

    try:
        obs = reset_env(task_name)
        done = obs.get("done", False)

        for step in range(1, MAX_STEPS + 1):
            if done:
                break

            action = llm_policy(obs)

            try:
                result = step_env(action)

                obs = result["observation"]
                reward = float(result.get("reward", 0.0))
                done = bool(result.get("done", False))
                info = result.get("info", {})

                error = None
                if isinstance(info, dict):
                    possible_error = info.get("error")
                    if possible_error:
                        error = str(possible_error)

            except Exception as step_exc:
                reward = 0.001
                done = True
                error = str(step_exc)

            rewards.append(reward)
            steps_taken = step

            log_step(step=step, action=action, reward=reward, done=done, error=error)

            if done:
                break

        score = normalize_score(rewards)
        success = score >= SUCCESS_SCORE_THRESHOLD

    except Exception as exc:
        rewards = [0.001]
        steps_taken = max(steps_taken, 1)
        score = 0.001
        success = False

        log_step(
            step=steps_taken,
            action="ERROR",
            reward=0.00,
            done=True,
            error=str(exc),
        )

    finally:
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)


# =========================
# MAIN
# =========================

def main() -> None:
    for task in TASKS:
        run_task(task)


if __name__ == "__main__":
    main()