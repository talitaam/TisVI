import csv
import os
import shutil
import stat
import time
import requests
from radon.raw import analyze
from radon.metrics import mi_visit, h_visit, mi_rank
from radon.complexity import cc_visit, average_complexity, sorted_results, cc_rank
from radon.visitors import ComplexityVisitor, HalsteadVisitor, GET_COMPLEXITY, GET_REAL_COMPLEXITY
from pygit2 import clone_repository
import threading
from statistics import median
from math import ceil
from git import Repo, Git
from send2trash import send2trash
import signal
import threadTemp
import findMetrics
from json import load, loads
import searchGraphQL


TIME_LIMIT_TO_FIND_LOC = 1200  # seconds
TIMESLEEP = 10  # seconds


# How many rows are already written in final.csv
def where_stop(filePath):
    row = 0
    if os.path.exists(filePath):
        fileFinal = open(filePath, 'r')
        row = sum(1 for line in csv.reader(fileFinal))
        fileFinal.close()
    return row

# Insert row in final.csv
def writeInFinalFile(node, url, totalLoc, totalSloc, validFiles, invalidFiles, filesNotRead, filesNoMetric, cc, ccRank, miMultiFalse, miMultiFalseRank, miMultiTrue, miMultiTrueRank, difficulty, effort, timeHas, bugs):
    fileFinal = open("final.csv", 'a', newline='')
    final = csv.writer(fileFinal)
    final.writerow((node[0], url, str(node[3]), node[6], str(totalLoc), str(totalSloc), str(validFiles), str(invalidFiles), str(filesNotRead), str(filesNoMetric), str(cc), ccRank, str(
        miMultiFalse), miMultiFalseRank, str(miMultiTrue), miMultiTrueRank, str(difficulty), str(effort), str(timeHas), str(bugs)))
    fileFinal.close()

def writeInFinalTagFile(fileNamePath, node, totalLoc, totalSloc, validFiles, invalidFiles, filesNotRead, filesNoMetric, cc, ccRank, miMultiFalse, miMultiFalseRank, miMultiTrue, miMultiTrueRank, difficulty, effort, timeHas, bugs, ):
    fileFinalTag = open(fileNamePath, 'a', newline='')
    finalTag = csv.writer(fileFinalTag)
    finalTag.writerow((node[0], node[1], node[2], node[3], str(totalLoc), str(totalSloc), str(validFiles), str(invalidFiles), str(filesNotRead), str(filesNoMetric), str(cc), ccRank, str(
        miMultiFalse), miMultiFalseRank, str(miMultiTrue), miMultiTrueRank, str(difficulty), str(effort), str(timeHas), str(bugs)))
    fileFinalTag.close()

