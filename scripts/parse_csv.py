import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()


def load_csv_to_sql(csv_file_path, table_name, mode="replace"):
    """
    Load data from a CSV file to a SQL table.

    Parameters:
    csv_file_path (str): Path to the CSV file.
    table_name (str): Name of the SQL table.
    mode (str): Valid options are:
                'replace' - Drop the table before inserting new values.
                'append' - Insert new values into the existing table.
                'fail' - Raise a ValueError if the table already exists.
    """
    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    database = os.getenv("DB_NAME")
    port = "3306"

    engine = create_engine(
        f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
    )

    data = pd.read_csv(csv_file_path)
    data.to_sql(table_name, con=engine, index=False, if_exists=mode)


load_csv_to_sql("summary_detail.csv", "summary_detail", mode="replace")
