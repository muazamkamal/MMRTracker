# Name: Muazam Kamal
# File: cli.py
# Purpose: Command-line interface use of the MMRTracker.

import sys

import imageprocess
import mmr
import matchfinder

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
            match = matchfinder.get_match("89967077", imageprocess.file_date(file_name))

            side = matchfinder.get_side(match["player_slot"])

            result = None

            if side == "Radiant" and match["radiant_win"] == True:
                result = "won"
            elif side == "Dire" and match["radiant_win"] == False:
                result = "won"
            else:
                result = "lost"

            match_ID = match["match_id"]

            print()

            print("You " + result + " your last match!")
            print("Match ID: {0:d}".format(match_ID))
            print("Link: https://www.opendota.com/matches/{0:d}".format(match_ID))
        except matchfinder.OpenDotaAPIError:
            print("fatal: Failed to fetch match.")