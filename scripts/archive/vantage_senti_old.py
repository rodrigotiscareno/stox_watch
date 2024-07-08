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


api_key = "9NLUTD6I2QZTR2BZ"


# function to get sentiment and news for a given symbol
def fetch_sentiment(symbol):
    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={symbol}&time_from={time_from}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data


def fetch_and_save_sentiment():
    # fetch the top 100 symbols.
    tickers = get_tickers()
    sentiments = []

    for symbol in tickers:
        data = fetch_sentiment(symbol)
        average_sentiment = []
        # checking for feed
        if "feed" in data:
            # getting the sentiment score from each article for given ticker
            for feed_item in data["feed"]:
                for sentiment in feed_item["ticker_sentiment"]:
                    if sentiment["ticker"] == symbol:
                        average_sentiment.append(
                            float(sentiment["ticker_sentiment_score"])
                        )
            # average sentiment score across articles
            if len(average_sentiment) > 0:
                sentiments.append(
                    float(sum(average_sentiment)) / float(len(average_sentiment))
                )
            # articles with no mention get a sentiment score of 0
            else:
                sentiments.append(float(0))
       # handling case were there is no sentiment for a given symbol
        else:
            sentiments.append(float(0))

    sentiments = [round(value, 3) for value in sentiments]

    # creating dataframe
    df = pd.DataFrame()
    df["ticker"] = tickers
    df["sentiment"] = sentiments
    df["updated_time"] = datetime.now()

    # uploading to db
    df.to_sql("sentiment", con=engine, index=False, if_exists="replace")


if __name__ == "__main__":
    fetch_and_save_sentiment()
