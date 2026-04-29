from view.prompts import currency_symbol


def print_portfolio(portfolio, prices):
    header = (
        f"{'Ticker':<10} {'Class':<14} {'Sector':<22} "
        f"{'Qty':>10} {'Buy':>12} {'Now':>12} {'TxValue':>14} {'CurValue':>14}"
    )
    print("\n" + header)
    print("-" * len(header))
    for a in portfolio.assets:
        cur = prices[a.ticker]
        sym = currency_symbol(a.currency)
        print(
            f"{a.ticker:<10} {a.asset_class:<14} {a.sector:<22} "
            f"{a.quantity:>10.2f} "
            f"{sym + format(a.purchase_price, '.2f'):>12} "
            f"{sym + format(cur, '.2f'):>12} "
            f"{sym + format(a.transaction_value, '.2f'):>14} "
            f"{sym + format(a.current_value(cur), '.2f'):>14}"
        )


def print_summary(portfolio, prices, fx_rates):
    base_sym = currency_symbol(portfolio.base_currency)
    total_tx = portfolio.transaction_value_in_base(fx_rates)
    total_cur = portfolio.current_value_in_base(prices, fx_rates)
    pnl = total_cur - total_tx
    pct = pnl / total_tx * 100 if total_tx else 0.0
    print(f"\nTotals in {portfolio.base_currency}:")
    print(f"  Transaction value: {base_sym}{total_tx:>12.2f}")
    print(f"  Current value:     {base_sym}{total_cur:>12.2f}")
    print(f"  Unrealized P&L:    {base_sym}{pnl:>12.2f} ({pct:+.2f}%)")


def print_weights(label, weights):
    print(f"\nWeights by {label}:")
    for k, v in sorted(weights.items(), key=lambda x: -x[1]):
        print(f"  {k:<22} {v * 100:>6.2f}%")
