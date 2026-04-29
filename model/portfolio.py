from dataclasses import dataclass, field

from model.asset import Asset


@dataclass
class Portfolio:
    assets: list[Asset]
    base_currency: str = "EUR"

    def add(self, asset: Asset) -> None:
        self.assets.append(asset)

    def remove(self, ticker: str) -> None:
        self.assets = [a for a in self.assets if a.ticker != ticker]

    def currencies(self) -> set[str]:
        return {a.currency for a in self.assets}

    def transaction_value_in_base(self, fx_rates: dict[str, float]) -> float:
        return sum(a.transaction_value * fx_rates[a.currency] for a in self.assets)

    def current_value_in_base(
        self, prices: dict[str, float], fx_rates: dict[str, float]
    ) -> float:
        return sum(
            a.current_value(prices[a.ticker]) * fx_rates[a.currency]
            for a in self.assets
        )

    def weights(
        self, prices: dict[str, float], fx_rates: dict[str, float]
    ) -> dict[str, float]:
        total = self.current_value_in_base(prices, fx_rates)
        return {
            a.ticker: a.current_value(prices[a.ticker]) * fx_rates[a.currency] / total
            for a in self.assets
        }

    def weights_by(
        self, attr: str, prices: dict[str, float], fx_rates: dict[str, float]
    ) -> dict[str, float]:
        total = self.current_value_in_base(prices, fx_rates)
        groups: dict[str, float] = {}
        for a in self.assets:
            key = getattr(a, attr)
            value = a.current_value(prices[a.ticker]) * fx_rates[a.currency]
            groups[key] = groups.get(key, 0.0) + value
        return {k: v / total for k, v in groups.items()}
