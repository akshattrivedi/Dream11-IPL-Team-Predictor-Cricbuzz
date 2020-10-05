from pycricbuzz import Cricbuzz
import requests

import common_utils as commonUtils

def getCurrentIplMatch():
    cricbuzz = Cricbuzz()
    iplMatchFoundFlag = False
    matches = cricbuzz.matches()
    maxMatchID = None
    currentIplMatch = {}

    for match in matches:
        if match["srs"] == "Indian Premier League 2020" and match["toss"] != "":
            matchID = match["id"]
            iplMatchFoundFlag = True

            if maxMatchID is None:
                maxMatchID = matchID
                currentIplMatch = match
            elif matchID > maxMatchID:
                maxMatchID = matchID
                currentIplMatch = match
    
    if not iplMatchFoundFlag:
        print("404! No Live IPL Match Found!")
        exit(0)

    return currentIplMatch

def getCurrentMatchPlayers(iplMatch):
    squadFoundFlag = False
    matchID = iplMatch["id"]
    url = "https://www.cricbuzz.com/api/cricket-match/" + matchID + "/full-commentary/0"
    
    while not squadFoundFlag:
        response = requests.get(url, verify = False)
        commentaryList = response.json()["commentary"][0]["commentaryList"]

        players = ""

        for commentary in commentaryList:
            if "(playing xi)" in commentary["commText"].lower():
                players = players + commentary["commText"] + ","

        players = players.lower().replace("b0$ (playing xi): ", "").replace(", ",",").split(",")[:-1]
        for i in range(len(players)):
            if "(" in players[i]:
                players[i] = players[i][:players[i].index("(")]
                

        if not players:
            print("SQUAD NOT DECIDED YET!")
        else:
            squadFoundFlag = True


    return players # playersList
    

