from datetime import datetime
from yahooquery import Ticker
from scripts.utility import read_constituents as get_tickers
import pandas as pd
from utils.parse_csv import load_csv_to_sql


def get_earnings(tickers):
    all_earnings = []
    for ticker in tickers:
        ticker = ticker.lower()
        current_ticker = Ticker(ticker)

        data = current_ticker.earnings

        earnings_quarterly_df = pd.DataFrame(data[ticker]["earningsChart"]["quarterly"])
        earnings_quarterly_df["ticker"] = ticker.upper()

        financials_quarterly_df = pd.DataFrame(
            data[ticker]["financialsChart"]["quarterly"]
        )
        financials_quarterly_df["ticker"] = ticker.upper()

        df = pd.merge(
            earnings_quarterly_df,
            financials_quarterly_df,
            on=["date", "ticker"],
            how="left",
        )

        df["year"] = df["date"].str[-4:]
        all_earnings.append(df)

    df = pd.concat(all_earnings)
    df["updated_on"] = datetime.now()
    df.to_csv("earnings.csv", index=False)


def main():
    tickers = get_tickers()
    get_earnings(tickers)
    load_csv_to_sql("earnings.csv", "earnings")


if __name__ == "__main__":
    main()
