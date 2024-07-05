import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

data = {
    "date": pd.date_range(start="2021-01-01", periods=10, freq="D"),
    "price": [10, 12, 15, 14, 13, 16, 18, 19, 17, 20],
}
df = pd.DataFrame(data)


def plot_data(df, stock_num):
    plt.figure(figsize=(10, 6))
    plt.plot(df["date"], df["price"], marker="o", linestyle="-", color="b")
    plt.title(f"Date vs Price for Stock {stock_num}")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(plt)


def portfolio_page(display_recs, display_recs_details):
    st.title("Stocks :)")

    budget = st.number_input("Enter your budget:", value=0, step=50)
    timeline = st.radio("Investment timeline:", ("Short-term", "Long-term"))

    st.button("Submit", on_click=display_recs)

    if st.session_state.display_recommendations:
        st.header("Recommendations:")
        st.write("stock 1:" + " How many to buy " + "at what cost")
        st.write("stock 2:" + " How many to buy " + "at what cost")
        st.write("stock 3:" + " How many to buy " + "at what cost")
        st.write("stock 4:" + " How many to buy " + "at what cost")
        st.write("stock 5:" + " How many to buy " + "at what cost")

        st.button("See more info", on_click=display_recs_details)
        if st.session_state.display_recommendation_details:
            for i in range(1, 6):
                st.header(f"Stock: {i}")
                plot_data(df, i)
                st.write("Current price: ")
                st.write("Projected price: ")
