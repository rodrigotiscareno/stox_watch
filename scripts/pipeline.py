from apscheduler.schedulers.background import BackgroundScheduler
from time import sleep

# import all API call functions here
from eodhd import fetch_and_save_sentiments
from vantage_bal_shts import fetch_and_save_bal_sht
from vantage_cash_flow import fetch_and_save_cash_flow


scheduler = BackgroundScheduler()


def fun1():
    fetch_and_save_sentiments()
    print("From Func1")


def fun2():
    fetch_and_save_bal_sht()
    print("From Func2")


def fun3():
    fetch_and_save_cash_flow()


if __name__ == "__main__":

    # determine times
    # scheduler.add_job(id='Scheduled task 1', func=fun1, trigger='interval', seconds=5)
    # scheduler.add_job(id="Scheduled task 2", func=fun2, trigger="interval", seconds=120)
    # scheduler.add_job(id="Scheduled task 3", func=fun3, trigger="interval", seconds=5)
    scheduler.start()
    while True:
        sleep(1)
