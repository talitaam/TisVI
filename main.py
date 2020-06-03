import csv
import os
import time
from statistics import median
from math import ceil
from datetime import date, datetime
from datetime import timedelta


def writeInFinalCSV(fileNamePath, nameWithOwner, totalLoc, totalSloc, cc, miMultiFalse, miMultiTrue, difficulty, effort, timeHas, bugs):
    fileFinalTag = open(fileNamePath, 'a', newline='')
    finalTag = csv.writer(fileFinalTag)
    finalTag.writerow((nameWithOwner, str(totalLoc), str(totalSloc), str(cc), str(
        miMultiFalse), str(miMultiTrue), str(difficulty), str(effort), str(timeHas), str(bugs)))
    fileFinalTag.close()

def where_stop(filePath):
    row = 0
    if os.path.exists(filePath):
        fileFinal = open(filePath, 'r')
        row = sum(1 for line in csv.reader(fileFinal))
        fileFinal.close()
    return row


totalRepo = 0

path = "FinalCSV"

"""
nameWithOwner, 0
totalLoc, 4
totalSloc, 5
cc, 10
miMultiFalse, 12
miMultiTrue, 14
difficulty, 16
effort, 17
timeHas, 18
bugs 19
"""

daysInOneYear = timedelta(days=365)

for fileName in os.listdir("RepoTags"):
    if not os.path.exists(path):
        os.mkdir(path)
    totalRepo += 1
    fileRepo = "RepoTags/" + fileName
    totalRows = where_stop(fileRepo)
    print("\n\n----------- Novo Repo -------------")
    print("Lendo " + fileName)
    fileToRead = open(fileRepo, encoding='utf-8')
    repo = csv.reader(fileToRead)
    totalLocFile = []
    totalSlocFile = []
    ccFile = []
    miMultiFalseFile = []
    miMultiTrueFile = []
    difficultyFile = []
    effortFile = []
    timeHasFile = []
    bugsFile = []
    nameWithOwner = ""
    numLine = 0
    equivYear = 0
    actualDate = 0
    newDate = ""
    for node in repo:
        if numLine > 1:
            if (node[3].find('/') != -1):
                splitDate = node[3].split('/')
                formatedDate = str(splitDate[2]) + "-" + str(splitDate[1]) + "-" +str(splitDate[0])
                newDate = date.fromisoformat(formatedDate)
                print("")
                print(newDate)
            else:
                newDate = date.fromisoformat(str(node[3]))
                print("")
                print(newDate)
            if numLine == 2:
                nameWithOwner = node[0]
                actualDate = newDate
                equivYear = 1
                fileYear = str(equivYear) + '.csv'
                fileNamePath = os.path.join(path, fileYear)
                if not os.path.exists(fileNamePath):
                    fileFinal = open(fileNamePath, 'w', newline='')
                    final = csv.writer(fileFinal)
                    final.writerow(('nameWithOwner', 'totalLoc', 'totalSloc','cc', 
                    'miMultiFalse', 'miMultiTrue', 'difficulty', 'effort', 'timeHas', 'bugs'))
                    fileFinal.close()
            elif (newDate > actualDate) or numLine == totalRows:
                print("\n---Entrou no year - " + "year: " + str(newDate) + " actual year: " + str(actualDate))
                print("Ano " + str(equivYear) + " - Repo: " + nameWithOwner)
                #print("quantidade linhas: " + str(len(totalLocFile)))
                #time.sleep(2)
                if(totalLocFile):
                    print(totalLocFile)
                    #time.sleep(10)
                    print(median(totalLocFile))
                    #print(median(totalSlocFile))
                    #print(median(ccFile))
                    #print(median(miMultiFalseFile))
                    #print(median(miMultiTrueFile))
                    #print(median(difficultyFile))
                    #print(median(effortFile))
                    #print(median(timeHasFile))
                    #print(median(bugsFile))
                    print("")
                    writeInFinalCSV(fileNamePath, nameWithOwner, median(totalLocFile), median(totalSlocFile), median(ccFile), median(miMultiFalseFile), median(miMultiTrueFile), median(difficultyFile), median(effortFile), median(timeHasFile), median(bugsFile))
                #time.sleep(5)
                totalLocFile = []
                totalSlocFile = []
                ccFile = []
                miMultiFalseFile = []
                miMultiTrueFile = []
                difficultyFile = []
                effortFile = []
                timeHasFile = []
                bugsFile = []
                actualDate = newDate
                equivYear += 1
                fileYear = str(equivYear) + '.csv'
                fileNamePath = os.path.join(path, fileYear)
                if not os.path.exists(fileNamePath):
                    fileFinal = open(fileNamePath, 'w', newline='')
                    final = csv.writer(fileFinal)
                    final.writerow(('nameWithOwner', 'totalLoc', 'totalSloc','cc', 
                    'miMultiFalse', 'miMultiTrue', 'difficulty', 'effort', 'timeHas', 'bugs'))
                    fileFinal.close()
            if str(node[10]) != "-1":
                print("loc: " + str(node[4]) + " sloc: " + str(node[5]) + " cc: " + str(node[10]) + " miF: " + str(node[12]) + 
                " miT: " + str(node[14]) + "\ndif: " + str(node[16]) + " eff: " + str(node[17]) + " time: " + str(node[18]) + " bug: " + str(node[19]))
                #time.sleep(2)
                totalLocFile.append(float(node[4]))
                totalSlocFile.append(float(node[5]))
                ccFile.append(float(node[10]))
                miMultiFalseFile.append(float(node[12]))
                miMultiTrueFile.append(float(node[14]))
                difficultyFile.append(float(node[16]))
                effortFile.append(float(node[17]))
                timeHasFile.append(float(node[18]))
                bugsFile.append(float(node[19]))
            else:
                print("Not valid.")
            if numLine == totalRows-1:
                print("\n---Entrou numline - " + "numlines: " + str(numLine) + " total rows: " + str(totalRows))
                print("Ano " + str(equivYear) + " - Repo: " + nameWithOwner)
                #print("quantidade linhas: " + str(len(totalLocFile)))
                #time.sleep(2)
                if(totalLocFile):
                    print(totalLocFile)
                    #time.sleep(10)
                    print(median(totalLocFile))
                    #print(median(totalSlocFile))
                    #print(median(ccFile))
                    #print(median(miMultiFalseFile))
                    #print(median(miMultiTrueFile))
                    #print(median(difficultyFile))
                    #print(median(effortFile))
                    #print(median(timeHasFile))
                    #print(median(bugsFile))
                    writeInFinalCSV(fileNamePath, nameWithOwner, median(totalLocFile), median(totalSlocFile), median(ccFile), median(miMultiFalseFile), median(miMultiTrueFile), median(difficultyFile), median(effortFile), median(timeHasFile), median(bugsFile))
                time.sleep(5)
        numLine += 1
    fileToRead.close()
   
print("Total repos = ", totalRepo)
print("\n ------------- Fim da execução ------------- \n")
