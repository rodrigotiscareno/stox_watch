from yahooquery import Ticker
from utility import read_constituents as get_tickers
import pandas as pd


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
    df.to_csv("earnings_trends.csv", index=False)


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
    df.to_csv("earnings.csv", index=False)


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
    df.to_csv("financial_stats.csv", index=False)


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
    df.to_csv("key_stats.csv", index=False)


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
    df.to_csv("summary_detail.csv", index=False)


def main():
    tickers = get_tickers()
    data_types = ["summary_detail"]

    if "earnings" in data_types:
        get_earnings(tickers)

    if "earnings_trends" in data_types:
        get_earnings_trends(tickers)

    if "financial_data" in data_types:
        get_financial_data(tickers)

    if "key_stats" in data_types:
        get_key_stats(tickers)

    if "summary_detail" in data_types:
        get_summary_detail(tickers)


if __name__ == "__main__":
    main()
