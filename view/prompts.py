CURRENCY_SYMBOLS = {
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "JPY": "¥",
    "CHF": "CHF ",
    "DKK": "kr ",
    "SEK": "kr ",
    "NOK": "kr ",
}


def currency_symbol(currency: str) -> str:
    return CURRENCY_SYMBOLS.get(currency, f"{currency} ")


def prompt_asset_details(current_price: float | None = None, currency: str = "") -> dict:
    quantity = _prompt_float("Quantity: ")
    if current_price is not None:
        sym = currency_symbol(currency)
        label = f"Purchase price (current: {sym}{current_price:.2f}): "
    else:
        label = "Purchase price: "
    return {
        "quantity": quantity,
        "purchase_price": _prompt_float(label),
    }


def _prompt_float(label: str) -> float:
    while True:
        try:
            return float(input(label).strip())
        except ValueError:
            print("Please enter a number.")
