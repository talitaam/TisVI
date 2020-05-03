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
global tags

TIME_LIMIT_TO_FIND_LOC = 150 #seconds
TIMESLEEP = 60 #seconds
COMPCICLO = """cc_visit(content)"""
MANUINDEX = """mi_visit(content,multi=True)"""
HASTMETRICS = """h_visit(content)"""


headers = {"Authorization": "Bearer YOUR KEY HERE"}

# Run an api graphql request
def run_query(json, headers):  
    request = requests.post('https://api.github.com/graphql', json=json, headers=headers)
    while (request.status_code == 502):
        time.sleep(2)
        request = requests.post('https://api.github.com/graphql', json=json, headers=headers)
    if request.status_code == 200:
        return request.json()  # json returned by request
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

#handle error in function clean_repository(folder) 
def on_rm_error(func, path, exc_info):
    # path contains the path of the file that couldn't be removed
    # let's just assume that it's read-only and unlink it.
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)

#clean local repository folder 
def clean_repository(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if not ".git" in filename: #to avoid error
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path, onerror=on_rm_error)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

#How many rows are already written in final.csv
def where_stop():
    row = 0
    if os.path.exists("final.csv"):
        fileFinal = open("final.csv", 'r')
        row = sum(1 for line in csv.reader(fileFinal))
        fileFinal.close()
    return row

#Insert row in final.csv
def writeInFinalFile(node, tagName, totalLoc, totalSloc, validFiles, invalidFiles, cc, ccRank, miMultiFalse, miMultiFalseRank, miMultiTrue, miMultiTrueRank, difficulty, effort, timeHas, bugs):
    fileFinal = open("final.csv", 'a', newline='')
    final = csv.writer(fileFinal)
    final.writerow((node[0], tagName, str(totalLoc), str(totalSloc), str(validFiles), str(invalidFiles), str(cc), ccRank, str(miMultiFalse), miMultiFalseRank, str(miMultiTrue), miMultiTrueRank, str(difficulty), str(effort), str(timeHas), str(bugs)))
    fileFinal.close()

#Clone repository and read files to count LOC
def cloneAndReadFileAndGetLoc(gitURL, repo_path, tagToClone):
    if (tagToClone is None):
        global tags
        reposit = Repo.clone_from(gitURL, repo_path)
        tags = reposit.tags
        for tag in tags:
            print(tag.name)
        print("Git clone finalizado. \nLendo arquivos do Repositório e calculando LOC.....")
    else:
        print("Checar tamanho do repo")
        time.sleep(15)
        g = Git(repo_path)
        g.checkout(tagToClone)
        print("Git checkout finalizado. \nLendo arquivos do Repositório e calculando LOC.....")
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



           

#Create base.csv
if not os.path.exists("base.csv"):
    print("\n -------------- Iniciando processo pesquisa GraphQl -------------- \n")

    # Query GraphQL to look for first 1000 repositories in Python over 100 stars
    query = """
    query example{
        search (query:"stars:>100 and language:Python", type: REPOSITORY, first:3{AFTER}) {
            pageInfo{
                hasNextPage
                endCursor
            }
            nodes {
                ... on Repository {
                    nameWithOwner
                    url
                    name
                    stargazers {
                        totalCount
                    }
                    releases {
                        totalCount
                    }
                    primaryLanguage {
                        name
                    }
                    createdAt
                    updatedAt
                }
            }
        }
    }
    """

    finalQuery = query.replace("{AFTER}", "")

    json = {
        "query": finalQuery, "variables": {}
    }

    total_pages = 1
    print("Executando Query\n[", end='')
    result = run_query(json, headers)  # Run Query
    print(result)
    nodes = result["data"]["search"]["nodes"]  # split string to show only the nodes
    next_page = result["data"]["search"]["pageInfo"]["hasNextPage"]

    page = 0
    while next_page and total_pages < 1:
        total_pages += 1
        cursor = result["data"]["search"]["pageInfo"]["endCursor"]
        next_query = query.replace("{AFTER}", ", after: \"%s\"" % cursor)
        json["query"] = next_query
        result = run_query(json, headers)
        nodes += result['data']['search']['nodes']
        next_page = result["data"]["search"]["pageInfo"]["hasNextPage"]
        print(".", end='')
    print("]")

    print("Criando arquivo base CSV")
    file = open("base.csv", 'w', newline='')
    repository = csv.writer(file)

    print("Salvando Repositorios:\n[", end='')
    repository.writerow(('nameWithOwner', 'url', 'name', 'stars', 'releases', 'primaryLanguage', 'createdAt', 'updatedAt'))
    num = 0
    for node in nodes:
        repository.writerow((node['nameWithOwner'], str(node['url']), node['name'], 
                            str(node['stargazers']['totalCount']), str(node['releases']['totalCount']),
                            node['primaryLanguage']['name'], node['createdAt'], node['updatedAt']))
        num = num + 1
        if (num % 10) == 0:
            print(".", end='')
    print("]\nProcesso concluido")
    file.close()


