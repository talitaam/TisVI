import csv
import os
import time
import math
import statistics
from statistics import median, mean
from math import ceil
from datetime import date, datetime
from datetime import timedelta
from numpy import quantile, median, max, min
import numpy as np


nameCSVreleases = "AnaliseFinalRelease.csv"
nameCSVrepo = "AnaliseFinalRepo.csv"

def writeCSVreleases(node, typeRelease, isFirstRow, isNotaMax, isLOCchanged, isMetricChanged, qtDias, porcValF, deltaLOC,
                     deltaSLOC, deltaMIF, deltaMIT, deltaDiff, deltaEff, deltaTimeH, deltaBug, deltaFiles, totalFiles):
    fileFinalTag = open(nameCSVreleases, 'a', newline='')
    finalTag = csv.writer(fileFinalTag, delimiter=';')
    finalTag.writerow((str(node[0]), str(node[2]), typeRelease, str(isFirstRow), str(isNotaMax), str(isLOCchanged),
     str(isMetricChanged), str(qtDias), str(porcValF).replace('.',','), str(deltaLOC), str(deltaSLOC), str(deltaMIF).replace('.',','), 
     str(deltaMIT).replace('.',','), str(deltaDiff).replace('.',','), str(deltaEff).replace('.',','), str(deltaTimeH).replace('.',','), 
     str(deltaBug).replace('.',','), str(deltaFiles), str(totalFiles)))
    fileFinalTag.close()

def writeCSVrepo(node, createdAt, countNV, countNM, countNF, countVR, totRel, contMetChange, countNotaMax, qtDias, porcValF, deltaLOC,
                     deltaSLOC, deltaMIF, deltaMIT, deltaDiff, deltaEff, deltaTimeH, deltaBug, deltaFiles, totalFiles):
    fileFinalTag = open(nameCSVrepo, 'a', newline='')
    finalTag = csv.writer(fileFinalTag, delimiter=';')
    finalTag.writerow((str(node[0]), createdAt, str(countNV), str(countNM), str(countNF), str(countVR), 
    str(totRel), str(contMetChange), str(countNotaMax), str(qtDias), str(porcValF).replace('.',','), 
    str(deltaLOC).replace('.',','), str(deltaSLOC).replace('.',','), 
    str(deltaMIF).replace('.',','), str(deltaMIT).replace('.',','), 
    str(deltaDiff).replace('.',','), str(deltaEff).replace('.',','), 
    str(deltaTimeH).replace('.',','), str(deltaBug).replace('.',','), 
    str(deltaFiles).replace('.',','), str(totalFiles).replace('.',',')))
    fileFinalTag.close()

def where_stop(filePath):
    row = 0
    if os.path.exists(filePath):
        fileFinal = open(filePath, 'r')
        row = sum(1 for line in csv.reader(fileFinal))
        fileFinal.close()
    return row

def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier

def round_half_away_from_zero(n, decimals=0):
    rounded_abs = round_half_up(abs(n), decimals)
    return math.copysign(rounded_abs, n)



"""
nameWithOwner, 0
tag, 2
published at, 3
totalLoc, 4
totalSloc, 5
miMultiFalse, 12
miMultiTrue, 14
difficulty, 16
effort, 17
timeHas, 18
bugs 19
totalFiles, 20
"""


totalRepo = 0

"""
data = [-2.15, 1.45, 4.35, -12.75] 
print("data = " + str(data))
#print(str(mean(data)))


rhaz_data = [round_half_away_from_zero(n, 1) for n in data]
print("rhaz_data = " + str(rhaz_data))
#print(str(mean(rhaz_data)))


data = [-2.1593, 1.4564, 4.3593, -12.7564] 
print("data = " + str(data))
#print(str(mean(data)))


rhaz_data = [round_half_away_from_zero(n, 1) for n in data]
print("rhaz_data = " + str(rhaz_data))
#print(str(mean(rhaz_data))

data = -34.54999999999999456662342
rhaz_data = np.around(data, decimals=1)
print("rhaz_data = " + str(rhaz_data))
print("rhaz_data = " + str(round(data,1)))

a=8.543
b=10.987

deltaMIF = np.around((((float(b) - float(a)) * 100) / float(a)), decimals=1)
print("deltaMIF = " + str(deltaMIF))
deltaMIF = np.around(deltaMIF, decimals=1)
print("deltaMIF np= " + str(deltaMIF))

c=3
totalFiles = 9
porcValF = ((int(c)/totalFiles)*100)
print("porcValF = " + str(porcValF))
porcValF = np.around(porcValF, decimals=1)
print("porcValF = " + str(porcValF))
if porcValF > 0:
    print("ok")

"""



