# Agentic AI Architecture for Stock Research

## Objective
Build a truly agentic stock research workflow without modifying the existing application flow.

## Design Principles
- Keep deterministic finance logic in tools.
- Let the LLM plan, adapt, and synthesize.
- Add explicit state, memory, and critique stages.
- Keep execution auditable via step traces.

## Component Map
1. UI/Entrypoint
- `agentic_app.py`: Streamlit UI for goal-driven analysis.

2. Orchestration Layer
- `agentic_ai/orchestrator.py`: Main run loop.
- `agentic_ai/planner.py`: Generates plan from goal.
- `agentic_ai/executor.py`: Runs plan steps via tools.
- `agentic_ai/critic.py`: Validates result completeness and risks.

3. Tooling Layer
- `agentic_ai/tools.py`: Tool registry + tool implementations.
- Uses existing deterministic modules:
  - `app/data/market_data.py`
  - `app/analysis/technical.py`
  - `app/analysis/signal_engine.py`
  - `app/analysis/technical_summary.py`
  - `app/analysis/financial.py`
  - `app/analysis/financial_summary.py`

4. State + Memory
- `agentic_ai/models.py`: Dataclasses for plan and state.
- `agentic_ai/memory.py`: JSON memory store for prior runs.

5. Utilities
- `agentic_ai/json_utils.py`: Robust JSON extraction/parsing for LLM outputs.

## Runtime Flow
1. User gives goal + symbol + sentiment.
2. Orchestrator loads memory context.
3. Planner creates a structured step plan.
4. Executor runs each selected tool.
5. Critic reviews coverage/quality.
6. LLM produces final recommendation using tool outputs + critic notes.
7. Run is persisted to memory for future context.

## Why This Is Agentic
- Dynamic plan generation based on user goal.
- Tool selection through plan steps.
- Multi-step execution and reflection.
- Persistent memory reuse.
- Explicit critique before final answer.
