#!/usr/bin/python3

import psycopg2
from configparser import ConfigParser

def config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        parameters = parser.items(section)
        for parameter in parameters:
            db[parameter[0]]= parameter[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

def connect():
    conn = None
    try:
        parameters = config()

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**parameters)
        print('Connection success')

        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
