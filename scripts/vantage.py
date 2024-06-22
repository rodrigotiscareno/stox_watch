import requests
import pandas as pd
from utility import read_constituents as get_tickers
from typing import List

# # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
# url = "https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey="
# r = requests.get(url)
# data = r.json()

# print(pd.DataFrame(data["most_actively_traded"]))


# Create a function to fetch cash flow data for a given symbol
def fetch_cash_flow(symbol):
    url = (
        f"https://www.alphavantage.co/query?function=CASH_FLOW&symbol={symbol}&apikey="
    )
    response = requests.get(url)
    data = response.json()
    return data


# Fetch cash flow data for the top 100 symbols.
cash_flow_data = {}
tickers = get_tickers()

for symbol in tickers:
    data = fetch_cash_flow(symbol)
    cash_flow_data[symbol] = data

print(cash_flow_data)
