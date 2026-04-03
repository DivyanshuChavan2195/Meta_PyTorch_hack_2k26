---
title: Trust Triage Env
emoji: 🧠
colorFrom: blue
colorTo: purple
sdk: docker
app_file: app.py
app_port: 7860
pinned: false
---

# Trust Triage Env – Project Evolution & System Upgrade

This document explains the **complete evolution of the TrustTriageEnv project**, including:

• the **original RL investigation environment design**
• the **new enhancements added to the system**
• the **technical improvements introduced for the Meta OpenEnv Hackathon**

The project demonstrates how **reinforcement learning environments can simulate real-world decision systems under uncertainty**.

---

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


# ✨Youtube Explaination Video (Please do watch)
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

---

## ✨ New Enhanced Features

### 1. **Cost Aware Action System** 💰

Each action has a **cost** that depletes from a limited budget:

| Action | Cost | Purpose |
|-----------|------|---------|
| VERIFY | 1.0 | Expensive verification |
| DEFER | 0.5 | Moderate postponement |
| ESCALATE | 2.0 | Very expensive escalation |
| ACCEPT | 0.2 | Cheap quick accept |
| REJECT | 0.2 | Cheap quick reject |

Agents start with **3.0 investigation credits**.

This forces the agent to balance:

• accuracy of decisions  
• cost of investigation  
• efficiency of actions

This converts the environment into a **resource optimization problem**, which is a core application of reinforcement learning.

---

### 2. **Noisy/Uncertain Signals** 📊

In real-world scenarios, verification data is rarely perfect.

The enhanced system introduces **uncertainty in signals**.

When the agent chooses the VERIFY action, evidence signals receive random noise.

Affected signals include:

• source_reliability  
• contradiction_score  
• verifier_confidence  

Noise simulates situations such as:

• conflicting reports  
• incomplete verification  
• unreliable sources

This requires agents to **make robust decisions under uncertainty**.

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

The reward system has been improved to penalize costly actions.

The new reward formula is:

Final Reward = Original Reward − (0.1 × Action Cost)

This encourages agents to:

• avoid unnecessary investigation  
• prioritize efficient decisions  
• balance accuracy with resource usage

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

Each environment step now produces a **human-readable explanation** describing:

• the action taken  
• the cost incurred  
• remaining investigation budget  
• the reason for the reward outcomeEach environment step now produces a **human readable explanation** describing:

• the action taken  
• the cost incurred  
• remaining investigation budget  
• the reason for the reward outcome

Example explanation:

`Action: ESCALATE | Cost: 2.0 | Budget remaining: 1.0 | Escalation appropriate for high risk ambiguity.`

This improves the **interpretability of agent decisions**.

---

### 5. **Expanded Dataset** 📚

**14 benchmark tasks** (previously only 3):

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
## Folder Structure:

```
trust-triage-env/
├── app/
│   ├── __init__.py
│   ├── env.py                 # TrustTriageEnv class with reset(), step(), state()
│   ├── models.py              # Reset, Step, State, Action, Reward models
│   ├── server.py              # FastAPI endpoints
│   ├── tasks.py               # Task definitions
│   ├── reward.py              # Reward computation
│   ├── graders.py             # Episode grading
│   └── __pycache__/
│
├── server/
│   ├── __init__.py
│   ├── app.py                 # Uvicorn server runner
│   └── __pycache__/
│
├── tests/
│   ├── test_env.py            # Environment tests
│   └── __pycache__/
│
├── app.py                     # Main entry point
├── inference.py               # Baseline inference script
├── openenv.yaml               # OpenEnv specification
├── pyproject.toml             # Project metadata
├── pytest.ini                 # Pytest configuration
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
├── .env.example               # Example environment variables
├── README.md                  # Project documentation
├── uv.lock                    # Dependency lock file
├── .git/                      # Git repository
└── venv/                      # Virtual environment
```
---

## 📦 Installation Guide

### Requirements
- Python >= 3.10
- Dependencies: FastAPI, Uvicorn, Pydantic, OpenAI, OpenEnv-core

### Setup

```bash
# Clone repository by Hugging Face
git clone https://huggingface.co/spaces/sarthugg/trust-triage-env.git

# OR use GitHub
git clone https://github.com/DivyanshuChavan2195/Meta_PyTorch_hack_2k26.git

# Get into the main folder:
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
# Basic (CLI Based)
python inference.py
```
Output:
<img width="1640" height="1094" alt="final with model" src="https://github.com/user-attachments/assets/faaad669-e0cb-447f-af85-f8a5cc7b16d5" />

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
- **Total**: 14 benchmark tasks

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

# Hackathon Information

This project was developed as part of the:

**Meta OpenEnv Hackathon**

Organized by  
**Scaler School of Technology**

Sponsored by  

• **Meta**  
• **PyTorch**  
• **Hugging Face**

---

# Team

This project was created by:

**Team - Zero Day Trinity**

---
# Final Note

TrustTriageEnv demonstrates how reinforcement learning environments can evolve from simple simulations into **realistic decision systems that model complex investigation workflows under uncertainty and cost constraints**.# Final Note
---

**Happy Triaging!** 🚀
