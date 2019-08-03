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
    solo_mmr = None
    party_mmr = None

    if mmr_screen != None:
        text = pytesseract.image_to_string(mmr_screen)

        text = text.split("\n")

        solo = None
        solo_remaining = None

        party = None
        party_remaining = None

        try:
            solo = text[0].split("Solo ")[1]
            party = text[1].split("Party ")[1]
        except IndexError:
            raise ValueError("Unexcepted MMR string format.")

        # Solo
        try:
            # Check for if it's still in calibration or not.

            solo_remaining = solo.split("TBD -")[1]
            solo = "TBD"
        except IndexError:
            # Check for the MMR value and convert to integers
            # Error will be raised if conversion fails.
            solo = int(solo.replace(',', ''))
            solo_remaining = 0

        # Party
        try:
            # Check for if it's still in calibration or not.

            party_remaining = party.split("TBD -")[1]
            party = "TBD"
        except IndexError:
            # Check for the MMR value and convert to integers
            # Error will be raised if conversion fails.
            party = int(party.replace(',', ''))
            party_remaining = 0

        if solo_remaining != 0:
            # Attempt to get the amount of games left for TBD MMR
            try:
                solo_remaining = int(solo_remaining.split(" ")[0])
            except IndexError:
                raise ValueError("Unexpected calibration string format.")

        if party_remaining != 0:
            try:
                party_remaining = int(party_remaining.split(" ")[0])
            except IndexError:
                raise ValueError("Unexpected calibration string format.")

        solo_mmr = Mmr(solo, solo_remaining)
        party_mmr = Mmr(party, party_remaining)

    return solo_mmr, party_mmr
