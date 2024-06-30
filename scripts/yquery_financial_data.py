from yahooquery import Ticker
from utility import read_constituents as get_tickers
import pandas as pd
from parse_csv import load_csv_to_sql
from datetime import datetime


def get_financial_data(tickers):
    all_data = []
    for ticker in tickers:
        ticker = ticker.lower()
        current_ticker = Ticker(ticker)

        response = current_ticker.financial_data
        df = pd.DataFrame([response[ticker]])
        df["ticker"] = ticker.upper()

        all_data.append(df)

    df = pd.concat(all_data)
    df["updated_on"] = datetime.now()
    df.to_csv("financial_stats.csv", index=False)


def main():
    tickers = get_tickers()
    get_financial_data(tickers)
    load_csv_to_sql("financial_stats.csv", "financial_stats")


if __name__ == "__main__":
    main()
