import time
import os
import schedule

from update_user_statistics import *

def update_user_stats():
    string = "wget https://metrics.torproject.org/userstats-relay-country.csv"

    os.system(string)

    update_user_data()

    remove_string = "rm " + file

    os.system(remove_string)

def onionperf_data():
    string = "python3 batch.py"

schedule.every().day.at("02:00").do(update_user_stats)
schedule.every().day.at("02:30").do(onionperf_data)

print("Scheduler Running")

while True:
    schedule.run_pending()
    time.sleep(60)