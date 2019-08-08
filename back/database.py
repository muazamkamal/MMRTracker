# Name: Muazam Kamal
# File: database.py
# Purpose:
#   Implementation of sqlite3.

import sqlite3
import matchprocess

# Only run this for the first database and tables setup.
def setup(db_name):
    if db_name[-3:] != ".db":
        db_name = db_name + ".db"

    connect = sqlite3.connect(db_name)
    c = connect.cursor()

    # Match database table
    try:
        c.execute("SELECT * FROM match")
    except sqlite3.OperationalError:
        c.execute("CREATE TABLE match (matchid INTEGER PRIMARY KEY, win INTEGER, duration INTEGER, hero TEXT, kills INTEGER, deaths INTEGER, assists INTEGER)")
        connect.commit()

    # MMR database table
    try:
        c.execute("SELECT * FROM mmr")
    except sqlite3.OperationalError:
        c.execute("CREATE TABLE mmr (time INTEGER PRIMARY KEY, matchid INTEGER, core INTEGER, coreremaining INTEGER, coredelta INTEGER, support INTEGER, supportremaining INTEGER, supportdelta INTEGER, FOREIGN KEY(matchid) REFERENCES match(matchid))")
        connect.commit()

    connect.close()

    return db_name

def fetch_latest(db):
    connect = sqlite3.connect(db)
    connect.row_factory = sqlite3.Row
    c = connect.cursor()

    result = None

    try:
        c.execute("SELECT * FROM mmr ORDER BY id DESC LIMIT 1")

        result = c.fetchone()
    except sqlite3.OperationalError:
        pass

    connect.close()

    return result

def add_mmr(db, core, support, time, previous = None):
    connect = sqlite3.connect(db)
    c = connect.cursor()

    insert = "INSERT INTO mmr VALUES(?, ?, ?, ?, ?, ?, ?, ?)"

    core_mmr = core.get_mmr()
    core_rem = core.get_remaining()
    core_delta = 0
    support_mmr = support.get_mmr()
    support_rem = support.get_remaining()
    support_delta = 0

    if previous != None:
        prev_core = previous["core"]
        prev_support = previous["support"]

        if core != "TBD" and prev_core != "TBD":
            core_delta = core_mmr - prev_core

        if support != "TBD" and prev_support != "TBD":
            support_delta = support_mmr - prev_support

    data = (time, None, core_mmr, core_rem, core_delta, support_mmr, support_rem, support_delta)

    c.execute(insert, data)
    connect.commit()

    connect.close()

def add_match(db, match):
    connect = sqlite3.connect(db)
    c = connect.cursor()

    insert = "INSERT INTO match VALUES(?, ?, ?, ?, ?, ?, ?)"

    match_id = match["match_id"]
    win = matchprocess.get_result(match)
    duration = match["duration"]
    hero = matchprocess.get_hero(match["hero_id"])
    kills = match["kills"]
    deaths = match["deaths"]
    assists = match["assists"]

    data = (match_id, win, duration, hero, kills, deaths, assists)

    c.execute(insert, data)
    connect.commit()

    connect.close()


def link(db, match_id, time):
    connect = sqlite3.connect(db)
    c = connect.cursor()

    c.execute("UPDATE mmr SET matchid = ? WHERE time = ?", (match_id, time))
    connect.commit()

    connect.close()