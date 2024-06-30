import yfinance as yf
import pandas as pd
from typing import List
from utility import read_constituents as get_tickers
from parse_csv import load_csv_to_sql


def fetch_prices(tickers: List[str], period: str) -> pd.DataFrame:
    all_prices = []
    for ticker in tickers:
        current_ticker = yf.Ticker(ticker)
        current_price_df = current_ticker.history(period=period, interval="1d")
        current_price_df["ticker"] = ticker
        all_prices.append(current_price_df)
    result = pd.concat(all_prices)
    result.columns = result.columns.str.lower()
    result.columns = result.columns.str.replace(" ", "_")
    return result


if __name__ == "__main__":
    tickers = get_tickers()
    period = "5y"
    prices_df = fetch_prices(tickers, period)
    prices_df.to_csv("prices.csv", index=False)
    load_csv_to_sql("prices.csv", "ticker_price")
