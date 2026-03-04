from app.analysis.technical import calculate_confidence

def generate_technical_summary(tech):
    trend = tech["trend"]
    momentum = tech["momentum"]
    macd = tech["macd"]
    bollinger = tech["bollinger"]
    support_resistance = tech["support_resistance"]
    volume = tech["volume"]
    sentiment = tech["sentiment"]

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
        f"Bollinger Bands show price is {bollinger['signal']} "
        f"(upper: {bollinger['Bollinger_High']}, lower: {bollinger['Bollinger_Low']})."
    )

    summary.append(
        f"Support is near {support_resistance['support']} and resistance near {support_resistance['resistance']} "
        f"(signal: {support_resistance['signal']})."
    )

    summary.append(
        f"Volume is {volume['volume_ratio']}x its 20-day average with a "
        f"{volume['price_change_1d']} one-day price move, suggesting {volume['signal']}."
    )

    summary.append(
        f"Market sentiment ({sentiment['source']}) is {sentiment['signal']} "
        f"with score {sentiment['value']}."
    )

    confidence = calculate_confidence([
        trend["score"],
        momentum["score"],
        macd["score"],
        bollinger["score"],
        support_resistance["score"],
        volume["score"],
        sentiment["score"],
    ])

    summary.append(f"Technical confidence: {confidence}%")
    return "\n".join(summary)





