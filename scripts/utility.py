from constituents import get_spy as get_constituents
from typing import List


def get_tickers(limit: int = 100) -> List[str]:
    df = get_constituents(limit)

    return list(df.Symbol)


def read_constituents() -> List[str]:
    file = open("security_universe.txt", "r")
    stocks = file.read()
    file.close()
    stocks = stocks.split("\n")
    return list(filter(None, stocks))


def write_contituents() -> None:
    stocks = get_tickers(limit=102)
    file = open("security_universe.txt", "w")
    for item in stocks:
        file.write(item + "\n")
    file.close()
