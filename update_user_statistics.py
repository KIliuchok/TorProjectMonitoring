#!/usr/bin/python3

import os

from psql_connection import *

file = "userstats-relay-country.csv"

def update_user_data():
    sql = """INSERT INTO "tor-statistics".user_statistics
    (date, country_id, user_estimate, lower_user_estimate, upper_user_estimate, fraction_of_relays_for_estimate) 
    VALUES%s ON CONFLICT DO NOTHING;"""

    connection = connect()

    cursor = connection.cursor()

    with open(file, 'r') as _file:

        i = 0

        while True:
            line = _file.readline()
            if not line:
                break

            if (i < 6):
                i += 1
                continue

            the_list = line.split(',')

            result = []

            print(the_list)

            for item in the_list:
                _item = item.strip()
                if (_item == ''): 
                    result.append(None)
                else:
                    result.append(_item)

            if result[1] == None:
                result[1] = "Total"

            print("Inserting ", result)

            cursor.execute(sql, (tuple(result), ))

        connection.commit()
        cursor.close()
        connection.close()

if __name__ == '__main__':

    string = "wget https://metrics.torproject.org/userstats-relay-country.csv"

    os.system(string)

    update_user_data()

    remove_string = "rm " + file

    os.system(remove_string)