# Name: Muazam Kamal
# File: main.py
# Purpose: Main entry file for MMR Tracker.

from PIL import Image
from PIL import ImageOps
import pytesseract
import sys

def usage(program):
    print("usage: python " + program + " <dota screenshot>\n")

def loadImage(file):
    try:
        # Conversion to remove alpha channel, because invert does not work on alpha channel.
        image = Image.open(file).convert("RGB")

        width, height = image.size

        ratio = round(width/height, 2)

        if ratio < 1.78 or ratio > 1.78:
            print("fatal: Screenshot aspect ratio did not match.")

            image = None
        else:
            topX = 0.73 * width
            topY = 0.17 * height

            bottomX = 0.86 * width
            bottomY = 0.25 * height

            image = image.crop((topX, topY, bottomX, bottomY))
            image = ImageOps.invert(image)

            newSize = tuple(2*x for x in image.size)

            image = image.resize(newSize, Image.ANTIALIAS)

        return image
    except (FileNotFoundError, PermissionError) as ex:
        print("fatal: " + ex.strerror)

def parseMMR(mmrScreen):
    solo = None
    party = None
    soloRemaining = None
    partyRemaining = None

    if mmrScreen != None:
        text = pytesseract.image_to_string(mmrScreen)

        text = text.split("\n")

        try:
            solo = text[0].split("Solo ")[1]
            party = text[1].split("Party ")[1]
        except IndexError:
            # Reset to None if pattern fails.
            solo = None
            party = None

        if (solo != None and party != None):
            # Solo
            try:
                # Check for if it's still in calibration or not.

                soloRemaining = solo.split("TBD -")[1]
                solo = "TBD"
            except IndexError:
                # Check for the MMR value and convert to integers
                solo = int(solo.replace(',', ''))
                pass

            # Party
            try:
                # Check for if it's still in calibration or not.

                partyRemaining = party.split("TBD -")[1]
                party = "TBD"
            except IndexError:
                # Check for the MMR value and convert to integers
                party = int(party.replace(',', ''))
                pass

            if soloRemaining != None:
                # Attempt to get the amount of games left for TBD MMR
                try:
                    soloRemaining = int(soloRemaining.split(" ")[0])
                except IndexError:
                    print("fatal: Solo TBD Games Remaining format error.")

                    solo = None
                    soloRemaining = None

                    party = None
                    partyRemaining = None

            if partyRemaining != None:
                try:
                    partyRemaining = int(partyRemaining.split(" ")[0])
                except IndexError:
                    print("fatal: Solo TBD Games Remaining format error.")

                    solo = None
                    soloRemaining = None

                    party = None
                    partyRemaining = None
        else:
            print("Invalid solo and/or party MMR.")

    return (solo, soloRemaining), (party, partyRemaining)

def cli():
    if len(sys.argv) < 2:
        usage(sys.argv[0])
    else:
        fileName = sys.argv[1]

        image = loadImage(fileName)

        solo, party = parseMMR(image)

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

if __name__ == '__main__':
    cli()
