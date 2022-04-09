
import datetime
import os
from db_operations import *

### Updating the OnionPerf Data for the last 3 days

def date_to_string(date_object):
    if date_object is not None:
        return "{:04d}-{:02d}-{:02d}.".format(date_object.year, date_object.month, date_object.day)
    else:
        return ""

ending = "onionperf.analysis.json.xz"
ending2 = "onionperf.analysis.json"
start = "https://collector.torproject.org/recent/onionperf/"

current_day = datetime.datetime.utcnow()
yesterday = current_day - datetime.timedelta(days=1)
yesterday = yesterday.date()

servers = ['op-us6.', 'op-nl6.', 'op-hk6a.', 'op-hk6.', 'op-de6a.']

i = 0
while (i < 3):
    for item in servers:
        _date = date_to_string(yesterday)
        string = "wget " + start + _date + item + ending

        os.system(string)
    yesterday = yesterday - datetime.timedelta(days=1)
    i += 1


current_day = datetime.datetime.utcnow()
yesterday = current_day - datetime.timedelta(days=1)
yesterday = yesterday.date()

i = 0
while (i < 3):
    for item in servers:
        _date = date_to_string(yesterday)
        string = "unxz " + _date + item + ending

        os.system(string)

    yesterday = yesterday - datetime.timedelta(days=1)
    i += 1

current_day = datetime.datetime.utcnow()
yesterday = current_day - datetime.timedelta(days=1)
yesterday = yesterday.date()


i = 0
while (i < 3):
    for item in servers:
        _date = date_to_string(yesterday)
        string = _date + item + ending2

        add_onionperf_daily(string)

        try:

            string1 = "onionperf visualize --data " + string + " data"

            os.system(string1) 

            visualize = "onionperf.viz.csv"

            insert_onionperf_data(visualize)

            remove2 = "rm onionperf.viz.csv"
            remove3 = "rm onionperf.viz.pdf"

            os.system(remove2)
            os.system(remove3)
        
        except:
            print("error occured")

    yesterday = yesterday - datetime.timedelta(days=1)
    i += 1
    
current_day = datetime.datetime.utcnow()
yesterday = current_day - datetime.timedelta(days=1)
yesterday = yesterday.date()

i = 0
while (i < 3):
    for item in servers:
        _date = date_to_string(yesterday)
        string = "rm " + _date + item + ending2
        
        

        os.system(string)

    yesterday = yesterday - datetime.timedelta(days=1)
    i += 1

