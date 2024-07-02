from typing import List
import yfinance as yf
import pandas as pd
from utility import read_constituents as get_tickers


def fetch_insider_purchases(tickers: List[str]) -> pd.DataFrame:
    all_insider_summaries = []
    for ticker in tickers:
        current_ticker = yf.Ticker(ticker)
        insider_df = current_ticker.insider_purchases
        insider_df.columns = insider_df.columns.str.lower().str.replace(" ", "_")
        insider_df = insider_df.rename(columns={"insider_purchases_last_6m": "type"})
        insider_df["ticker"] = ticker
        all_insider_summaries.append(insider_df)
    result = pd.concat(all_insider_summaries)
    result.columns = result.columns.str.lower()
    return result


def fetch_recommendations(tickers: List[str]) -> pd.DataFrame:
    all_recs = []
    for ticker in tickers:
        current_ticker = yf.Ticker(ticker)
        current_rec_df = current_ticker.upgrades_downgrades
        current_rec_df.index = pd.to_datetime(current_rec_df.index)
        current_rec_df = current_rec_df[current_rec_df.index > "2024-01-01"]
        current_rec_df["ticker"] = ticker
        all_recs.append(current_rec_df)
    result = pd.concat(all_recs)
    result.columns = result.columns.str.lower()
    return result


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


def main(period: str, data_types: List[str]):
    tickers = get_tickers()
    if "insider" in data_types:
        insider_df = fetch_insider_purchases(tickers)
        insider_df.to_csv("insider_summaries.csv", index=False)
    if "recs" in data_types:
        recs_df = fetch_recommendations(tickers)
        recs_df.to_csv("recs.csv", index=False)
    if "prices" in data_types:
        prices_df = fetch_prices(tickers, period)
        prices_df.to_csv("prices.csv", index=False)


if __name__ == "__main__":
    period = "5y"
    data_types = ["prices"]

    main(period, data_types)
