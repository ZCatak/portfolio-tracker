from model.asset import Asset
from model.portfolio import Portfolio
from view.view import pick_ticker
from view.prompts import prompt_asset_details




def run():
    portfolio = Portfolio(assets=[])

    while True:
        print("\n1) Add asset   2) Quit")
        choice = input("> ").strip()

        if choice == "1":
            add_asset(portfolio)
        elif choice == "2":
            break
        else:
            print("Invalid choice. Please try again.")

        ## TODO: Add option to show current and historical price of each ticker and graphing (yfinance, matplotlib).s

        ## TODO: View the current portfolio, displaying each asset's name, sector, asset class, quantity,purchase price, transaction value and current value. 
        ## via matplotlib of gewoon in terminal ff kijken    

        ## TODO: . See calculations for the total portfolio value and the (relative) weights of each asset including the option to see the same per asset class and sector.
        ## 
        ## TODO: Be able to perform a simulation over the upcoming fifteen years for the portfolio, demonstrating the impact of risk and uncertainty. Assume 100.000 simulated paths.
        ## Monte Carlo simulation, DNB dataset gebruiken voor rente? of gewoon
def add_asset(portfolio: Portfolio):
    ticker = pick_ticker()
    if ticker is None:
        return
    details = prompt_asset_details()
    portfolio.add(Asset(ticker=ticker, **details))
    print(f"Added {details['quantity']} of {ticker} at ${details['purchase_price']} each to portfolio.")