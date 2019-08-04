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

        solo, party = mmr.parse(image)

        if solo.get_calibration() == True:
            print("Solo: " + solo.get_mmr() + ", " + str(solo.get_remaining()) + " games remaining.")
        else:
            print("Solo: " + str(solo.get_mmr()))

        if party.get_calibration() == True:
            print("Party: " + party.get_mmr() + ", " + str(party.get_remaining()) + " games remaining.")
        else:
            print("Party: " + str(party.get_mmr()))

        try:
            time = imageprocess.file_date(file_name)
            match = matchfinder.get_match("89967077", time)
            solo.set_match_id(match["match_id"])
            party.set_match_id(match["match_id"])

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

            database.setup()

            # previous_mmr = database.fetch_latest()
            # database.add_mmr(solo, party, time, previous_mmr)
            # database.add_match(match)
            database.link(match_ID, time)

        except matchfinder.OpenDotaAPIError:
            print("fatal: Failed to fetch match.")