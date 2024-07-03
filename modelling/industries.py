import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.get_data import fetch_data
from utils.parse_csv import load_df_to_sql
import pandas as pd


def main():
    query = "SELECT ticker, sector FROM ticker_information"

    df = fetch_data(query)

    unique_sectors = df["sector"].unique()

    matrix = pd.DataFrame(0, index=df["ticker"].unique(), columns=unique_sectors)

    for _, row in df.iterrows():
        matrix.at[row["ticker"], row["sector"]] = 1

    matrix_reset = matrix.reset_index()
    matrix_reset.rename(columns={"index": "ticker"}, inplace=True)
    matrix_reset.columns = matrix_reset.columns.str.lower()
    matrix_reset.columns = matrix_reset.columns.str.replace(" ", "_")
    load_df_to_sql(matrix_reset, "ticker_industries")


if __name__ == "__main__":
    main()
