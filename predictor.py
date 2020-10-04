import common_utils as commonUtils

def dream11Analyzer(playerProfileAndStatisticsList):
    print("DREAM 11")
    batsmanDecidingFactor = "average"
    bowlerDecidingFactor  = "average"
    batsmanList = []
    bowlerList  = []


    for player in playerProfileAndStatisticsList:
        if player["role"].find("Bat") != -1:
            batsmanList.append(player)
        elif player["role"].find("Bowl") != -1:
            bowlerList.append(player)

    commonUtils.bubblesort(batsmanList, "bat", batsmanDecidingFactor, False)
    commonUtils.bubblesort(bowlerList, "bowl", bowlerDecidingFactor, True)

    print("<------------------- BATSMAN ------------------->")
    print("NAME\t\t\tAVERAGE")
    for batsman in batsmanList:
        print(batsman["name"],"\t\t",batsman["bat"][batsmanDecidingFactor])

    print()
    print("<------------------- BOWLER ------------------->")
    print("NAME\t\t\tAVERAGE")
    for bowler in bowlerList:
        print(bowler["name"],"\t\t",bowler["bowl"][bowlerDecidingFactor])
