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
import operator


nameCSVreleases = "AnaliseFinalRelease.csv"
nameCSVrepo = "AnaliseFinalRepo.csv"

def writeCSVreleases(node, typeRelease, isFirstRow, isNotaMax, isSLOCchanged, isMetricChanged, qtDias, qtDiasChangedRel, 
                    porcValF, deltaLOC,deltaSLOC, deltaMIF, deltaMIT, deltaDiff, deltaEff, deltaTimeH, deltaBug, 
                    deltaFiles, totalFiles):
    fileFinalTag = open(nameCSVreleases, 'a', newline='')
    finalTag = csv.writer(fileFinalTag, delimiter=';')
    finalTag.writerow((str(node[0]), str(node[2]), typeRelease, str(isFirstRow), str(isNotaMax), str(isSLOCchanged),
     str(isMetricChanged), str(qtDias), str(qtDiasChangedRel), str(porcValF).replace('.',','), str(deltaLOC), 
     str(deltaSLOC), str(deltaMIF).replace('.',','), str(deltaMIT).replace('.',','), str(deltaDiff).replace('.',','), 
     str(deltaEff).replace('.',','), str(deltaTimeH).replace('.',','), str(deltaBug).replace('.',','), 
     str(deltaFiles), str(totalFiles)))
    fileFinalTag.close()

