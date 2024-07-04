import requests
import pandas as pd
from scripts.utility import read_constituents as get_tickers
from typing import List
import csv
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

# Calculate the date 30 days ago from today
date_30_days_ago = datetime.now() - timedelta(days=30)
time_from = date_30_days_ago.strftime('%Y%m%dT%H%M')


api_key = "9NLUTD6I2QZTR2BZ"


# function to sentiment and news for a given symbol
def fetch_sentiment(symbol):
    url = (
        f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={symbol}&time_from={time_from}&apikey={api_key}"
    )
    response = requests.get(url)
    data = response.json()
    return data

def fetch_and_save_sentiment():
    # Fetch the top 100 symbols.
    tickers = get_tickers()
    sentiments = []

    # for i, symbol in enumerate(tickers):
        # if i>=1:
        #     break
    for symbol in tickers:
        data = fetch_sentiment(symbol)
        #print(data)
        #print(data)
        # print(symbol)
        average_sentiment = []
        if "feed" in data:
            for feed_item in data["feed"]:
                for sentiment in feed_item["ticker_sentiment"]:
                    if sentiment["ticker"] == symbol:
                        average_sentiment.append(float(sentiment["ticker_sentiment_score"]))
            if len(average_sentiment) > 0:            
                sentiments.append(float(sum(average_sentiment))/float(len(average_sentiment)))
            else:
                sentiments.append(float(0))
        else:
            sentiments.append(float(0))
            #print(sentiments)

    sentiments = [round(value, 3) for value in sentiments]

    # Convert to pandas DataFrame
    df = pd.DataFrame()
    # Setting headers
    df["ticker"] = tickers
    df["sentiment"] = sentiments
    df["updated_time"] = datetime.now()

    df.to_sql("senti", con=engine, index=False, if_exists="replace")


if __name__ == "__main__":
    fetch_and_save_sentiment()
