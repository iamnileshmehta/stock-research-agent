def clean_numbers(obj):
    if isinstance(obj, dict):
        return {k: clean_numbers(v) for k, v in obj.items()}
    
    elif isinstance(obj, list):
        return [clean_numbers(v) for v in obj]
    
    elif hasattr(obj, "item"):
        return obj.item()
    
    return obj


def format_currency(value):
    if value is None:
        return "N/A"
    if abs(value) >= 1e9:
        return f"${value/1e9:.2f}B"
    if abs(value) >= 1e6:
        return f"${value/1e6:.2f}M"
    return f"${value:.2f}"

def format_percentage(value):
    if value is None:
        return "N/A"
    return f"{value:.2f}%"
