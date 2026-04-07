import os
import json
import time
import requests
from openai import OpenAI


# =========================
# ENV CONFIG
# =========================

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN", "")

# Your deployed environment URL
ENV_BASE_URL = "https://sarthugg-trust-triage-env.hf.space"


# =========================
# OPENAI CLIENT (SAFE)
# =========================

client = None
if HF_TOKEN:
    try:
        client = OpenAI(
            api_key=HF_TOKEN,
            base_url=API_BASE_URL
        )
    except Exception as e:
        print(f"[WARN] Failed to initialize OpenAI client: {e}")
        client = None


# =========================
# TASKS
# =========================

TASKS = ["easy_1", "medium_1", "hard_1"]


# =========================
# HEURISTIC FALLBACK POLICY
# =========================

def heuristic_policy(obs):
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
# LLM POLICY (OPTIONAL)
# =========================

def llm_policy(obs):
    if client is None:
        return heuristic_policy(obs)

    prompt = f"""
You are a trust and safety decision agent.

Given the observation below, choose exactly one action from:
ACCEPT, REJECT, VERIFY, DEFER, ESCALATE

Observation:
{json.dumps(obs, indent=2)}

Return only the action name.
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a careful trust and safety evaluator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0
        )

        action = response.choices[0].message.content.strip().upper()

        allowed = {"ACCEPT", "REJECT", "VERIFY", "DEFER", "ESCALATE"}
        if action in allowed:
            return action

        return heuristic_policy(obs)

    except Exception as e:
        print(f"[WARN] LLM call failed, falling back to heuristic: {e}")
        return heuristic_policy(obs)


# =========================
# API HELPERS
# =========================

def reset_env(task_id):
    response = requests.post(f"{ENV_BASE_URL}/reset", params={"task_id": task_id}, timeout=30)
    response.raise_for_status()
    return response.json()


def step_env(action):
    response = requests.post(
        f"{ENV_BASE_URL}/step",
        json={"action": action},
        timeout=30
    )
    response.raise_for_status()
    return response.json()


# =========================
# MAIN EVAL LOOP
# =========================

def run_task(task_id):
    print(f"\n[START] Task: {task_id}")

    obs = reset_env(task_id)
    total_reward = 0.0
    done = False
    step_num = 0

    while not done and step_num < 5:
        action = llm_policy(obs)

        print(f"[STEP] {step_num + 1}")
        print(f"Action: {action}")
        print(f"Observation: {json.dumps(obs)}")

        result = step_env(action)

        obs = result["observation"]
        reward = result["reward"]
        done = result["done"]
        info = result.get("info", {})

        total_reward += reward
        step_num += 1

        print(f"Reward: {reward}")
        print(f"Done: {done}")
        print(f"Info: {json.dumps(info)}")

        time.sleep(0.5)

    avg_score = max(0.0, min(1.0, total_reward / max(step_num, 1)))

    print(f"[END] Task: {task_id}")
    print(f"Total Reward: {total_reward}")
    print(f"Score: {avg_score:.3f}")

    return {
        "task_id": task_id,
        "total_reward": total_reward,
        "score": avg_score
    }


def main():
    all_results = []

    for task_id in TASKS:
        try:
            result = run_task(task_id)
            all_results.append(result)
        except Exception as e:
            print(f"[ERROR] Task {task_id} failed: {e}")
            all_results.append({
                "task_id": task_id,
                "total_reward": 0.0,
                "score": 0.0
            })

    print("\n===== FINAL RESULTS =====")
    print(json.dumps(all_results, indent=2))


if __name__ == "__main__":
    main()