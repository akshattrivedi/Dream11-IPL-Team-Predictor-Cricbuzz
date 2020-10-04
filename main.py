import urllib3

import cricbuzz_trends as cricbuzzTrends
import cricbuzz_live as cricbuzzLive
import predictor

teamWithURLIDsDict = {
    "Chennai Super Kings" : "58", "Royal Challengers Bangalore" : "59",
    "Delhi Capitals" : "61", "Mumbai Indians" : "62",
    "Kolkata Knight Riders" : "63", "Rajasthan Royals" : "64",
    "Kings XI Punjab" : "65", "Sunrisers Hyderabad" : "255"
    }

if __name__ == "__main__":
    print("DREAM 11")
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    currentIplMatch = cricbuzzLive.getCurrentIplMatch()
    print(currentIplMatch["team1"]["name"], "VS", currentIplMatch["team2"]["name"])
    print("TOSS:", currentIplMatch["toss"])

    currentMatchPlayersList = cricbuzzLive.getCurrentMatchPlayers(currentIplMatch)
    print("SQUAD PLAYERS:",currentMatchPlayersList)

    playersProfileAndStatistics = cricbuzzTrends.getAllPlayersProfileAndStatistics(teamWithURLIDsDict[currentIplMatch["team1"]["name"]], teamWithURLIDsDict[currentIplMatch["team2"]["name"]], currentMatchPlayersList)
    # print(json.dumps(playersProfileAndStatistics, indent=4))
    # print("LIST SIZE OF ALL PLAYERS: ",len(playersProfileAndStatistics))
    
    predictor.dream11Analyzer(playersProfileAndStatistics)
    

