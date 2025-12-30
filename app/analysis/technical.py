import pandas as pd
import ta
from app.utils.formatting import format_currency, format_percentage


def compute_technical_indicators(price_df: pd.DataFrame) -> dict:
    """
    Compute a set of technical indicators for the given price DataFrame.

    Parameters:
    price_df (pd.DataFrame): DataFrame containing 'open', 'high', 'low', 'Close', and 'volume' columns.

    Returns:
    dict: A dictionary containing computed technical indicators.
    """
    
    df = price_df.copy()

    #Moving Averages
    df['SMA_20'] = ta.trend.sma_indicator(df['Close'], window=20)
    df['SMA_50'] = ta.trend.sma_indicator(df['Close'], window=50)

    #RSI
    df['RSI'] = ta.momentum.rsi(df['Close'], window=14)

    #MACD
    macd_series = ta.trend.macd_diff(df["Close"])
    df["MACD"] = macd_series.astype(float)

    bollinger = ta.volatility.BollingerBands(df['Close'], window=20, window_dev=2)
    df['Bollinger_High'] = bollinger.bollinger_hband()

    latest = df.iloc[-1]

    return{
        "trend": {
            "price": round(latest['Close'], 2),
            "SMA_20": round(latest['SMA_20'], 2),
            "SMA_50": round(latest['SMA_50'], 2),
            "trend_signal": ("bullish" if latest['SMA_20'] > latest['SMA_50'] else "bearish"),
            
        },
        "momentum": {
            "RSI": round(latest['RSI'], 2),
            "rsi_signal": ("overbought" if latest['RSI'] > 70 else "oversold" if latest['RSI'] < 30 else "neutral"),

        },
        "macd": {
            "value": round(float(latest['MACD']), 2),
            "signal": ("bullish" if latest['MACD'] > 0 else "bearish"),
        },
        "bollinger": {
            "Bollinger_High": round(latest['Bollinger_High'], 2),
            "signal": ("above" if latest['Close'] > latest['Bollinger_High'] else "below"),
        }
        
    }

def calculate_confidence(scores: list[int]) -> int:
    agreement = sum(1 for s in scores if s != 0)
    total = len(scores)
    return int((agreement / total) * 100)




