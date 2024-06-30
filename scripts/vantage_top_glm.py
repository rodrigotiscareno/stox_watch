import requests
import pandas as pd
from utility import read_constituents as get_tickers
from typing import List
import csv
from parse_csv import load_csv_to_sql

api_key = "9NLUTD6I2QZTR2BZ"


# function to fetch top gainers/losers/mostactive data for a given symbol
def fetch_top_gL():
    url = f"https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    print(data)
    return data


def fetch_and_save_top_glm():
    data = fetch_top_gL()
    top_gainers = pd.DataFrame(data["top_gainers"])
    top_gainers["category"] = "top_gainers"

    top_losers = pd.DataFrame(data["top_losers"])
    top_losers["category"] = "top_losers"

    most_actively_traded = pd.DataFrame(data["most_actively_traded"])
    most_actively_traded["category"] = "most_actively_traded"

    # Concatenate all dataframes
    df = pd.concat([top_gainers, top_losers, most_actively_traded])

    csv_file_path = "top_glm.csv"
    df.to_csv(csv_file_path, index=False)

    load_csv_to_sql("top_glm.csv", "top_glm")


if __name__ == "__main__":
    fetch_and_save_top_glm()
