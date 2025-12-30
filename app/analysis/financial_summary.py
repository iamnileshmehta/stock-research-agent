from app.utils.formatting import format_currency, format_percentage
from app.analysis.financial import compute_fundamental_indicators as f
from app.utils.currency import format_currency_babel



def generate_financial_summary(fundamentals: dict) -> str:
    # Function to generate a financial summary from given data
    market_cap = fundamentals["market_cap"]
    valuation = fundamentals["valuation"]
    profitability = fundamentals["profitability"]
    liquidity = fundamentals["liquidity"]
    debt_management = fundamentals["debt_management"]
    cash_flow = fundamentals["cash_flow"]
    net_profit_margin = fundamentals["net_profit_margin"]
    earnings_per_share = fundamentals.get("earnings_per_share", {})
    dividend_yield = fundamentals.get("dividend_yield", {})


    cash_flow_formatted = format_currency_babel(str(cash_flow['cash_flow']), currency_code='INR')
    debt_management_formatted = format_percentage(debt_management['Debt_to_Equity'])

    summary = []

    summary.append(f"Market Capitalization: {format_currency_babel(str(market_cap['market_cap']), currency_code='INR')}\n")
    summary.append(f"Valuation: The stock is considered {valuation['signal']['label']}\n")
    summary.append(f"Profitability: The return on equity (ROE) is {profitability['ROE']}%, indicating {profitability['signal']['label']} profitability.\n")
    summary.append(f"Liquidity: The current ratio is {liquidity['Current_Ratio']}, which is {liquidity['signal']['label']} for meeting short-term obligations.\n")
    summary.append(f"Debt Management: The debt to equity ratio is {debt_management_formatted}, indicating {debt_management['signal']['label']} debt levels.\n")
    summary.append(f"Cash Flow: The cash flow is {cash_flow_formatted}, which is {cash_flow['signal']['label']}.\n")
    summary.append(f"Net Profit Margin: The net profit margin is {net_profit_margin['net_profit_margin']}%, indicating {net_profit_margin['signal']['label']}.\n")
    summary.append(f"Earnings Per Share (EPS): The EPS is {earnings_per_share.get('earnings_per_share', 'N/A')}.\n")
    summary.append(f"Dividend Yield: The dividend yield is {dividend_yield.get('dividend_yield', 'N/A')}%.\n")


    return "\n".join(summary)