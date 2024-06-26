from utility import read_constituents as get_tickers

from typing import List
import yfinance as yf
import pandas as pd


if __name__ == "__main__":
    ticker_information = {}
    all_prices = []
    all_recs = []
    all_insider_summaries = []
    recommendations = {}

    for ticker in get_tickers():
        current_ticker = yf.Ticker(ticker)

        insider_df = current_ticker.insider_purchases
        insider_df.columns = insider_df.columns.str.lower().str.replace(" ", "_")
        insider_df = insider_df.pivot_table(
            index=None,
            columns="insider_purchases_last_6m",
            values=["shares", "trans"],
            aggfunc="first",
        )
        insider_df.columns = insider_df.columns.str.lower().str.replace(" ", "_")
        insider_df = insider_df.rename(columns={"insider_purchases_last_6m": "type"})
        insider_df.columns.name = None
        insider_df = insider_df.reset_index(names=["type"])
        insider_df["ticker"] = ticker

        current_rec_df = current_ticker.upgrades_downgrades
        current_rec_df.index = pd.to_datetime(current_rec_df.index)
        current_rec_df = current_rec_df[
            current_rec_df.index > "2024-01-01"
        ].reset_index(drop=False)
        current_rec_df["ticker"] = ticker

        ticker_information[ticker] = current_ticker.info

        current_price_df = current_ticker.history(period="5y", interval="1d")
        current_price_df["ticker"] = ticker

        all_prices.append(current_price_df)
        all_recs.append(current_rec_df)
        all_insider_summaries.append(insider_df)

    prices_df = pd.concat(all_prices)
    prices_df.reset_index(inplace=True, drop=False)
    prices_df.to_csv("prices.csv")

    recs_df = pd.concat(all_recs)
    recs_df.reset_index(inplace=True, drop=False)
    recs_df.to_csv("recs.csv")

    info_df = pd.DataFrame.from_dict(ticker_information, orient="index")
    info_df.reset_index(inplace=True)
    info_df.rename(columns={"index": "ticker"}, inplace=True)
    info_df.to_csv("ticker_information.csv", index=False)

    insider_df = pd.concat(all_insider_summaries)
    insider_df.to_csv("insider_summaries.csv", index=False)
