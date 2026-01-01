# 📊 Stock Research Agent (AI-Assisted Stock Analysis)

An end-to-end rule-based stock research system that combines technical analysis, fundamental analysis, and LLM-generated insights to produce actionable stock market reports.

This project is designed with clean architecture, modular design, and explainable logic, focusing on engineering discipline rather than black-box AI.

🚀 Features

Market Data Collection
- Fetches real-time and historical stock data using Yahoo Finance (yfinance)
- Retrieves both price data and fundamental metrics

Technical Analysis (Rule-Based)
- Indicators used:
- Simple Moving Average (SMA 20, SMA 50)
- Relative Strength Index (RSI)
- MACD

Clear rule-based signals:
- Bullish / Bearish / Neutral
  
Fundamental Analysis (Rule-Based)
- Valuation metrics: PE Ratio, Price to Book
- Profitability: ROE, Net Profit Margin
- Liquidity: Current Ratio, Quick Ratio
- Debt Management: Debt to Equity
- Cash Flow & Dividend metrics

AI-Generated Insights (LLM)
- Uses Gemini (free tier) as the LLM
- LLM does not perform analysis

LLM only:
- Interprets already-computed indicators
- Generates human-readable summaries
- Produces actionable insights

⚠️ Analysis logic is fully deterministic and explainable.
AI is used only for narration, not decision-making.

🖥️ Streamlit Dashboard
The Streamlit UI provides:
- Stock symbol input
- Technical signal overview
- Fundamental summary
- AI-generated analyst view
- Clean, readable output for retail investors
- Design Philosophy
- Explainability over hype
- Rules before AI
- Separation of concerns
- Production-ready structure
- Agentic architecture without overengineering

This project intentionally avoids:
- Blind ML predictions
- Overfitting
- Uninterpretable outputs

👨‍💻 Author

Nilesh Mehta

AI-ML Engineer
