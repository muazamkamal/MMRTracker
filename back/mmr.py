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

        # Solo
        try:
            # Check for if it's still in calibration or not.

            core_remaining = core.split("Requires ")[1]
            core = "TBD"
        except IndexError:
            # Check for the MMR value and convert to integers
            # Error will be raised if conversion fails.
            core = int(core.replace(',', ''))
            core_remaining = 0

        # Party
        try:
            # Check for if it's still in calibration or not.

            support_remaining = support.split("Requires ")[1]
            support = "TBD"
        except IndexError:
            # Check for the MMR value and convert to integers
            # Error will be raised if conversion fails.
            support = int(support.replace(',', ''))
            support_remaining = 0

        if core_remaining != 0:
            # Attempt to get the amount of games left for TBD MMR
            try:
                core_remaining = int(core_remaining.split(" ")[0])
            except IndexError:
                raise ValueError("Unexpected calibration string format.")

        if support_remaining != 0:
            try:
                support_remaining = int(support_remaining.split(" ")[0])
            except IndexError:
                raise ValueError("Unexpected calibration string format.")

        core_mmr = Mmr(core, core_remaining)
        support_mmr = Mmr(support, support_remaining)

    return core_mmr, support_mmr
