from model.asset import Asset
from model.portfolio import Portfolio
from model.prices import get_current_prices
from view.view import pick_ticker, pick_asset_class, pick_sector, pick_owned_ticker
from view.prompts import prompt_asset_details
from view.portfolio_view import print_portfolio, print_summary, print_weights


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
                pass
                #simulate_portfolio(portfolio)
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
    tickers = [a.ticker for a in portfolio.assets]
    prices = get_current_prices(tickers)
    print_portfolio(portfolio, prices)
    print_summary(portfolio, prices)
    print_weights("ticker", portfolio.weights(prices))
    print_weights("sector", portfolio.weights_by("sector", prices))
    print_weights("asset class", portfolio.weights_by("asset_class", prices))


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
    asset_class = pick_asset_class()
    if asset_class is None:
        return
    sector = pick_sector(asset_class)
    if sector is None:
        return
    details = prompt_asset_details()
    portfolio.add(Asset(ticker=ticker, asset_class=asset_class, sector=sector, **details))
    print(f"Added {details['quantity']} of {ticker} at ${details['purchase_price']} each.")
