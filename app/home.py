import streamlit as st
import pandas as pd
from datetime import datetime

from app_funcs.query import (
    get_rated_volume,
    get_rated_forecast_results,
    get_top_earning_performers,
    get_gainers_n_losers,
)

top_volume_stocks = get_rated_volume()
top_forecast_stocks = get_rated_forecast_results()
top_earning_performers = get_top_earning_performers()


def format_datetime(dt_str):
    dt = datetime.strptime(str(dt_str), "%Y-%m-%d %H:%M:%S")
    return dt.strftime("%B %d, %Y %I:%M %p")


def home_page():
    st.title("Stox Watch")
    st.write("Welcome to Stox Watch. The ultimate trading decision support tool.")

    st.header("Biggest Gainers and Losers 🚀")

    st.header("The Top 5 ⭐️")

    card_style = """
    <style>
        .card {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px;
            margin: 10px;
            border-radius: 10px;
            background-color: #f8f9fa;
            box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
            transition: 0.3s;
        }
        .card:hover {
            box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
        }
        .card-content {
            flex: 1;
        }
        .card-title {
            font-size: 1.25rem;
            font-weight: bold;
        }
        .card-text {
            font-size: 1rem;
            color: #333;
        }
    </style>
    """

    st.markdown(card_style, unsafe_allow_html=True)

    def display_volume_card(stock):
        formatted_datetime = format_datetime(stock["updated_on"])
        st.markdown(
            f"""
            <div class="card">
                <div class="card-content">
                    <div class="card-title">{stock['name']}</div>
                    <div class="card-text"><strong>Volume: </strong>{stock['volume']:,}</div>
                    <div class="card-text"><strong>Price: </strong>${stock['close']:.2f}</div>
                    <div class="card-text"><strong>Last Updated On: </strong>{formatted_datetime}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    def display_forecast_card(stock):
        formatted_datetime = format_datetime(stock["updated_time"])
        st.markdown(
            f"""
            <div class="card">
                <div class="card-content">
                    <div class="card-title">{stock['ticker']}</div>
                    <div class="card-text"><strong>RMSE: </strong>{stock['rmse']}</div>
                    <div class="card-text"><strong>Return Factor: </strong>{stock['return_factor']:.2f}</div>
                    <div class="card-text"><strong>Last Updated On: </strong>{formatted_datetime}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    def display_earning_card(stock):
        st.markdown(
            f"""
            <div class="card">
                <div class="card-content">
                    <div class="card-title">{stock['ticker']}</div>
                    <div class="card-text"><strong>Current Quarter: </strong>{stock['current_quarter']}</div>
                    <div class="card-text"><strong>Previous Quarter: </strong>{stock['previous_quarter']}</div>
                    <div class="card-text"><strong>Earnings Growth Percentage: </strong>{stock['earnings_growth_percentage']:.2f}%</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with st.expander("By Volume"):
        for _, row in top_volume_stocks.iterrows():
            stock = {
                "name": row["ticker"],
                "volume": row["volume"],
                "close": row["close"],
                "updated_on": row["updated_on"],
            }
            display_volume_card(stock)

    with st.expander("Forecasted"):
        st.write("** Based on a 1-year forecast.")
        for _, row in top_forecast_stocks.iterrows():
            stock = {
                "ticker": row["ticker"],
                "rmse": row["rmse"],
                "return_factor": row["return_factor"],
                "updated_time": row["updated_time"],
            }
            display_forecast_card(stock)

    with st.expander("Top Earnings Performers"):
        for _, row in top_earning_performers.iterrows():
            stock = {
                "ticker": row["ticker"],
                "current_quarter": row["current_quarter"],
                "previous_quarter": row["previous_quarter"],
                "earnings_growth_percentage": row["earnings_growth_percentage"],
            }
            display_earning_card(stock)


if __name__ == "__main__":
    home_page()
