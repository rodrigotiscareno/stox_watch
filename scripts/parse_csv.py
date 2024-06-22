import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()


def load_csv_to_sql(csv_file_path, table_name):
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    database = os.getenv("DB_NAME")
    port = "3306"

    engine = create_engine(
        f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
    )

    data = pd.read_csv(csv_file_path)
    data.to_sql(table_name, con=engine, index=False, if_exists="replace")


load_csv_to_sql("prices.csv", "ticker_price")
