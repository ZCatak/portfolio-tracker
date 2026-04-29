from model.asset import Asset
from model.portfolio import Portfolio
from model.prices import get_current_prices, get_current_price, get_currency, get_fx_rates
from view.view import pick_ticker, pick_asset_class, pick_sector, pick_owned_ticker, pick_currency
from view.prompts import prompt_asset_details, prompt_cash_amount
from view.portfolio_view import print_portfolio, print_summary, print_weights
from model.simulation import simulate_portfolio


## TODO: Add option to show current and historical price of each ticker and graphing (yfinance, matplotlib).s

## TODO: View the current portfolio, displaying each asset's name, sector, asset class, quantity,purchase price, transaction value and current value.
## via matplotlib of gewoon in terminal ff kijken

## TODO: . See calculations for the total portfolio value and the (relative) weights of each asset including the option to see the same per asset class and sector.
##
## TODO: Be able to perform a simulation over the upcoming fifteen years for the portfolio, demonstrating the impact of risk and uncertainty. Assume 100.000 simulated paths.
## Monte Carlo simulation, DNB dataset gebruiken voor rente? of gewoon


def run():
    portfolio = Portfolio(assets=[])

    while True:
        print("\n1) Add asset   2) View portfolio   3) Simulate portfolio   4) Remove asset   5) Quit")
        choice = input("> ").strip()

        if choice == "1":
            add_asset(portfolio)
        elif choice == "2":
            if not portfolio.assets:
                print("Your portfolio is empty. Please add assets first.")
            else:
                view_portfolio(portfolio)
        elif choice == "3":
            if not portfolio.assets:
                print("Your portfolio is empty. Please add assets first.")
            else:
                simulate(portfolio)
        elif choice == "4":
            if not portfolio.assets:
                print("Your portfolio is empty. Please add assets first.")
            else:
                remove_asset(portfolio)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")


def view_portfolio(portfolio: Portfolio):
    real_tickers = [a.ticker for a in portfolio.assets if not a.ticker.startswith("CASH-")]
    prices = get_current_prices(real_tickers) if real_tickers else {}
    for a in portfolio.assets:
        if a.ticker.startswith("CASH-"):
            prices[a.ticker] = 1.0
    fx_rates = get_fx_rates(portfolio.currencies(), portfolio.base_currency)
    print_portfolio(portfolio, prices)
    print_summary(portfolio, prices, fx_rates)
    print_weights("ticker", portfolio.weights(prices, fx_rates))
    print_weights("sector", portfolio.weights_by("sector", prices, fx_rates))
    print_weights("asset class", portfolio.weights_by("asset_class", prices, fx_rates))


def simulate(portfolio: Portfolio):
    real_tickers = [a.ticker for a in portfolio.assets if not a.ticker.startswith("CASH-")]
    prices = get_current_prices(real_tickers) if real_tickers else {}
    for a in portfolio.assets:
        if a.ticker.startswith("CASH-"):
            prices[a.ticker] = 1.0
    fx_rates = get_fx_rates(portfolio.currencies(), portfolio.base_currency)
    simulate_portfolio(portfolio, prices, fx_rates)


def remove_asset(portfolio: Portfolio):
    owned = sorted({a.ticker for a in portfolio.assets})
    ticker = pick_owned_ticker(owned)
    if ticker is None:
        return
    if ticker not in owned:
        print(f"{ticker} is not in your portfolio.")
        return
    portfolio.remove(ticker)
    print(f"Removed {ticker} from your portfolio.")


def add_asset(portfolio: Portfolio):
    ticker = pick_ticker()
    if ticker is None:
        return
    if ticker == "CASH":
        add_cash(portfolio)
        return
    currency = get_currency(ticker)
    current_price = get_current_price(ticker)
    asset_class = pick_asset_class()
    if asset_class is None:
        return
    sector = pick_sector(asset_class)
    if sector is None:
        return
    details = prompt_asset_details(current_price=current_price, currency=currency)
    portfolio.add(
        Asset(
            ticker=ticker,
            asset_class=asset_class,
            sector=sector,
            currency=currency,
            **details,
        )
    )
    print(f"Added {details['quantity']} of {ticker} at {details['purchase_price']:.2f} {currency} each.")


def add_cash(portfolio: Portfolio):
    currency = pick_currency()
    if currency is None:
        return
    amount = prompt_cash_amount(currency)
    ticker = f"CASH-{currency}"
    portfolio.add(
        Asset(
            ticker=ticker,
            asset_class="Cash",
            sector="Cash",
            currency=currency,
            quantity=amount,
            purchase_price=1.0,
        )
    )
    print(f"Added {amount:.2f} {currency} cash.")
