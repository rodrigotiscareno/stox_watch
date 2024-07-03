from datetime import datetime
import requests
import pandas as pd
from utils.parse_csv import load_df_to_sql

api_key = "9NLUTD6I2QZTR2BZ"


# function to fetch top gainers/losers/mostactive data for a given symbol
def fetch_top_gL():
    url = f"https://www.alphavantage.co/query?function=TOP_GAINERS_LOSERS&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
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

    df["updated_on"] = datetime.now()

    load_df_to_sql(df, "top_glm")


def main():
    fetch_and_save_top_glm()


if __name__ == "__main__":
    main()
