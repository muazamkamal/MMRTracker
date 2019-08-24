# Name: Muazam Kamal
# File: front.py
# Purpose: Front-end use of the MMRTracker.

import sys
import os.path

import imageprocess
import mmr
import matchfinder
import matchprocess
import database

if __name__ == '__main__':
    file_name = sys.argv[1]
    db_name = sys.argv[2]

    image = imageprocess.load_image(file_name)

    core, support = mmr.parse(image)

    time = imageprocess.file_date(file_name)
    match = matchfinder.get_match("89967077", time)
    match_ID = match["match_id"]
    core.set_match_id(match_ID)
    support.set_match_id(match_ID)

    # DB name might changed, adding ".db" if needed.
    db_name = database.setup(db_name)

    previous_mmr = database.fetch_latest(db_name)
    database.add_mmr(db_name, core, support, time, previous_mmr)
    database.add_match(db_name, match)
    database.link(db_name, match_ID, time)