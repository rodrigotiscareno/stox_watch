import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.get_data import fetch_data
import numpy as np
from gurobipy import Model, GRB, quicksum
import pandas as pd
from datetime import datetime
import uuid


M = sys.maxsize

NUM_COMPANIES = 100

query = "SELECT DISTINCT sector FROM ticker_information"
SECTORS = [
    sector.replace(" ", "_").lower() for sector in list(fetch_data(query)["sector"])
]
NUM_PRODUCTS = len(SECTORS)


def get_industry_matrix():

    df = fetch_data("SELECT * FROM ticker_industries ORDER BY ticker")
    df = df[SECTORS]
    assert list(df.columns) == SECTORS
    return df.values.tolist()


def get_covariance():
    query = "SELECT * FROM covariance_matrix"
    df = fetch_data(query)

    df = df.sort_values(by="ticker")

    sorted_columns = sorted(df.columns.drop(["ticker", "updated_time"]))
    df = df[["ticker"] + sorted_columns]

    covar_lists = np.zeros((100, 100))

    for i in range(100):
        for j in range(100):
            covar_lists[i][j] = df.iloc[i, j + 1]

    return covar_lists


def get_tickers():
    query = "SELECT DISTINCT ticker FROM ticker_information ORDER BY ticker"
    return sorted(
        [ticker.replace(" ", "_") for ticker in list(fetch_data(query)["ticker"])]
    )


def get_return_factors():
    query = "SELECT ticker, return_factor FROM ticker_predictions ORDER BY ticker"
    df = fetch_data(query)
    df_sorted = df.sort_values(by="ticker")
    return df_sorted["return_factor"].tolist()


def get_ticker_price():
    query = """
    SELECT tp.ticker, tp.close
    FROM ticker_price tp
    JOIN (
        SELECT ticker, MAX(date) AS latest_date
        FROM ticker_price
        GROUP BY ticker
    ) AS latest_prices
    ON tp.ticker = latest_prices.ticker AND tp.date = latest_prices.latest_date
    ORDER BY tp.ticker;
    """

    df = fetch_data(query)

    return df["close"].tolist()


def main(
    budget: int = 100_000,
    p: float = 0.9,
    lambda_risk_coefficient: float = 0.8,
    unique_companies: int = 10,
    unique_industries: int = 4,
    N: int = 15,
):

    expected_return = get_return_factors()
    price = get_ticker_price()
    product_matrix = get_industry_matrix()
    covariance = get_covariance()

    m = Model("MSCI 436 Investment Portfolio Optimization")

    x = m.addVars(NUM_COMPANIES, lb=0, name="x")
    y = m.addVars(NUM_COMPANIES, vtype=GRB.BINARY, name="y")
    z = m.addVars(NUM_PRODUCTS, vtype=GRB.BINARY, name="z")

    m.addConstr(
        quicksum(price[i] * x[i] for i in range(NUM_COMPANIES)) <= budget, "Budget"
    )
    m.addConstr(quicksum(y[i] for i in range(NUM_COMPANIES)) >= unique_companies)
    for i in range(NUM_COMPANIES):
        m.addConstr(price[i] * x[i] <= p * budget)

    for i in range(NUM_COMPANIES):
        m.addConstr(x[i] >= N * y[i])

    for i in range(NUM_COMPANIES):
        m.addConstr(x[i] <= M * y[i])

    m.addConstr(quicksum(z[j] for j in range(NUM_PRODUCTS)) >= unique_industries)

    for j in range(NUM_PRODUCTS):
        m.addConstr(
            quicksum(y[i] * product_matrix[i][j] for i in range(NUM_COMPANIES)) >= z[j]
        )
        m.addConstr(
            quicksum(y[i] * product_matrix[i][j] for i in range(NUM_COMPANIES))
            <= M * z[j]
        )

    covar_lists = [list(row) for row in covariance]

    covariance_component = lambda_risk_coefficient * quicksum(
        quicksum(x[i] * x[j] * covar_lists[i][j] for j in range(NUM_COMPANIES))
        for i in range(NUM_COMPANIES)
    )

    objective = quicksum(
        expected_return[i] * x[i] * price[i] for i in range(NUM_COMPANIES)
    )
    objective -= covariance_component
    m.setObjective(objective, GRB.MAXIMIZE)

    m.setParam(GRB.Param.FeasibilityTol, 1e-6)
    m.setParam(GRB.Param.IntFeasTol, 1e-9)
    m.optimize()

    if m.status == GRB.OPTIMAL:

        tickers = get_tickers()

        shares_to_buy = []
        total_investment = 0
        total_return = 0
        industries_invested_in = set()

        for i in range(NUM_COMPANIES):
            if x[i].X > 0:
                industries = [
                    SECTORS[j] for j in range(NUM_PRODUCTS) if product_matrix[i][j] == 1
                ]
                shares_to_buy.append(
                    (tickers[i], x[i].X, price[i], expected_return[i], industries)
                )
                total_investment += x[i].X * price[i]
                total_return += expected_return[i] * x[i].X * price[i]
                industries_invested_in.update(industries)

        results_df = pd.DataFrame(
            shares_to_buy,
            columns=["ticker", "shares", "price", "expected_return", "industries"],
        )
        results_df["investment"] = results_df["shares"] * results_df["price"]
        results_df["total_expected_return"] = (
            results_df["shares"] * results_df["price"] * results_df["expected_return"]
        )

        results_df["run_id"] = uuid.uuid4()

        results_df["updated_time"] = datetime.now()

        return results_df

    else:
        print("Optimization was not successful. Status code:", m.status)
        return None


if __name__ == "__main__":
    results_df = main()
    if results_df is not None:
        print(results_df)
