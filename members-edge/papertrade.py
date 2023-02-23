import sqlite3
from sqlite3 import Error
import pandas as pd
from datetime import datetime
import os
import dotenv
import json
from urllib.request import urlopen
from pathlib import Path
import log

logger = log.setup_logger(__name__)

# What? You thought I would just hardcode the API Key?
dotenv.load_dotenv()
FMP_API = str(os.getenv("FMP_API"))

# Many thanks to sqlitetutorial.net

# Define database


def create_connection(db_file):
    """create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        logger.info(e)

    return conn


def create_table(conn, create_table_sql):
    """create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        logger.info(e)


def create_db():
    database = Path("./db/papertrades.db")

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
        logger.info("success players")
        # create positions table
        create_table(conn, sql_create_positions_table)
        logger.info("success positions")
        # create cash balances table
        create_table(conn, sql_create_cash_table)
        logger.info("success cash")
        # create rounds calendar
        create_table(conn, sql_create_rounds_table)
        logger.info("success calendar")
        # create rules table
        create_table(conn, sql_create_rules_table)
        logger.info("success rules")
        # create performance table
        create_table(conn, sql_create_performance_table)
        logger.info("success performance")
        # create links table
        create_table(conn, sql_create_links_table)
        logger.info("success links")
    else:
        logger.info("Error! cannot create the database connection.")


def convertTuple(tup):
    new_str_list = [str(i) for i in tup]
    str_ret = " ".join(new_str_list)
    return str_ret


def define_round(
    conn, round_info
):  # input round_info is tuple(str desc,str begin_date,str end_date)
    """
    Create a new round with start and end date
    :param conn: Connection to the SQLite database
    :param round_info:
    :return: round id
    """
    sql = """ INSERT OR IGNORE INTO rounds(desc,begin_date,end_date)
              VALUES(?,?,?) """
    cur = conn.cursor()
    cur.execute(sql, round_info)
    conn.commit()
    return cur.lastrowid


def define_rules(
    conn, round_rules
):  # input round_rules is tuple(int round,int seed, int max %, int max_cap, int min_cap, str description)
    """
    Create rules for the round with description
    :param conn: Connection to the SQLite database
    :param round_rules: tuple(int round,int seed, int max %, int max_cap, int min_cap, int max_pos, str description)
    :return: round id"""
    sql = """ INSERT OR IGNORE INTO rules(round,seed,max,max_cap,min_cap,max_pos,description)
              VALUES(?,?,?,?,?,?,?) """
    cur = conn.cursor()
    cur.execute(sql, round_rules)
    conn.commit()
    return cur.lastrowid


def round_rules(conn, round):
    """
    Query rules for current round
    :param conn: Connection to the SQLite database
    :param name: tuple(int round,)
    :return: tuple(int id, int round,int seed,int max, int max_cap, int min_cap,int max_pos,str description)
    """
    sql = """ SELECT * FROM rules WHERE round=? """
    cur = conn.cursor()
    cur.execute(sql, round)
    rules = cur.fetchall()
    return rules[
        0
    ]  # (str name, float cash_balance, float port_value, int round, int player_id,)


def credit_player(
    conn, credit
):  # id integer,name text,cash_balance real,port_value real,round integer,player_id integer,
    """
    Credit new account with value of seed defined in round rules.
    :param conn: Connection to the SQLite database
    :param credit: tuple(str name,float cash_balance, float port_value, int round, int player_id,)
    :return: round id"""
    sql = """ INSERT OR IGNORE INTO performance(name,cash_balance,port_value,round,player_id)
              VALUES(?,?,?,?,?) """
    cur = conn.cursor()
    cur.execute(sql, credit)
    conn.commit()
    return cur.lastrowid


def cash_transact(
    conn, transaction
):  # transaction is tuple(float cash_balance, str name)
    """
    Update a player's cash balance
    :param conn: Connection to the SQLite database
    :param name: tuple(float cash_balance, str name)
    :return: lastrowid
    """
    sql = """ UPDATE performance SET cash_balance=? WHERE name=? """
    cur = conn.cursor()
    cur.execute(sql, transaction)
    conn.commit()
    return cur.lastrowid


def player_perf(conn, name):
    """
    Query a player's performance info
    :param conn: Connection to the SQLite database
    :param name: tuple(str name,)
    :return: tuple(int id, text name, float cash_balance, float port_value, int round, int player_id)
    """
    sql = """ SELECT * FROM performance WHERE name=? """
    cur = conn.cursor()
    cur.execute(sql, name)
    playerinfo = cur.fetchall()
    return playerinfo[0]


