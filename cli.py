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
        fileName = sys.argv[1]

        image = imageprocess.loadImage(fileName)

        solo, party = mmr.parse(image)

        if solo != (None, None) and party != (None, None):

            if solo[1] != None:
                print("Solo: " + solo[0] + ", {0:d} games remaining.".format(solo[1]))
            else:
                print("Solo {0:d}".format(solo[0]))

            if party[1] != None:
                print("Party: " + party[0] + ", {0:d} games remaining.".format(party[1]))
            else:
                print("Party {0:d}".format(party[0]))

            id = matchfinder.getSteamID("https://steamcommunity.com/id/muazamkamal/")

            try:
                match = matchfinder.getMatch(id)

                side = matchfinder.getSide(match["player_slot"])

                result = None

                if side == "Radiant" and match["radiant_win"] == True:
                    result = "won"
                if side == "Dire" and match["radiant_win"] == False:
                    result = "won"
                else:
                    result = "lost"

                print()

                print("You " + result + " your last match!")
                print("Match ID: {0:d}".format(match["match_id"]))
            except matchfinder.OpenDotaAPIError as e:
                print("fatal: Failed to fetch matches with the account id " + e.errors)