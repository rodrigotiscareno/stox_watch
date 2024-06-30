import yfinance as yf
import pandas as pd
from typing import List
from utility import read_constituents as get_tickers
from parse_csv import load_csv_to_sql


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


if __name__ == "__main__":
    tickers = get_tickers()
    insider_df = fetch_insider_purchases(tickers)
    insider_df.to_csv("insider_summaries.csv", index=False)
    load_csv_to_sql("insider_summaries.csv", "insider_summaries")
