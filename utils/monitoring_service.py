import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine


#4 Types of Logging
# 1: pipeline start
# 2: pipeline in process (fetching data)
# 3: pipeline finish (writing data)
# 4: error

def log_monitor_to_sql(process_text, status):
    load_dotenv()

    username = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    database = os.getenv("DB_NAME")
    port = "3306"

    engine = create_engine(
        f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
    )

    data = {
        'date_time': [datetime.now()],
        'process': [process_text],
        'pipeline_status': [status]
    }
    
    df = pd.DataFrame(data)
    df.to_sql("monitoring", con=engine, index=False, if_exists="append")

    
def main(process_text, status):
   log_monitor_to_sql(process_text, status)

if __name__ == "__main__":
    process_text = "TEST"
    status = "TEST"
    main(process_text, status)


