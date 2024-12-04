
def format_number(value, decimals=2) -> str:
    value = float(value)

    if value.is_integer():
        return f"{int(value):,}"
    return f"{value:,.{decimals}f}"
