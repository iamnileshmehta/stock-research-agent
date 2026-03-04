def _to_score(signal):
    if isinstance(signal, dict):
        if "score" in signal:
            return int(signal["score"])
        if "signal" in signal:
            return _to_score(signal["signal"])
        return 0

    if isinstance(signal, str):
        normalized = signal.strip().lower()
        if normalized in {"bullish", "oversold", "near_support", "accumulation"}:
            return +1
        if normalized in {"bearish", "overbought", "near_resistance", "distribution"}:
            return -1
        return 0

    if isinstance(signal, (int, float)):
        if signal > 0:
            return +1
        if signal < 0:
            return -1
    return 0


def trend_signal(price, sma_20, sma_50):
    """
    Trend logic:
    - Price > SMA20 and SMA50 → Bullish
    - Price < SMA50 → Bearish
    - Overlap / mixed → Neutral
    """
    if price > sma_20 and price > sma_50:
        return +1, "bullish"
    elif price < sma_50:
        return -1, "bearish"
    else:
        return 0, "neutral"
    

def momentum_signal(rsi):
    """
    RSI logic:
    - RSI > 70 → Overbought (Bearish)
    - RSI < 30 → Oversold (Bullish)
    - Else → Neutral
    """
    if rsi > 70:
        return -1, "overbought"
    elif rsi < 30:
        return +1, "oversold"
    else:
        return 0, "neutral"
    
def macd_signal(macd_value):
    """
    MACD logic:
    - MACD > 0 → Bullish
    - MACD < 0 → Bearish
    """
    if macd_value > 0:
        return +1, "bullish"
    elif macd_value < 0:
        return -1, "bearish"
    else:
        return 0, "neutral"
    
def bollinger_signal(price, bollinger_high):
    """
    Bollinger Bands logic:
    - Price > Upper Band → Overbought (Bearish)
    - Price < Upper Band → Neutral
    """
    if price > bollinger_high:
        return -1, "above"
    else:
        return 0, "below"
    

def final_signal(*signals):
    """
    Aggregate signals:
    - If 2 or more indicators are bullish → Overall Bullish
    - If 2 or more indicators are bearish → Overall Bearish
    - Else → Neutral
    """
    if len(signals) == 1 and isinstance(signals[0], (list, tuple)):
        signals = tuple(signals[0])

    scores = [_to_score(s) for s in signals]
    total_score = sum(scores)

    if total_score >= 2:
        return "bullish"
    elif total_score <= -2:
        return "bearish"
    else:
        return "neutral"
    
    
def generate_technical_signal(technical_data):
    """
    combine all indicator signals to verdict.
    """
    price = technical_data["trend"]["price"]
    sma_20 = technical_data["trend"]["SMA_20"]
    sma_50 = technical_data["trend"]["SMA_50"]
    rsi = technical_data["momentum"]["RSI"]
    macd = technical_data["macd"]["value"]
    bollinger_high = technical_data["bollinger"]["Bollinger_High"]

    trend_score, trend_label = trend_signal(price, sma_20, sma_50)
    rsi_score, rsi_label = momentum_signal(rsi)
    macd_score, macd_label = macd_signal(macd)
    bollinger_score, bollinger_label = bollinger_signal(price, bollinger_high)

    total_score = trend_score + rsi_score + macd_score + bollinger_score

    return {
        "score": total_score,
        "signal": final_signal(total_score),
        "components": {
            "trend": trend_label,
            "momentum": rsi_label,
            "macd": macd_label,
            "bollinger": bollinger_label
        }
    }
