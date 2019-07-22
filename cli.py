# Name: Muazam Kamal
# File: cli.py
# Purpose: Command-line interface use of the MMRTracker.

import sys

import imageprocess
import mmr

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
                print("Solo: " + solo[0])
                print("\t {0:d}".format(solo[1]))
            else:
                print("Solo {0:d}".format(solo[0]))

            if party[1] != None:
                print("Party: " + party[0])
                print("\t {0:d}".format(party[1]))
            else:
                print("Party {0:d}".format(party[0]))

