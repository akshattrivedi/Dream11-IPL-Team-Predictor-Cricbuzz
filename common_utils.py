from bs4 import BeautifulSoup
import requests

def beautifulSoup(url):
    response = requests.get(url, verify = False)
    return BeautifulSoup(response.content, features= 'lxml')

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