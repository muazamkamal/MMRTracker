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

def get_match(steam_id, file_date):
    found_match = None

    url = "https://api.opendota.com/api/players/" + steam_id + "/matches"
    query = {
        "limit": 20,
        "lobby_type": 7 # Only query for ranked matches.
    }

    response = requests.get(url, query)

    if response.status_code != 200:
        raise OpenDotaAPIError(errors = steam_id)

    matches = response.json()

    earliest_time = 0

    for curr_match in matches:
        if curr_match["start_time"] < file_date:
            if curr_match["start_time"] > earliest_time:
                found_match = curr_match
                earliest_time = found_match["start_time"]

    if found_match == None:
        format_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(file_date))

        raise OpenDotaAPIError(errors = format_date)

    return found_match