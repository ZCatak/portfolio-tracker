import yfinance as yf
import pandas as pd


def get_current_prices(tickers: list[str]) -> dict[str, float]:
    closes = _fetch_closes(tickers, period="1d")
    return {t: float(closes[t].iloc[-1]) for t in closes.columns}


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
