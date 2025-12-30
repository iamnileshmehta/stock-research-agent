from babel.numbers import format_currency

def format_currency_babel(number_string, currency_code='INR'):
    """Formats a number string using Babel for specific locales/currencies."""
    try:
        # Convert string to float
        number_float = float(number_string)

        # Format the number using Babel's robust formatting rules
        # 'INR' is the currency code, 'en_IN' is the locale
        formatted_number = format_currency(number_float, currency=currency_code, locale='en_IN')
        return formatted_number
    except ValueError:
        return "Invalid input"

# # Example Usage:
# long_number = "100000.50"
# # For Euros in Germany:
# print(format_currency_babel(long_number, currency_code='EUR'))
# # Output: €100,000.50

# # For British Pounds:
# print(format_currency_babel(long_number, currency_code='GBP'))
# # Output: £100,000.50