def writeCSVrepo(node, createdAt, countNV, countNM, countNF, countVR, totRel, contMetChange, countNotaMax, qtDias, 
                qtDiasChangedRel, porcValF, deltaLOC,deltaSLOC, deltaMIF, deltaMIT, deltaDiff, deltaEff, deltaTimeH, 
                deltaBug, deltaFiles, totalFiles):
    fileFinalTag = open(nameCSVrepo, 'a', newline='')
    finalTag = csv.writer(fileFinalTag, delimiter=';')
    finalTag.writerow((str(node[0]), createdAt, str(countNV), str(countNM), str(countNF), str(countVR), 
    str(totRel), str(contMetChange), str(countNotaMax), str(qtDias).replace('.',','), 
    str(qtDiasChangedRel).replace('.',','), str(porcValF).replace('.',','), 
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

#if not os.path.isfile(nameCSVreleases):
fileFinal = open(nameCSVreleases, 'w', newline='')
final = csv.writer(fileFinal, delimiter=';')
final.writerow(('nameWithOwner', 'tag', 'typeRelease','isFirstRow(bool)', 'isNotaMax(bool)',
                    'isSLOCchanged(bool)', 'isMetricChanged(bool)', 'qtDias', 'qtDiasChangedRel', 'porcValF(%)', 
                    'deltaLOC(qtd)', 'deltaSLOC(qtd)', 'deltaMIF', 'deltaMIT', 'deltaDiff', 'deltaEff',
                    'deltaTimeH', 'deltaBug', 'deltaFiles(qtd)', 'totalFiles(qtd)'))
fileFinal.close()

#if not os.path.isfile(nameCSVrepo):
fileFinal = open(nameCSVrepo, 'w', newline='')
final = csv.writer(fileFinal, delimiter=';')
final.writerow(('nameWithOwner', 'createdAt','countNV', 'countNM', 'countNF', 'countVR', 'totRel(qtd)', 
                    'countMetChange', 'countNotaMax', 'qtDiasLastRel', 'qtDiasChangedRel', 'porcValF(%)', 
                    'deltaLOC(qtd)','deltaSLOC(qtd)', 'deltaMIF', 'deltaMIT', 'deltaDiff', 'deltaEff', 
                    'deltaTimeH', 'deltaBug', 'deltaFiles(qtd)', 'totalFiles(qtd)'))
fileFinal.close()


for fileName in os.listdir("RepoTags"):
    #if not os.path.exists(path):
        #os.mkdir(path)
    fileRepo = "RepoTags/" + fileName
    totalRows = where_stop(fileRepo)
    print("\n\n----------- Novo Repo -------------")
    print("Lendo " + fileName)
    fileToRead = open(fileRepo, encoding='utf-8')
    repo = csv.reader(fileToRead)
    sortedlist = sorted(repo, key=operator.itemgetter(3))
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
    diasLastRel = []
    diasLastChanged = []
    numLine = 0
    pastNode = ""
    actualDate = ""
    newDate = ""
    pastDate = ""
    pastChangedDate = ""
    pastTotalFiles = 0
    createdAt = ""
    firstValidRelease = False
    for node in sortedlist:
        typeRelease = "" # NV - not valid, NM - no metrics, NF - no files, VR - valid Release
        isFirstRow = 0
        isSLOCchanged = 0
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
        qtDiasLastChanged = 0
        totalFiles = 0
        firstNode = []
        if numLine >= 0 and node[3] != "publishedAt":
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
            if numLine == 0:
                totalReleases = int(node[2])
                createdAt = str(node[3])
            actualDate = newDate
            if numLine > 0:
                diasPastNode = actualDate - pastDate
                qtDias = diasPastNode.days
                #print("diasPastNode = " + str(diasPastNode.days))
                #if numLine == 2:
                    #isFirstRow = 1
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
                    if not pastNode:
                        pastChangedDate = actualDate
                        porcValF = np.around(((int(node[6])/totalFiles)*100), decimals=1)
                        isFirstRow = 1
                    if isFirstRow == 0 and pastNode:
                        if float(pastNode[16]) == 0.0000:
                            pastNode16 = 100
                        else:
                            pastNode16 = float(pastNode[16])
                        if float(pastNode[17]) == 0.0000:
                            pastNode17 = 100
                        else:
                            pastNode17 = float(pastNode[17])
                        if float(pastNode[18]) == 0.0000:
                            pastNode18 = 100
                        else:
                            pastNode18 = float(pastNode[18])
                        if float(pastNode[19]) == 0.0000:
                            pastNode19 = 100
                        else:
                            pastNode19 = float(pastNode[19])
                        deltaLOC = int(node[4]) - int(pastNode[4])
                        deltaSLOC = int(node[5]) - int(pastNode[5])
                        deltaMIF = np.around((((float(node[12]) - float(pastNode[12])) * 100) / float(pastNode[12])), decimals=2)
                        deltaMIT = np.around((((float(node[14]) - float(pastNode[14])) * 100) / float(pastNode[14])), decimals=2)
                        deltaDiff = np.around((((float(node[16]) - float(pastNode[16])) * 100) / pastNode16), decimals=2)
                        deltaEff = np.around((((float(node[17]) - float(pastNode[17])) * 100) / pastNode17), decimals=2)
                        deltaTimeH = np.around((((float(node[18]) - float(pastNode[18])) * 100) / pastNode18), decimals=2)
                        deltaBug = np.around((((float(node[19]) - float(pastNode[19])) * 100) / pastNode19), decimals=2)
                        """
                        deltaMIF = np.around((float(node[12]) - float(pastNode[12])), decimals=3)
                        deltaMIT = np.around((float(node[14]) - float(pastNode[14])), decimals=3)
                        deltaDiff = np.around((float(node[16]) - float(pastNode[16])), decimals=4)
                        deltaEff = np.around((float(node[17]) - float(pastNode[17])), decimals=4)
                        deltaTimeH = np.around((float(node[18]) - float(pastNode[18])), decimals=4)
                        deltaBug = np.around((float(node[19]) - float(pastNode[19])), decimals=5)
                        """
                        deltaFiles = totalFiles - pastTotalFiles
                        porcValF = np.around(((int(node[6])/totalFiles)*100), decimals=1)                        
                        if deltaSLOC != 0:
                            isSLOCchanged = 1
                        if deltaSLOC != 0.000 or deltaMIF != 0.000 or deltaMIT != 0.000 or deltaDiff != 0.000 or deltaEff != 0.000 or deltaTimeH!= 0.000 or deltaBug != 0.000:
                            #if firstValidRelease == True:
                            diasPastChangedNode = actualDate - pastChangedDate
                            qtDiasLastChanged = diasPastChangedNode.days
                            diasLastChanged.append(qtDiasLastChanged)
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
                            totalDeltaF.append(deltaFiles)
                            totalF.append(totalFiles)
                            pastChangedDate = actualDate
                            porcVF.append(porcValF)
                    if float(node[14])==100 and float(node[16])==0:
                        isNotaMax = 1
                        countNotaMax += 1
                    pastTotalFiles = totalFiles
                    pastNode = node
                diasLastRel.append(qtDias)
                writeCSVreleases(node, typeRelease, isFirstRow, isNotaMax, isSLOCchanged, isMetricChanged, qtDias, 
                                qtDiasLastChanged, porcValF, deltaLOC,deltaSLOC, deltaMIF, deltaMIT, deltaDiff, 
                                deltaEff, deltaTimeH, deltaBug, deltaFiles, totalFiles)
            pastDate = newDate
        numLine +=1
    writeCSVrepo(node, createdAt, countNV, countNM, countNF, countVR, totalReleases, contMetChange, countNotaMax, 
                (np.around(median(diasLastRel), decimals=2)), (np.around(median(diasLastChanged), decimals=2)),
                (np.around(median(porcVF), decimals=2)), (np.around(median(tLoc), decimals=2)), 
                (np.around(median(tSloc), decimals=2)), (np.around(median(miF), decimals=3)), 
                (np.around(median(miT), decimals=3)), (np.around(median(diff), decimals=4)), 
                (np.around(median(eff), decimals=4)), (np.around(median(timeH), decimals=4)), 
                (np.around(median(bugs), decimals=4)), (np.around(median(totalDeltaF), decimals=2)), 
                (np.around(median(totalFiles), decimals=2)))

print("_____________________FIM Execução__________________________")