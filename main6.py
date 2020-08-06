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





def writeCSVrepo(nameWithOwner, createdAt, countNV, countNM, countNF, countVR, totRel, contMetChange, countNotaMax, 
                porcValF, diasLastRel, diasLastChanged, qtDiasLastFirst, deltaLOC, deltaSLOC, deltaMIF, 
                deltaMIT, deltaDiff, deltaEff, deltaTimeH, deltaBug, deltaFiles, totalFiles):
    fileFinalTag = open(nameCSVrepo, 'a', newline='')
    finalTag = csv.writer(fileFinalTag, delimiter=';')
    finalTag.writerow((nameWithOwner, createdAt, str(countNV), str(countNM), str(countNF), str(countVR), 
    str(totRel), str(contMetChange), str(countNotaMax), str(porcValF).replace('.',','), 
    str(diasLastRel).replace('.',','), str(diasLastChanged).replace('.',','), str(qtDiasLastFirst),
    str(deltaLOC), str(deltaSLOC), str(deltaMIF).replace('.',','), str(deltaMIT).replace('.',','), 
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


#if not os.path.isfile(nameCSVrepo):
fileFinal = open(nameCSVrepo, 'w', newline='')
final = csv.writer(fileFinal, delimiter=';')
final.writerow(('nameWithOwner', 'createdAt','countNV', 'countNM', 'countNF', 'countVR', 'totRel(qtd)', 
                    'countMetChange', 'countNotaMax', 'porcValF(%)(med)', 'qtDiasEntreRel(med)', 
                    'qtDiasEntreChangedRel(med)', 'qtDiasLastFirst', 'deltaLOC(qtd)','deltaSLOC(qtd)', 
                    'deltaMIF', 'deltaMIT', 'deltaDiff', 'deltaEff', 'deltaTimeH', 'deltaBug', 
                    'deltaFiles(qtd)', 'totalFiles(qtd)(med)'))
fileFinal.close()


for fileName in os.listdir("RepoTags"):
    #if not os.path.exists(path):
        #os.mkdir(path)
    fileRepo = "RepoTags/" + fileName
    totalRows = where_stop(fileRepo)
    print("\n\n----------- Novo Repo -------------")
    print("Lendo " + fileName)
    print("total rows: " + str(totalRows))
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
    numLine = 0
    porcVF = []
    totalF = []
    pastNode = ""
    actualDate = ""
    newDate = ""
    pastDate = ""
    pastChangedDate = ""
    pastTotalFiles = 0
    createdAt = ""
    diasLastRel = []
    diasLastChanged = []
    firstNode = []
    lastNode = []
    firstDate = "" 
    lastDate = ""
    totFilesFirst = 0
    totFilesLast = 0
    nameWithOwner = ""
    for node in sortedlist:
        #print(node[2] + " - " + node[3])
        typeRelease = "" # NV - not valid, NM - no metrics, NF - no files, VR - valid Release
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
        if numLine >= 0 and node[3] != "publishedAt":
            #print(str(numLine))
            if numLine == 0:
                totalReleases = int(node[2])
                createdAt = str(node[3])
                nameWithOwner = node[0]
            if (node[3].find('/') != -1):
                changeFormart = datetime.strptime(str(node[3]), "%m/%d/%Y")
                newDate = date(changeFormart.year, changeFormart.month, changeFormart.day)
            else:
                newDate = date.fromisoformat(str(node[3]))
            actualDate = newDate
            if numLine > 0:
                diasPastNode = actualDate - pastDate
                qtDias = diasPastNode.days
                if len(node) == 20:
                    totalFiles = int(node[6]) + int(node[7]) + int(node[8]) + int(node[9])
                else:
                    totalFiles = int(node[20])
                if node[12] == "-1" or node[12] == "-2":
                    totalFiles = 0
                    countNV += 1
                elif node[12] == "-3" and totalFiles > 0:
                    countNM += 1
                elif node[12] == "-3":
                    countNF += 1
                else:
                    countVR += 1
                    if not pastNode:
                        pastChangedDate = actualDate
                        firstNode = node
                        firstDate = actualDate
                        totFilesFirst = totalFiles
                    if pastNode:
                        lastNode = node
                        lastDate = actualDate
                        totFilesLast = totalFiles
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
                        deltaMIF = np.around((((float(node[12]) - float(pastNode[12])) * 100) / float(pastNode[12])), decimals=3)
                        deltaMIT = np.around((((float(node[14]) - float(pastNode[14])) * 100) / float(pastNode[14])), decimals=3)
                        deltaDiff = np.around((((float(node[16]) - float(pastNode[16])) * 100) / pastNode16), decimals=4)
                        deltaEff = np.around((((float(node[17]) - float(pastNode[17])) * 100) / pastNode17), decimals=4)
                        deltaTimeH = np.around((((float(node[18]) - float(pastNode[18])) * 100) / pastNode18), decimals=4)
                        deltaBug = np.around((((float(node[19]) - float(pastNode[19])) * 100) / pastNode19), decimals=5)
                        """
                        deltaMIF = np.around((float(node[12]) - float(pastNode[12])), decimals=3)
                        deltaMIT = np.around((float(node[14]) - float(pastNode[14])), decimals=3)
                        deltaDiff = np.around((float(node[16]) - float(pastNode[16])), decimals=4)
                        deltaEff = np.around((float(node[17]) - float(pastNode[17])), decimals=4)
                        deltaTimeH = np.around((float(node[18]) - float(pastNode[18])), decimals=4)
                        deltaBug = np.around((float(node[19]) - float(pastNode[19])), decimals=5)
                        """                    
                        if deltaSLOC != 0:
                            isSLOCchanged = 1
                        if deltaSLOC != 0.000 or deltaMIF != 0.000 or deltaMIT != 0.000 or deltaDiff != 0.000 or deltaEff != 0.000 or deltaTimeH!= 0.000 or deltaBug != 0.000:
                            contMetChange += 1
                            diasPastChangedNode = actualDate - pastChangedDate
                            qtDiasLastChanged = diasPastChangedNode.days
                            diasLastChanged.append(qtDiasLastChanged)
                            pastChangedDate = actualDate
                    if float(node[14])==100 and float(node[17])==0 and float(node[19])==0:
                        countNotaMax += 1
                    porcValF = np.around(((int(node[6])/totalFiles)*100), decimals=1)
                    porcVF.append(porcValF)
                    totalF.append(totalFiles)
                    pastNode = node
                diasLastRel.append(qtDias)
            pastDate = newDate
        numLine +=1
    deltaLOC = 0
    deltaSLOC = 0
    deltaMIF = 0
    deltaMIT = 0
    deltaDiff = 0
    deltaEff = 0
    deltaTimeH = 0
    deltaBug = 0
    deltaFiles = 0
    if firstNode and lastNode:
        if float(firstNode[16]) == 0.0000:
            firstNode16 = 100
        else:
            firstNode16 = float(firstNode[16])
        if float(firstNode[17]) == 0.0000:
            firstNode17 = 100 
        else:
            firstNode17 = float(firstNode[17])
        if float(firstNode[18]) == 0.0000:
            firstNode18 = 100
        else:
            firstNode18 = float(firstNode[18])
        if float(firstNode[19]) == 0.0000:
            firstNode19 = 100
        else:
            firstNode19 = float(firstNode[19])
        deltaLOC = int(lastNode[4]) - int(firstNode[4])
        deltaSLOC = int(lastNode[5]) - int(firstNode[5])
        deltaMIF = np.around((((float(lastNode[12]) - float(firstNode[12])) * 100) / float(firstNode[12])), decimals=3)
        deltaMIT = np.around((((float(lastNode[14]) - float(firstNode[14])) * 100) / float(firstNode[14])), decimals=3)
        deltaDiff = np.around((((float(lastNode[16]) - float(firstNode[16])) * 100) / firstNode16), decimals=4)
        deltaEff = np.around((((float(lastNode[17]) - float(firstNode[17])) * 100) / firstNode17), decimals=4)
        deltaTimeH = np.around((((float(lastNode[18]) - float(firstNode[18])) * 100) / firstNode18), decimals=4)
        deltaBug = np.around((((float(lastNode[19]) - float(firstNode[19])) * 100) / firstNode19), decimals=4)
        """
        deltaMIF = np.around((float(node[12]) - float(pastNode[12])), decimals=3)
        deltaMIT = np.around((float(node[14]) - float(pastNode[14])), decimals=3)
        deltaDiff = np.around((float(node[16]) - float(pastNode[16])), decimals=4)
        deltaEff = np.around((float(node[17]) - float(pastNode[17])), decimals=4)
        deltaTimeH = np.around((float(node[18]) - float(pastNode[18])), decimals=4)
        deltaBug = np.around((float(node[19]) - float(pastNode[19])), decimals=5)
        """
        deltaFiles = totFilesLast - totFilesFirst
        diasPastNode = lastDate - firstDate
        qtDiasLastFirst = diasPastNode.days     
    writeCSVrepo(nameWithOwner, createdAt, countNV, countNM, countNF, countVR, totalReleases, contMetChange, countNotaMax,
                (np.around(median(porcVF), decimals=2)),(np.around(median(diasLastRel), decimals=2)), 
                (np.around(median(diasLastChanged), decimals=2)), qtDiasLastFirst, 
                deltaLOC, deltaSLOC, deltaMIF, deltaMIT, deltaDiff, deltaEff, deltaTimeH, deltaBug, 
                deltaFiles, (np.around(median(totalF), decimals=2)))

print("_____________________FIM Execução__________________________")