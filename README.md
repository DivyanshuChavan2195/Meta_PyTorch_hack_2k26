# RL Based News Investigation (Trust Triage Env) - Enhanced Edition

---
- title: Trust Triage Env
- emoji: 🧠
- colorFrom: blue
- colorTo: purple
- sdk: docker
- app_file: app.py
- app_port: 7860
- pinned: false
---

# Trust Triage Env – Project Evolution & System Upgrade

This document explains the **complete evolution of the TrustTriageEnv project**, including:

• the **original RL investigation environment design**
• the **new enhancements added to the system**
• the **technical improvements introduced for the Meta OpenEnv Hackathon**

The project demonstrates how **reinforcement learning environments can simulate real-world decision systems under uncertainty**.

---

# Project Background

TrustTriageEnv is a **Reinforcement Learning Style decision environment** designed to simulate how an automated trust & safety system processes incoming claims.

In many real world platforms, AI systems must quickly decide how to respond to incoming claims that may contain misinformation, uncertain data, or incomplete evidence.

Instead of simply predicting whether a claim is True or False, the system must decide **how to Investigate the Claim** before making a Final Decision.

This environment models that workflow.

The agent interacts with the environment by selecting actions such as:

• ACCEPT – accept the claim as true
• REJECT – reject the claim as false
• VERIFY – request additional verification signals
• DEFER – postpone decision until more evidence appears
• ESCALATE – escalate the claim for human review

Through repeated interaction, an agent learns **Decision Strategies under Uncertainty**.

---

<img width="1920" height="1080" alt="6" src="https://github.com/user-attachments/assets/47fedf0e-37df-4ddb-a57a-bac26fea7100" />

<img width="1920" height="1080" alt="5" src="https://github.com/user-attachments/assets/ad33107a-2939-46cb-b2f7-a47811a717c2" />

# Youtube Explaination Video
https://youtu.be/SNfxrL9Ex5E

---
### Core Features

• Claim investigation workflow simulation
• Step based environment (`step()`, `reset()` and `state()` models)
• Reward evaluation based on decision accuracy
• Final grading system for evaluating episodes
• Basic dataset containing a small number of tasks

### Observation Signals

Each claim contained signals such as:

• source reliability
• contradiction score
• verifier confidence
• number of supporting evidence items

These signals allowed agents to reason about the **credibility of incoming claims**.

### Decision Objective

The goal of the agent was to choose actions that **maximize reward while correctly identifying claims**.

While effective, the original system had limitations:

• no resource constraints
• no uncertainty modeling
• limited dataset
• minimal interpretability of decisions
---

## ✨ New Features (Enhanced Edition)

### 1. **Cost-Aware Action System** 💰

Each action has a **cost** that depletes from a limited budget:

| Action | Cost | Purpose |
|-----------|------|---------|
| VERIFY | 1.0 | Expensive verification |
| DEFER | 0.5 | Moderate postponement |
| ESCALATE | 2.0 | Very expensive escalation |
| ACCEPT | 0.2 | Cheap quick accept |
| REJECT | 0.2 | Cheap quick reject |

**Budget**: Agents start with **3.0 credits** and must manage resource usage.

```python
# Agent starts with budget = 3.0
# After ESCALATE (cost 2.0): budget = 1.0
# After VERIFY (cost 1.0): budget = 0.0
```

---

### 2. **Noisy/Uncertain Signals** 📊

When an agent chooses **VERIFY**, signals become **noisy** (±0.1 uncertainty):

Affected signals:
- `source_reliability`
- `contradiction_score`
- `verifier_confidence`

```python
# Example:
Original: source_reliability = 0.70
Noise added: +0.08
Result: 0.78

# Values clipped to [0, 1] range
```

---

### 3. **Reward Cost Penalty** 💸

Rewards are penalized based on action cost:

```
Final Reward = Original Reward - (0.1 × Action Cost)
```

**Example:**
```
Correct rejection (REJECT, cost 0.2):
Original reward: +1.0
Cost penalty: 0.1 × 0.2 = 0.02
Final reward: +0.98

High-risk escalation (ESCALATE, cost 2.0):
Original reward: +0.6
Cost penalty: 0.1 × 2.0 = 0.2
Final reward: +0.40
```

---

### 4. **Explanation Output** 📝

Every step returns a detailed explanation:

```
Action: ESCALATE | Cost: 2.0 | Budget remaining: 1.0 | Escalation appropriate for high-risk ambiguity.
```

Contains:
- Action taken
- Cost incurred
- Budget remaining
- Reason for reward

---

### 5. **Expanded Dataset** 📚

**15 benchmark tasks** (previously 3):

**Easy (5 tasks):**
- False claims: Asteroid impact, world ending, vaccine magnetism
- True claims: Water boiling point, Paris capital

**Medium (5 tasks):**
- Uncertain: Earthquake, tech acquisition, disease variant
- False: Celebrity scandal
- True: Scientific study benefits

**Hard (4 tasks):**
- Uncertain: Hospital denial, political payments, environmental disaster, research breakthrough

---

### 6. **Baseline Metrics Tracking** 📈

Inference script now tracks 4 metrics:

```
Average Final Score: 0.96
Average Reward: 0.72
Average Cost: 1.11 (NEW)
Average Steps: 1.1 (NEW)
```

Per-episode breakdown:
```
easy_1: steps=1, reward=0.98, cost=0.20, score=1.00
medium_2: steps=2, reward=0.58, cost=1.20, score=0.40
hard_1: steps=1, reward=0.40, cost=2.00, score=1.00
```

---

## 📦 Installation

### Requirements
- Python >= 3.10
- Dependencies: FastAPI, Uvicorn, Pydantic, OpenAI, OpenEnv-core

