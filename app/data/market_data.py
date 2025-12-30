import yfinance as yf

def get_stock_data(symbol: str, period="6mo"):
    """
    Fetches historical market data for a given stock ticker symbol.

    Args:
        ticker_symbol (str): The stock ticker symbol (e.g., 'AAPL' for Apple).
        period (str): The period over which to fetch data (default is '1mo').
       
    Returns:
        pandas.DataFrame: A DataFrame containing the historical market data.
    """

    ticker = yf.Ticker(symbol)
    hist = ticker.history(period=period)

    return {
        "price_data": hist,
        "info": ticker.info
    }


def get_fundamental_data(symbol: str) -> dict:
    ticker = yf.Ticker(symbol)
    info = ticker.info or {}

    fundamentals = {
        # Valuation
        "PE_Ratio": info.get("trailingPE"),
        "price_to_book": info.get("priceToBook"),
        "market_cap": info.get("marketCap"),

        # Profitability (convert to %)
        "return_on_equity": (
            info.get("returnOnEquity") * 100
            if info.get("returnOnEquity") is not None else None
        ),

        # Liquidity
        "Current_Ratio": info.get("currentRatio"),
        "Quick_Ratio": info.get("quickRatio"),

        # Debt
        "debt_to_equity": info.get("debtToEquity"),

        # Cash flow
        "cash_flow": info.get("operatingCashflow"),

        # Margins
        "net_profit_margin": (
            info.get("profitMargins") * 100
            if info.get("profitMargins") is not None else None
        ),

        # Income
        "earnings_per_share": info.get("trailingEps"),
        "dividend_yield": (
            info.get("dividendYield") * 100
            if info.get("dividendYield") is not None else None
        ),
    }

    # Remove None values to avoid downstream crashes
    fundamentals = {k: v for k, v in fundamentals.items() if v is not None}

    return {
        "fundamental_data": fundamentals,
        "raw_info": info
    }


