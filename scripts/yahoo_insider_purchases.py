import yfinance as yf
import pandas as pd
from typing import List
from scripts.utility import read_constituents as get_tickers
from utils.parse_csv import load_df_to_sql
from datetime import datetime


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


def main():
    tickers = get_tickers()
    insider_df = fetch_insider_purchases(tickers)
    insider_df["updated_on"] = datetime.now()
    load_df_to_sql(insider_df, "insider_summaries")


if __name__ == "__main__":
    main()
