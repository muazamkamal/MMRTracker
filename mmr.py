# Name: Muazam Kamal
# File: mmr.py
# Purpose: OCR, parsing and calculation of the MMR.

import pytesseract

def parse(mmrScreen):
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
