import common_utils as commonUtils

def getAllPlayersProfileAndStatistics(teamAUrlId, teamBUrlId, currentMatchPlayers):
    teamsUrlIds = [teamAUrlId, teamBUrlId]
    allPlayersProfileAndStatsList = []

    teamCount = 1
    for teamUrlId in teamsUrlIds:
        squadUrl = "https://www.cricbuzz.com/cricket-team/blah-blah/" + teamUrlId + "/players"
        soup = commonUtils.beautifulSoup(squadUrl)

        atags = soup.findAll("a")

        counter = 0
        for a in atags:
            if a.has_attr("href") and "profiles" in a["href"] and squadPlayersToProfileMapping(currentMatchPlayers, a.text):
                counter = counter + 1
        teamSize = counter
        # print("Team Size:",teamSize)
        commonUtils.printProgressBar(0, teamSize, prefix = 'Fetching Data for Team' + str(teamCount) + ' :', suffix = 'Complete', length = 50)

        counter = 0
        for a in atags:
            if a.has_attr("href") and "profiles" in a["href"] and squadPlayersToProfileMapping(currentMatchPlayers, a.text):
                playerProfileAndStatistics = getPlayerProfileAndStatistics(a["href"])
                allPlayersProfileAndStatsList.append(playerProfileAndStatistics)
                # print(json.dumps(playerProfileAndStatistics,indent=4))
                commonUtils.printProgressBar(counter + 1, teamSize, prefix = 'Fetching Data for Team' + str(teamCount) + ' :', suffix = 'Complete', length = 50)
                counter = counter + 1
        
        teamCount = teamCount + 1

    return allPlayersProfileAndStatsList


def getPlayerProfileAndStatistics(href):
    url = "https://www.cricbuzz.com" + href
    soup = commonUtils.beautifulSoup(url)

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

def squadPlayersToProfileMapping(currentMatchPlayersList, playerProfileName):
    for currentMatchPlayer in currentMatchPlayersList:
        # print(playerProfileName,currentMatchPlayer) # EACH Player Debugger
        if playerProfileName.lower().find(currentMatchPlayer.lower()) != -1:
            return True

    return False

def getPlayerStat(htmlTag):
    return 0 if htmlTag.text == "-" or htmlTag.text == "" else htmlTag.text
