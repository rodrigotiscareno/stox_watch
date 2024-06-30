import requests
import pandas as pd
from utility import read_constituents as get_tickers
from typing import List
import csv
from parse_csv import load_csv_to_sql

api_key = "9NLUTD6I2QZTR2BZ"

# function to fetch top gainers/losers/mostactive data for a given symbol
def fetch_top_gL():
    url = (
        f"https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={api_key}"
    )
    response = requests.get(url)
    data = response.json()
    return data

def fetch_and_save_top_glm():
    # Fetch top 100 symbols.
    tickers = get_tickers()

    data = fetch_top_gL()
    top_gainers = data["top_gainers"]
    top_losers = data["top_losers"]
    most_active = data["most_actively_traded"]

    gainers_tickers = [g['ticker'] for g in top_gainers]
    losers_tickers = [l['ticker'] for l in top_losers]
    most_active_tickers =  [m['ticker'] for m in top_losers]

    # DO NOT REMOVE: Good for testing when top 100 stocks do not show up in the data
    # df = pd.DataFrame({
    #     'gainers': gainers_tickers,
    #     'losers': losers_tickers,
    #     'most_active': most_active_tickers
    # })

    # Find matches with top 100 tickers
    gainers_match = [ticker for ticker in tickers if ticker in gainers_tickers]
    losers_match = [ticker for ticker in tickers if ticker in losers_tickers]
    most_active_match = [ticker for ticker in tickers if ticker in most_active_tickers]

    # Prepare data for the DataFrame
    max_len = max(len(gainers_match), len(losers_match), len(most_active_match))
    gainers_match.extend([None] * (max_len - len(gainers_match)))
    losers_match.extend([None] * (max_len - len(losers_match)))
    most_active_match.extend([None] * (max_len - len(most_active_match)))

    # Convert to pandas DataFrame
    df = pd.DataFrame({
        'gainers': gainers_match,
        'losers': losers_match,
        'most_active': most_active_match
    })

    # Save DataFrame to CSV
    csv_file_path = "../notebooks/data/top_glm.csv"
    df.to_csv(csv_file_path, index=False)

    load_csv_to_sql("../notebooks/data/top_glm.csv", "top_glm")

if __name__ == "__main__":
    fetch_and_save_top_glm()