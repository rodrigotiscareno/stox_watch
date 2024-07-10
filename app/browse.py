import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import altair as alt

from scripts.utility import get_tickers

from app_funcs.query import (
    get_forecasted_ticker_price,
    get_sentiment,
    get_ticker_info
    )

def display_info_card(info):
    st.markdown(
        f"""
        <div class="card">
            <div class="card-content">
                <div class="card-title"><strong>{info['name']}</strong></div>
                <div class="card-text"><strong>Industry: </strong>{info['industry']}</div>
                <div class="card-text"><strong>Address: </strong>{info['address']}</div>
                <div class="card-text"><strong>Country: </strong>{info['country']}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def browse_page():
    st.title("Browse Stocks")
    
    tickers = get_tickers()
    selected_ticker = st.selectbox('Select a stock', tickers)
    info_df = get_ticker_info(selected_ticker)
    
    st.markdown("")     

    st.header("Information")
    info = {
                "name": info_df["ticker"].to_string()[2:],
                "address": info_df["address1"].to_string()[2:],
                "country": info_df["country"].to_string()[2:],
                "industry": info_df["industry"].to_string()[2:],
            }
    display_info_card(info)
    
    st.markdown("")     

    st.header("Price Forecast")

    forecasted_price_df = get_forecasted_ticker_price(selected_ticker)
    forecast_chart = (
        alt.Chart(forecasted_price_df)
        .mark_line()
        .encode(
            x=alt.X("date:T", title="Date"),
            y=alt.Y("forecasted_price:Q", title="Forecasted Price"),
        )
        .properties(width=800, height=300, title=f"Forecasted Price for {selected_ticker}")
    )
    st.altair_chart(forecast_chart, use_container_width=True)

    
    st.markdown("")   
      
    st.header("Sentiment Heatmap")
    
    sentiment_df = get_sentiment(selected_ticker)
    sentiment_df['time_published'] = pd.to_datetime(sentiment_df['time_published'])
    sentiment_df['month_day'] = sentiment_df['time_published'].dt.strftime('%Y-%b-%d')  
    chart = alt.Chart(sentiment_df).mark_rect().encode(
        x=alt.X('hours(time_published):O', title='Hour of Day'),
        y=alt.Y('month_day:O', title='Date'),
        color=alt.Color('mean(sentiment):Q', scale=alt.Scale(scheme='redyellowgreen'), title='Sentiment Score'),
        tooltip=['month_day', 'hours(time_published)', 'sentiment']
    ).properties(
        width=800,
        height=400,
        title=f"Sentiment Heatmap for {selected_ticker}"
    )
    st.altair_chart(chart, use_container_width=True)