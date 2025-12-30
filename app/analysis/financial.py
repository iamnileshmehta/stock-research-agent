import app.analysis.financial as af
from app.utils.formatting import format_currency, format_percentage



def compute_fundamental_indicators(f: dict) -> dict:
    return {
        "market_cap": {
            "market_cap": round(f["market_cap"], 2),
            "signal": {
                "label": "large" if f["market_cap"] > 1000000000 else "small",
                "score": +1 if f["market_cap"] > 1000000000 else 0
            }
        },

        "valuation": {
            "PE_Ratio": round(f["PE_Ratio"], 2),
            "signal": {
                "label": "undervalued" if f["PE_Ratio"] < 15 else
                         "overvalued" if f["PE_Ratio"] > 25 else
                         "fairly_valued",
                "score": +1 if f["PE_Ratio"] < 15 else
                         -1 if f["PE_Ratio"] > 25 else 0
            }
        },

        "profitability": {
            "ROE": round(f["return_on_equity"], 2),
            "signal": {
                "label": "strong" if f["return_on_equity"] > 15 else "weak",
                "score": +1 if f["return_on_equity"] > 15 else 0
            }
        },

        "liquidity": {
            "Current_Ratio": round(f["Current_Ratio"], 2),
            "signal": {
                "label": "healthy" if f["Current_Ratio"] > 1.5 else "unhealthy",
                "score": +1 if f["Current_Ratio"] > 1.5 else 0
            }
        },

        "debt_management": {
            "Debt_to_Equity": round(f["debt_to_equity"], 2),
            "signal": {
                "label": "low_debt" if f["debt_to_equity"] < 1 else "high_debt",
                "score": +1 if f["debt_to_equity"] < 1 else 0
            }
        },

        "cash_flow": {
            "cash_flow": f["cash_flow"],
            "signal": {
                "label": "positive" if f["cash_flow"] > 0 else "negative",
                "score": +1 if f["cash_flow"] > 0 else -1
            }
        },

        "net_profit_margin": {
            "net_profit_margin": round(f["net_profit_margin"], 2),
            "signal": {
                "label": "high_margin" if f["net_profit_margin"] > 20 else "low_margin",
                "score": +1 if f["net_profit_margin"] > 20 else 0
            }
        },

        "earnings_per_share": {
            "earnings_per_share": round(f["earnings_per_share"], 2),
            "signal": {
                "label": "positive" if f["earnings_per_share"] > 0 else "negative",
                "score": +1 if f["earnings_per_share"] > 0 else -1
            }
        },

        "dividend_yield": {
            "dividend_yield": round(f["dividend_yield"], 2),
            "signal": {
                "label": "attractive" if f["dividend_yield"] > 3 else "unattractive",
                "score": +1 if f["dividend_yield"] > 3 else 0
            }
        }

    }

def generate_financial_report(fundamentals: dict) -> dict:
    scores = {
        k: v["signal"]["score"]
        for k, v in fundamentals.items()
    }
    

    total_score = sum(scores.values())

    if total_score >= 2:
        signal = "Strong Bullish"
    elif total_score == 1:
        signal = "Bullish"
    elif total_score == 0:
        signal = "Neutral"
    elif total_score == -1:
        signal = "Bearish"
    else:
        signal = "Strong Bearish"

    return {
        "score": total_score,
        "signal": signal,
        "components": scores
    }

