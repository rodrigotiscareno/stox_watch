import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamlit_option_menu import option_menu

# Graphing stuff -------------------------------------------------------
# Sample data (to be replaced with stock data)
data = {
    "date": pd.date_range(start="2021-01-01", periods=10, freq="D"),
    "price": [10, 12, 15, 14, 13, 16, 18, 19, 17, 20],
}
df = pd.DataFrame(data)


# Function to plot data
def plot_data(df, stock_num):
    plt.figure(figsize=(10, 6))
    plt.plot(df["date"], df["price"], marker="o", linestyle="-", color="b")
    plt.title(f"Date vs Price for Stock {stock_num}")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(plt)


# CSS Formatting stuff -------------------------------------------------------
# Function to load CSS file
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Load the CSS file
local_css("style.css")

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Button stuff -------------------------------------------------------
# Initialize session state
if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False

if "button_clicked2" not in st.session_state:
    st.session_state.button_clicked2 = False


# Function to handle button click
def display_recs():
    st.session_state.button_clicked = True


def display_recs_details():
    st.session_state.button_clicked2 = True


# Pages stuff -------------------------------------------------------
# Define pages
def home_page():
    st.title("Home")
    st.write(
        "Welcome to _____. A tool that allows you to gain insights into the market and customize predictions to suit your needs. Navigate to portolio to get started."
    )
    st.header("Top 5 Today")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("By Volume")
        top_volume_stocks = ["Stock 1A", "Stock 1B", "Stock 1C", "Stock 1D", "Stock 1E"]
        volume_info = [5, 10, 15, 20, 25]  # Input the volume numbers for each stock
        for stock, info in zip(top_volume_stocks, volume_info):
            st.write(stock)
            st.write(f"  - Volume: {info}")

    with col2:
        st.subheader("Forecasted")
        top_forecasted_stocks = [
            "Stock 2A",
            "Stock 2B",
            "Stock 2C",
            "Stock 2D",
            "Stock 2E",
        ]
        forecasted_today = [1, 2, 3, 4, 5]  # Input the current price of the stock
        forecasted_tomorrow = [
            2,
            3,
            4,
            5,
            6,
        ]  # Input the forecasted price for the stock
        for stock, today, tomorrow in zip(
            top_forecasted_stocks, forecasted_today, forecasted_tomorrow
        ):
            st.write(stock)
            st.write(f"  - Today: ${today}")
            st.write(f"  - Tomorrow: ${tomorrow}")

    with col3:
        st.subheader("Top Gainers")
        top_gainers_stocks = [
            "Stock 3A",
            "Stock 3B",
            "Stock 3C",
            "Stock 3D",
            "Stock 3E",
        ]
        percent_climb = [
            10,
            20,
            30,
            40,
            50,
        ]  # Input the percentage climb for each stock
        for stock, climb in zip(top_gainers_stocks, percent_climb):
            st.write(stock)
            st.write(f"  - Percent: {climb}%")


def portfolio_page():
    st.title("Stocks :)")

    budget = st.number_input("Enter your budget:", value=0, step=50)
    timeline = st.radio("Investment timeline:", ("Short-term", "Long-term"))

    # set up button
    st.button("Submit", on_click=display_recs)
    # Display text if button is clicked
    if st.session_state.button_clicked:
        st.header("Recommendations:")
        st.write("stock 1:" + " How many to buy " + "at what cost")
        st.write("stock 2:" + " How many to buy " + "at what cost")
        st.write("stock 3:" + " How many to buy " + "at what cost")
        st.write("stock 4:" + " How many to buy " + "at what cost")
        st.write("stock 5:" + " How many to buy " + "at what cost")

        st.button("See more info", on_click=display_recs_details)
        if st.session_state.button_clicked2:
            for i in range(1, 6):
                st.header(f"Stock: {i}")
                plot_data(df, i)
                st.write("Current price: ")
                st.write("Projected price: ")


# Old pages, distributed the functionality to other pages
# def about_page():
#     st.title("About")
#     st.write("We will go in depth into your recommendations on this page")

#     for i in range(1, 6):
#         st.header(f"Stock: {i}")
#         plot_data(df, i)
#         st.write ("Current price: ")
#         st.write ("Projected price: ")

# def top_stocks():
#     st.title("Top Stocks")
#     st.write("Maybe just display top 5 or something?")


# Sidebar menu ------------------------------------------------------
with st.sidebar:
    selected = option_menu(
        menu_title="Navigate",
        options=["Home", "Portfolio"],
    )

    if selected == "Home":
        st.session_state.page = "Home"
    elif selected == "Portfolio":
        st.session_state.page = "Portfolio"

# Display the selected page
if st.session_state.page == "Home":
    home_page()
elif st.session_state.page == "Portfolio":
    portfolio_page()

# # Run the app
# if __name__ == '__main__':
#     st.write('Running Streamlit app...')
