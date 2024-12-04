from decimal import Decimal, ROUND_HALF_UP


def format_percentage(profit_percentage: float) -> str:
    """
    Format a profit percentage with a sign and up to one decimal place.

    If the percentage is an integer, it is formatted without decimal places.
    If the percentage has a fractional part, it is formatted with one decimal place.

    Parameters:
    profit_percentage (float): The profit percentage to format.

    Returns:
    str: The formatted percentage string with a sign.

    Examples:
    >>> format_percentage(31.0)
    '+31%'
    >>> format_percentage(31.53)
    '+31.5%'
    >>> format_percentage(-31.0)
    '-31%'
    >>> format_percentage(-31.5)
    '-31.5%'
    """
    profit_decimal = Decimal(profit_percentage).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)

    if profit_decimal % 1 == 0:
        # If the number is an integer, format it as an integer with a sign
        formatted_percentage = f"{profit_decimal:+.0f}%"
    else:
        # If the number has a fractional part, format it with one decimal place and a sign
        formatted_percentage = f"{profit_decimal:+.1f}%"
    return formatted_percentage
