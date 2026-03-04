import streamlit as st

from app.main import run_analysis
from app.llm.factory import get_llm

st.set_page_config(
    page_title="Stock Research Agent",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.title("Stock Research Agent")
st.caption("Rule-based Technical & Fundamental Analysis with Chat")

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "analysis_symbol" not in st.session_state:
    st.session_state.analysis_symbol = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "llm" not in st.session_state:
    st.session_state.llm = None
if "market_sentiment_score" not in st.session_state:
    st.session_state.market_sentiment_score = 0.0


def ensure_llm():
    if st.session_state.llm is None:
        st.session_state.llm = get_llm()
    return st.session_state.llm


def build_chat_prompt(user_message: str) -> str:
    result = st.session_state.analysis_result
    symbol = st.session_state.analysis_symbol

    history = st.session_state.chat_history[-6:]
    history_text = "\n".join(
        f"{entry['role'].title()}: {entry['content']}" for entry in history
    )

    return (
        "You are a stock research assistant. Answer clearly and concisely.\n"
        f"Use the analysis below for {symbol} as your primary context.\n\n"
        f"Technical Summary:\n{result['technical_summary']}\n\n"
        f"Fundamental Summary:\n{result['financial_summary']}\n\n"
        f"AI Summary:\n{result['response']}\n\n"
        f"Conversation so far:\n{history_text}\n\n"
        f"User question: {user_message}\n\n"
        "If the question cannot be answered from the provided analysis, say so and suggest what data is missing."
    )


symbol = st.text_input("Enter stock symbol", value=st.session_state.analysis_symbol)
market_sentiment_score = st.slider(
    "Market sentiment score (-1 bearish, +1 bullish)",
    min_value=-1.0,
    max_value=1.0,
    value=float(st.session_state.market_sentiment_score),
    step=0.1,
)

col1, col2 = st.columns([1, 1])

with col1:
    analyze_clicked = st.button("Analyze", type="primary")
with col2:
    clear_clicked = st.button("Clear")

if clear_clicked:
    st.session_state.analysis_result = None
    st.session_state.analysis_symbol = ""
    st.session_state.chat_history = []
    st.session_state.market_sentiment_score = 0.0
    st.rerun()

if analyze_clicked:
    if not symbol.strip():
        st.warning("Please enter a valid stock symbol.")
    else:
        with st.spinner("Analyzing stock..."):
            result = run_analysis(
                symbol.strip().upper(), market_sentiment_score=market_sentiment_score
            )

        st.session_state.analysis_result = result
        st.session_state.analysis_symbol = symbol.strip().upper()
        st.session_state.chat_history = []
        st.session_state.market_sentiment_score = market_sentiment_score


if st.session_state.analysis_result:
    result = st.session_state.analysis_result
    current_symbol = st.session_state.analysis_symbol

    st.subheader(f"Results for {current_symbol}")

    st.markdown("### Technical Analysis")
    st.write(result["technical_summary"])
    st.caption(f"Input sentiment score used: {st.session_state.market_sentiment_score:.1f}")

    st.markdown("### Fundamental Analysis")
    st.write(result["financial_summary"])

    st.markdown("### AI Financial Summary")
    st.write(result["response"])

    st.markdown("---")
    st.markdown("### Chat about this analysis")

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_message = st.chat_input("Ask follow-up questions about this stock analysis...")

    if user_message:
        st.session_state.chat_history.append({"role": "user", "content": user_message})

        with st.chat_message("user"):
            st.write(user_message)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    llm = ensure_llm()
                    prompt = build_chat_prompt(user_message)
                    assistant_reply = llm.generate(prompt)
                except Exception as exc:
                    assistant_reply = f"Failed to generate chat response: {exc}"

            st.write(assistant_reply)

        st.session_state.chat_history.append(
            {"role": "assistant", "content": assistant_reply}
        )
