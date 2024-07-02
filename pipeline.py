from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor

import time

from scripts.vantage_bal_shts import fetch_and_save_bal_sht
from scripts.vantage_cash_flow import fetch_and_save_cash_flow
from scripts.vantage_inc_stmts import fetch_and_save_income_statements
from scripts.vantage_top_glm import fetch_and_save_top_glm

from scripts.eodhd import fetch_and_save_sentiments

from scripts.yahoo_insider_purchases import main as fetch_and_save_insider_purchases
from scripts.yahoo_prices import main as fetch_and_save_ticker_prices
from scripts.yahoo_recommendations import main as fetch_and_save_recommendations

from scripts.yquery_earnings_trends import main as fetch_and_save_earnings_trends
from scripts.yquery_earnings import main as fetch_and_save_earnings
from scripts.yquery_financial_data import main as fetch_and_save_financial_data
from scripts.yquery_key_stats import main as fetch_and_save_key_stats
from scripts.yquery_summary_detail import main as fetch_and_save_summary_detail

from modelling.arima import main as forecast_prices

from send_email import main as notification


def email_notifier(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            notification(
                subject=f"Task {func.__name__} completed",
                sentences=f"The task {func.__name__} has been completed successfully.",
            )
            return result
        except Exception as e:
            notification(
                subject=f"Task {func.__name__} failed",
                sentences=f"The task {func.__name__} failed with error: {e}",
            )
            raise

    return wrapper


executors = {"default": ThreadPoolExecutor(10)}

job_defaults = {"max_instances": 5}

scheduler = BackgroundScheduler(executors=executors, job_defaults=job_defaults)


@email_notifier
def balance_sheets():
    fetch_and_save_bal_sht()


@email_notifier
def sentiments():
    fetch_and_save_sentiments()


@email_notifier
def cash_flow():
    fetch_and_save_cash_flow()


@email_notifier
def income_statements():
    fetch_and_save_income_statements()


@email_notifier
def top_n_stats():
    fetch_and_save_top_glm()


@email_notifier
def insider_purchases():
    fetch_and_save_insider_purchases()


@email_notifier
def ticker_prices():
    fetch_and_save_ticker_prices()


@email_notifier
def recs():
    fetch_and_save_recommendations()


@email_notifier
def earnings_trends():
    fetch_and_save_earnings_trends()


@email_notifier
def earnings():
    fetch_and_save_earnings()


@email_notifier
def financial_data():
    fetch_and_save_financial_data()


@email_notifier
def key_stats():
    fetch_and_save_key_stats()


@email_notifier
def summary_detail():
    fetch_and_save_summary_detail()


@email_notifier
def price_forecast():
    forecast_prices()


if __name__ == "__main__":

    scheduler.add_job(ticker_prices, "cron", hour=17, minute=17)
    scheduler.add_job(price_forecast, "cron", hour=5, minute=0)

    scheduler.add_job(financial_data, "cron", hour=7, minute=0)
    scheduler.add_job(sentiments, "cron", hour=7, minute=10)
    scheduler.add_job(summary_detail, "cron", hour=7, minute=20)
    scheduler.add_job(recs, "cron", hour=7, minute=30)
    scheduler.add_job(top_n_stats, "cron", hour=7, minute=40)
    scheduler.add_job(insider_purchases, "cron", hour=7, minute=50)
    scheduler.add_job(income_statements, "cron", hour=8, minute=0)
    scheduler.add_job(earnings_trends, "cron", hour=8, minute=10)
    scheduler.add_job(earnings, "cron", hour=8, minute=20)
    scheduler.add_job(balance_sheets, "cron", hour=8, minute=30)
    scheduler.add_job(key_stats, "cron", hour=8, minute=40)
    scheduler.add_job(cash_flow, "cron", hour=8, minute=50)

    scheduler.start()
    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
