import sqlite3
from sqlite3 import Error
import yfinance
import pandas as pd
from datetime import datetime
import os
import dotenv
import json
from urllib.request import urlopen

# What? You thought I would just hardcode the API Key?
dotenv.load_dotenv()
API = str(os.getenv("FMP_API"))

# Many thanks to sqlitetutorial.net

# Define database

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_db():
    database = r"D:\\github\\python\\burryedge\\flowbot-master\\data\\ruthcalls.db"

    sql_create_callers_table = """ CREATE TABLE IF NOT EXISTS callers (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        begin_date text,
                                        target_date text
                                    ); """

    sql_create_thesis_table = """CREATE TABLE IF NOT EXISTS thesis (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    ticker text NOT NULL,
                                    target integer NOT NULL,
                                    direction integer NOT NULL,
                                    why text NOT NULL,
                                    percent_wager integer NOT NULL,
                                    status_id integer NOT NULL,
                                    call_id integer NOT NULL,
                                    begin_date text NOT NULL,
                                    target_date text NOT NULL,
                                    FOREIGN KEY (call_id) REFERENCES callers (id)
                                );"""

    sql_create_points_table = """CREATE TABLE IF NOT EXISTS points (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    points integer NOT NULL,
                                    call_id integer NOT NULL,
                                    FOREIGN KEY (call_id) REFERENCES callers (id)
                                );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create callers table
        create_table(conn, sql_create_callers_table)

        # create thesis table
        create_table(conn, sql_create_thesis_table)

        #create points table
        create_table(conn, sql_create_points_table)
    else:
        print("Error! cannot create the database connection.")


def add_caller(conn, caller):
    """
    Create a new caller into the callers table
    :param conn:
    :param caller:
    :return: caller id
    """
    sql = ''' INSERT INTO callers(name,begin_date,target_date)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, caller)
    conn.commit()
    return cur.lastrowid

def create_thesis(conn, thesis):
    """
    Create a new thesis
    :param conn:
    :param thesis:
    :return:
    """

    sql = ''' INSERT INTO thesis(name,ticker,target,direction,why,percent_wager,status_id,call_id,begin_date,target_date)
              VALUES(?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, thesis)
    conn.commit()

    return cur.lastrowid

def first_points(conn, score):
    """
    Add points
    :param conn:
    :param score:
    :return:
    """

    sql = ''' INSERT INTO points(name,points,call_id)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, score)
    conn.commit()

    return cur.lastrowid

def update_points(conn, points):
    """
    update points for a caller
    :param conn:
    :param points:
    :return: caller id
    """
    sql = ''' UPDATE points
              SET points = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, points)
    conn.commit()

def query_all_players(conn):
    """
    Query all rows in the callers table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM callers")

    rows = cur.fetchall()

    for row in rows:
        print(row)
    
def query_caller(conn, name):
    """
    Query caller by Discord ID in the callers table
    :param conn: the Connection object
    :param name: the player's Discord User ID
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT id FROM callers WHERE name=?", (name))

    caller_id = cur.fetchall()

    return caller_id

def query_pick(conn, id):
    """
    Query caller by DB ID in the thesis table
    :param conn: the Connection object
    :param id: the player's database ID
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT ticker,target,direction,target_date FROM thesis WHERE id=?", (id))

    caller_pick= cur.fetchall()

    return caller_pick


def close_thesis(conn, name):
    """
    Delete a thesis by caller name
    :param conn:  Connection to the SQLite database
    :param name: the player's Discord User ID
    :return:
    """
    sql = 'DELETE FROM thesis WHERE name=?'
    cur = conn.cursor()
    cur.execute(sql, (name,))
    conn.commit()

def reset_game(conn):
    """
    Delete all rows in the thesis table
    :param conn: Connection to the SQLite database
    :return:
    """
    sql = 'DELETE FROM thesis'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

def stock_pull(symbol):
    base = "https://financialmodelingprep.com/api/v3/quote/"
    appx = "?apikey=" + API
    url = base + symbol + appx
    return url

def get_jsonparsed_data(url):
    """
    Receive the content of ``url``, parse it as JSON and return the object.

    Parameters
    ----------
    url : str

    Returns
    -------
    dict
    """
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)

def baberuth(name, ticker, direction, target, why, percent_wager, target_date):
    database = r"D:\\github\\python\\burryedge\\flowbot-master\\data\\ruthcalls.db"

    # assign start date to shot call in YYYY-MM-DD
    begin_date = datetime.today().strftime('%Y-%m-%d')

    # create the database connection
    conn = create_connection(database)
    with conn:
        # add new caller - YOU MUST FORCE THE TYPES OR THE DATABASE REJECTS THE INSERT
        caller = (str(name), str(begin_date), str(target_date))
        caller_id = add_caller(conn, caller)

        # add new thesis - YOU MUST FORCE THE TYPES OR THE DATABASE REJECTS THE INSERT
        thesis = (str(name), str(ticker), int(target), int(direction), str(why), int(percent_wager), int(1), int(caller_id), str(begin_date), str(target_date))
        create_thesis(conn, thesis)

        # initial point credit - YOU MUST FORCE THE TYPES OR THE DATABASE REJECTS THE INSERT
        score = (str(name), int(1000), int(caller_id))
        first_points(conn, score)

def babe_swing(name):
    database = r"D:\github\python\burryedge\flowbot-master\data\ruthcalls.db"

    # check today's date
    today = datetime.today().strftime('%Y-%m-%d')
    query_date = datetime.strptime(today,'%Y-%m-%d')

    # create the database connection
    conn = create_connection(database)
    with conn:

        caller_id = query_caller(conn, name)
        pick = query_pick(conn, caller_id) #returns (ticker,target,direction,target_date)
        ticker = pick[0]
        target = pick[1]
        direction = pick[2]
        target_dstring = pick[3]
        target_date = datetime.strptime(target_dstring,'%Y-%m-%d')
        url = stock_pull(ticker)
        data = get_jsonparsed_data(url)
        price = data['price']
        if direction == 1:
            if query_date >= target_date:
                if price >= target:
                    new_score = 1500
                    score_msg = f' Your new score is {new_score}'
                    response = "It's kinda late, but you're over target. +500." + score_msg
                else:
                    new_score = 500
                    score_msg = f' Your new score is {new_score}'
                    response = "Caught in the bottom of the 9th inning. You're out! -500." + score_msg
            else:
                if price >= target:
                    new_score = 1500
                    score_msg = f' Your new score is {new_score}'
                    response = "It's outta the park, folks! +500." + score_msg
                else:
                    response = "Nope. Not yet."
        elif direction == 0:
            if query_date >= target_date:
                if price <= target:
                    new_score = 1500
                    score_msg = f' Your new score is {new_score}'
                    response = "It's kinda late, but it's over the fence. +500." + score_msg
                else:
                    new_score = 500
                    score_msg = f' Your new score is {new_score}'
                    response = "Caught in the bottom of the 9th inning. You're out! -500." + score_msg
            else:
                if price <= target:
                    new_score = 1500
                    score_msg = f' Your new score is {new_score}'
                    response = "It's outta the park, folks! +500." + score_msg
                else:
                    response = "Nope. Not yet."
        else:
            response = "Something went wrong."
        #temp data to make code functional
        #new_score = 1500

        update_points(conn, (new_score, caller_id))
    return response

#Artifact for one-time command line runs
'''
if __name__ == '__main__':
    create_db()
'''
