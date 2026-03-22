from dataclasses import dataclass, field
from typing import Any


@dataclass
class PlanStep:
    id: int
    name: str
    tool: str
    args: dict[str, Any] = field(default_factory=dict)
    purpose: str = ""


@dataclass
class StepObservation:
    step_id: int
    step_name: str
    tool: str
    status: str
    output: Any = None
    error: str | None = None


@dataclass
class CriticResult:
    passed: bool
    score: int
    notes: list[str] = field(default_factory=list)


@dataclass
class AgentState:
    goal: str
    symbol: str
    market_sentiment_score: float | None = None
    plan: list[PlanStep] = field(default_factory=list)
    observations: list[StepObservation] = field(default_factory=list)
    critic: CriticResult | None = None
    final_answer: str = ""
    meta: dict[str, Any] = field(default_factory=dict)
