from dataclasses import dataclass, field

from model.asset import Asset


@dataclass
class Portfolio:
    assets: list[Asset]

    def add(self, asset: Asset) -> None:
        self.assets.append(asset)

    def remove(self, ticker: str) -> None:
        self.assets = [a for a in self.assets if a.ticker != ticker]

    @property
    def total_transaction_value(self) -> float:
        return sum(a.transaction_value for a in self.assets)

    def total_current_value(self, prices: dict[str, float]) -> float:
        return sum(a.current_value(prices[a.ticker]) for a in self.assets)

    def weights(self, prices: dict[str, float]) -> dict[str, float]:
        total = self.total_current_value(prices)
        return {
            a.ticker: a.current_value(prices[a.ticker]) / total
            for a in self.assets
        }

    def weights_by(self, attr: str, prices: dict[str, float]) -> dict[str, float]:
        total = self.total_current_value(prices)
        groups: dict[str, float] = {}
        for a in self.assets:
            key = getattr(a, attr)
            groups[key] = groups.get(key, 0.0) + a.current_value(prices[a.ticker])
        return {k: v / total for k, v in groups.items()}