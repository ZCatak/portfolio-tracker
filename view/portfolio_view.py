def print_portfolio(portfolio, prices):
    header = (
        f"{'Ticker':<10} {'Class':<14} {'Sector':<22} "
        f"{'Qty':>10} {'Buy':>10} {'Now':>10} {'TxValue':>12} {'CurValue':>12}"
    )
    print("\n" + header)
    print("-" * len(header))
    for a in portfolio.assets:
        cur = prices[a.ticker]
        print(
            f"{a.ticker:<10} {a.asset_class:<14} {a.sector:<22} "
            f"{a.quantity:>10.2f} {a.purchase_price:>10.2f} {cur:>10.2f} "
            f"{a.transaction_value:>12.2f} {a.current_value(cur):>12.2f}"
        )


def print_summary(portfolio, prices):
    total_tx = portfolio.total_transaction_value
    total_cur = portfolio.total_current_value(prices)
    pnl = total_cur - total_tx
    pct = pnl / total_tx * 100 if total_tx else 0.0
    print(f"\nTotal transaction value: {total_tx:>12.2f}")
    print(f"Total current value:     {total_cur:>12.2f}")
    print(f"Unrealized P&L:          {pnl:>12.2f} ({pct:+.2f}%)")


def print_weights(label, weights):
    print(f"\nWeights by {label}:")
    for k, v in sorted(weights.items(), key=lambda x: -x[1]):
        print(f"  {k:<22} {v * 100:>6.2f}%")
