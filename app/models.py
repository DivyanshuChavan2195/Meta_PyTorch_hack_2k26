from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal
from enum import Enum


# ENUMS
# ----------------------------

class ActionType(str, Enum):
    ACCEPT = "ACCEPT"
    REJECT = "REJECT"
    VERIFY = "VERIFY"
    DEFER = "DEFER"
    ESCALATE = "ESCALATE"


class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


# CORE MODELS
# ----------------------------

class Reset(BaseModel):
    claim_id: str
    claim_text: str
    source_reliability: float = Field(..., ge=0.0, le=1.0)
    evidence_count: int = Field(..., ge=0)
    contradiction_score: float = Field(..., ge=0.0, le=1.0)
    verifier_confidence: float = Field(..., ge=0.0, le=1.0)
    risk_level: RiskLevel
    time_step: int = Field(..., ge=0)
    history: List[str] = Field(default_factory=list)
    done: bool = False
    last_action_error: bool = False
    budget_remaining: float = Field(default=3.0, ge=0.0)
    total_cost: float = Field(default=0.0, ge=0.0)


# Alias for backward compatibility with inference.py
Observation = Reset


class Action(BaseModel):
    action: ActionType


class Reward(BaseModel):
    value: float
    reason: str


class Step(BaseModel):
    observation: Reset
    reward: float
    done: bool
    info: Dict[str, Any]
    explanation: str = ""


# Alias for backward compatibility with inference.py
StepResult = Step


class State(BaseModel):
    task_id: str
    ground_truth: Literal["true", "false", "uncertain"]
    current_observation: Reset
    steps_taken: int
    max_steps: int
    final_action: Optional[ActionType] = None


# Alias for backward compatibility with inference.py
EnvState = State