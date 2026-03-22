from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from app.analysis.financial import compute_fundamental_indicators, generate_financial_report
from app.analysis.signal_engine import final_signal
from app.analysis.technical import compute_technical_indicators
from app.analysis.technical_summary import generate_technical_summary
from app.data.market_data import get_fundamental_data, get_stock_data
from app.utils.formatting import clean_numbers


@dataclass
class ToolSpec:
    name: str
    description: str
    fn: Callable[..., Any]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolSpec] = {}

    def register(self, spec: ToolSpec) -> None:
        self._tools[spec.name] = spec

    def list_descriptions(self) -> list[dict[str, str]]:
        return [
            {
                "name": spec.name,
                "description": spec.description,
            }
            for spec in self._tools.values()
        ]

    def execute(self, tool_name: str, **kwargs: Any) -> Any:
        if tool_name not in self._tools:
            raise ValueError(f"Unknown tool: {tool_name}")
        return self._tools[tool_name].fn(**kwargs)


def tool_fetch_market_context(symbol: str, period: str = "6mo") -> dict[str, Any]:
    data = get_stock_data(symbol, period=period)
    price_df = data["price_data"]
    if price_df.empty:
        raise ValueError(f"No market data returned for symbol {symbol}")

    close_col = "Close" if "Close" in price_df.columns else "close"
    latest_close = float(price_df[close_col].iloc[-1])
    prev_close = float(price_df[close_col].iloc[-2]) if len(price_df) > 1 else latest_close
    pct_change = ((latest_close - prev_close) / prev_close * 100) if prev_close else 0.0

    return {
        "symbol": symbol.upper(),
        "period": period,
        "rows": int(len(price_df)),
        "latest_close": round(latest_close, 2),
        "one_day_change_pct": round(pct_change, 2),
    }


def tool_run_technical_analysis(symbol: str, market_sentiment_score: float | None = None) -> dict[str, Any]:
    data = get_stock_data(symbol)
    technical = compute_technical_indicators(
        data["price_data"],
        market_sentiment_score=market_sentiment_score,
    )
    technical = clean_numbers(technical)

    signal = final_signal(
        technical["trend"],
        technical["momentum"],
        technical["macd"],
        technical["bollinger"],
        technical["support_resistance"],
        technical["volume"],
        technical["sentiment"],
    )

    summary = generate_technical_summary(technical)

    return {
        "symbol": symbol.upper(),
        "signal": signal,
        "technical": technical,
        "summary": summary,
    }


def tool_run_fundamental_analysis(symbol: str) -> dict[str, Any]:
    fundamental_raw = get_fundamental_data(symbol)
    fundamentals = fundamental_raw.get("fundamental_data", {})

    if not fundamentals:
        return {
            "symbol": symbol.upper(),
            "status": "limited_data",
            "message": "No fundamental metrics available from data provider.",
        }

    indicators = compute_fundamental_indicators(fundamentals)
    report = generate_financial_report(indicators)
    valuation = indicators.get("valuation", {}).get("signal", {}).get("label", "unknown")
    profitability = indicators.get("profitability", {}).get("signal", {}).get("label", "unknown")
    liquidity = indicators.get("liquidity", {}).get("signal", {}).get("label", "unknown")
    debt = indicators.get("debt_management", {}).get("signal", {}).get("label", "unknown")

    summary = (
        f"Fundamental signal: {report['signal']} (score: {report['score']}). "
        f"Valuation is {valuation}; profitability is {profitability}; "
        f"liquidity is {liquidity}; debt profile is {debt}."
    )

    return {
        "symbol": symbol.upper(),
        "status": "ok",
        "report": report,
        "summary": summary,
        "indicators": clean_numbers(indicators),
    }


def build_default_registry() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(
        ToolSpec(
            name="fetch_market_context",
            description="Fetch latest market context (latest close, short-term change, row count).",
            fn=tool_fetch_market_context,
        )
    )
    registry.register(
        ToolSpec(
            name="run_technical_analysis",
            description="Run deterministic technical analysis and return scored signal + summary.",
            fn=tool_run_technical_analysis,
        )
    )
    registry.register(
        ToolSpec(
            name="run_fundamental_analysis",
            description="Run deterministic fundamental analysis and return report + summary.",
            fn=tool_run_fundamental_analysis,
        )
    )
    return registry
