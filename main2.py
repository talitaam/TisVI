import csv
import os
import time
from statistics import median
from math import ceil
from numpy import quantile, median, max, min


def writeInFinalCSV(fileNamePath, ano, q1, valor, q3, qtd):
    fileFinalTag = open(fileNamePath, 'a', newline='')
    finalTag = csv.writer(fileFinalTag)
    finalTag.writerow((str(ano), str(q1), str(valor), str(q3),str(qtd)))
    fileFinalTag.close()

def where_stop(filePath):
    row = 0
    if os.path.exists(filePath):
        fileFinal = open(filePath, 'r')
        row = sum(1 for line in csv.reader(fileFinal))
        fileFinal.close()
    return row


path = "FinalMetrics"

metrics = {"1": "totalLoc.csv", 
        "2": "totalSloc.csv", 
        "3": "cc.csv", 
        "4": "miMultiFalse.csv", 
        "5": "miMultiTrue.csv", 
        "6": "difficulty.csv", 
        "7": "effort.csv", 
        "8": "timeHas.csv", 
        "9": "bugs.csv"}

for fileName in os.listdir("FinalCSV"):
    if not os.path.exists(path):
        os.mkdir(path)
    fileRepo = "FinalCSV/" + fileName
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
    numLine = 0
    for node in repo:
        if numLine > 0 and str(node[1]) != "-1":
            totalLocFile.append(float(node[1]))
            totalSlocFile.append(float(node[2]))
            ccFile.append(float(node[3]))
            miMultiFalseFile.append(float(node[4]))
            miMultiTrueFile.append(float(node[5]))
            difficultyFile.append(float(node[6]))
            effortFile.append(float(node[7]))
            timeHasFile.append(float(node[8]))
            bugsFile.append(float(node[9]))
        if numLine == totalRows-1:
            values = {"1": str(median(totalLocFile)), 
                    "2": str(median(totalSlocFile)), 
                    "3": str(median(ccFile)), 
                    "4": str(median(miMultiFalseFile)), 
                    "5": str(median(miMultiTrueFile)), 
                    "6": str(median(difficultyFile)), 
                    "7": str(median(effortFile)), 
                    "8": str(median(timeHasFile)), 
                    "9": str(median(bugsFile))}
            quar1 = {"1": str(quantile(totalLocFile,.25)), 
                    "2": str(quantile(totalSlocFile,.25)), 
                    "3": str(quantile(ccFile,.25)), 
                    "4": str(quantile(miMultiFalseFile,.25)), 
                    "5": str(quantile(miMultiTrueFile,.25)), 
                    "6": str(quantile(difficultyFile,.25)), 
                    "7": str(quantile(effortFile,.25)), 
                    "8": str(quantile(timeHasFile,.25)), 
                    "9": str(quantile(bugsFile,.25))} 
            quar3 = {"1": str(quantile(totalLocFile,.75)), 
                    "2": str(quantile(totalSlocFile,.75)), 
                    "3": str(quantile(ccFile,.75)), 
                    "4": str(quantile(miMultiFalseFile,.75)), 
                    "5": str(quantile(miMultiTrueFile,.75)), 
                    "6": str(quantile(difficultyFile,.75)), 
                    "7": str(quantile(effortFile,.75)), 
                    "8": str(quantile(timeHasFile,.75)), 
                    "9": str(quantile(bugsFile,.75))}         
            quantidade = {"1": str(len(totalLocFile)), 
                    "2": str(len(totalSlocFile)), 
                    "3": str(len(ccFile)), 
                    "4": str(len(miMultiFalseFile)), 
                    "5": str(len(miMultiTrueFile)), 
                    "6": str(len(difficultyFile)), 
                    "7": str(len(effortFile)), 
                    "8": str(len(timeHasFile)), 
                    "9": str(len(bugsFile))}
            print("\n---Entrou numline - " + "numlines: " + str(numLine) + " total rows: " + str(totalRows))
            yearSplit = fileName.split('.')
            year = yearSplit[0]
            #print("\ntotalLocFile: " + str(totalLocFile))
            #time.sleep(5)
            #print("\ntotalSlocFile: " + str(totalSlocFile))
            #time.sleep(5)
            #print("\nccFile: " + str(ccFile))
            #time.sleep(5)
            #print("\nmiMultiFalseFile: " + str(miMultiFalseFile))
            #time.sleep(5)
            #print("\nmiMultiTrueFile: " + str(miMultiTrueFile))
            #time.sleep(5)
            #print("\ndifficultyFile: " + str(difficultyFile))
            #time.sleep(5)
            #print("\neffortFile: " + str(effortFile))
            #time.sleep(5)
            #print("\ntimeHasFile: " + str(timeHasFile))
            #time.sleep(5)
            #print("\nbugsFile: " + str(bugsFile))
            #time.sleep(5)
            print("\nyear: " + str(year))
            for x in range(1,10):
                idx = str(x)
                print("idx: " + idx)
                metric = metrics[idx]
                print("metric: " + metric)
                q1 = quar1[idx]
                print("q1: " + q1)
                value = values[idx]
                print("value: " + value)
                q3 = quar3[idx]
                print("q3: " + q3)
                qtd = quantidade[idx]
                print("qtd: " + qtd)
                fileNamePath = os.path.join(path, metric)
                if not os.path.exists(fileNamePath):
                    fileFinal = open(fileNamePath, 'w', newline='')
                    final = csv.writer(fileFinal)
                    final.writerow(('Ano', 'Quartil 1', 'Mediana', 'Quartil 3', 'QuantidadeRepo'))
                    fileFinal.close()
                writeInFinalCSV(fileNamePath, year, q1, value, q3, qtd)     
        numLine += 1
    fileToRead.close()
   
print("\n ------------- Fim da execução ------------- \n")
