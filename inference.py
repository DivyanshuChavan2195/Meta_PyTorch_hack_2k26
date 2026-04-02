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
Evidence count: {obs.evidence_count}
Contradiction score: {obs.contradiction_score}
Verifier confidence: {obs.verifier_confidence}
Risk level: {obs.risk_level}
History: {obs.history}

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

    except Exception as e:
        print(f"LLM call failed: {e}")
        return heuristic_policy(obs)


def choose_action(obs):
    if USE_LLM:
        return llm_policy(obs)
    return heuristic_policy(obs)


def run_task(task_id):
    env = TrustTriageEnv()
    obs = env.reset(task_id)
    done = False
    total_reward = 0.0
    total_cost = 0.0
    final_score = 0.0
    steps = 0

    print(f"\n=== Running task: {task_id} ===")

    while not done:
        steps += 1
        action = choose_action(obs)
        print(f"Step {steps}: {action}")

        result = env.step(Action(action=action))
        obs = result.observation
        total_reward += result.reward
        total_cost = obs.total_cost
        done = result.done
        final_score = result.info.get("final_score", 0.0)

        print(f"  Reward: {result.reward:+.2f}")
        print(f"  Reason: {result.info.get('reason', '')}")
        print(f"  Done: {done}")

    return {
        "task_id": task_id,
        "steps": steps,
        "total_reward": total_reward,
        "total_cost": total_cost,
        "final_score": final_score
    }


def main():
    print("=== TrustTriageEnv Baseline Inference ===")
    print(f"Using model: {MODEL_NAME if USE_LLM else 'heuristic_baseline'}")

    results = []
    for task_id in TASKS:
        result = run_task(task_id)
        results.append(result)

    avg_score = sum(r["final_score"] for r in results) / len(results)
    avg_reward = sum(r["total_reward"] for r in results) / len(results)
    avg_cost = sum(r["total_cost"] for r in results) / len(results)
    avg_steps = sum(r["steps"] for r in results) / len(results)

    print("\n=== Final Results ===")
    for r in results:
        print(
            f"{r['task_id']}: "
            f"steps={r['steps']}, "
            f"reward={r['total_reward']:.2f}, "
            f"cost={r['total_cost']:.2f}, "
            f"score={r['final_score']:.2f}"
        )

    print(f"\nAverage Final Score: {avg_score:.2f}")
    print(f"Average Reward: {avg_reward:.2f}")
    print(f"Average Cost: {avg_cost:.2f}")
    print(f"Average Steps: {avg_steps:.1f}")


if __name__ == "__main__":
    main()