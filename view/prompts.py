def prompt_asset_details() -> dict:
    return {
        "sector": _prompt_text("Sector: "),
        "quantity": _prompt_float("Quantity: "),
        "purchase_price": _prompt_float("Purchase price: "),
    }


def _prompt_text(label: str) -> str:
    while True:
        value = input(label).strip()
        if value:
            return value
        print("Please enter a value.")


def _prompt_float(label: str) -> float:
    while True:
        try:
            return float(input(label).strip())
        except ValueError:
            print("Please enter a number.")
