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

def get_steam_id(steamURL):
    # api_key = "96627D1BE896D49A6ADBE6864A28F80F"
    # community_id = steamURL.split("/id/")[1]
    # community_id = community_id.replace('/', '')

    # url = "http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/"
    # params = {
    #     'key':api_key,
    #     'vanityurl':community_id
    # }

    # data = requests.get(url, params)
    # print(data.json())

    return "89967077"

def get_match(steamID, fileDate):
    foundMatch = None

    url = "https://api.opendota.com/api/players/" + steamID + "/recentMatches"

    response = requests.get(url)

    if response.status_code != 200:
        raise OpenDotaAPIError(errors = steamID)

    matches = response.json()

    earliestTime = 0

    for currMatch in matches:
        if currMatch["start_time"] < fileDate:
            if currMatch["start_time"] > earliestTime:
                foundMatch = currMatch
                earliestTime = foundMatch["start_time"]

    if foundMatch == None:
        formatDate = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(fileDate))

        raise OpenDotaAPIError(errors = formatDate)

    return foundMatch

def get_side(slot):
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