def drop_round(conn, round):  # input round is tuple(int round,)
    """
    Drop unnecessary rounds created in testing
    :param conn: Connection to the SQLite Database
    :param round: tuple(int round,)
    :return: None
    """
    sql1 = """ DELETE FROM rules WHERE round=? """
    sql2 = """ DELETE FROM rounds WHERE round=? """
    cur = conn.cursor()
    cur.execute(sql1, round)
    cur.execute(sql2, round)
    conn.commit()


def current_round(conn):
    """
    Fetches last defined round
    :param conn: Connection to the SQLite Database
    :return: int round
    """
    sql = """ SELECT * FROM rounds ORDER BY round DESC LIMIT 1; """
    cur = conn.cursor()
    cur.execute(sql)
    round_id = cur.fetchall()[0][0]
    return round_id


def new_player(conn, player):  # input player is tuple(name,positions,round)
    """
    Create a new player into the players table
    :param conn: Connection to the SQLite database
    :param player: tuple(str name, int positions, int round)
    :return: player id
    """
    sql = """ INSERT OR IGNORE INTO players(name,positions,round)
              VALUES(?,?,?) """
    cur = conn.cursor()
    cur.execute(sql, player)
    conn.commit()
    return cur.lastrowid


def player_info(conn, name):
    """
    Query a player's info
    :param conn: Connection to the SQLite database
    :param name: tuple(str name,)
    :return: tuple(int id, text name, int positions, int round)
    """
    sql = """ SELECT * FROM players WHERE name=? """
    cur = conn.cursor()
    cur.execute(sql, name)
    playerinfo = cur.fetchall()
    return playerinfo[0]


def update_player(
    conn, player_update
):  # player_update is tuple(int positions, int round, str name)
    """
    Update a player's round
    :param conn: Connection to the SQLite database
    :param name: tuple(int positions, int round, str name)
    :return: lastrowid
    """
    sql = """ UPDATE players SET positions=? AND round=? WHERE name=? """
    cur = conn.cursor()
    cur.execute(sql, player_update)
    conn.commit()
    return cur.lastrowid


def create_position(
    conn, buy_order
):  # buy_order is tuple(str name, str ticker, real basis, int amount, str why, intbool status_id, int player_id, str begin_date, int position_id, int round)
    """
    Create a new position with thesis
    :param conn: Connection to the SQLite database
    :param buy_order: Tuple matching POSITIONS table
    :return: lastrowid
    """
    sql = """ INSERT OR IGNORE INTO positions(name,ticker,basis,amount,why,status_id,player_id,begin_date,position_id,round)
              VALUES(?,?,?,?,?,?,?,?,?,?) """
    cur = conn.cursor()
    cur.execute(sql, buy_order)
    conn.commit()
    return cur.lastrowid


def final_position(
    conn, link_info
):  # player_id integer,name text,ticker text,position_id integer,round integer,link text,
    """
    Create a final position with long-form thesis link
    :param conn: Connection to the SQLite database
    :param link_info: tuple matching LINKS table
    :return: lastrowid
    """
    stuff = "stuff"
    sql = """ INSERT OR IGNORE INTO links(player_id,name,ticker,position_id,round,link)
              VALUES(?,?,?,?,?,?) """
    cur = conn.cursor()
    cur.execute(sql, link_info)
    conn.commit()
    return cur.lastrowid


# ================= Functional Section ========================


def create_round(
    desc, begin_date, end_date, seed, max_pct, max_cap, min_cap, max_pos, detail
):
    database = Path("./db/papertrades.db")

    # create the database connection
    conn = create_connection(database)
    with conn:
        # Add new round dates
        round_info = (str(desc), str(begin_date), str(end_date))
        round_id = define_round(
            conn, round_info
        )  # input round_info is tuple(str desc,str begin_date,str end_date)

        # Add round's rules
        round_rules = (
            int(round_id),
            int(seed),
            int(max_pct),
            int(max_cap),
            int(min_cap),
            int(max_pos),
            str(detail),
        )
        rule_id = define_rules(conn, round_rules)
        # input round_rules is tuple(int round,int seed, int max %, int max_cap, int min_cap, int max_pos, str description)

    response = f"Ruleset {rule_id} for round {round_id} created successfully."
    return response


