import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from model.prices import get_history

OUTPUT_PATH = "simulation.png"

YEARS = 15
PATHS = 100_000
TRADING_DAYS = 252


def simulate_portfolio(portfolio, prices, fx_rates):
    real = [a for a in portfolio.assets if not a.ticker.startswith("CASH-")]
    if not real:
        print("Need at least one non-cash asset to simulate.")
        return

    tickers = [a.ticker for a in real]
    values = np.array(
        [a.current_value(prices[a.ticker]) * fx_rates[a.currency] for a in real]
    )
    weights = values / values.sum()

    history = get_history(tickers, period="5y")[tickers].values
    daily_log = np.log(history[1:] / history[:-1])
    daily_port = daily_log @ weights
    mu = daily_port.mean() * TRADING_DAYS
    sigma = daily_port.std() * np.sqrt(TRADING_DAYS)

    cash = sum(
        a.quantity * fx_rates[a.currency]
        for a in portfolio.assets
        if a.ticker.startswith("CASH-")
    )
    initial = values.sum()
    z = np.random.normal(size=(YEARS, PATHS))
    log_steps = (mu - 0.5 * sigma**2) + sigma * z
    cum = np.vstack([np.zeros((1, PATHS)), np.cumsum(log_steps, axis=0)])
    paths = initial * np.exp(cum) + cash

    pcts = np.percentile(paths, [5, 50, 95], axis=1)
    years = np.arange(YEARS + 1)
    plt.fill_between(years, pcts[0], pcts[2], alpha=0.3, label="5-95%")
    plt.plot(years, pcts[1], label="Median")
    plt.xlabel("Years")
    plt.ylabel(f"Portfolio value ({portfolio.base_currency})")
    plt.title(
        f"Monte Carlo: {PATHS:,} paths, mu={mu:.1%}, sigma={sigma:.1%}"
    )
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_PATH)
    plt.close()
    p5, p50, p95 = pcts[:, -1]
    print(f"\nSaved plot to {OUTPUT_PATH}")
    print(f"15-year terminal value ({portfolio.base_currency}):")
    print(f"  5th  percentile: {p5:>14,.2f}")
    print(f"  median:          {p50:>14,.2f}")
    print(f"  95th percentile: {p95:>14,.2f}")
