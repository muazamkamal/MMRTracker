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

    url = "https://api.opendota.com/api/players/" + steamID + "/matches"
    query = {
        "limit": 20,
        "lobby_type": 7 # Only query for ranked matches.
    }

    response = requests.get(url, query)

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

def get_hero(hero_id):
    switcher = {
        1: "Anti-Mage",
        2: "Axe",
        3: "Bane",
        4: "Bloodseeker",
        5: "Crystal Maiden",
        6: "Drow Ranger",
        7: "Earthshaker",
        8: "Juggernaut",
        9: "Mirana",
        10: "Morphling",
        11: "Shadow Fiend",
        12: "Phantom Lancer",
        13: "Puck",
        14: "Pudge",
        15: "Razor",
        16: "Sand King",
        17: "Storm Spirit",
        18: "Sven",
        19: "Tiny",
        20: "Vengeful Spirit",
        21: "Windranger",
        22: "Zeus",
        23: "Kunkka",
        25: "Lina",
        26: "Lion",
        27: "Shadow Shaman",
        28: "Slardar",
        29: "Tidehunter",
        30: "Witch Doctor",
        31: "Lich",
        32: "Riki",
        33: "Enigma",
        34: "Tinker",
        35: "Sniper",
        36: "Necrophos",
        37: "Warlock",
        38: "Beastmaster",
        39: "Queen of Pain",
        40: "Venomancer",
        41: "Faceless Void",
        42: "Wraith King",
        43: "Death Prophet",
        44: "Phantom Assassin",
        45: "Pugna",
        46: "Templar Assassin",
        47: "Viper",
        48: "Luna",
        49: "Dragon Knight",
        50: "Dazzle",
        51: "Clockwerk",
        52: "Leshrac",
        53: "Nature's Prophet",
        54: "Life Stealer",
        55: "Dark Seer",
        56: "Clinkz",
        57: "Omniknight",
        58: "Enchantress",
        59: "Huskar",
        60: "Night Stalker",
        61: "Broodmother",
        62: "Bounty Hunter",
        63: "Weaver",
        64: "Jakiro",
        65: "Batrider",
        66: "Chen",
        67: "Spectre",
        68: "Ancient Apparition",
        69: "Doom",
        70: "Ursa",
        71: "Spirit Breaker",
        72: "Gyrocopter",
        73: "Alchemist",
        74: "Invoker",
        75: "Silencer",
        76: "Outworld Devourer",
        77: "Lycan",
        78: "Brewmaster",
        79: "Shadow Demon",
        80: "Lone Druid",
        81: "Chaos Knight",
        82: "Meepo",
        83: "Treant Protector",
        84: "Ogre Magi",
        85: "Undying",
        86: "Rubick",
        87: "Disruptor",
        88: "Nyx Assassin",
        89: "Naga Siren",
        90: "Keeper of the Light",
        91: "Io",
        92: "Visage",
        93: "Slark",
        94: "Medusa",
        95: "Troll Warlord",
        96: "Centaur",
        97: "Magnus",
        98: "Timbersaw",
        99: "Bristleback",
        100: "Tusk",
        101: "Skywrath Mage",
        102: "Abaddon",
        103: "Elder Titan",
        104: "Legion Commander",
        105: "Techies",
        106: "Ember Spirit",
        107: "Earth Spirit",
        108: "Underlord",
        109: "Terrorblade",
        110: "Phoenix",
        111: "Oracle",
        112: "Winter Wyvern",
        113: "Arc Warden",
        114: "Monkey King",
        119: "Dark Willow",
        120: "Pangolier",
        121: "Grimstroke",
        129: "Mars"
    }

    return switcher.get(hero_id, "Invalid hero id.")