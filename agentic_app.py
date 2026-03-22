import json

import streamlit as st

from agentic_ai.orchestrator import AgentOrchestrator


st.set_page_config(
    page_title="Agentic Stock Research",
    layout="wide",
)

st.title("Agentic Stock Research")
st.caption("Goal-driven, tool-using multi-step stock analysis agent")

if "agent_output" not in st.session_state:
    st.session_state.agent_output = None

if "agent" not in st.session_state:
    st.session_state.agent = AgentOrchestrator()


col1, col2 = st.columns([1, 2])

with col1:
    symbol = st.text_input("Stock symbol", value="AAPL")
    sentiment = st.slider(
        "Market sentiment (-1 to +1)",
        min_value=-1.0,
        max_value=1.0,
        value=0.0,
        step=0.1,
    )

with col2:
    goal = st.text_area(
        "Research goal",
        value="Evaluate whether this stock is suitable for a medium-term swing position.",
        height=100,
    )

run_clicked = st.button("Run Agent", type="primary")

if run_clicked:
    if not symbol.strip() or not goal.strip():
        st.warning("Please provide both symbol and goal.")
    else:
        with st.spinner("Running agent plan..."):
            st.session_state.agent_output = st.session_state.agent.run(
                goal=goal,
                symbol=symbol,
                market_sentiment_score=sentiment,
            )


if st.session_state.agent_output:
    out = st.session_state.agent_output

    st.subheader(f"Final Report: {out['symbol']}")
    st.write(out["final_answer"])

    st.markdown("### Critic")
    st.write(f"Score: {out['critic']['score']} / 100")
    if out["critic"]["notes"]:
        for note in out["critic"]["notes"]:
            st.write(f"- {note}")

    st.markdown("### Plan")
    for step in out["plan"]:
        st.write(f"{step['id']}. {step['name']} (`{step['tool']}`)")

    st.markdown("### Execution Trace")
    for obs in out["observations"]:
        with st.expander(f"Step {obs['step_id']}: {obs['step_name']} [{obs['status']}]"):
            if obs["error"]:
                st.error(obs["error"])
            else:
                st.code(json.dumps(obs["output"], indent=2, default=str), language="json")
