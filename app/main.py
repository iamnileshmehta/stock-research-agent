from app.llm.factory import get_llm
from dotenv import load_dotenv

from app.data.market_data import get_stock_data, get_fundamental_data
from app.analysis.technical import compute_technical_indicators
from app.analysis.technical_summary import generate_technical_summary
from app.analysis.financial_summary import generate_financial_summary

from app.utils.formatting import clean_numbers

from app.analysis.signal_engine import final_signal

from app.analysis.financial import compute_fundamental_indicators, generate_financial_report

from app.utils.formatting import format_currency, format_percentage

from app.utils.currency import format_currency_babel

load_dotenv()

def run_analysis(symbol: str):

    # Load LLM
    llm = get_llm()

    # Fetch market data
    data = get_stock_data(symbol)

    # Fetch fundamental data
    fundamental_data = get_fundamental_data(symbol)

    
    # Compute fundamental indicators
    fundamental = compute_fundamental_indicators(fundamental_data["fundamental_data"])
    fundamental = clean_numbers(fundamental)

    # Compute technical indicators
    technical = compute_technical_indicators(data["price_data"])
    technical = clean_numbers(technical)

    # Generate financial report
    report = generate_financial_report(fundamental)

    # Generate technical signal
    signal = final_signal(technical["trend"], technical["momentum"], technical["macd"], technical["bollinger"])
    print("Overall Technical Signal:", signal)


    #Time Horizon
    time_horizon = {
    "technical": "Short-term (1–4 weeks)",
    "fundamental": "Long-term (6–24 months)",
    "combined": "Medium-term (1–6 months)"
}
    report["time_horizon"] = time_horizon


    # Generate technical summary
    technical_summary = generate_technical_summary(technical)
    # Generate financial summary
    financial_summary = generate_financial_summary(fundamental)

    # ask LLM for actionable insights
    prompt = (
        "Based on the following fundamental and technical analysis summary, provide actionable stock trading insights:\n\n"
        f"{financial_summary, technical_summary}\n\n"
        "Please provide concise and clear recommendations."
    )  

    response = llm.generate(prompt)

    return {
        "technical_summary": technical_summary,
        "financial_summary": financial_summary,
        "signal": signal,
        "report": report,
        "response": response
    }


if __name__ == "__main__":
    run_analysis()


