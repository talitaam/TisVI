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

class cloneTofindMetrics():
    totalLoc = 0
    totalSloc = 0
    totalFiles = 0
    validFiles = 0
    invalidFiles = 0
    filesNotRead = 0
    filesNoMetric = 0
    cc = 0
    miMultiFalse = -1
    miMultiTrue = -1
    difficulty = -1
    effort = -1
    timeHas = -1
    bugs = -1

    # handle error in function clean_repository(folder)
    def on_rm_error(self, func, path, exc_info):
        # path contains the path of the file that couldn't be removed
        # let's just assume that it's read-only and unlink it.
        os.chmod(path, stat.S_IWRITE)
        os.unlink(path)

    # clean local repository folder
    def clean_repository(self, folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if not ".git" in filename:  # to avoid error
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path, onerror=self.on_rm_error)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))


    # Clone repository and read files to count LOC
    def cloneAndReadFileAndGetMetrics(self, gitURL, tagToClone):
        ANALYSE = """analyze(content)"""
        #COMPCICLO = """cc_visit(content)"""
        MANUINDEX = """mi_visit(content,multi=True)"""
        HASTMETRICS = """h_visit(content)"""
        self.totalFiles = 0
        self.totalLoc = 0
        self.totalSloc = 0
        self.validFiles = 0
        self.invalidFiles = 0
        self.filesNotRead = 0
        self.filesNoMetric = 0
        self.cc = 0
        self.miMultiFalse = -1
        self.miMultiTrue = -1
        self.difficulty = -1
        self.effort = -1
        self.timeHas = -1
        self.bugs = -1
        #valCC = []
        valMIfalse = []
        valMItrue = []
        valDiff = []
        valEffort = []
        valTimeHas = []
        valBugs = []
        numRepo = 0
        repo_path = 'Repository/' + str(numRepo)
        countRepo = 0
        totalRepo = 0
        if os.path.exists('Repository/'):
            totalRepo = len([f for f in os.listdir('Repository/') if os.path.isdir(os.path.join('Repository/', f))])
            #print("repos in Repository: " + str(totalRepo))
        while countRepo != totalRepo:
            if os.path.exists(repo_path): #Delete previous repositories and check a valid path
                try:
                    self.clean_repository(repo_path)
                    send2trash(repo_path)
                except OSError:
                    print(repo_path + " não foi excluído OS ERROR")
                    time.sleep(60)
                    break
                except Exception:
                    print("Repositório não excluído")
                    pass
                countRepo += 1
            numRepo += 1
            repo_path = 'Repository/' + str(numRepo)
        numRepo = 0
        repo_path = 'Repository/' + str(numRepo)
        while os.path.exists(repo_path):
            numRepo += 1
            repo_path = 'Repository/' + str(numRepo)
        if (tagToClone is None): #Clone original repository
            try:
                print("Começando o git clone...")
                reposit = Repo.clone_from(gitURL, repo_path) #clone repo and checkout the tag
            except:
                print("Não foi possível clonar o repositório")
                self.miMultiFalse = -2
                self.miMultiTrue = -2
                self.difficulty = -2
                self.effort = -2
                self.timeHas = -2
                self.bugs = -2
                exit()
            reposit.close()
            print("Clone finalizado. Lendo arquivos do Repositório e calculando métricas...")
            tagToClone = "Main Repo"
        else: #clone repo by tag
            toTag = "--branch " + str(tagToClone)
            try:
                print("Começando o git clone...")
                reposit = Repo.clone_from(gitURL, repo_path, multi_options=[toTag, '--single-branch']) #clone repo and checkout the tag
            except:
                print("Não foi possível clonar a tag")
                exit()
            reposit.close()
            print("Clone finalizado. Lendo arquivos do Repositório e calculando métricas...")
        for root, _, files in os.walk(repo_path):
            for file in files:
                if file.endswith('.py'):
                    self.totalFiles += 1
        print("totalFiles: " + str(self.totalFiles))
        time.sleep(10)
        for root, _, files in os.walk(repo_path):
            for file in files:
                if file.endswith('.py'):
                    fullpath = os.path.join(root, file)
                    if os.path.exists(fullpath) and os.path.isfile(fullpath) and os.access(fullpath, os.R_OK):
                        content = ""
                        try:
                            with open(fullpath, encoding="utf8") as f:
                                content = f.read()
                                print("----->>>>>Executou o f.read()<<<<<------")
                        except:
                            print("__________________________________")
                            print(fullpath)
                            print("Entrou no Except ao tentar executar open() ou read()")
                            print("__________________________________")
                        if content:
                                try: #check if radon methos can be run
                                    exec(ANALYSE)
                                    #exec(COMPCICLO)
                                    exec(MANUINDEX)
                                    exec(HASTMETRICS)
                                except SyntaxError:
                                    print("Something went wrong - métricas não podem ser calculadas - " + tagToClone)
                                    print(fullpath)
                                    print("-----------")
                                    # print(b)
                                    self.invalidFiles += 1 #cannot run one of the methods to get the metrics
                                else:
                                    b = analyze(content) #radon method to get loc and sloc
                                    #x = cc_visit(content) #get cc metric for each function in file
                                    y = mi_visit(content, multi=False) #get mi metric not considering multistrings
                                    y2 = mi_visit(content, multi=True) #get mi metric  considering multistrings
                                    z = h_visit(content) # get halstead metrics
                                    #valCCintern = []
                                    #for item in x:
                                        #d = GET_COMPLEXITY(item)
                                        #valCCintern.append(d) #get cc metric for each function and add in a list
                                    #valCCintern.sort()
                                    if y and z:
                                        self.validFiles += 1
                                        self.totalLoc += b[0]
                                        self.totalSloc += b[2]
                                        #valCC.append(ceil(median(valCCintern))) #get cc metric for file and add in a list
                                        valMIfalse.append(y) #add metric in a list
                                        valMItrue.append(y2)
                                        valDiff.append(z[0][8])
                                        valEffort.append(z[0][9])
                                        valTimeHas.append(z[0][10])
                                        valBugs.append(z[0][11])
                                    else:
                                        print("Arquivo não retornou todos as métricas necessárias - " + tagToClone)
                                        print(fullpath)
                                        print("-----------")
                                        self.filesNoMetric += 1 #methods ran but returned no values
                        else:
                            print("__________________________________")
                            print(fullpath)
                            print("Não retorna conteúdo no f.read()")
                            print("__________________________________")
                            self.filesNotRead += 1            
                    else:
                        print("File não pode ser aberto - " + tagToClone)
                        print(fullpath)
                        print("-----------")
                        self.filesNotRead += 1 # file could not be openned 
        print("\n------------------------------------")
        print("Total loc: " + str(self.totalLoc) + " - Files validos: " + str(self.validFiles) + " - Files invalidos: " + str(self.invalidFiles) + " - Files sem metricas: " + str(self.filesNoMetric) + " - Files não lidos: " + str(self.filesNotRead))
        if valMIfalse and valDiff:
            #valCC.sort()
            valMIfalse.sort()
            valMItrue.sort()
            valDiff.sort()
            valEffort.sort()
            valTimeHas.sort()
            valBugs.sort()
            #self.cc = ceil(median(valCC)) #get cc metric for the repository
            self.miMultiFalse = median(valMIfalse)
            self.miMultiTrue = median(valMItrue)
            self.difficulty = median(valDiff)
            self.effort = median(valEffort)
            self.timeHas = median(valTimeHas)
            self.bugs = median(valBugs)
        else:
            self.miMultiFalse = -3
            self.miMultiTrue = -3
            self.difficulty = -3
            self.effort = -3
            self.timeHas = -3
            self.bugs = -3
        #print("tam valCC: " + str(len(valCC)))
        print("miMultiFalse: " + str(self.miMultiFalse) + " - difficulty: " + str(self.difficulty))
    
    def getMetrics(self):
        return {"validFiles": str(self.validFiles), 
        "invalidFiles": str(self.invalidFiles), 
        "filesNotRead": str(self.filesNotRead),
        "filesNoMetric": str(self.filesNoMetric), 
        "totalLoc": str(self.totalLoc), 
        "totalSloc": str(self.totalSloc), 
        "cc": str(self.cc), 
        "miMultiFalse": str(self.miMultiFalse), 
        "miMultiTrue": str(self.miMultiTrue), 
        "difficulty": str(self.difficulty), 
        "effort": str(self.effort), 
        "timeHas": str(self.timeHas), 
        "bugs": str(self.bugs),
        "totalFiles": str(self.totalFiles)}

