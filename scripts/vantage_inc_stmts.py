import requests
import pandas as pd
from utility import read_constituents as get_tickers
from parse_csv import load_csv_to_sql

api_key = "9NLUTD6I2QZTR2BZ"


# function to fetch income statements data for a given symbol
def fetch_income_statements(symbol):
    url = f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data


def fetch_and_save_income_statements():
    # Fetch income statements data for the top 100 symbols.
    tickers = get_tickers()

    all_cleaned_data = []
    annual_rep_headers = []

    # Fetch income statements annual reports for top stocks
    for i, symbol in enumerate(tickers):
        data = fetch_income_statements(symbol)
        if i == 0:
            annual_rep_headers = list(data["annualReports"][0].keys())
            annual_rep_headers.insert(0, "ticker")
        cleaned_data = [symbol]
        for k in annual_rep_headers[1:]:
            cleaned_data.append(data["annualReports"][0][k])
        all_cleaned_data.append(cleaned_data)

    # Convert to pandas DataFrame
    df = pd.DataFrame(all_cleaned_data)
    # Setting headers
    df.columns = annual_rep_headers

    # csv file name
    csv_file = "income_statements_data.csv"
    # Save DataFrame to CSV
    df.to_csv(csv_file, index=False)

    load_csv_to_sql("income_statements_data.csv", "inc_stmts")


if __name__ == "__main__":
    fetch_and_save_income_statements()
