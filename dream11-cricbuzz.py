import json
import requests
import urllib3
from pycricbuzz import Cricbuzz
from bs4 import BeautifulSoup

teamWithURLIDsDict = {
    "Chennai Super Kings" : "58", "Royal Challengers Bangalore" : "59",
    "Delhi Capitals" : "61", "Mumbai Indians" : "62",
    "Kolkata Knight Riders" : "63", "Rajasthan Royals" : "64",
    "Kings XI Punjab" : "65", "Sunrisers Hyderabad" : "255"
    }

def getCurrentIplMatch():
    cricbuzz = Cricbuzz()
    matches = cricbuzz.matches()
    maxMatchNum = None
    currentIplMatch = {}

    for match in matches:
        if match["srs"] == "Indian Premier League 2020" and match["toss"] != "" :
            matchNumber = ""
            numbers = [letter for letter in list(match["mnum"]) if letter.isdigit()]
            for number in numbers:
                matchNumber = matchNumber + number
            matchNumber = int(matchNumber)

            if maxMatchNum is None:
                maxMatchNum = matchNumber
                currentIplMatch = match
            elif matchNumber > maxMatchNum:
                maxMatchNum = matchNumber
                currentIplMatch = match

    return currentIplMatch

def getCurrentMatchPlayers(iplMatch):
    return iplMatch["team1"]["squad"] + iplMatch["team2"]["squad"]

def getPlayerStat(htmlTag):
    return 0 if htmlTag.text == "-" or htmlTag.text == "" else htmlTag.text

def getPlayerProfileAndStatistics(href):
    url = "https://www.cricbuzz.com" + href
    # print(url)
    #Connection to web page
    response = requests.get(url, verify = False)

    soup = BeautifulSoup(response.content, features= 'lxml')

    playerName = soup.select("#playerProfile > div:nth-of-type(1) > div:nth-of-type(2) > h1")[0].string
    playerRole = soup.select("#playerProfile > div:nth-of-type(2) > div:nth-of-type(1) > div > div:nth-of-type(9)")[0].string

    trs = soup.findAll("tr")
    counter = 0

    # BATTING INIT VARIABLES
    batMatches, batInnings, NO, batRuns, highest, batAverage, batStrikeRate, hundreds, fifties, fours, sixes = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

    # BOWLING INIT VARIABLES
    bowlMatches, bowlInnings, balls, bowlRuns, wickets, economy, bowlAverage, bowlStrikeRate, fiveWicket, tenWicket = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

    for tr in trs:
        try:
            matchType = tr.td.strong.string
        except AttributeError:
            continue

        if matchType == "IPL" and counter == 0: # BATTING STATS
            tds = tr.findAll("td")

            batMatches = int(getPlayerStat(tds[1]))
            batInnings = int(getPlayerStat(tds[2]))
            NO = int(getPlayerStat(tds[3]))
            batRuns = int(getPlayerStat(tds[4]))
            highest = int(getPlayerStat(tds[5]))
            batAverage = float(getPlayerStat(tds[6]))
            batStrikeRate = float(getPlayerStat(tds[8]))
            hundreds = int(getPlayerStat(tds[9]))
            fifties = int(getPlayerStat(tds[11]))
            fours = int(getPlayerStat(tds[12]))
            sixes = int(getPlayerStat(tds[13]))


        if matchType == "IPL" and counter == 1: # BOWLING STATS
            tds = tr.findAll("td")

            bowlMatches = int(getPlayerStat(tds[1]))
            bowlInnings = int(getPlayerStat(tds[2]))
            balls = int(getPlayerStat(tds[3]))
            bowlRuns = int(getPlayerStat(tds[4]))
            wickets = int(getPlayerStat(tds[5]))
            economy = float(getPlayerStat(tds[8]))
            bowlAverage = float(getPlayerStat(tds[9]))
            bowlStrikeRate = float(getPlayerStat(tds[10]))
            fiveWicket = int(getPlayerStat(tds[11]))
            tenWicket = int(getPlayerStat(tds[12]))

        if matchType == 'IPL':
            counter = counter + 1
    
    return {
        "name" : playerName,
        "role" : playerRole,
        "bat" : {
            "matches"   : batMatches,
            "innings"   : batInnings,
            "no"        : NO,
            "runs"      : batRuns,
            "highest"   : highest,
            "average"   : batAverage,
            "strikerate": batStrikeRate,
            "hundreds"  : hundreds,
            "fifties"   : fifties,
            "fours"     : fours,
            "sixes"     : sixes
        },
        "bowl" : {
            "matches"   : bowlMatches,
            "innings"   : bowlInnings,
            "balls"     : balls,
            "runs"      : bowlRuns,
            "wickets"   : wickets,
            "economy"   : economy,
            "average"   : bowlAverage,
            "strikerate": bowlStrikeRate,
            "fivewicket": fiveWicket,
            "tenwicket" : tenWicket
        }
    }

