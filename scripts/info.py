from constituents import get_spy as get_constituents
from typing import List
import yfinance as yf
import pandas as pd


def get_tickers(limit: int = 100) -> List[str]:
    df = get_constituents(limit)

    return list(df.Symbol)


ticker_information = {}
all_prices = []
for ticker in get_tickers(limit=100):
    current_ticker = yf.Ticker(ticker)

    ticker_information[ticker] = current_ticker.info

    current_price_df = current_ticker.history(period="5y", interval="1d")
    current_price_df["Ticker"] = ticker

    all_prices.append(current_price_df)


prices_df = pd.concat(all_prices)
prices_df.reset_index(inplace=True, drop=False)
prices_df.to_csv("prices.csv")


info_df = pd.DataFrame.from_dict(ticker_information, orient="index")
info_df.reset_index(inplace=True)
info_df.rename(columns={"index": "Ticker"}, inplace=True)
info_df.to_csv("ticker_information.csv", index=False)
