from dataclasses import dataclass

from model.asset import Asset

@dataclass
class Portfolio:
    assets: list[Asset]
    
    