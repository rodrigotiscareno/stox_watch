import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os


def connect():
    load_dotenv()
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    port = "3306"

    engine = create_engine(
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{port}/{DB_NAME}"
    )
    return engine


def get_rated_volume(limit=5):
    engine = connect()
    query = f"""
    SELECT * 
    FROM ticker_price
    WHERE `Date`  IN (SELECT MAX(`Date`) FROM ticker_price GROUP BY ticker)
    ORDER BY volume DESC
    LIMIT {limit};
    """
    return pd.read_sql(query, engine)


def get_rated_forecast_results(limit=5):
    engine = connect()
    query = f"""
    SELECT *
    FROM ticker_forecasted_prices tfp 
    GROUP BY ticker
    ORDER BY return_factor DESC
    LIMIT {limit};
    """
    return pd.read_sql(query, engine)


def get_volume_per_day(limit=21):
    engine = connect()

    query = f"""SELECT 
        Date, 
        SUM(volume) AS total_volume
    FROM 
        (SELECT DISTINCT 
            Date, 
            open, 
            high, 
            low, 
            close, 
            volume, 
            dividends, 
            stock_splits, 
            ticker, 
            updated_on 
        FROM 
            ticker_price
        ) AS distinct_ticker_price
    GROUP BY 
        Date
    ORDER BY Date DESC
    LIMIT {limit}"""
    return pd.read_sql(query, engine)


def get_gainers_n_losers(category, order_by, limit=5):
    engine = connect()
    query = f"""
    SELECT *
    FROM top_glm tg 
    WHERE category = '{category}'
    ORDER BY {order_by} DESC
    LIMIT {limit}
    """
    return pd.read_sql(query, engine)


def get_top_earning_performers(limit=5):
    engine = connect()
    quarters = ("1Q2024", "2Q2024")
    query = text(
        """
    WITH quarters AS (
        SELECT
            ticker,
            date,
            year,
            earnings,
            CASE
                WHEN date LIKE '1Q%' THEN 1
                WHEN date LIKE '2Q%' THEN 2
                WHEN date LIKE '3Q%' THEN 3
                WHEN date LIKE '4Q%' THEN 4
            END AS quarter_number
        FROM earnings
    ),
    growth_calculation AS (
        SELECT
            current.ticker,
            current.date AS current_quarter,
            previous.date AS previous_quarter,
            ((current.earnings - previous.earnings) / previous.earnings) * 100 AS earnings_growth_percentage
        FROM 
            quarters current
        JOIN 
            quarters previous 
        ON 
            current.ticker = previous.ticker
            AND (
                (current.year = previous.year AND current.quarter_number = previous.quarter_number + 1)
                OR (current.year = previous.year + 1 AND current.quarter_number = 1 AND previous.quarter_number = 4)
            )
    ),
    ranked_growth AS (
        SELECT
            ticker,
            current_quarter,
            previous_quarter,
            earnings_growth_percentage,
            ROW_NUMBER() OVER (PARTITION BY ticker ORDER BY earnings_growth_percentage DESC) AS rn
        FROM 
            growth_calculation
    ),
    top_growth AS (
        SELECT
            ticker,
            current_quarter,
            previous_quarter,
            earnings_growth_percentage
        FROM 
            ranked_growth
        WHERE rn = 1
    )
    SELECT 
        ticker,
        current_quarter,
        previous_quarter,
        earnings_growth_percentage
    FROM 
        top_growth
    WHERE current_quarter IN :quarters
    ORDER BY 
        earnings_growth_percentage DESC
    LIMIT :limit;
    """
    )
    params = {"quarters": quarters, "limit": limit}
    return pd.read_sql(query, engine, params=params)


def get_forecasted_ticker_price(ticker):
    engine = connect()
    query = f"""
    SELECT *
    FROM ticker_forecasted_prices
    WHERE ticker = '{ticker}'
    AND forecast_type='short_term'
    ORDER BY `date`
    LIMIT 100;
    """
    return pd.read_sql(query, engine)


def get_sentiment(ticker):
    engine = connect()
    query = f"""
    SELECT ticker, sentiment, time_published
    FROM sentiment
    WHERE ticker = '{ticker}'
    ORDER BY time_published DESC;
    """
    return pd.read_sql(query, engine)


def get_recent_sentiment(ticker):
    engine = connect()
    query = f"""
    SELECT ticker, sentiment
    FROM sentiment
    WHERE ticker = '{ticker}'
    ORDER BY time_published DESC
    LIMIT 1;
    """
    return pd.read_sql(query, engine)


def get_ticker_info(ticker):
    engine = connect()
    query = f"""
    SELECT ticker, address1 ,city, country, website, industry
    FROM ticker_information
    WHERE ticker = '{ticker}';
    """
    return pd.read_sql(query, engine)


def get_pipeline_all():
    engine = connect()
    query = f"""
    SELECT *
    FROM monitoring
    WHERE date_time >= DATE_SUB(NOW(), INTERVAL 2 DAY)
    ORDER BY date_time DESC;
    """
    return pd.read_sql(query, engine)


def get_pipeline_start():
    engine = connect()
    query = f"""
    SELECT *
    FROM monitoring
    WHERE date_time >= DATE_SUB(NOW(), INTERVAL 2 DAY)
    AND pipeline_status = 'START'
    ORDER BY date_time DESC;
    """
    return pd.read_sql(query, engine)


def get_pipeline_fetching():
    engine = connect()
    query = f"""
    SELECT *
    FROM monitoring
    WHERE date_time >= DATE_SUB(NOW(), INTERVAL 2 DAY)
    AND pipeline_status = 'FETCHING'
    ORDER BY date_time DESC;
    """
    return pd.read_sql(query, engine)


def get_pipeline_finish():
    engine = connect()
    query = f"""
    SELECT *
    FROM monitoring
    WHERE date_time >= DATE_SUB(NOW(), INTERVAL 2 DAY)
    AND pipeline_status = 'FINISH'
    ORDER BY date_time DESC;
    """
    return pd.read_sql(query, engine)


def get_pipeline_error():
    engine = connect()
    query = f"""
    SELECT *
    FROM monitoring
    WHERE date_time >= DATE_SUB(NOW(), INTERVAL 2 DAY)
    AND pipeline_status = 'ERROR'
    ORDER BY date_time DESC;
    """
    return pd.read_sql(query, engine)


def get_recs_aggregated(ticker):
    engine = connect()
    query = f"""
    SELECT ticker, tograde, COUNT(*) AS count
    FROM recs
    GROUP BY ticker, tograde
    HAVING ticker= '{ticker}'
    """
    return pd.read_sql(query, engine)
