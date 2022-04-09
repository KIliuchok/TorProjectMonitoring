#!/usr/bin/python3

# Written By Kostiantyn Iliuchok

from numpy import mean
from psql_connection import *
from json_helper import *
import argparse
import sys

def insert_onionperf_data(file):

    sql = """INSERT INTO "tor-statistics".onionperf_data 
    (id, label, filesize_bytes, error_code, server, time_to_first_byte, time_to_last_byte, mbps, start, origin_server) 
    VALUES%s ON CONFLICT DO NOTHING;"""

    server_origin = file.split(".")[0]

    connection = connect()

    cursor = connection.cursor()

    print("here ")

    with open(file, 'r') as _file:

        count = 0

        while True:
            line = _file.readline()
            if count == 0:
                count += 1
                continue

            if not line:
                break

            the_list = line.split(',')

            result = []

            for item in the_list:
                _item = item.strip()
                if (_item == ''): 
                    result.append(None)
                else:
                    result.append(_item)
                

            result.append(server_origin)     

            cursor.execute(sql, (tuple(result), ))

        connection.commit()
        cursor.close()
        connection.close()

def update_user_data(file):
    sql = """INSERT INTO "tor-statistics"."user_statistics"
    (date, country_id, user_estimate, lower_user_estimate, upper_user_estimate, fraction_of_relays_for_estimate) 
    VALUES%s ON CONFLICT DO NOTHING;"""

    connection = connect()

    cursor = connection.cursor()

    sql_execution(file, sql, 0, "Total")


def update_relay_and_bridges(file, file2, file3, file4, file5):

    sql1 = """INSERT INTO "tor-statistics"."relays_and_bridges"
    (date, avg_relays, avg_bridges) VALUES%s ON CONFLICT (date) DO NOTHING
    """

    sql2 = """INSERT INTO "tor-statistics"."relays_and_bridges"
    (date, version, relays_number_for_version) VALUES%s ON CONFLICT (date) DO UPDATE
    SET version = EXCLUDED.version,
    relays_number_for_version = EXCLUDED.relays_number_for_version;
    """

    sql3 = """INSERT INTO "tor-statistics"."relays_and_bridges"
    (date, bsd, linux, macos, other, windows) VALUES%s ON CONFLICT (date) DO UPDATE
    SET bsd = EXCLUDED.bsd, 
    linux = EXCLUDED.linux,
    macos = EXCLUDED.macos, 
    other = EXCLUDED.other,
    windows = EXCLUDED.windows;
    """

    sql4 = """INSERT INTO "tor-statistics"."relays_and_bridges"
    (date, announced_ipv6_relays, reachable_ipv6_relays, exiting_ipv6_relays) VALUES%s ON CONFLICT (date) DO UPDATE
    SET announced_ipv6_relays = EXCLUDED.announced_ipv6_relays, 
    reachable_ipv6_relays = EXCLUDED.reachable_ipv6_relays,
    exiting_ipv6_relays = EXCLUDED.exiting_ipv6_relays;
    """

    sql5 = """INSERT INTO "tor-statistics"."relays_and_bridges"
    (date, announced_ipv6_bridges) VALUES%s ON CONFLICT (date) DO UPDATE
    SET announced_ipv6_bridges = EXCLUDED.announced_ipv6_bridges;
    """


    sql_execution(file, sql1, 6)

    sql_execution(file2, sql2, 6)

    sql_execution(file3, sql3, 6)

    sql_execution(file4, sql4, 6, ignore_field=1)

    sql_execution(file5, sql5, 6, ignore_field=1)

def add_onionperf_daily(file):

    server_origin = file.split(".")[1]

    try:
        extracted_build_times = json_extract_from_file(file, "buildtime_seconds")
        mean_build_time = mean(extracted_build_times)

        extracted_error_number = json_extract_from_file(file, "is_success")

        number_of_measurements = len(extracted_error_number)

        suc = 0
        err = 0

        for item in extracted_error_number:
            if (item == "true"):
                suc += 1
            else:
                err += 1

        result = []
        result.append(file.split('.')[0])
        result.append(mean_build_time)
        result.append(number_of_measurements)
        result.append(err)
        result.append(server_origin)


        sql = """INSERT INTO "tor-statistics"."onionperf_daily_additional" (date, circuit_build_time, number_of_measurements, number_of_failures, server_origin)
        VALUES%s ON CONFLICT (date) DO NOTHING;
        """

        conn = connect()
        cur = conn.cursor()
        cur.execute(sql, (tuple(result),))
        conn.commit()
        cur.close()
        conn.close()
    except:
        print(file + " not found")
    

            

def sql_execution(file, sql_query, ignore_lines, replace_empty=None, ignore_field=None):
    connection = connect()
    cursor = connection.cursor()

    with open(file, 'r') as _file:
        count = 0
        while True:

            line = _file.readline()

            if (count < ignore_lines):
                count+=1
                continue

            print(count)

            print(line)

            if not line:
                break

            split = line.split(',')
            result = []
            if ignore_field != None:
                split.remove(split[ignore_field])
            for item in split:
                _item = item.strip()
                if (_item == ''):
                    result.append(replace_empty)
                else:
                    result.append(_item)

            #print("Inserting ", tuple(result))   

            cursor.execute(sql_query, (tuple(result),))
    connection.commit()
    cursor.close()
    connection.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--action', type=str, required=True)
    parser.add_argument('--file', type=str, required=True)
    parser.add_argument('--file2', type=str, required=False)
    parser.add_argument('--file3', type=str, required=False)
    parser.add_argument('--file4', type=str, required=False)
    parser.add_argument('--file5', type=str, required=False)


    args = parser.parse_args()

    if (args.action == "UserData"):
        update_user_data(args.file)
    
    if (args.action == "Onionperf"):
        insert_onionperf_data(args.file)

    if (args.action == "RelayAndBridgeInfo"):
        update_relay_and_bridges(args.file, args.file2, args.file3, args.file4, args.file5)

    if (args.action == "OnionPerfDaily"):
        add_onionperf_daily(args.file)