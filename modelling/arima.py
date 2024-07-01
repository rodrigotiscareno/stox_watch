from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
import itertools


def main():
    load_dotenv()

    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    port = "3306"

    engine = create_engine(
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{port}/{DB_NAME}"
    )

    query = "SELECT * FROM ticker_price"

    df = pd.read_sql(query, engine)

    price_dataframes = {ticker: df_group for ticker, df_group in df.groupby("ticker")}

    ticker_return_predictions = []
    forecasted_prices_all = []

    for ticker, df in price_dataframes.items():
        df["Date"] = pd.to_datetime(df["Date"])
        df.set_index("Date", inplace=True)

        if not df.index.freq:
            df = df.asfreq("B")

        split_idx = int(len(df) * 0.8)
        train, test = df.iloc[:split_idx], df.iloc[split_idx:]

        train_returns = train["close"].pct_change().dropna()
        test_returns = test["close"].pct_change().dropna()

        p = range(0, 3)
        d = range(0, 2)
        q = range(0, 3)
        pdq = list(itertools.product(p, d, q))

        best_aic = float("inf")
        best_pdq = None

        for param in pdq:
            try:
                model = ARIMA(train_returns, order=param)
                results = model.fit()
                if results.aic < best_aic:
                    best_aic = results.aic
                    best_pdq = param
            except:
                continue

        best_model = ARIMA(train_returns, order=best_pdq)
        fitted_model = best_model.fit()

        forecasted_returns = fitted_model.forecast(steps=len(test_returns))

        rmse = mean_squared_error(test_returns, forecasted_returns, squared=False)

        future_forecasted_returns = fitted_model.forecast(steps=365)

        last_price = df["close"].iloc[-1]
        future_forecasted_prices = (
            last_price * (1 + future_forecasted_returns).cumprod()
        )

        last_date = df.index[-1]
        forecast_dates = pd.date_range(
            start=last_date + pd.Timedelta(days=1),
            periods=len(future_forecasted_prices),
            freq="B",
        )
        future_forecasted_prices.index = forecast_dates

        k_last_known_price = df["close"].iloc[-1]
        last_predicted_price = future_forecasted_prices.iloc[-1]
        return_factor = last_predicted_price / k_last_known_price

        ticker_return_predictions.append(
            {"ticker": ticker, "rmse": rmse, "return_factor": return_factor}
        )

        forecasted_prices_all.append(
            pd.DataFrame(
                {
                    "ticker": ticker,
                    "date": future_forecasted_prices.index,
                    "forecasted_price": future_forecasted_prices.values,
                }
            )
        )

    predictions_df = pd.DataFrame(ticker_return_predictions)
    predictions_df["updated_time"] = datetime.now()

    forecasted_prices_df = pd.concat(forecasted_prices_all)
    forecasted_prices_df["updated_time"] = datetime.now()

    predictions_df.to_sql(
        "ticker_predictions", con=engine, index=False, if_exists="replace"
    )

    forecasted_prices_df.to_sql(
        "ticker_forecasted_prices", con=engine, index=False, if_exists="replace"
    )


if __name__ == "__main__":
    main()
