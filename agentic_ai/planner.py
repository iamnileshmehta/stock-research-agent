from typing import Any

from app.llm.base import BaseLLM

from .json_utils import safe_json_loads
from .models import PlanStep


class Planner:
    def __init__(self, llm: BaseLLM) -> None:
        self.llm = llm

    def create_plan(
        self,
        goal: str,
        symbol: str,
        tools: list[dict[str, str]],
        memory_context: list[dict[str, Any]] | None = None,
    ) -> list[PlanStep]:
        memory_context = memory_context or []
        allowed_tool_names = {t["name"] for t in tools}

        prompt = (
            "You are a planning agent for stock research. "
            "Return ONLY valid JSON with this schema: "
            "{\"steps\": [{\"name\": str, \"tool\": str, \"args\": object, \"purpose\": str}]}. "
            "Use only the provided tools. Keep between 2 and 5 steps.\n\n"
            f"Goal: {goal}\n"
            f"Symbol: {symbol}\n"
            f"Available tools: {tools}\n"
            f"Recent memory context: {memory_context}\n"
            "Important: include symbol in tool args when needed."
        )

        fallback = {
            "steps": [
                {
                    "name": "Get current market context",
                    "tool": "fetch_market_context",
                    "args": {"symbol": symbol, "period": "6mo"},
                    "purpose": "Understand latest price context.",
                },
                {
                    "name": "Run technical analysis",
                    "tool": "run_technical_analysis",
                    "args": {"symbol": symbol},
                    "purpose": "Generate deterministic technical signal.",
                },
                {
                    "name": "Run fundamental analysis",
                    "tool": "run_fundamental_analysis",
                    "args": {"symbol": symbol},
                    "purpose": "Assess company fundamentals.",
                },
            ]
        }

        raw = self.llm.generate(prompt)
        parsed = safe_json_loads(raw, fallback)
        steps = parsed.get("steps", []) if isinstance(parsed, dict) else fallback["steps"]

        validated: list[PlanStep] = []
        for idx, step in enumerate(steps, start=1):
            if not isinstance(step, dict):
                continue
            tool = str(step.get("tool", "")).strip()
            if tool not in allowed_tool_names:
                continue
            args = step.get("args", {})
            if not isinstance(args, dict):
                args = {}
            args.setdefault("symbol", symbol)
            validated.append(
                PlanStep(
                    id=idx,
                    name=str(step.get("name", f"Step {idx}")),
                    tool=tool,
                    args=args,
                    purpose=str(step.get("purpose", "")),
                )
            )

        return validated if validated else [
            PlanStep(id=1, name=s["name"], tool=s["tool"], args=s["args"], purpose=s["purpose"])
            for s in fallback["steps"]
        ]