def main():
    
    if not os.path.exists("base.csv"):
        createBase = searchGraphQL.searchAttributes()
        createBase.createBaseOrTagFile("base", "", "", "", "")
        print("\n ------------------- Fim arquivo base ------------------- \n")
        print(" ------------------- Criar arquivo baseFiltrado ------------------- ")
    
    contNode = 0
    
    if os.path.exists("baseFiltrada.csv") and not os.path.exists("finalFiltrado.csv"):
        # Insert table header in final.csv
        if not os.path.exists("final.csv"):
            fileFinal = open("final.csv", 'w', newline='')
            final = csv.writer(fileFinal)
            final.writerow(('nameWithOwner', 'url', 'releases', 'updateAt', 'totalLoc', 'totalSloc', 'validFiles', 'invalidFiles', 'filesNotRead', 'filesNoMetric', 'cc', 'ccRank',
                    'miMultiFalse', 'miMultiFalseRank', 'miMultiTrue', 'miMultiTrueRank', 'difficulty', 'effort', 'timeHas', 'bugs'))
            fileFinal.close()
        lastLine = where_stop("final.csv")
        print("lastLine: " + str(lastLine) + "\n")
        fileBase = open("baseFiltrada.csv", 'r')
        base = csv.reader(fileBase)
        for node in base:
            print("\n----------------INÍCIO REPO--------------------\n")
            print("Reposiótio: " + node[0])
            if ((contNode >= lastLine) and contNode != 0):
                calculateMetrics1 = findMetrics.cloneTofindMetrics()
                gitURL = node[1] + ".git"
                t = threadTemp.thread_with_trace(target=calculateMetrics1.cloneAndReadFileAndGetMetrics, args=(gitURL, None)) 
                t.daemon = True
                t.start() 
                t.join(TIME_LIMIT_TO_FIND_LOC)
                time.sleep(2) 
                if t.is_alive():  # If thread is still active
                    print("\n--> Excedeu limite de tempo. Interrompendo análise do repositório.....")
                    t.kill()
                    t.join()
                    time.sleep(TIMESLEEP)
                    print("\nis still alive? " + str(t.is_alive()))
                    writeInFinalFile(node, gitURL, -1, -1, -1, -1, -1, -1, -1, "Z",-1, "Z", -1, "Z", -1, -1, -1, -1)
                else:
                    m = calculateMetrics1.getMetrics()
                    if int(m['cc']) != -1:
                        ccRank = cc_rank(int(m['cc']))
                        miMultiFalseRank = mi_rank(float(m['miMultiFalse']))
                        miMultiTrueRank = mi_rank(float(m['miMultiTrue']))
                        print("--------------")
                        print("Gravando: ")
                        print("Total loc: " + str(m['totalLoc']) + " - Files validos: " + str(m['validFiles']) + " - Files invalidos: " + str(m['invalidFiles']) + "\nFiles sem metricas: " + str(m['filesNoMetric']) + " - Files não lidos: " + str(m['filesNotRead']))
                        print("cc: " + str(m['cc']) + " - miMultiFalse: " + str(m['miMultiFalse']) + "\ndifficulty: " + str(m['difficulty']) + " - bugs: " + str(m['bugs']))
                        writeInFinalFile(node, gitURL, m['totalLoc'], m['totalSloc'], m['validFiles'], m['invalidFiles'], m['filesNotRead'], m['filesNoMetric'], m['cc'], ccRank, m['miMultiFalse'], miMultiFalseRank, m['miMultiTrue'], miMultiTrueRank, m['difficulty'], m['effort'], m['timeHas'], m['bugs'])
                    else:
                        writeInFinalFile(node, gitURL, -1, -1, -1, -1, -1, -1, -1, "Z",-1, "Z", -1, "Z", -1, -1, -1, -1)
            contNode += 1
        fileBase.close()
        print("\n ------------------- Fim arquivo final ------------------- \n")
        print(" ------------------- Criar arquivo finalFiltrado ------------------- ")


    path = "RepoTags"

    if os.path.exists("finalFiltrado.csv"):
        contRepo = 0
        if os.path.exists(path):
            contRepo = len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
        else:
            os.mkdir(path)
        lastline = where_stop("finalFiltrado.csv")
        fileFinalFiltrado = open("finalFiltrado.csv", 'r')
        finalFiltrado = csv.reader(fileFinalFiltrado)
        contNode = 0
        print("\nQuant total repos para analisar: " + str(lastline - 1))
        print("Quant files em RepoTags: " + str(contRepo) + "\n")
        owner=""
        name=""
        print("Checking: \n")
        if(contRepo <= lastline-1):        
            for node in finalFiltrado:
                if contNode > 0:
                    splitOwnerName = node[0].split('/')
                    owner = splitOwnerName[0]
                    name = splitOwnerName[1]
                checkFile = path + "/" + owner + "-" + name + ".csv"
                #print("contNode: " + str(contNode) + " >= conteRepo: " + str(contRepo) + " ?")
                if ((not os.path.exists(checkFile) or (contNode > contRepo)) and contNode!=0):
                    print("\n--->>> Novo repositório: "+ node[0])
                    if not os.path.exists(checkFile):
                        contRepo +=1
                    createRepoTag = searchGraphQL.searchAttributes()
                    createRepoTag.createBaseOrTagFile("tag", path, owner, name, node)
                print("OK - " + checkFile)
                contNode += 1

        print("\n ------ Fim geração dos arquivos .csv com tags------- \n")

    
    pathFinal = "RepoTagsFinal"
    contRepoTags = 0
    contRepoTagsFinal = 0

    if os.path.exists(path):
        contRepoTags = len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
        if os.path.exists(pathFinal):
            contRepoTagsFinal = len([f for f in os.listdir(pathFinal) if os.path.isfile(os.path.join(pathFinal, f))])
        else:
            os.mkdir(pathFinal)

    print("\n--->>> contRepoTagsFinal: " + str(contRepoTagsFinal))
    print("--->>> contRepoTags: " + str(contRepoTags))

    if (contRepoTagsFinal <= contRepoTags) and os.path.exists(path) and os.path.exists(pathFinal):
        for f in os.listdir(path):
            for filename in os.listdir(pathFinal):
                if f == filename:
                    print("\n________________________________________\n")
                    fPath = os.path.join(path, f)
                    fileNamePath = os.path.join(pathFinal, filename)
                    if os.path.isfile(fPath):
                        if os.path.isfile(fileNamePath):
                            remove = False
                            print("fPath: " + str(fPath))
                            print("fileNamePath: " + str(fileNamePath))
                            quantTags = where_stop(fileNamePath) - 2
                            print("quantTags: " + str(quantTags))
                            readFileRepoTagFinal = open(fileNamePath, 'r')
                            fileRepoTagFinal = csv.reader(readFileRepoTagFinal)
                            if quantTags<2:
                                print("________________________________________\n")
                                remove = True
                            else:
                                contNodeTemp = 0
                                for node in fileRepoTagFinal:
                                    if contNodeTemp ==1:
                                        totalTags = int(node[2])
                                        if quantTags < totalTags:
                                            print("________________________________________\n")
                                            remove = True
                                    contNodeTemp +=1
                            readFileRepoTagFinal.close()
                            if remove:
                                print("Removendo arquivo... " + str(fileNamePath))
                                os.remove(fileNamePath)
                                print("...Arquivo removido")
        for f in os.listdir(path):
            fPath = os.path.join(path, f)
            fileNamePath = os.path.join(pathFinal, f)
            if not os.path.isfile(fileNamePath):
                print("\nfPath: " + str(fPath))
                print("fileNamePath: " + str(fileNamePath))
                readFileRepoTag = open(fPath, 'r')
                fileRepoTag = csv.reader(readFileRepoTag)
                contNode = 0
                print("\n----------------INÍCIO REPO--------------------\n")
                for node in fileRepoTag:
                    if(contNode < 2):
                        print(str(node[0]) + " - " + str(node[2]))
                        writeFileRepoTagFinal = open(fileNamePath, 'a', newline='')
                        fileRepoTagFinal = csv.writer(writeFileRepoTagFinal)
                        fileRepoTagFinal.writerow((node))
                        writeFileRepoTagFinal.close()
                    else:
                        gitURL = node[1]
                        tagName = node[2]
                        calculateMetrics2 = findMetrics.cloneTofindMetrics()
                        print("\n----------- Próxima Tag -------------\n")
                        print("Reposiótio: " + node[0])
                        print("Analisando tag: " + tagName + "\n")
                        time.sleep(3)
                        t1 = threadTemp.thread_with_trace(target=calculateMetrics2.cloneAndReadFileAndGetMetrics, args=(gitURL, tagName)) 
                        t1.daemon = True
                        t1.start() 
                        t1.join(TIME_LIMIT_TO_FIND_LOC)
                        time.sleep(2) 
                        if t1.is_alive():  # If thread is still active
                            print("\n--> Excedeu limite de tempo. Interrompendo análise do repositório.....")
                            t1.kill()
                            t1.join()
                            time.sleep(TIMESLEEP)
                            print("\nis still alive? " + str(t1.is_alive()))
                            writeInFinalTagFile(fileNamePath, node, -1, -1, -1, -1, -1, -1, -1, "Z",-1, "Z", -1, "Z", -1, -1, -1, -1)
                        else:
                            m = calculateMetrics2.getMetrics()
                            if int(m['cc']) != -1:
                                ccRank = cc_rank(int(m['cc']))
                                miMultiFalseRank = mi_rank(float(m['miMultiFalse']))
                                miMultiTrueRank = mi_rank(float(m['miMultiTrue']))
                                print("--------------")
                                print("Gravando: ")
                                print("Total loc: " + str(m['totalLoc']) + " - Files validos: " + str(m['validFiles']) + " - Files invalidos: " + str(m['invalidFiles']) + "\nFiles sem metricas: " + str(m['filesNoMetric']) + " - Files não lidos: " + str(m['filesNotRead']))
                                print("cc: " + str(m['cc']) + " - miMultiFalse: " + str(m['miMultiFalse']) + "\ndifficulty: " + str(m['difficulty']) + " - bugs: " + str(m['bugs']))
                                writeInFinalTagFile(fileNamePath, node, m['totalLoc'], m['totalSloc'], m['validFiles'], m['invalidFiles'], m['filesNotRead'], m['filesNoMetric'], m['cc'], ccRank, m['miMultiFalse'], miMultiFalseRank, m['miMultiTrue'], miMultiTrueRank, m['difficulty'], m['effort'], m['timeHas'], m['bugs'])
                            else:
                                writeInFinalTagFile(fileNamePath, node, -1, -1, -1, -1, -1, -1, -1, "Z",-1, "Z", -1, "Z", -1, -1, -1, -1)
                    contNode += 1
                readFileRepoTag.close()
                print("\n ------ Fim ------- \n")

    print("\n ---------------------- Fim da execução ---------------------- \n")




if __name__ == "__main__":
    main()
