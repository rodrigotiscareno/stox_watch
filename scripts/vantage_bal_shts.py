import requests
import pandas as pd
from utility import read_constituents as get_tickers
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from datetime import datetime

load_dotenv()

username = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
database = os.getenv("DB_NAME")
port = "3306"

engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
)

api_key = "9NLUTD6I2QZTR2BZ"


def fetch_bal_sht(symbol):
    url = f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data


def fetch_and_save_bal_sht():
    tickers = get_tickers()

    all_cleaned_data = []
    annual_rep_headers = []

    for i, symbol in enumerate(tickers):
        data = fetch_bal_sht(symbol)
        if i == 0:
            annual_rep_headers = list(data["annualReports"][0].keys())
            annual_rep_headers.insert(0, "ticker")
        cleaned_data = [symbol]
        for k in annual_rep_headers[1:]:
            cleaned_data.append(data["annualReports"][0][k])
        all_cleaned_data.append(cleaned_data)

    df = pd.DataFrame(all_cleaned_data)
    df.columns = annual_rep_headers

    df["updated_time"] = datetime.now()

    df.to_sql("bal_shts", con=engine, index=False, if_exists="replace")


if __name__ == "__main__":
    fetch_and_save_bal_sht()