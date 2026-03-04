import pandas as pd
import ta


def _find_column(df: pd.DataFrame, options: list[str]) -> str:
    for col in options:
        if col in df.columns:
            return col
    raise KeyError(f"None of these columns were found: {options}")


def _sentiment_label(score: int) -> str:
    if score > 0:
        return "bullish"
    if score < 0:
        return "bearish"
    return "neutral"


def compute_technical_indicators(
    price_df: pd.DataFrame, market_sentiment_score: float | None = None
) -> dict:
    """
    Compute a set of technical indicators for the given price DataFrame.

    Parameters:
    price_df (pd.DataFrame): DataFrame containing OHLCV data.
    market_sentiment_score (float | None): Optional external sentiment value in
    the range [-1, 1]. If not provided, sentiment is inferred from technicals.

    Returns:
    dict: A dictionary containing computed technical indicators.
    """
    df = price_df.copy()
    close_col = _find_column(df, ["Close", "close"])
    high_col = _find_column(df, ["High", "high"])
    low_col = _find_column(df, ["Low", "low"])
    volume_col = _find_column(df, ["Volume", "volume"])

    # Moving averages
    df["SMA_20"] = ta.trend.sma_indicator(df[close_col], window=20)
    df["SMA_50"] = ta.trend.sma_indicator(df[close_col], window=50)

    # RSI
    df["RSI"] = ta.momentum.rsi(df[close_col], window=14)

    # MACD
    macd_series = ta.trend.macd_diff(df[close_col])
    df["MACD"] = macd_series.astype(float)

    # Bollinger bands
    bollinger = ta.volatility.BollingerBands(df[close_col], window=20, window_dev=2)
    df["Bollinger_High"] = bollinger.bollinger_hband()
    df["Bollinger_Low"] = bollinger.bollinger_lband()

    # Volume trend
    df["Volume_SMA_20"] = ta.trend.sma_indicator(df[volume_col], window=20)

    latest = df.iloc[-1]
    prev_close = df[close_col].iloc[-2] if len(df) > 1 else latest[close_col]

    close = float(latest[close_col])
    sma_20 = float(latest["SMA_20"])
    sma_50 = float(latest["SMA_50"])
    rsi = float(latest["RSI"])
    macd = float(latest["MACD"])
    boll_high = float(latest["Bollinger_High"])
    boll_low = float(latest["Bollinger_Low"])
    volume = float(latest[volume_col])
    volume_sma = float(latest["Volume_SMA_20"])
    price_change = close - float(prev_close)

    if close > sma_20 and close > sma_50:
        trend_score, trend_signal = +1, "bullish"
    elif close < sma_50:
        trend_score, trend_signal = -1, "bearish"
    else:
        trend_score, trend_signal = 0, "neutral"

    if rsi > 70:
        momentum_score, rsi_signal = -1, "overbought"
    elif rsi < 30:
        momentum_score, rsi_signal = +1, "oversold"
    else:
        momentum_score, rsi_signal = 0, "neutral"

    if macd > 0:
        macd_score, macd_signal = +1, "bullish"
    elif macd < 0:
        macd_score, macd_signal = -1, "bearish"
    else:
        macd_score, macd_signal = 0, "neutral"

    if close > boll_high:
        bollinger_score, bollinger_signal = -1, "above_upper_band"
    elif close < boll_low:
        bollinger_score, bollinger_signal = +1, "below_lower_band"
    else:
        bollinger_score, bollinger_signal = 0, "within_bands"

    lookback = min(20, len(df))
    support = float(df[low_col].tail(lookback).min())
    resistance = float(df[high_col].tail(lookback).max())
    support_gap_pct = ((close - support) / support * 100) if support else 0.0
    resistance_gap_pct = ((resistance - close) / close * 100) if close else 0.0
    sr_score = +1 if support_gap_pct <= 2 else -1 if resistance_gap_pct <= 2 else 0
    sr_signal = (
        "near_support" if sr_score == +1 else "near_resistance" if sr_score == -1 else "mid_range"
    )

    volume_ratio = (volume / volume_sma) if volume_sma else 1.0
    if volume_ratio >= 1.2 and price_change > 0:
        volume_score, volume_signal = +1, "accumulation"
    elif volume_ratio >= 1.2 and price_change < 0:
        volume_score, volume_signal = -1, "distribution"
    else:
        volume_score, volume_signal = 0, "normal"

    if market_sentiment_score is None:
        inferred = (trend_score + momentum_score + macd_score + volume_score) / 4
        sentiment_score = +1 if inferred > 0.25 else -1 if inferred < -0.25 else 0
        sentiment_value = round(inferred, 2)
        sentiment_source = "technical_inference"
    else:
        provided = max(min(float(market_sentiment_score), 1.0), -1.0)
        sentiment_score = +1 if provided > 0.2 else -1 if provided < -0.2 else 0
        sentiment_value = round(provided, 2)
        sentiment_source = "external_input"

    return {
        "trend": {
            "price": round(close, 2),
            "SMA_20": round(sma_20, 2),
            "SMA_50": round(sma_50, 2),
            "trend_signal": trend_signal,
            "score": trend_score,
        },
        "momentum": {
            "RSI": round(rsi, 2),
            "rsi_signal": rsi_signal,
            "score": momentum_score,
        },
        "macd": {
            "value": round(macd, 2),
            "signal": macd_signal,
            "score": macd_score,
        },
        "bollinger": {
            "Bollinger_High": round(boll_high, 2),
            "Bollinger_Low": round(boll_low, 2),
            "signal": bollinger_signal,
            "score": bollinger_score,
        },
        "support_resistance": {
            "support": round(support, 2),
            "resistance": round(resistance, 2),
            "support_gap_pct": round(support_gap_pct, 2),
            "resistance_gap_pct": round(resistance_gap_pct, 2),
            "signal": sr_signal,
            "score": sr_score,
        },
        "volume": {
            "volume": int(volume),
            "volume_sma_20": int(volume_sma) if volume_sma == volume_sma else 0,
            "volume_ratio": round(volume_ratio, 2),
            "price_change_1d": round(price_change, 2),
            "signal": volume_signal,
            "score": volume_score,
        },
        "sentiment": {
            "value": sentiment_value,
            "source": sentiment_source,
            "signal": _sentiment_label(sentiment_score),
            "score": sentiment_score,
        },
    }

def calculate_confidence(scores: list[int]) -> int:
    agreement = sum(1 for s in scores if s != 0)
    total = len(scores)
    return int((agreement / total) * 100)




