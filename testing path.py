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

COMPCICLO = """cc_visit(content)"""
MANUINDEX = """mi_visit(content,multi=True)"""
HASTMETRICS = """h_visit(content)"""

global totalLoc
global totalSloc
global validFiles
global invalidFiles
global cc
global miMultiFalse
global miMultiTrue
global difficulty
global effort
global timeHas
global bugs


if True:
    #clone_repository(gitURL, repo_path)
    global totalLoc
    global totalSloc
    global validFiles
    global invalidFiles
    global cc
    global miMultiFalse
    global miMultiTrue
    global difficulty
    global effort
    global timeHas
    global bugs
    totalLoc = 0
    totalSloc = 0
    validFiles = 0
    invalidFiles = 0
    cc = -1
    miMultiFalse = -1
    miMultiTrue = -1
    difficulty = -1
    effort = -1
    timeHas = -1
    bugs = -1
    valCC = []
    valMIfalse = []
    valMItrue = []
    valDiff = []
    valEffort =[]
    valTimeHas = []
    valBugs = []
    repo_path= "androguard"
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith('.py'):
                fullpath = os.path.join(root, file)
                with open(fullpath, encoding="utf8") as f:
                    content = f.read()
                    b = analyze(content)
                    if content:
                        try:
                            exec(COMPCICLO)
                            exec(MANUINDEX)
                            exec(HASTMETRICS)
                        except SyntaxError:
                            print("\n-----------")
                            print(file)
                            print("Something went wrong")
                            print(b)
                            invalidFiles +=1
                            print("\n")
                        else:
                            #i = 0
                            #for item in b:
                                #if i == 0:
                                    #totalLoc += item
                                    #i += 1
                            totalLoc += b[0]
                            totalSloc += b[2]
                            x = cc_visit(content) 
                            y = mi_visit(content,multi=False)
                            y2= mi_visit(content,multi=True)
                            z = h_visit(content)
                            #print("\n-----------")
                            #print("Nothing went wrong")
                            #print(b)
                            #print("MI mulit false:" + str(y))
                            #print("MI mulit true:" + str(y2))
                            #print(z[0])
                            #print("difficulty: " + str(z[0][8]))
                            #print("effort: " + str(z[0][9]))
                            #print("time: " + str(z[0][10]))
                            #print("bugs: " + str(z[0][11]))
                            validFiles += 1
                            valCCintern = []
                            for item in x:
                                d=GET_COMPLEXITY(item)
                                valCCintern.append(d)
                            valCCintern.sort()
                            #print(valCCintern)
                            if valCCintern and y and z:
                                #print(median(valCCintern))
                                #print(ceil(median(valCCintern)))
                                valCC.append(ceil(median(valCCintern)))
                                valMIfalse.append(y)
                                valMItrue.append(y2)
                                valDiff.append(z[0][8])
                                valEffort.append(z[0][9])
                                valTimeHas.append(z[0][10])
                                valBugs.append(z[0][11])
    print("\n------------------------------------")
    print("Num de Files validos: " + str(validFiles))
    print("Num de Files invalidos: " + str(invalidFiles))
    valCC.sort()
    valMIfalse.sort()
    valMItrue.sort()
    valDiff.sort()
    valEffort.sort()
    valTimeHas.sort()
    valBugs.sort()
    cc = ceil(median(valCC))
    miMultiFalse = median(valMIfalse)
    miMultiTrue = median(valMItrue)
    difficulty = median(valDiff)
    effort = median(valEffort)
    timeHas = median(valTimeHas)
    bugs = median(valBugs)
    print(" - cc: " + str(cc))
    print(" - miMultiFalse: " + str(miMultiFalse))
    print(" - miMultiTrue: " + str(miMultiTrue))
    print(" - difficulty: " + str(difficulty))
    print(" - effort: " + str(effort))
    print(" - timeHas: " + str(timeHas))
    print(" - bugs: " + str(bugs))
    print("total loc: " + str(totalLoc))
