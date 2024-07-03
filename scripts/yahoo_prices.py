import yfinance as yf
import pandas as pd
from typing import List
from scripts.utility import read_constituents as get_tickers
from utils.parse_csv import load_df_to_sql
from datetime import datetime


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
    result = result.reset_index()
    return result


def main():
    tickers = get_tickers()
    period = "5y"
    prices_df = fetch_prices(tickers, period)
    prices_df["updated_on"] = datetime.now()
    load_df_to_sql(prices_df, "ticker_price")


if __name__ == "__main__":
    main()
