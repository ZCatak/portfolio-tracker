from dataclasses import dataclass


@dataclass
class Asset:
    ticker: str
    sector: str
    asset_class: str
    quantity: float
    purchase_price: float