if not os.path.isfile(nameCSVreleases):
    fileFinal = open(nameCSVreleases, 'w', newline='')
    final = csv.writer(fileFinal, delimiter=';')
    final.writerow(('nameWithOwner', 'tag', 'typeRelease','isFirstRow(bool)', 'isNotaMax(bool)',
                    'isLOCchanged(bool)', 'isMetricChanged(bool)', 'qtDias', 'porcValF(%)', 'deltaLOC(qtd)',
                     'deltaSLOC(qtd)', 'deltaMIF(%)', 'deltaMIT(%)', 'deltaDiff(%)', 'deltaEff(%)',
                      'deltaTimeH(%)', 'deltaBug(%)', 'deltaFiles(qtd)', 'totalFiles(qtd)'))
    fileFinal.close()

if not os.path.isfile(nameCSVrepo):
    fileFinal = open(nameCSVrepo, 'w', newline='')
    final = csv.writer(fileFinal, delimiter=';')
    final.writerow(('nameWithOwner', 'createdAt','countNV', 
                    'countNM', 'countNF', 'countVR', 'totRel(qtd)', 'countMetChange', 'countNotaMax', 
                    'qtDias', 'porcValF(%)', 'deltaLOC(qtd)',
                     'deltaSLOC(qtd)', 'deltaMIF(%)', 'deltaMIT(%)', 'deltaDiff(%)', 'deltaEff(%)', 'deltaTimeH(%)', 
                     'deltaBug(%)', 'deltaFiles(qtd)', 'totalFiles(qtd)'))
    fileFinal.close()


