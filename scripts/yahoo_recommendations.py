import yfinance as yf
import pandas as pd
from typing import List
from utility import read_constituents as get_tickers
from parse_csv import load_csv_to_sql


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


if __name__ == "__main__":
    tickers = get_tickers()
    recs_df = fetch_recommendations(tickers)
    recs_df.to_csv("recs.csv", index=False)
    load_csv_to_sql("recs.csv", "recs")
