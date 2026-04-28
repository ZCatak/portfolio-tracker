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



def add_asset(portfolio: Portfolio):
    ticker = pick_ticker()
    if ticker is None:
        return
    details = prompt_asset_details()
    portfolio.add(Asset(ticker=ticker, **details))
    print(f"Added {details['quantity']} of {ticker} at ${details['purchase_price']} each to portfolio.")