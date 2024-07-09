import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import pandas as pd
from scripts.utility import read_constituents as get_tickers
from datetime import datetime, timedelta
from dotenv import load_dotenv
from sqlalchemy import create_engine


load_dotenv()

username = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
database = os.getenv("DB_NAME")
port = "3306"

engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
)

# date 30 days ago
date_30_days_ago = datetime.now() - timedelta(days=30)
time_from = date_30_days_ago.strftime("%Y%m%dT%H%M")


api_key = os.getenv("VANTAGE_KEY")


# function to get sentiment and news for a given symbol
def fetch_sentiment(symbol):
    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={symbol}&time_from={time_from}&limit=1000&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data


# function to convert time string to datetime object
def convert_to_datetime(time_str):
    return datetime.strptime(time_str, "%Y%m%dT%H%M%S")


def fetch_and_save_sentiment():
    # fetch the top 100 symbols.
    tickers = get_tickers()

    sentiments = []
    list_tickers = []
    time_published = []

    # retriving sentiment for each ticker
    for symbol in tickers:
        data = fetch_sentiment(symbol)
        # checking for feed
        if "feed" in data:
            # getting the sentiment score from each article for given ticker
            for feed_item in data["feed"]:
                for sentiment in feed_item["ticker_sentiment"]:
                    if sentiment["ticker"] == symbol:
                        sentiments.append(float(sentiment["ticker_sentiment_score"]))
                        list_tickers.append(symbol)
                # getting the date of the article
                if "time_published" in feed_item:
                    time_published.append(str(feed_item["time_published"]))
        # handling case were there is no sentiment for a given symbol
        else:
            sentiments.append(float(0))
            list_tickers.append(symbol)
            time_published.append("19700101T000000")

    # rounding sentiment scores to 3 decimal points
    sentiments = [round(value, 3) for value in sentiments]

    # setting the time_published date to be the same fromat as updated_time
    time_published_datetime_list = [
        datetime.strptime(time_str, "%Y%m%dT%H%M%S") for time_str in time_published
    ]

    # creating dataframe
    df = pd.DataFrame()
    df["ticker"] = list_tickers
    df["sentiment"] = sentiments
    df["time_published"] = time_published_datetime_list
    df["updated_time"] = datetime.now()

    # uploading to db
    df.to_sql("sentiment", con=engine, index=False, if_exists="replace")


if __name__ == "__main__":
    fetch_and_save_sentiment()
