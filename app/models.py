from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict, Any


class Observation(BaseModel):
    claim_id: str
    claim_text: str
    source_reliability: float = Field(ge=0.0, le=1.0)
    evidence_count: int = Field(ge=0)
    contradiction_score: float = Field(ge=0.0, le=1.0)
    verifier_confidence: float = Field(ge=0.0, le=1.0)
    risk_level: Literal["low", "medium", "high"]
    time_step: int = Field(ge=0)
    history: List[str] = []
    done: bool = False
    last_action_error: bool = False


class Action(BaseModel):
    action: Literal["ACCEPT", "REJECT", "VERIFY", "DEFER", "ESCALATE"]


class Reward(BaseModel):
    value: float
    reason: str


class StepResult(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: Dict[str, Any]


class EnvState(BaseModel):
    task_id: str
    ground_truth: Literal["true", "false", "uncertain"]
    current_observation: Observation
    steps_taken: int
    max_steps: int
    final_action: Optional[str] = None