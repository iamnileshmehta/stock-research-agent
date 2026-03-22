import json
from typing import Any

from app.llm.base import BaseLLM

from .models import AgentState, StepObservation
from .tools import ToolRegistry


class Executor:
    def __init__(self, registry: ToolRegistry, llm: BaseLLM) -> None:
        self.registry = registry
        self.llm = llm

    def execute_step(self, step_id: int, step_name: str, tool: str, args: dict[str, Any]) -> StepObservation:
        try:
            output = self.registry.execute(tool, **args)
            return StepObservation(
                step_id=step_id,
                step_name=step_name,
                tool=tool,
                status="success",
                output=output,
            )
        except Exception as exc:
            return StepObservation(
                step_id=step_id,
                step_name=step_name,
                tool=tool,
                status="failed",
                error=str(exc),
            )

    def compose_final_answer(self, state: AgentState) -> str:
        observation_payload = []
        for obs in state.observations:
            observation_payload.append(
                {
                    "step_id": obs.step_id,
                    "step_name": obs.step_name,
                    "tool": obs.tool,
                    "status": obs.status,
                    "output": obs.output,
                    "error": obs.error,
                }
            )

        critic_notes = state.critic.notes if state.critic else []
        critic_score = state.critic.score if state.critic else 0

        prompt = (
            "You are a senior stock research analyst. "
            "Using ONLY the tool outputs below, produce a final report in plain text with sections: "
            "Recommendation, Evidence, Risks, Time Horizon, Next Checks. "
            "If evidence is missing, say it clearly. Do not fabricate values.\n\n"
            f"Goal: {state.goal}\n"
            f"Symbol: {state.symbol}\n"
            f"Sentiment input: {state.market_sentiment_score}\n"
            f"Critic score: {critic_score}\n"
            f"Critic notes: {critic_notes}\n"
            f"Tool outputs: {json.dumps(observation_payload, default=str)}"
        )

        return self.llm.generate(prompt)