def getAllPlayersProfileAndStatistics(teamAUrlId, teamBUrlId, currentMatchPlayers):
    teamsUrlIds = [teamAUrlId, teamBUrlId]
    allPlayersProfileAndStatsList = []

    teamCount = 1
    for teamUrlId in teamsUrlIds:
        squadUrl = "https://www.cricbuzz.com/cricket-team/blah-blah/" + teamUrlId + "/players"
        response = requests.get(squadUrl, verify = False)
        soup = BeautifulSoup(response.content, features= 'lxml')

        atags = soup.findAll("a")

        counter = 0
        for a in atags:
            if a.has_attr("href") and "profiles" in a["href"] and squadPlayersToProfileMapping(currentMatchPlayers, a.text):
                counter = counter + 1
        teamSize = counter
        # print("Team Size:",teamSize)
        printProgressBar(0, teamSize, prefix = 'Fetching Data for Team' + str(teamCount) + ' :', suffix = 'Complete', length = 50)

        counter = 0
        for a in atags:
            if a.has_attr("href") and "profiles" in a["href"] and squadPlayersToProfileMapping(currentMatchPlayers, a.text):
                playerProfileAndStatistics = getPlayerProfileAndStatistics(a["href"])
                allPlayersProfileAndStatsList.append(playerProfileAndStatistics)
                # print(json.dumps(playerProfileAndStatistics,indent=4))
                printProgressBar(counter + 1, teamSize, prefix = 'Fetching Data for Team' + str(teamCount) + ' :', suffix = 'Complete', length = 50)
                counter = counter + 1
        
        teamCount = teamCount + 1

    return allPlayersProfileAndStatsList

def squadPlayersToProfileMapping(currentMatchPlayersList, playerProfileName):
    for currentMatchPlayer in currentMatchPlayersList:
        if playerProfileName.lower().find(currentMatchPlayer.lower()) != -1:
            # print(playerProfileName) # EACH Player Debugger
            return True

    return False


def dream11Analyzer(playerProfileAndStatisticsList):
    print("\nDREAM 11")
    batsmanDecidingFactor = "average"
    bowlerDecidingFactor  = "average"
    batsmanList = []
    bowlerList  = []


    for player in playerProfileAndStatisticsList:
        if player["role"].find("Bat") != -1:
            batsmanList.append(player)
        elif player["role"].find("Bowl") != -1:
            bowlerList.append(player)

    bubblesort(batsmanList, "bat", batsmanDecidingFactor, False)
    bubblesort(bowlerList, "bowl", bowlerDecidingFactor, True)

    print()
    print("<------------------- BATSMAN ------------------->")
    print("NAME\t\t\tAVERAGE")
    for batsman in batsmanList:
        print(batsman["name"],"\t\t",batsman["bat"][batsmanDecidingFactor])

    print()
    print("<------------------- BOWLER ------------------->")
    print("NAME\t\t\tAVERAGE")
    for bowler in bowlerList:
        print(bowler["name"],"\t\t",bowler["bowl"][bowlerDecidingFactor])


def bubblesort(list, playerType, decidingFactor, ascendingFlag):
    for iter_num in range(len(list)-1,0,-1):
        for idx in range(iter_num):
            if ascendingFlag and list[idx][playerType][decidingFactor] > list[idx+1][playerType][decidingFactor]:
                temp = list[idx]
                list[idx] = list[idx+1]
                list[idx+1] = temp
            elif (not ascendingFlag) and list[idx][playerType][decidingFactor] < list[idx+1][playerType][decidingFactor]:
                temp = list[idx]
                list[idx] = list[idx+1]
                list[idx+1] = temp

        
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()




if __name__ == "__main__":
    print("DREAM 11")
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    currentIplMatch = getCurrentIplMatch()
    print(currentIplMatch["team1"]["name"], "VS", currentIplMatch["team2"]["name"])
    print("TOSS:", currentIplMatch["toss"])

    currentMatchPlayers = getCurrentMatchPlayers(currentIplMatch)
    print("SQUAD PLAYERS:",currentMatchPlayers)

    playersProfileAndStatistics = getAllPlayersProfileAndStatistics(teamWithURLIDsDict[currentIplMatch["team1"]["name"]], teamWithURLIDsDict[currentIplMatch["team2"]["name"]], currentMatchPlayers)
    # print(json.dumps(playersProfileAndStatistics, indent=4))
    # print("LIST SIZE OF ALL PLAYERS: ",len(playersProfileAndStatistics))
    
    dream11Analyzer(playersProfileAndStatistics)
    

