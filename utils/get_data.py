import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv


def fetch_data(query):
    load_dotenv()

    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    database = os.getenv("DB_NAME")
    port = "3306"

    connection_string = (
        f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}"
    )

    engine = create_engine(connection_string)

    return pd.read_sql(query, engine)
