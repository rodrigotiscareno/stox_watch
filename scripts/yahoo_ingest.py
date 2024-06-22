from utility import read_constituents as get_tickers

from typing import List
import yfinance as yf
import pandas as pd


if __name__ == "__main__":
    # ticker_information = {}
    # all_prices = []

    recommendations = {}
    for ticker in get_tickers():
        current_ticker = yf.Ticker(ticker)

        df = current_ticker.upgrades_downgrades

        df = df.loc[[df.GradeDate > "2024-01-01"]]
        recommendations[ticker] = current_ticker.upgrades_downgrades

    print(recommendations)

    # ticker_information[ticker] = current_ticker.info

    # current_price_df = current_ticker.history(period="5y", interval="1d")
    # current_price_df["ticker"] = ticker

    # all_prices.append(current_price_df)

    # prices_df = pd.concat(all_prices)
    # prices_df.reset_index(inplace=True, drop=False)
    # prices_df.to_csv("prices.csv")

    # info_df = pd.DataFrame.from_dict(ticker_information, orient="index")
    # info_df.reset_index(inplace=True)
    # info_df.rename(columns={"index": "ticker"}, inplace=True)
    # info_df.to_csv("ticker_information.csv", index=False)
