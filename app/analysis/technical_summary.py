from app.analysis.technical import calculate_confidence

def generate_technical_summary(tech):
    trend = tech["trend"]
    momentum = tech["momentum"]
    macd = tech["macd"]
    bollinger = tech["bollinger"]

    summary = []

    summary.append(
        f"The stock is trading at {trend['price']} compared to its "
        f"20-day SMA ({trend['SMA_20']}) and 50-day SMA ({trend['SMA_50']}), "
        f"indicating a {trend['trend_signal']} trend."
    )

    summary.append(
        f"RSI is at {momentum['RSI']}, suggesting {momentum['rsi_signal']} momentum."
    )

    summary.append(
        f"MACD is {macd['value']}, indicating a {macd['signal']} bias."
    )

    summary.append(
        f"The current price is {bollinger['signal']} the upper Bollinger Band ({bollinger['Bollinger_High']})."
    )

    confidence = calculate_confidence([
    trend,
    momentum,
    macd,
    bollinger
])

    return "\n".join(summary)