def register_player(name):
    """Register a player for a new round. New player or rollover."""
    database = Path("./db/papertrades.db")

    # create the database connection
    conn = create_connection(database)
    with conn:
        round_id = current_round(conn)
        check = player_info(conn, (str(name),))
        rules = round_rules(conn, (int(round_id),))
        if not check:
            # input player is tuple(name,positions,round)
            player = (str(name), int(0), int(round_id))
            registrant = new_player(conn, player)
            credit = (
                str(name),
                float(rules[2]),
                float(rules[2]),
                int(round_id),
                int(registrant),
            )  # id integer,name text,cash_balance real,port_value real,round integer,player_id integer,
            ledger = credit_player(conn, credit)
            response = f"{name} successfully registered for Round {round_id} as new investor #{registrant}. ${rules[2]} credited in ledger entry {ledger}."
        elif check[3] < round_id:
            # player_update is tuple(int positions, int round, str name)
            player_update = (int(check[2]), int(round_id), str(name))
            updated = update_player(conn, player_update)
            response = f"Investor #{updated} successfully rolled to Round {round_id}."
        else:
            response = "ERROR: You are already registered for this round."

    return response


def buy_order(
    name: str, ticker: str, basis: float, amount: int, why: str, link: str = None
):
    """Place an instantaneous buy order."""

    database = Path("./db/papertrades.db")
    # buy_order is tuple(str name, str ticker, real basis, int amount, str why, intbool status_id, int player_id, str begin_date, int position_id, int round)

    # assign start date to position in YYYY-MM-DD
    begin_date = datetime.today().strftime("%Y-%m-%d")

    # create the database connection
    conn = create_connection(database)
    with conn:

        round_id = current_round(conn)
        check = player_info(
            conn, (str(name),)
        )  # playerinfo tuple(int id, text name, int positions, int round)
        rules = round_rules(
            conn, (int(round_id),)
        )  # rules tuple(int id,int round, int seed, int max, int max_cap, int min_cap, int max_pos, str description,)

        if not check:
            response = f"{name} is not registered for this round. Please run `/paper_register`."
        elif check[3] != round_id:
            response = f"{name} is not registered for this round. Please run `/paper_register`."
        else:
            newposid = check[2] + 1
            max_pos = rules[6]
            if newposid > max_pos:
                response = f"There are already {check[3]} positions held by {name}. No new positions beyond the maximum of {rules[6]} can be opened this round."
            elif newposid == max_pos:
                stuff = "stuff"  # change input to require link to be entered.
                buy_command = (
                    str(name),
                    str(ticker),
                    float(basis),
                    int(amount),
                    str(why),
                    int(1),
                    int(check[0]),
                    str(begin_date),
                    int(newposid),
                    int(check[3]),
                )
                player_update = (
                    int(newposid),
                    int(round_id),
                    str(name),
                )  # updates position instead of round
                updated = update_player(conn, player_update)  # returns player id
                posbuyid = create_position(
                    conn, buy_command
                )  # returns purchase order number
                link_add = (
                    int(updated),
                    str(name),
                    str(ticker),
                    int(posbuyid),
                    int(round_id),
                    str(link),
                )  # player_id integer,name text,ticker text,position_id integer,round integer,link text,
                link_info = final_position(conn, link_add)
                response = f"Order number {posbuyid} completed for {name} (player {updated}). Link association number {link_info} filed."
            else:
                buy_command = (
                    str(name),
                    str(ticker),
                    float(basis),
                    int(amount),
                    str(why),
                    int(1),
                    int(check[0]),
                    str(begin_date),
                    int(newposid),
                    int(check[3]),
                )
                player_update = (
                    int(newposid),
                    int(round_id),
                    str(name),
                )  # updates position instead of round
                updated = update_player(conn, player_update)  # returns player id
                posbuyid = create_position(
                    conn, buy_command
                )  # returns purchase order number
                response = (
                    f"Order number {posbuyid} completed for {name} (player {updated})."
                )

    return response


def delete_round(round: int):
    """Deletes erroneous rounds from table.
    Returns courtesy message"""
    database = Path("./db/papertrades.db")

    # create the database connection
    conn = create_connection(database)
    with conn:
        drop_round(conn, (int(round),))
    response = f"Round {round} deleted from database."

    return response


def show_table(table_name):
    database = Path("./db/papertrades.db")

    # create the database connection
    conn = create_connection(database)
    with conn:
        cur = conn.cursor()
        sql = f"SELECT * FROM {table_name}"
        cur.execute(sql)
        contents = cur.fetchall()
        logger.info(contents)
        logger.info(type(contents))
        output = ""
        for i in range(len(contents)):
            # Driver code
            tuple = contents[i]
            snip = convertTuple(tuple)
            logger.info(snip)
            output = output + "\n" + snip
    return output


# Artifact for one-time command line runs
"""
if __name__ == '__main__':
    create_db()
"""
