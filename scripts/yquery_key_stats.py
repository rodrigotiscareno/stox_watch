from yahooquery import Ticker
from utils.utility import read_constituents as get_tickers
import pandas as pd
from utils.parse_csv import load_csv_to_sql
from datetime import datetime


def get_key_stats(tickers):
    all_data = []
    for ticker in tickers:
        ticker = ticker.lower()
        current_ticker = Ticker(ticker)

        response = current_ticker.key_stats
        df = pd.DataFrame([response[ticker]])
        df["ticker"] = ticker.upper()

        all_data.append(df)

    df = pd.concat(all_data)
    df["updated_on"] = datetime.now()
    df.to_csv("key_stats.csv", index=False)


def main():
    tickers = get_tickers()
    get_key_stats(tickers)
    load_csv_to_sql("key_stats.csv", "key_stats")


if __name__ == "__main__":
    main()
