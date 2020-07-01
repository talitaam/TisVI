import csv
import os
import time
from statistics import median
from math import ceil
from datetime import date, datetime
from datetime import time, timedelta
from numpy import quantile, median, max, min


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

"""
higherNumFail = 0
daysInOneYear = timedelta(days=365)

for fileName in os.listdir("RepoTags"):
    #print("Lendo " + fileName)
    fileRepo = "RepoTags/" + fileName
    totalRows = where_stop(fileRepo)
    fileRead = open("RepoTags/" + fileName, encoding='utf-8')
    repo = csv.reader(fileRead)
    totalLocFile = []
    ccFile = []
    miMultiFalseFile = []
    nameWithOwner = ""
    numLine = 0
    newDate = ""
    actualDate = ""
    pastDate = ""
    faltaAno = False
    for node in repo:
        if numLine>1:
            if (node[3].find('/') != -1):
                pastDate = newDate
                changeFormart = datetime.strptime(str(node[3]), "%m/%d/%Y")
                #print("changeFormart: " + str(changeFormart))
                newDate = date(changeFormart.year, changeFormart.month, changeFormart.day)
                #print("")
                #print("newDate " + str(newDate))
            else:
                pastDate = newDate
                newDate = date.fromisoformat(str(node[3]))
                #print("")
                #print("newDate: " + str(newDate))
            if numLine == 2:
                nameWithOwner = node[0]
                actualDate = newDate
                pastDate = newDate
            if ((newDate - actualDate) > daysInOneYear):
                print("\n---Entrou no year")
                print("actualDate: " + str(actualDate))
                print("pastDate: " + str(pastDate))
                print("newDate: " + str(newDate))
                print("actualDate: " + str(actualDate))
                print("newDate - actualDate: " + str(newDate - actualDate))
                if not totalLocFile or ((newDate - pastDate) > daysInOneYear):
                    print("newDate - pastDate: " + str(newDate - pastDate))
                    print("\n" + nameWithOwner + " - NÃO HÁ METRICA PARA UM INTERVALO DE ANO")
                    faltaAno = True
                actualDate = newDate
                totalLocFile = []
                ccFile = []
                miMultiFalseFile = []
            if str(node[10]) != "-1":
                totalLocFile.append(float(node[4]))
                ccFile.append(float(node[10]))
                miMultiFalseFile.append(float(node[12]))
        numLine += 1
    fileRead.close()
    if faltaAno == True:
        higherNumFail += 1
        os.rename("RepoTags/" + fileName, "RepoTagsIncorrect2/" + fileName)
print("Quantidade excluída: " + str(higherNumFail))
print("\n ------ Fim de um repositorio ------ \n")
"""
#------------------------------------------------------------
"""
totalRepo = 0

for fileName in os.listdir("RepoTags"):
    if not os.path.exists(path):
        os.mkdir(path)
    fileRepo = "RepoTags/" + fileName
    totalRows = where_stop(fileRepo)
    fileToRead = open(fileRepo, encoding='utf-8')
    repo = csv.reader(fileToRead)
    desconsideraRepo = False
    numLine = 0
    for node in repo:
        if numLine == 2:
            nameWithOwner = node[0]
            #print("nameWithOwner: " + nameWithOwner)
            if os.path.exists("RepoPercent.csv"):
                fileBase = open("RepoPercent.csv", 'r')
                base = csv.reader(fileBase)
                for item in base:
                    if item[0] == nameWithOwner:
                        validFiles = float(item[1])
                        if validFiles < 63:
                            print("item[0]: " + item[0])
                            desconsideraRepo = True
                        break
                fileBase.close()
        if desconsideraRepo == True:
            break
        numLine += 1
    fileToRead.close()
    if not os.path.exists("RepoTagsIncorrect3"):
        os.mkdir("RepoTagsIncorrect3")
    if desconsideraRepo == True:
        totalRepo += 1
        os.rename("RepoTags/" + fileName, "RepoTagsIncorrect3/" + fileName)
print("Quantidade excluída: " + str(totalRepo))
print("\n ------ Fim de um repositorio ------ \n")
"""
#----------------------------------------------------------------------------

"""
if os.path.exists("RepoPercent.csv"):
    validFiles =[]
    fileBase = open("RepoPercent.csv", 'r')
    base = csv.reader(fileBase)
    numLine = 0
    for item in base:
        if numLine > 0:
            validFiles.append(float(item[1]))
        numLine += 1
    fileBase.close()
    minimo = min(validFiles)
    q1 = quantile(validFiles,.25)
    q2 = quantile(validFiles,.50)
    med = median(validFiles)
    q3 = quantile(validFiles,.75)
    maximo = max(validFiles)
    print("min: " + str(minimo))
    print("Q1: " + str(q1))
    print("Q2: " + str(q2))
    print("median: " + str(med))
    print("Q3: " + str(q3))
    print("max: " + str(maximo))

"""



#----------------------------------------------------------------------------



#higherNumFail = 0
daysInOneYear = timedelta(days=365)

