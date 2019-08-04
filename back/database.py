# Name: Muazam Kamal
# File: database.py
# Purpose:
#   Implementation of sqlite3.

import sqlite3
import matchprocess

# Only run this for the first database and tables setup.
def setup():
    connect = sqlite3.connect("mmrtracker.db")
    c = connect.cursor()

    try:
        c.execute("SELECT * FROM match")
    except sqlite3.OperationalError:
        c.execute("CREATE TABLE match (matchid INTEGER PRIMARY KEY, win INTEGER, duration INTEGER, hero TEXT, kills INTEGER, deaths INTEGER, assists INTEGER)")
        connect.commit()

    try:
        c.execute("SELECT * FROM mmr")
    except sqlite3.OperationalError:
        c.execute("CREATE TABLE mmr (time INTEGER PRIMARY KEY, matchid INTEGER, solo INTEGER, soloremaining INTEGER, solodelta INTEGER, party INTEGER, partyremaining INTEGER, partydelta INTEGER, FOREIGN KEY(matchid) REFERENCES match(matchid))")
        connect.commit()

    connect.close()

def fetch_latest():
    connect = sqlite3.connect("mmrtracker.db")
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

def add_mmr(solo, party, time, previous = None):
    connect = sqlite3.connect("mmrtracker.db")
    c = connect.cursor()

    insert = "INSERT INTO mmr VALUES(?, ?, ?, ?, ?, ?, ?, ?)"

    solo_mmr = solo.get_mmr()
    solo_rem = solo.get_remaining()
    solo_delta = 0
    party_mmr = party.get_mmr()
    party_rem = party.get_remaining()
    party_delta = 0

    if previous != None:
        prev_solo = previous["solo"]
        prev_party = previous["party"]

        if solo != "TBD" and prev_solo != "TBD":
            solo_delta = solo_mmr - prev_solo

        if party != "TBD" and prev_party != "TBD":
            party_delta = party_mmr - prev_party

    data = (time, None, solo_mmr, solo_rem, solo_delta, party_mmr, party_rem, party_delta)

    c.execute(insert, data)
    connect.commit()

    connect.close()

def add_match(match):
    connect = sqlite3.connect("mmrtracker.db")
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


def link(match_id, time):
    connect = sqlite3.connect("mmrtracker.db")
    c = connect.cursor()

    c.execute("UPDATE mmr SET matchid = ? WHERE time = ?", (match_id, time))
    connect.commit()

    connect.close()