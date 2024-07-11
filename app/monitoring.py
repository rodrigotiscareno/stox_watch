import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import altair as alt

from scripts.utility import get_tickers, read_constituents

from app_funcs.query import get_pipeline_all, get_pipeline_start, get_pipeline_fetching, get_pipeline_finish, get_pipeline_error

def print_in_white_block(text, status):
    if status == "START":
        colour = "#5bc0eb"
    elif status == "FETCHING":
        colour = "#fde74c"
    elif status == "FINISH":
        colour = "#9bc53d"
    else:
        colour = "#FF6865"

    block_style = f"""
    <div style="
        background-color: {colour};
        padding: 20px;
        border-radius: 5px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        height: 50px;  /* Adjust the height as needed */
    ">
        <p style="color: black; margin: 0; text-align: left; flex: 1;"><strong>{status}: </strong>{text}</p>
    </div>
    """
    st.markdown(block_style, unsafe_allow_html=True)

def monitoring_page():
    st.title("Monitoring")
    st.write("View pipelines and filter by status")
    
    filter = st.selectbox("Filter by Pipeline Status", ["All", "START", "FETCHING", "FINISH", "ERROR"])

    if filter == "All":     
        df = get_pipeline_all()
        header = "All Pipeline Processes"
    elif filter == "START":
        df = get_pipeline_start()
        header = "START Pipeline Processes"
    elif filter == "FETCHING":
        df = get_pipeline_fetching()
        header = "FETCHING Pipeline Processes"
    elif filter == "FINISH":
        df = get_pipeline_finish()
        header = "FINISH Pipeline Processes"
    else:
        df = get_pipeline_error()
        header = "ERROR Pipeline Processes"



    print(df)
    
    st.subheader(header)

    for index, row in df.iterrows():
        formatted_str = f"{row['process']} pipeline @ {row['date_time']}"
        print_in_white_block(formatted_str, row['pipeline_status'])