import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.get_data import fetch_data
from utils.parse_csv import load_df_to_sql


def main():

    df = fetch_data("SELECT ticker, date, close FROM ticker_price")
    df_pivot = df.pivot(index="date", columns="ticker", values="close")

    returns = df_pivot.pct_change().dropna()

    cov_matrix = returns.cov()
    cov_matrix_reset = cov_matrix.reset_index()

    cov_matrix_reset.rename(columns={"index": "ticker"}, inplace=True)
    cov_matrix_reset["updated_time"] = datetime.now()
    load_df_to_sql(cov_matrix_reset, "covariance_matrix")


if __name__ == "__main__":
    main()
