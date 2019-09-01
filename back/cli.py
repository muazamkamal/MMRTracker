# Name: Muazam Kamal
# File: cli.py
# Purpose: Command-line interface use of the MMRTracker.

import sys

import imageprocess
import mmr
import matchfinder
import matchprocess
import database

def usage(program):
    print("usage: python " + program + " <dota screenshot>\n")

def cli():
    if len(sys.argv) < 2:
        usage(sys.argv[0])
    else:
        file_name = sys.argv[1]

        image = imageprocess.load_image(file_name)

        core, support = mmr.parse(image)

        if core.get_calibration() == True:
            print("Core: " + core.get_mmr() + ", " + str(core.get_remaining()) + " games remaining.")
        else:
            print("Core: " + str(core.get_mmr()))

        if support.get_calibration() == True:
            print("Support: " + support.get_mmr() + ", " + str(support.get_remaining()) + " games remaining.")
        else:
            print("Support: " + str(support.get_mmr()))

        try:
            time = imageprocess.file_date(file_name)
            match = matchfinder.get_match("89967077", time)
            core.set_match_id(match["match_id"])
            support.set_match_id(match["match_id"])

            result = matchprocess.get_result(match)

            if result == True:
                result = "won"
            else:
                result = "lost"

            match_ID = match["match_id"]

            print()

            print("You " + result + " your last match!")
            print("Match ID: {0:d}".format(match_ID))
            print("Played as: " + matchprocess.get_hero(match["hero_id"]))
            print("Link: https://www.opendota.com/matches/{0:d}".format(match_ID))

            db_name = "s3_1_beta"
            db_name = database.setup(db_name)

            previous_mmr = database.fetch_latest(db_name)
            database.add_mmr(db_name, core, support, time, previous_mmr)
            database.add_match(db_name, match)
            database.link(db_name, match_ID, time)

        except matchfinder.OpenDotaAPIError:
            print("fatal: Failed to fetch match.")