for fileName in os.listdir("RepoTags"):
    #print("Lendo " + fileName)
    fileRepo = "RepoTags/" + fileName
    totalRows = where_stop(fileRepo)
    fileRead = open("RepoTags/" + fileName, encoding='utf-8')
    repo = csv.reader(fileRead)
    totalLocFile = []
    ccFile = []
    miMultiFalseFile = []
    nameWithOwner = ""
    numLine = 0
    newDate = ""
    actualDate = ""
    pastDate = ""
    qtdYearsTotal = 0
    qtdYearsSemTag = 0
    print("\n\n-----------------Novo Repo------------------")
    for node in repo:
        if numLine>1:
            if (node[3].find('/') != -1):
                pastDate = newDate
                changeFormart = datetime.strptime(str(node[3]), "%m/%d/%Y")
                #print("changeFormart: " + str(changeFormart))
                newDate = date(changeFormart.year, changeFormart.month, changeFormart.day)
                #print("")
                #print("newDate " + str(newDate))
            else:
                pastDate = newDate
                newDate = date.fromisoformat(str(node[3]))
                #print("")
                #print("newDate: " + str(newDate))
            if numLine == 2:
                nameWithOwner = node[0]
                actualDate = newDate
                pastDate = newDate
            if ((newDate - actualDate) > daysInOneYear):
                print("\n---Entrou no year")
                print("actualDate: " + str(actualDate))
                print("pastDate: " + str(pastDate))
                print("newDate: " + str(newDate))
                print("actualDate: " + str(actualDate))
                print("newDate - actualDate: " + str(newDate - actualDate))
                print("newDate - pastDate: " + str(newDate - pastDate))
                if ((newDate - pastDate) > daysInOneYear):
                    years = ceil((newDate - pastDate) / daysInOneYear)
                    print("years: " + str(ceil((newDate - pastDate) / daysInOneYear)))
                    if not totalLocFile:
                        qtdYearsSemTag += int(years)
                        print("Sem loc qtdYearsSemTag: " + str(qtdYearsSemTag))
                    else:
                        qtdYearsSemTag += int(years-1)
                        print("Com loc qtdYearsSemTag: " + str(qtdYearsSemTag))
                else:
                    years = 1
                    if not totalLocFile:
                        qtdYearsSemTag += int(years)
                qtdYearsTotal += int(years)
                if not totalLocFile:
                    print("newDate - pastDate: " + str(newDate - pastDate))
                    print("\n" + nameWithOwner + " - NÃO HÁ METRICA PARA UM INTERVALO DE ANO")
                    faltaAno = True
                actualDate = newDate
                totalLocFile = []
                ccFile = []
                miMultiFalseFile = []
            if str(node[10]) != "-1":
                totalLocFile.append(float(node[4]))
                ccFile.append(float(node[10]))
                miMultiFalseFile.append(float(node[12]))
            if numLine == totalRows-1:
                qtdYearsTotal += 1
                if not totalLocFile:
                    qtdYearsSemTag += 1
        numLine += 1
    fileRead.close()
    print("")
    print(nameWithOwner)
    print("qtdYearsTotal: " + str(qtdYearsTotal))
    print("qtdYearsSemTag: " + str(qtdYearsSemTag))
    #time.sleep(5)
    #if not os.path.exists("RepoTags4AnosTodosAnos"):
    #    os.mkdir("RepoTags4AnosTodosAnos")
    #if not os.path.exists("RepoTags4AnosSem1Year"):
    #    os.mkdir("RepoTags4AnosSem1Year")
    #if not os.path.exists("RepoTags4AnosSemYears"):
     #   os.mkdir("RepoTags4AnosSemYears")
    if not os.path.exists("RepoTagsRestante"):
        os.mkdir("RepoTagsRestante")
    if qtdYearsTotal >= 4 and qtdYearsSemTag == 0:
        pass
        #os.rename("RepoTags/" + fileName, "RepoTags4AnosTodosAnos/" + fileName)
    #elif qtdYearsTotal >= 4 and qtdYearsSemTag == 1:
     #   os.rename("RepoTags/" + fileName, "RepoTags4AnosSem1Year/" + fileName)
    #elif qtdYearsTotal >= 4 and qtdYearsSemTag > 0:
     #   os.rename("RepoTags/" + fileName, "RepoTags4AnosSemYears/" + fileName)
    else:
        os.rename("RepoTags/" + fileName, "RepoTagsRestante/" + fileName)

print("\n ------ Fim de um repositorio ------ \n")

#----------------------------------------------------------------------------

daysInOneYear = timedelta(days=365)
path = "FinalCSV"
totalRepo = 0

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
    actualDate = ""
    newDate = ""
    pastDate = ""
    for node in repo:
        if numLine > 1:
            if (node[3].find('/') != -1):
                pastDate = newDate
                changeFormart = datetime.strptime(str(node[3]), "%m/%d/%Y")
                print("changeFormart: " + str(changeFormart))
                newDate = date(changeFormart.year, changeFormart.month, changeFormart.day)
                print("")
                print("newYear: " + str(newDate))
            else:
                pastDate = newDate
                newDate = date.fromisoformat(str(node[3]))
                print("")
                print("newYear: " + str(newDate))
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
                actualDate = newDate
                totalLocFile = []
                totalSlocFile = []
                ccFile = []
                miMultiFalseFile = []
                miMultiTrueFile = []
                difficultyFile = []
                effortFile = []
                timeHasFile = []
                bugsFile = []
                if ((newDate - pastDate) > daysInOneYear):
                    years = ceil((newDate - pastDate) / daysInOneYear)
                else:
                    years = 1
                equivYear += int(years)
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
                #time.sleep(5)
        numLine += 1
    fileToRead.close()
   
print("Total repos = ", totalRepo)

print("\n ------------- Fim da execução ------------- \n")