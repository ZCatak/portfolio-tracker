import yfinance as yf
import pandas as pd


def get_current_prices(tickers: list[str]) -> dict[str, float]:
    closes = _fetch_closes(tickers, period="1d")
    return {t: float(closes[t].iloc[-1]) for t in closes.columns}


def get_current_price(ticker: str) -> float:
    return get_current_prices([ticker])[ticker]


def get_currency(ticker: str) -> str:
    info = yf.Ticker(ticker).fast_info
    ccy = info.get("currency") if hasattr(info, "get") else info["currency"]
    if not ccy:
        raise RuntimeError(f"No currency metadata for {ticker}")
    return ccy.upper()


def get_fx_rates(currencies: set[str], base: str) -> dict[str, float]:
    rates: dict[str, float] = {}
    for ccy in currencies:
        if ccy == base:
            rates[ccy] = 1.0
            continue
        pair = f"{ccy}{base}=X"
        price = yf.Ticker(pair).fast_info["last_price"]
        if not price:
            raise RuntimeError(f"No FX rate for {pair}")
        rates[ccy] = float(price)
    return rates


def get_history(tickers: list[str], period: str = "5y") -> pd.DataFrame:
    return _fetch_closes(tickers, period=period)


def _fetch_closes(tickers: list[str], period: str) -> pd.DataFrame:
    data = yf.download(tickers, period=period, progress=False, auto_adjust=True)
    if data is None or data.empty:
        raise RuntimeError(f"No price data returned for {tickers}")
    closes = data["Close"]
    if isinstance(closes, pd.Series):
        closes = closes.to_frame(name=tickers[0])
    return closes
