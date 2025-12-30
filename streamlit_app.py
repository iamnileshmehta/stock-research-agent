

import streamlit as st
from app.analysis import technical_summary, financial_summary
from app.main import run_analysis
import sys
import os

st.set_page_config(
    page_title="Stock Research Agent",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.title("📊 Stock Research Agent")
st.caption("Rule-based Technical & Fundamental Analysis")

symbol = st.text_input("Enter stock symbol")

if st.button("Analyze"):
    with st.spinner("Analyzing stock..."):
        result = run_analysis(symbol)

    st.subheader(f"📌 Results for {symbol}")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📈 Technical Analysis")
        st.write(result["technical_summary"])

    with col2:
        st.markdown("### 💰 Fundamental Analysis")
        st.write(result["financial_summary"])

    st.markdown("### 🧠 AI Financial Summary")
    st.write(result["response"])
    
