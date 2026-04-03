import os
from dotenv import load_dotenv
from openai import OpenAI

from app.env import TrustTriageEnv
from app.models import Action
from app.tasks import TASKS

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
HF_TOKEN = os.getenv("HF_TOKEN", "")

USE_LLM = bool(OPENAI_API_KEY)

client = None
if USE_LLM:
    client = OpenAI(
        api_key=OPENAI_API_KEY,
        base_url=API_BASE_URL
    )

SYSTEM_PROMPT = """
You are an agent acting inside a fact-triage environment.

You must choose exactly one action from:
ACCEPT
REJECT
VERIFY
DEFER
ESCALATE

Choose the safest and most rational action based on the observation.
Respond with only the action word.
""".strip()


def log_start(task: str, env_name: str, model: str):
    print(f"[START] task={task} env={env_name} model={model}")


def log_step(step: int, action: str, reward: float, done: bool, error: str | None):
    reward_str = f"{reward:.2f}"
    done_str = "true" if done else "false"
    error_str = "null" if error is None else error.replace("\n", " ").strip()
    print(f"[STEP] step={step} action={action} reward={reward_str} done={done_str} error={error_str}")


def log_end(success: bool, steps: int, rewards: list[float]):
    success_str = "true" if success else "false"
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={success_str} steps={steps} rewards={rewards_str}")


def heuristic_policy(obs):
    if obs.contradiction_score > 0.7:
        return "REJECT"
    if obs.verifier_confidence > 0.75:
        return "ACCEPT"
    if obs.risk_level == "high" and 0.3 <= obs.verifier_confidence <= 0.7:
        return "ESCALATE"
    return "VERIFY"


def llm_policy(obs):
    prompt = f"""
Claim: {obs.claim_text}
Source reliability: {obs.source_reliability}
Evidence count: {getattr(obs, 'evidence_count', 'unknown')}
Contradiction score: {obs.contradiction_score}
Verifier confidence: {obs.verifier_confidence}
Risk level: {obs.risk_level}
History: {getattr(obs, 'history', '')}

What should the agent do next?
""".strip()

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=10
        )
        action = (response.choices[0].message.content or "").strip().upper()

        if action not in ["ACCEPT", "REJECT", "VERIFY", "DEFER", "ESCALATE"]:
            return heuristic_policy(obs)

        return action

    except Exception:
        return heuristic_policy(obs)


def choose_action(obs):
    if USE_LLM:
        return llm_policy(obs)
    return heuristic_policy(obs)


def run_task(task_id):
    env = TrustTriageEnv()
    rewards = []
    steps = 0
    success = False

    try:
        obs = env.reset(task_id)
        log_start(task=task_id, env_name="trust_triage_env", model=MODEL_NAME)

        done = False
        while not done:
            steps += 1
            action = choose_action(obs)

            try:
                result = env.step(Action(action=action))
                obs = result.observation
                reward = float(result.reward)
                done = bool(result.done)
                rewards.append(reward)

                log_step(
                    step=steps,
                    action=action,
                    reward=reward,
                    done=done,
                    error=None
                )

            except Exception as step_exc:
                log_step(
                    step=steps,
                    action=action,
                    reward=0.0,
                    done=True,
                    error=str(step_exc)
                )
                done = True
                return {
                    "success": False,
                    "steps": steps,
                    "rewards": rewards,
                }

        success = True

    except Exception as episode_exc:
        if steps == 0:
            # still emit step 0 if reset failed
            log_step(step=0, action="NONE", reward=0.0, done=True, error=str(episode_exc))
        success = False

    finally:
        try:
            env.close()
        except Exception:
            pass

        log_end(success=success, steps=steps, rewards=rewards)

    return {
        "success": success,
        "steps": steps,
        "rewards": rewards,
    }


def main():
    for task_id in TASKS:
        run_task(task_id)


if __name__ == "__main__":
    main()