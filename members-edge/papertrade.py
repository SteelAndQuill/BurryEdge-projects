import sqlite3
from sqlite3 import Error
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
    database = r"D:\github\python\burryedge\flowbot-master\data\papertrades.db"

    sql_create_players_table = """ CREATE TABLE IF NOT EXISTS players (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        positions integer,
                                        round integer,
                                        UNIQUE(id, name)
                                    ); """

    sql_create_positions_table = """CREATE TABLE IF NOT EXISTS positions (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    ticker text NOT NULL,
                                    basis real NOT NULL,
                                    amount integer NOT NULL,
                                    why text NOT NULL,
                                    status_id integer NOT NULL,
                                    player_id integer NOT NULL,
                                    begin_date text NOT NULL,
                                    end_date text,
                                    position_id integer NOT NULL,
                                    round integer NOT NULL,
                                    FOREIGN KEY (player_id) REFERENCES players (id),
                                    FOREIGN KEY (round) REFERENCES rounds (round),
                                    UNIQUE(name, ticker, round)
                                );"""

    sql_create_cash_table = """CREATE TABLE IF NOT EXISTS cash (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    cash_balance real NOT NULL,
                                    player_id integer NOT NULL,
                                    FOREIGN KEY (player_id) REFERENCES players (id)
                                );"""

    sql_create_rounds_table = """CREATE TABLE IF NOT EXISTS rounds (
                                    round integer PRIMARY KEY,
                                    desc text NOT NULL,
                                    begin_date text NOT NULL,
                                    end_date text NOT NULL
                                );"""

    sql_create_rules_table = """CREATE TABLE IF NOT EXISTS rules (
                                    id integer PRIMARY KEY,
                                    round integer NOT NULL,
                                    seed integer NOT NULL,
                                    max integer NOT NULL,
                                    max_cap integer NOT NULL,
                                    min_cap integer NOT NULL,
                                    max_pos integer NOT NULL,
                                    description text NOT NULL,
                                    FOREIGN KEY (round) REFERENCES rounds (round),
                                    UNIQUE(round)
                                );"""

    sql_create_performance_table = """CREATE TABLE IF NOT EXISTS performance (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        cash_balance real NOT NULL,
                                        port_value real NOT NULL,
                                        round integer NOT NULL,
                                        player_id integer NOT NULL,
                                        FOREIGN KEY (player_id) REFERENCES players (id),
                                        UNIQUE(id, name, round)
                                    );"""

    sql_create_links_table = """CREATE TABLE IF NOT EXISTS links (
                                    id integer PRIMARY KEY,
                                    player_id integer NOT NULL,
                                    name text NOT NULL,
                                    ticker text NOT NULL,
                                    position_id integer NOT NULL,
                                    round integer NOT NULL,
                                    link text NOT NULL,
                                    FOREIGN KEY (player_id) REFERENCES players (id),
                                    UNIQUE(name, ticker, round)
                                );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create players table
        create_table(conn, sql_create_players_table)
        print("success players")
        # create positions table
        create_table(conn, sql_create_positions_table)
        print("success positions")
        #create cash balances table
        create_table(conn, sql_create_cash_table)
        print("success cash")
        #create rounds calendar
        create_table(conn, sql_create_rounds_table)
        print("success calendar")
        #create rules table
        create_table(conn, sql_create_rules_table)
        print("success rules")
        #create performance table
        create_table(conn, sql_create_performance_table)
        print("success performance")
        #create links table
        create_table(conn, sql_create_links_table)
        print("success links")
    else:
        print("Error! cannot create the database connection.")

def convertTuple(tup):
    new_str_list = [str(i) for i in tup] 
    str_ret = ' '.join(new_str_list)
    return str_ret

def define_round(conn, round_info): #input round_info is tuple(str desc,str begin_date,str end_date)
    """
    Create a new round with start and end date
    :param conn: Connection to the SQLite database
    :param round_info:
    :return: round id
    """
    sql = ''' INSERT OR IGNORE INTO rounds(desc,begin_date,end_date) 
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, round_info)
    conn.commit()
    return cur.lastrowid

def define_rules(conn, round_rules): #input round_rules is tuple(int round,int seed, int max %, int max_cap, int min_cap, str description)
    """
    Create rules for the round with description
    :param conn: Connection to the SQLite database
    :param round_rules: tuple(int round,int seed, int max %, int max_cap, int min_cap, int max_pos, str description)
    :return: round id"""
    sql = ''' INSERT OR IGNORE INTO rules(round,seed,max,max_cap,min_cap,max_pos,description)
              VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, round_rules)
    conn.commit()
    return cur.lastrowid

def new_player(conn, player): #input player is tuple(name,positions,round)
    """
    Create a new player into the players table
    :param conn: Connection to the SQLite database
    :param player: tuple(str name, int positions, int round)
    :return: player id
    """
    sql = ''' INSERT OR IGNORE INTO players(name,positions,round)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, player)
    conn.commit()
    return cur.lastrowid

def create_position(conn, buy_order): #buy_order is tuple(str name, str ticker, real basis, int amount, str why, intbool status_id, int player_id, str begin_date, int position_id, int round)
    """
    Create a new position with thesis
    :param conn: Connection to the SQLite database
    :param thesis:
    :return:
    """

    sql = ''' INSERT OR IGNORE INTO positions(name,ticker,basis,amount,why,status_id,player_id,begin_date,position_id,round)
              VALUES(?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, buy_order)
    conn.commit()
    return cur.lastrowid

# Functional Section

def create_round(desc, begin_date, end_date, seed, max_pct, max_cap, min_cap, max_pos, detail): 
    database = r"D:\\github\\python\\burryedge\\flowbot-master\\data\\papertrades.db"

    # create the database connection
    conn = create_connection(database)
    with conn:
        #Add new round dates
        round_info = (str(desc),str(begin_date),str(end_date))
        round_id = define_round(conn, round_info)#input round_info is tuple(str desc,str begin_date,str end_date)

        #Add round's rules
        round_rules = (int(round_id),int(seed),int(max_pct),int(max_cap),int(min_cap),int(max_pos),str(detail))
        rule_id = define_rules(conn, round_rules)
        #input round_rules is tuple(int round,int seed, int max %, int max_cap, int min_cap, int max_pos, str description)

    response = f'Ruleset {rule_id} for round {round_id} created successfully.'
    return response

def show_table(table_name):
    database = r"D:\\github\\python\\burryedge\\flowbot-master\\data\\papertrades.db"

    # create the database connection
    conn = create_connection(database)
    with conn:
        cur = conn.cursor()
        sql = f'SELECT * FROM {table_name}'
        cur.execute(sql)
        contents = cur.fetchall()
        print(contents)
        print(type(contents))
        output = ''
        for i in range(len(contents)):
            # Driver code
            tuple = contents[i]
            snip = convertTuple(tuple)
            print(snip)
            output = output + "\n" + snip
    return output

#Artifact for one-time command line runs
'''
if __name__ == '__main__':
    create_db()
'''