print("\n ------------------- Começo leitura repositorios ------------------- \n")

numRepo = 0
contNode = 0
totalLoc = 0
lastLine = where_stop()

print("lastLine: " + str(lastLine) + "\n")

#Insert table header in final.csv
if not os.path.exists("final.csv"):
    fileFinal = open("final.csv", 'w', newline='')
    final = csv.writer(fileFinal)
    final.writerow(('nameWithOwner', 'tag', 'totalLoc', 'totalSloc', 'validFiles', 'invalidFiles', 'cc', 'ccRank', 'miMultiFalse', 'miMultiFalseRank', 'miMultiTrue', 'miMultiTrueRank', 'difficulty', 'effort', 'timeHas', 'bugs'))
    fileFinal.close()


fileBase = open("base.csv", 'r')
base = csv.reader(fileBase)

for node in base:
    if ((contNode >= lastLine) and contNode != 0):
        repo_path = 'Repository/' + str(numRepo)
        while os.path.exists(repo_path):
            if totalLoc != -1: #to avoid possible error
                clean_repository(repo_path)
            numRepo += 1
            repo_path = 'Repository/' + str(numRepo)
        print(" ----- Inicio " + repo_path + " ----- \n")
        gitURL = node[1] + ".git"
        print("Começa o git clone")
        print(gitURL)
        negativeValues = False
        clrd = threading.Thread(target=cloneAndReadFileAndGetLoc, args=(gitURL, repo_path, None))
        clrd.daemon = True
        clrd.start()
        clrd.join(TIME_LIMIT_TO_FIND_LOC) # Wait for x seconds or until process finishes
        if clrd.is_alive(): # If thread is still active
            print("\n--> Excedeu limite de tempo. Interrompendo análise do repositório.....")
            th = threading.currentThread()
            th._stop
            time.sleep(TIMESLEEP)
            negativeValues = True
        if negativeValues:# Define a negative value for LOC
            totalLoc = -1 
            totalSloc = -1
            validFiles = -1
            invalidFiles = -1
        if totalLoc != -1:
            ccRank = cc_rank(cc)
            miMultiFalseRank = mi_rank(miMultiFalse)
            miMultiTrueRank = mi_rank(miMultiTrue)
        writeInFinalFile(node, "original", totalLoc, totalSloc, validFiles, invalidFiles, cc, ccRank, miMultiFalse, miMultiFalseRank, miMultiTrue, miMultiTrueRank, difficulty, effort, timeHas, bugs)
        if tags:
            for tag in tags:
                #if (tag.name == "alpha_0" or tag.name == "1.3" or tag.name == "1.6"):
                    print("Analisando tag: " + tag.name)
                    clrd = threading.Thread(target=cloneAndReadFileAndGetLoc, args=(gitURL, repo_path, tag.name))
                    clrd.daemon = True
                    clrd.start()
                    clrd.join(TIME_LIMIT_TO_FIND_LOC)  # Wait for x seconds or until process finishes
                    if clrd.is_alive():  # If thread is still active
                        print("\n--> Excedeu limite de tempo. Interrompendo análise do repositório.....")
                        th = threading.currentThread()
                        th._stop
                        time.sleep(TIMESLEEP)
                        negativeValues = True
                    if negativeValues:# Define a negative value for LOC
                        totalLoc = -1 
                        totalSloc = -1
                        validFiles = -1
                        invalidFiles = -1
                    if totalLoc != -1:
                        ccRank = cc_rank(cc)
                        miMultiFalseRank = mi_rank(miMultiFalse)
                        miMultiTrueRank = mi_rank(miMultiTrue)
                    writeInFinalFile(node, tag.name, totalLoc, totalSloc, validFiles, invalidFiles, cc, ccRank, miMultiFalse, miMultiFalseRank, miMultiTrue, miMultiTrueRank, difficulty, effort, timeHas, bugs)
        print("\n ------ Fim " + repo_path + " ------- \n")
        if totalLoc != -1: #to avoid possible error
            if os.path.exists(repo_path):
                clean_repository(repo_path)
    else:
        contNode +=1
        numRepo += 1
        
fileBase.close()

print("\n ---------------------- Fim da execução ---------------------- \n")
