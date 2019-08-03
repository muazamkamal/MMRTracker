# Name: Muazam Kamal
# File: mmr.py
# Purpose: MMR related functions and class.

import pytesseract

class Mmr:

    # Constructor
    def __init__(self, mmr, rem):
        self._calibrate = self.__calibration(mmr, rem)

        self._mmr = mmr
        self._remaining = rem

    # Accessors

    def get_mmr(self):
        return self._mmr

    def get_remaining(self):
        return self._remaining

    def get_calibration(self):
        return self._calibrate

    # Validator

    def __calibration(self, mmr, rem):
        in_calibration = None

        if type(mmr) is int:
            if mmr < 0:
                raise ValueError("Negative MMR is invalid.")

            if rem != 0:
                raise ValueError("Calibrated MMR should have 0 calibration games left.")

            in_calibration = False
        elif mmr == "TBD":
            if rem < 1 or rem > 10:
                raise ValueError("Calibration games should be between 1 to 10.")

            in_calibration = True
        else:
            raise ValueError("Invalid MMR input.")

        return in_calibration

def parse(mmr_screen):
    solo = None
    party = None
    solo_remaining = None
    party_remaining = None

    if mmr_screen != None:
        text = pytesseract.image_to_string(mmr_screen)

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

                solo_remaining = solo.split("TBD -")[1]
                solo = "TBD"
            except IndexError:
                # Check for the MMR value and convert to integers
                solo = int(solo.replace(',', ''))
                pass

            # Party
            try:
                # Check for if it's still in calibration or not.

                party_remaining = party.split("TBD -")[1]
                party = "TBD"
            except IndexError:
                # Check for the MMR value and convert to integers
                party = int(party.replace(',', ''))
                pass

            if solo_remaining != None:
                # Attempt to get the amount of games left for TBD MMR
                try:
                    solo_remaining = int(solo_remaining.split(" ")[0])
                except IndexError:
                    print("fatal: Solo TBD Games Remaining format error.")

                    solo = None
                    solo_remaining = None

                    party = None
                    party_remaining = None

            if party_remaining != None:
                try:
                    party_remaining = int(party_remaining.split(" ")[0])
                except IndexError:
                    print("fatal: Solo TBD Games Remaining format error.")

                    solo = None
                    solo_remaining = None

                    party = None
                    party_remaining = None
        else:
            print("Invalid solo and/or party MMR.")

    return (solo, solo_remaining), (party, party_remaining)
