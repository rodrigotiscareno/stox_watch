from yahooquery import Ticker
from utility import read_constituents as get_tickers
import pandas as pd
from parse_csv import load_csv_to_sql
from datetime import datetime


def get_earnings_trends(tickers):
    all_trends = []
    for ticker in tickers:
        ticker = ticker.lower()
        current_ticker = Ticker(ticker)
        t = current_ticker.earnings_trend

        data = t[ticker]["trend"]

        all_data = []
        for entry in data:
            base_info = {
                "period": entry["period"],
                "endDate": entry["endDate"],
                "growth": entry["growth"],
            }

            earnings = {**base_info, **entry["earningsEstimate"]}
            earnings["type"] = "earningsEstimate"

            revenue = {**base_info, **entry["revenueEstimate"]}
            revenue["type"] = "revenueEstimate"

            eps_trend = {**base_info, **entry["epsTrend"]}
            eps_trend["type"] = "epsTrend"

            eps_revisions = {**base_info, **entry["epsRevisions"]}
            eps_revisions["type"] = "epsRevisions"

            all_data.extend([earnings, revenue, eps_trend, eps_revisions])

        df = pd.DataFrame(all_data)
        df["ticker"] = ticker.upper()

        all_trends.append(df)

    df = pd.concat(all_trends)
    df["updated_on"] = datetime.now()
    df.to_csv("earnings_trends.csv", index=False)


def main():
    tickers = get_tickers()
    get_earnings_trends(tickers)
    load_csv_to_sql("earnings_trends.csv", "earnings_trends")


if __name__ == "__main__":
    main()
