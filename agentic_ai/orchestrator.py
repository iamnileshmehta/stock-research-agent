from datetime import datetime, timezone

from dotenv import load_dotenv
from app.llm.base import BaseLLM
from app.llm.factory import get_llm

from .critic import Critic
from .executor import Executor
from .memory import JsonMemoryStore
from .models import AgentState
from .planner import Planner
from .tools import build_default_registry

load_dotenv()


class AgentOrchestrator:
    def __init__(
        self,
        llm: BaseLLM | None = None,
        memory_path: str = ".agentic_memory/memory.json",
    ) -> None:
        self.llm = llm or get_llm()
        self.registry = build_default_registry()
        self.memory = JsonMemoryStore(memory_path)
        self.planner = Planner(self.llm)
        self.executor = Executor(self.registry, self.llm)
        self.critic = Critic()

    def run(
        self,
        goal: str,
        symbol: str,
        market_sentiment_score: float | None = None,
        max_steps: int = 6,
    ) -> dict:
        state = AgentState(
            goal=goal.strip(),
            symbol=symbol.strip().upper(),
            market_sentiment_score=market_sentiment_score,
        )

        memory_context = self.memory.recent_for_symbol(state.symbol, limit=3)
        tools = self.registry.list_descriptions()
        state.plan = self.planner.create_plan(
            goal=state.goal,
            symbol=state.symbol,
            tools=tools,
            memory_context=memory_context,
        )[:max_steps]

        for step in state.plan:
            args = dict(step.args)
            if step.tool == "run_technical_analysis" and "market_sentiment_score" not in args:
                args["market_sentiment_score"] = state.market_sentiment_score
            observation = self.executor.execute_step(
                step_id=step.id,
                step_name=step.name,
                tool=step.tool,
                args=args,
            )
            state.observations.append(observation)

        state.critic = self.critic.review(state)
        state.final_answer = self.executor.compose_final_answer(state)

        run_record = {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "symbol": state.symbol,
            "goal": state.goal,
            "market_sentiment_score": state.market_sentiment_score,
            "plan": [
                {
                    "id": s.id,
                    "name": s.name,
                    "tool": s.tool,
                    "args": s.args,
                    "purpose": s.purpose,
                }
                for s in state.plan
            ],
            "critic": {
                "passed": state.critic.passed,
                "score": state.critic.score,
                "notes": state.critic.notes,
            },
            "final_answer": state.final_answer,
        }
        self.memory.append_run(run_record)

        return {
            "symbol": state.symbol,
            "goal": state.goal,
            "plan": run_record["plan"],
            "observations": [
                {
                    "step_id": o.step_id,
                    "step_name": o.step_name,
                    "tool": o.tool,
                    "status": o.status,
                    "output": o.output,
                    "error": o.error,
                }
                for o in state.observations
            ],
            "critic": run_record["critic"],
            "final_answer": state.final_answer,
        }
