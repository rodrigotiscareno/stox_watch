from datetime import datetime
from yahooquery import Ticker
from utility import read_constituents as get_tickers
import pandas as pd
from parse_csv import load_csv_to_sql


def get_summary_detail(tickers):
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
    df.to_csv("summary_detail.csv", index=False)


def main():
    tickers = get_tickers()
    get_summary_detail(tickers)
    load_csv_to_sql("summary_detail.csv", "summary_detail")


if __name__ == "__main__":
    main()
