from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from statsmodels.tsa.arima.model import ARIMA
import itertools


def forecast_stock(df, forecast_steps, historical_length):
    df = df.iloc[-historical_length:]
    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", inplace=True)

    if not df.index.freq:
        df = df.asfreq("B")

    train_returns = df["close"].pct_change().dropna()
    best_aic = float("inf")
    best_pdq = None
    p = range(0, 3)
    d = range(0, 2)
    q = range(0, 3)
    pdq = list(itertools.product(p, d, q))

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
    forecasted_returns = fitted_model.forecast(steps=forecast_steps)

    last_price = df["close"].iloc[-1]
    future_forecasted_prices = last_price * (1 + forecasted_returns).cumprod()

    last_predicted_price = future_forecasted_prices.iloc[-1]
    return_factor = last_predicted_price / last_price

    return future_forecasted_prices, return_factor


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

    forecast_durations = {
        "short_term": (5, 30),
        "medium_term": (130, 180),
        "long_term": (252, 365),
    }
    forecasted_results = []

    for ticker, df in price_dataframes.items():
        for forecast_type, (days_forecast, days_history) in forecast_durations.items():
            forecast_prices, return_factor = forecast_stock(
                df, days_forecast, days_history
            )
            for date, price in forecast_prices.items():
                forecasted_results.append(
                    {
                        "ticker": ticker,
                        "date": date,
                        "forecasted_price": price,
                        "return_factor": return_factor,
                        "forecast_type": forecast_type,
                    }
                )

    forecasted_prices_df = pd.DataFrame(forecasted_results)
    forecasted_prices_df["updated_time"] = datetime.now()

    forecasted_prices_df.to_sql(
        "ticker_forecasted_prices", con=engine, index=False, if_exists="replace"
    )


if __name__ == "__main__":
    main()
