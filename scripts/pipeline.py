from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor

import time

from vantage_bal_shts import fetch_and_save_bal_sht
from vantage_cash_flow import fetch_and_save_cash_flow
from vantage_inc_stmts import fetch_and_save_income_statements
from vantage_top_glm import fetch_and_save_top_glm

from eodhd import fetch_and_save_sentiments

from yahoo_insider_purchases import main as fetch_and_save_insider_purchases
from yahoo_prices import main as fetch_and_save_ticker_prices
from yahoo_recommendations import main as fetch_and_save_recommendations

from yquery_earnings_trends import main as fetch_and_save_earnings_trends
from yquery_earnings import main as fetch_and_save_earnings
from yquery_financial_data import main as fetch_and_save_financial_data
from yquery_key_stats import main as fetch_and_save_key_stats
from yquery_summary_detail import main as fetch_and_save_summary_detail


from datetime import datetime


executors = {"default": ThreadPoolExecutor(10)}

job_defaults = {"max_instances": 5}

scheduler = BackgroundScheduler(executors=executors, job_defaults=job_defaults)


def balance_sheets():
    fetch_and_save_bal_sht()


def sentiments():
    fetch_and_save_sentiments()


def cash_flow():
    fetch_and_save_cash_flow()


def income_statements():
    fetch_and_save_income_statements()


def top_n_stats():
    fetch_and_save_top_glm()


def insider_purchases():
    fetch_and_save_insider_purchases()


def ticker_prices():
    fetch_and_save_ticker_prices()


def recs():
    fetch_and_save_recommendations()


def earnings_trends():
    fetch_and_save_earnings_trends()


def earnings():
    fetch_and_save_earnings()


def financial_data():
    fetch_and_save_financial_data()


def key_stats():
    fetch_and_save_key_stats()


def summary_detail():
    fetch_and_save_summary_detail()


if __name__ == "__main__":

    scheduler.add_job(ticker_prices, "cron", hour=4, minute=30)

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