for fileName in os.listdir("RepoTags"):
    #if not os.path.exists(path):
        #os.mkdir(path)
    totalRepo += 1
    fileRepo = "RepoTags/" + fileName
    totalRows = where_stop(fileRepo)
    print("\n\n----------- Novo Repo -------------")
    print("Lendo " + fileName)
    fileToRead = open(fileRepo, encoding='utf-8')
    repo = csv.reader(fileToRead)
    countNV = 0
    countNM = 0
    countNF = 0
    countVR = 0
    totalReleases = 0
    contMetChange = 0
    countNotaMax = 0
    tLoc = []
    tSloc = []
    miF = []
    miT = []
    diff = []
    eff = []
    timeH = []
    bugs = []
    porcVF = []
    totalDeltaF = []
    totalF = []
    dias = []
    numLine = 0
    pastNode = ""
    actualDate = ""
    newDate = ""
    pastDate = ""
    pastTotalFiles = 0
    createdAt = ""
    for node in repo:
        typeRelease = "" # NV - not valid, NM - no metrics, NF - no files, VR - valid Release
        isFirstRow = 0
        isLOCchanged = 0
        isMetricChanged = 0
        isNotaMax = 0
        porcValF = 0
        deltaLOC = 0
        deltaSLOC = 0
        deltaMIF = 0
        deltaMIT = 0
        deltaDiff = 0
        deltaEff = 0
        deltaTimeH = 0
        deltaBug = 0
        deltaFiles = 0
        qtDias = 0
        totalFiles = 0
        if numLine > 0:
            if numLine == 1:
                totalReleases = int(node[2])
            print("")
            print(str(numLine))
            if (node[3].find('/') != -1):
                changeFormart = datetime.strptime(str(node[3]), "%m/%d/%Y")
                #print("changeFormart: " + str(changeFormart))
                newDate = date(changeFormart.year, changeFormart.month, changeFormart.day)
                #print("")
                #print("newYear: " + str(newDate))
            else:
                newDate = date.fromisoformat(str(node[3]))
                #print("")
                #print("newYear: " + str(newDate))
            if numLine == 1:
                totalReleases = int(node[2])
                createdAt = str(node[3])
            actualDate = newDate
            if numLine > 1:
                diasPastNode = actualDate - pastDate
                qtDias = diasPastNode.days
                dias.append(qtDias)
                #print("diasPastNode = " + str(diasPastNode.days))
                if numLine == 2:
                    isFirstRow = 1
                if len(node) == 20:
                    totalFiles = int(node[6]) + int(node[7]) + int(node[8]) + int(node[9])
                else:
                    totalFiles = int(node[20])
                if node[12] == "-1" or node[12] == "-2":
                    typeRelease = "NV"
                    totalFiles = 0
                    countNV += 1
                elif node[12] == "-3" and totalFiles > 0:
                    typeRelease = "NM"
                    countNM += 1
                elif node[12] == "-3":
                    typeRelease = "NF"
                    countNF += 1
                else:
                    countVR += 1
                    typeRelease = "VR"
                    if isFirstRow == 0 and pastNode and float(pastNode[14]) !=100 and float(pastNode[16]) != 0:
                        deltaLOC = int(node[4]) - int(pastNode[4])
                        deltaSLOC = int(node[5]) - int(pastNode[5])
                        deltaMIF = np.around((((float(node[12]) - float(pastNode[12])) * 100) / float(pastNode[12])), decimals=2)
                        deltaMIT = np.around((((float(node[14]) - float(pastNode[14])) * 100) / float(pastNode[14])), decimals=2)
                        deltaDiff = np.around((((float(node[16]) - float(pastNode[16])) * 100) / float(pastNode[16])), decimals=2)
                        deltaEff = np.around((((float(node[17]) - float(pastNode[17])) * 100) / float(pastNode[17])), decimals=2)
                        deltaTimeH = np.around((((float(node[18]) - float(pastNode[18])) * 100) / float(pastNode[18])), decimals=2)
                        deltaFiles = totalFiles - pastTotalFiles
                        deltaBug = np.around((((float(node[19]) - float(pastNode[19])) * 100) / float(pastNode[19])), decimals=2)
                        porcValF = np.around(((int(node[6])/totalFiles)*100), decimals=1)
                        if deltaLOC > 0:
                            isLOCchanged = 1
                        if deltaMIT != 0.000 or deltaDiff != 0.000 or deltaBug != 0.000:
                            isMetricChanged = 1
                            contMetChange += 1
                            tLoc.append(deltaLOC)
                            tSloc.append(deltaSLOC)
                            miF.append(deltaMIF)
                            miT.append(deltaMIT)
                            diff.append(deltaDiff)
                            eff.append(deltaEff)
                            timeH.append(deltaTimeH)
                            bugs.append(deltaBug)
                            porcVF.append(porcValF)
                            totalDeltaF.append(deltaFiles)
                            totalF.append(totalFiles)
                    if float(node[14])==100 and float(node[16])==0:
                        isNotaMax = 1
                        countNotaMax += 1
                    pastTotalFiles = totalFiles
                    pastNode = node
                writeCSVreleases(node, typeRelease, isFirstRow, isNotaMax, isLOCchanged, isMetricChanged, qtDias, porcValF, deltaLOC,
                     deltaSLOC, deltaMIF, deltaMIT, deltaDiff, deltaEff, deltaTimeH, deltaBug, deltaFiles, totalFiles)
            pastDate = newDate
        numLine +=1
    writeCSVrepo(node, createdAt, countNV, countNM, countNF, countVR, totalReleases, contMetChange, countNotaMax, qtDias, 
                (np.around(median(porcValF), decimals=2)), (np.around(median(tLoc), decimals=2)), 
                (np.around(median(tSloc), decimals=2)), (np.around(median(miF), decimals=2)), 
                (np.around(median(miT), decimals=2)), (np.around(median(diff), decimals=2)), 
                (np.around(median(eff), decimals=2)), (np.around(median(timeH), decimals=2)), 
                (np.around(median(bugs), decimals=2)), (np.around(median(totalDeltaF), decimals=2)), 
                (np.around(median(totalFiles), decimals=2)))



"""
            if numLine == 2:
                nameWithOwner = node[0]
                equivYear = 1
                actualDate = newDate
                pastDate = newDate
                print("newDate - actualDate: " + str(newDate - actualDate))
                print("")
                fileYear = str(equivYear) + '.csv'
                fileNamePath = os.path.join(path, fileYear)
                if not os.path.exists(fileNamePath):
                    fileFinal = open(fileNamePath, 'w', newline='')
                    final = csv.writer(fileFinal)
                    final.writerow(('nameWithOwner', 'totalLoc', 'totalSloc','cc', 
                    'miMultiFalse', 'miMultiTrue', 'difficulty', 'effort', 'timeHas', 'bugs'))
                    fileFinal.close()
            if ((newDate - actualDate) > daysInOneYear) or numLine == totalRows:
                print("\n---Entrou no year")
                print("newDate - actualDate: " + str(newDate - actualDate))
                print("Ano " + str(equivYear) + " - Repo: " + nameWithOwner)
                #print("quantidade linhas: " + str(len(totalLocFile)))
                #time.sleep(2)
        """