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

        self._match_id = None

    # Accessors

    def get_mmr(self):
        return self._mmr

    def get_remaining(self):
        return self._remaining

    def get_calibration(self):
        return self._calibrate

    # Mutators

    def set_match_id(self, match_id):
        self._match_id = match_id

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
    core_mmr = None
    support_mmr = None

    if mmr_screen != None:
        text = pytesseract.image_to_string(mmr_screen)

        text = text.split("\n")

        core = None
        core_remaining = None

        support = None
        support_remaining = None

        try:
            core = text[0].split("Core ")[1]
            support = text[1].split("Support ")[1]
        except IndexError:
            raise ValueError("Unexcepted MMR string format.")

        # Remove any spaces and convert to uppercase.
        core = core.replace(' ', '')
        core = core.upper()

        support = support.replace(' ', '')
        support = support.upper()

        # Core

        # If TBD exists
        if core.find("TBD-") != -1 and core.find("GAMESREMAINING") != -1:
            core = core.replace("TBD-", '')
            core = core.replace("GAMESREMAINING", '')

            core_remaining = int(core)
            core = "TBD"
        else:
            core = core.replace(',', '')

            if core.isdigit():
                core = int(core)
                core_remaining = 0
            else:
                raise ValueError("Unexcepted Core MMR string format.")

        # Support

        # If TBD exists
        if support.find("TBD-") != -1 and support.find("GAMESREMAINING") != -1:
            support = support.replace("TBD-", '')
            support = support.replace("GAMESREMAINING", '')

            support_remaining = int(support)
            support = "TBD"
        else:
            support = support.replace(',', '')

            if support.isdigit():
                support = int(support)
                support_remaining = 0
            else:
                raise ValueError("Unexcepted Support MMR string format.")

        core_mmr = Mmr(core, core_remaining)
        support_mmr = Mmr(support, support_remaining)

    return core_mmr, support_mmr
