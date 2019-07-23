# Name: Muazam Kamal
# File: matchfinder.py
# Purpose:
#   Finding the closest match to the time of the screenshot, using the OpenDota API

import requests
import time

class FindMatchException(Exception):
    def __init__(self, message=None, errors=None):
        super().__init__(message)

        self.errors = errors

class OpenDotaAPIError(FindMatchException):
    pass

def getSteamID(steamURL):
    # apiKey = "96627D1BE896D49A6ADBE6864A28F80F"
    # communityID = steamURL.split("/id/")[1]
    # communityID = communityID.replace('/', '')

    # url = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/"
    # params = {
    #     'key':apiKey,
    #     'vanityurl':communityID
    # }

    # data = requests.get(url, params)
    # print(data.json())

    return "89967077"

def getMatch(steamID):
    foundMatch = None

    url = "https://api.opendota.com/api/players/" + steamID + "/matches"
    query = {
        'limit':10
    }

    response = requests.get(url, query)

    if response.status_code != 200:
        raise OpenDotaAPIError(errors = steamID)

    matches = response.json()

    earliestTime = 0

    for currMatch in matches:
        if currMatch["start_time"] < time.time():
            if currMatch["start_time"] > earliestTime:
                foundMatch = currMatch
                earliestTime = foundMatch["start_time"]

    return foundMatch

def getSide(slot):
    switcher = {
        0:"Radiant",
        1:"Radiant",
        2:"Radiant",
        3:"Radiant",
        4:"Radiant",
        128:"Dire",
        129:"Dire",
        130:"Dire",
        131:"Dire",
        132:"Dire"
    }

    return switcher.get(slot, "Invalid player slot.")