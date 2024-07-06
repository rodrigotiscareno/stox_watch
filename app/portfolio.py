import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

data = {
    "date": pd.date_range(start="2021-01-01", periods=10, freq="D"),
    "price": [10, 12, 15, 14, 13, 16, 18, 19, 17, 20],
}
df = pd.DataFrame(data)


def display_recs():
    st.session_state.display_recommendations = True


def display_recs_details():
    st.session_state.display_recommendation_details = True


def plot_data(df, stock_num):
    plt.figure(figsize=(10, 6))
    plt.plot(df["date"], df["price"], marker="o", linestyle="-", color="b")
    plt.title(f"Date vs Price for Stock {stock_num}")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(plt)


def portfolio_page():
    st.title("Stock Portfolio Recommendations")

    budget = st.number_input(
        "Enter your budget:", min_value=50000, step=1000, format="%d"
    )
    risk = st.slider(
        "Choose your risk level (1 = Low Risk, 10 = High Risk):",
        min_value=1,
        max_value=10,
    )
    timeline = st.select_slider(
        "Select your investment timeline:",
        options=["Short-term", "Medium-term", "Long-term"],
    )
    max_investment = st.slider(
        "Maximum % of budget into one stock:",
        min_value=0.0,
        max_value=1.0,
        step=0.05,
        format="%.2f",
    )
    diversification = st.radio(
        "Level of diversification (1 = Low, 3 = High):", (1, 2, 3)
    )

    st.button("Submit", on_click=display_recs)

    if st.session_state.display_recommendations:
        st.header("Recommendations:")
        for i in range(1, 6):  # Assuming 5 stock recommendations
            st.subheader(f"Stock {i}:")
            st.write("How many to buy: XYZ")  # Placeholder for actual calculation
            st.write("At what cost: XYZ")  # Placeholder for actual calculation

        st.button("See more info", on_click=display_recs_details)
        if st.session_state.display_recommendation_details:
            for i in range(1, 6):
                st.header(f"Stock: {i}")
                plot_data(df, i)
                st.write("Current price: XYZ")  # Placeholder
                st.write("Projected price: XYZ")  # Placeholder
