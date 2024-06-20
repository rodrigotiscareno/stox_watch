import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


def get_dia() -> pd.DataFrame:
    """
    Retrieve and return a DataFrame containing information about all the tickers in the Dow Jones Industrial Average.

    Returns:
        pandas.DataFrame: A DataFrame containing the ticker information for the Dow Jones Industrial Average.
    """
    url = "https://www.dogsofthedow.com/dow-jones-industrial-average-companies.htm"
    request = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = bs(request.text, "lxml")
    stats = soup.find(
        "table", class_="tablepress tablepress-id-42 tablepress-responsive"
    )
    pulled_df = pd.read_html(str(stats))[0]
    return pulled_df


def get_spy(limit: int = 100) -> pd.DataFrame:
    """
    Retrieve and return a DataFrame containing information about the S&P 500 companies limited by a specified number.

    Args:
        limit (int, optional): Number of S&P 500 companies' data to return. Defaults to 100.

    Returns:
        pandas.DataFrame: A DataFrame containing the limited S&P 500 companies' data.
    """
    url = "https://www.slickcharts.com/sp500"
    request = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = bs(request.text, "lxml")
    stats = soup.find("table", class_="table table-hover table-borderless table-sm")
    df = pd.read_html(str(stats))[0]
    df["% Chg"] = df["% Chg"].str.strip("()-%")
    df["% Chg"] = pd.to_numeric(df["% Chg"])
    df["Chg"] = pd.to_numeric(df["Chg"])
    return df[:limit]


def get_qqq() -> pd.DataFrame:
    """
    Retrieve and return a DataFrame containing information about all tickers in the NASDAQ-100 index.

    Returns:
        pandas.DataFrame: A DataFrame sorted by 'Market Cap $bn' containing information about NASDAQ-100 tickers.
    """
    urls = [
        "https://www.dividendmax.com/market-index-constituents/nasdaq-100",
        "https://www.dividendmax.com/market-index-constituents/nasdaq-100?page=2",
        "https://www.dividendmax.com/market-index-constituents/nasdaq-100?page=3",
    ]
    dfs = []
    for url in urls:
        request = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = bs(request.text, "lxml")
        stats = soup.find("table", class_="mdc-data-table__table")
        temp = pd.read_html(str(stats))[0]
        dfs.append(temp)
    df = pd.concat(dfs, ignore_index=True)
    df.rename(columns={"Market Cap": "Market Cap $bn"}, inplace=True)
    df["Market Cap $bn"] = df["Market Cap $bn"].str.strip("£$bn")
    df["Market Cap $bn"] = pd.to_numeric(df["Market Cap $bn"])
    df = df.sort_values("Market Cap $bn", ascending=False)
    return df
