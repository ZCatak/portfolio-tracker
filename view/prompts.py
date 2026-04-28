def prompt_asset_details() -> dict:
    return {
        "quantity": _prompt_float("Quantity: "),
        "purchase_price": _prompt_float("Purchase price: "),
    }


def _prompt_float(label: str) -> float:
    while True:
        try:
            return float(input(label).strip())
        except ValueError:
            print("Please enter a number.")