### Setup

```bash
# Clone repository
git clone https://huggingface.co/spaces/sarthugg/trust-triage-env.git
cd trust-triage-env

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1 # Windows
source venv/bin/activate # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

---

## 🚀 Usage

### Run Inference Script

```bash
# Basic (heuristic policy)
python inference.py
```

<img width="1060" height="808" alt="score with new features" src="https://github.com/user-attachments/assets/c5d1d4d7-264e-4d1d-9dd2-b71eb7b9e5ba" />

### With OpenAI LLM

Create `.env`:
```
OPENAI_API_KEY=your-api-key
MODEL_NAME=gpt-4-mini
API_BASE_URL=https://api.openai.com/v1
```

Then run:
```bash
python inference.py
```

---

### Start FastAPI Server

```bash
uvicorn app.server:app --reload
```

Access at: `http://localhost:7860/docs`

**Endpoints:**
- `GET /` - Health check
- `POST /reset?task_id=easy_1` - Reset environment
- `POST /step` - Perform action
- `GET /state` - Get current state
- `GET /docs` - Swagger UI

---

## 📊 Observation Space

Each observation includes:

```python
{
"claim_id": str,
"claim_text": str,
"source_reliability": float [0, 1],
"evidence_count": int,
"contradiction_score": float [0, 1],
"verifier_confidence": float [0, 1],
"risk_level": "low" | "medium" | "high",
"time_step": int,
"history": List[str],
"done": bool,
"last_action_error": bool,
"budget_remaining": float, # NEW
"total_cost": float # NEW
}
```

---

## 🎬 Action Space

```python
class ActionType(str, Enum):
ACCEPT = "ACCEPT"
REJECT = "REJECT"
VERIFY = "VERIFY"
DEFER = "DEFER"
ESCALATE = "ESCALATE"
```

Send action as:
```json
{"action": "ACCEPT"}
```

---

## 📈 Example Episode

```
Task: medium_2 (Tech acquisition - uncertain)
Initial Budget: 3.0

Step 1: VERIFY (cost 1.0)
├─ Adds noise to signals
├─ Updates with verification data
├─ Reward: -0.30 (after cost penalty)
├─ Budget: 2.0
└─ Done: False

Step 2: ACCEPT (cost 0.2)
├─ Accepts with high confidence
├─ Reward: +0.78 (after cost penalty)
├─ Budget: 1.8
└─ Done: True (terminal action)

Final Metrics:
├─ Total reward: 0.58
├─ Total cost: 1.20
├─ Steps: 2
└─ Final score: 0.40
```

---

## 🏗️ Project Structure

```
trust-triage-env/
├── app/
│ ├── __init__.py
│ ├── env.py # Main environment (cost, noise, budget)
│ ├── models.py # Pydantic models (observation, action, reward)
│ ├── reward.py # Reward computation (with cost penalty)
│ ├── graders.py # Episode grading logic
│ ├── tasks.py # 15 benchmark tasks (expanded)
│ ├── server.py # FastAPI endpoints
│ └── ...
├── server/
│ └── app.py # Uvicorn entry point
├── tests/
│ └── test_env.py # Unit tests
├── inference.py # Baseline inference script (with metrics)
├── requirements.txt # Dependencies
├── pyproject.toml # Project config
├── Dockerfile # Docker build
└── README.md # This file
```

---

## 🔍 Key Changes

| Component | Change | Impact |
|-----------|--------|--------|
| `models.py` | Added `budget_remaining`, `total_cost`, `explanation` fields | Track resources and interpretability |
| `env.py` | Added cost mapping, noise function, budget deduction | Cost-aware decision-making |
| `reward.py` | Added cost penalty calculation | Incentivize efficiency |
| `tasks.py` | Expanded from 3 → 15 tasks | Comprehensive benchmarking |
| `inference.py` | Added cost & steps tracking | Better performance analysis |

---

## 📋 Specifications

### Cost Mapping
```python
ACTION_COSTS = {
"VERIFY": 1.0,
"DEFER": 0.5,
"ESCALATE": 2.0,
"ACCEPT": 0.2,
"REJECT": 0.2,
}
```

### Noise Function
```python
def add_noise(value: float, noise_range: float = 0.1) -> float:
"""Add random noise [-0.1, +0.1] and clip to [0, 1]."""
noise = random.uniform(-noise_range, noise_range)
noisy_value = value + noise
return max(0.0, min(1.0, noisy_value))
```

### Tasks
- **Easy**: 5 tasks (obvious true/false claims)
- **Medium**: 5 tasks (uncertain + false + true)
- **Hard**: 4 tasks (high-risk uncertain claims)
- **Total**: 15 benchmark tasks

---

## 🧪 Testing

```bash
# Run tests
pytest tests/

# Run inference on all 15 tasks
python inference.py

# Start server and test endpoints
uvicorn app.server:app --reload
```

---

## 🚢 Deployment

### Docker

```bash
docker build -t trust-triage-env .
docker run -p 7860:7860 trust-triage-env
```

### Hugging Face Spaces

```bash
git push https://HF_TOKEN@huggingface.co/spaces/sarthugg/trust-triage-env main
```

### GitHub

```bash
git push github main
```

---


## 📊 Performance Baseline

Current heuristic baseline on 15 tasks:

```
Average Final Score: 0.96
Average Reward: 0.72
Average Cost: 1.11
Average Steps: 1.1

Easy tasks: 1.00 score (5/5 correct)
Medium tasks: 0.96 score (4.8/5 correct)
Hard tasks: 0.92 score (3.68/4 correct)
```

---

## 📝 License

This project is part of the Meta PyTorch Hackathon 2k26.

---

**Happy Triaging!** 🚀
