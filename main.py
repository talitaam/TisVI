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

global query
global totalLoc
global totalSloc
global validFiles
global invalidFiles
global filesNotRead
global filesNoMetric
global cc
global miMultiFalse
global miMultiTrue
global difficulty
global effort
global timeHas
global bugs
global tags

TIME_LIMIT_TO_FIND_LOC = 600  # seconds
TIMESLEEP = 10  # seconds
COMPCICLO = """cc_visit(content)"""
MANUINDEX = """mi_visit(content,multi=True)"""
HASTMETRICS = """h_visit(content)"""

query = """"""
totalLoc = 0
totalSloc = 0
validFiles = 0
invalidFiles = 0
filesNotRead = 0
filesNoMetric = 0
cc = -1
miMultiFalse = -1
miMultiTrue = -1
difficulty = -1
effort = -1
timeHas = -1
bugs = -1
tags = ""


headers = {"Authorization": "Bearer Your Key Here"}


# Run an api graphql request
def run_query(json, headers):
    request = requests.post(
        'https://api.github.com/graphql', json=json, headers=headers)
    while (request.status_code == 502):
        time.sleep(2)
        request = requests.post(
            'https://api.github.com/graphql', json=json, headers=headers)
    if request.status_code == 200:
        return request.json()  # json returned by request
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


# handle error in function clean_repository(folder)
def on_rm_error(func, path, exc_info):
    # path contains the path of the file that couldn't be removed
    # let's just assume that it's read-only and unlink it.
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)


# clean local repository folder
def clean_repository(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if not ".git" in filename:  # to avoid error
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path, onerror=on_rm_error)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


# How many rows are already written in final.csv
def where_stop():
    row = 0
    if os.path.exists("final.csv"):
        fileFinal = open("final.csv", 'r')
        row = sum(1 for line in csv.reader(fileFinal))
        fileFinal.close()
    return row

# Insert row in final.csv
def writeInFinalFile(node, tag, totalLoc, totalSloc, validFiles, invalidFiles, filesNotRead, filesNoMetric, cc, ccRank, miMultiFalse, miMultiFalseRank, miMultiTrue, miMultiTrueRank, difficulty, effort, timeHas, bugs):
    fileFinal = open("final.csv", 'a', newline='')
    final = csv.writer(fileFinal)
    final.writerow((node[0], tag, str(totalLoc), str(totalSloc), str(validFiles), str(invalidFiles), str(filesNotRead), str(filesNoMetric), str(cc), ccRank, str(
        miMultiFalse), miMultiFalseRank, str(miMultiTrue), miMultiTrueRank, str(difficulty), str(effort), str(timeHas), str(bugs)))
    fileFinal.close()


# Clone repository and read files to count LOC
def cloneAndReadFileAndGetLoc(gitURL, tagToClone):
    global tags
    numRepo = 0
    repo_path = 'Repository/' + str(numRepo)
    while os.path.exists(repo_path): #Delete previous repositories and check a valid path
        try:
            clean_repository(repo_path)
            send2trash(repo_path)
        except OSError as ose:
            print(repo_path + " não foi excluído - " + ose)
        except Exception:
            print("Repositório não excluído")
            pass
        numRepo += 1
        repo_path = 'Repository/' + str(numRepo)
    if (tagToClone is None): #Clone original repository
        reposit = Repo.clone_from(gitURL, repo_path)
        tags = reposit.tags #get the tags from original repository
        print("tag lenght é " + str(len(tags)))
        reposit.close()
        for tag in tags:
            print(tag.name)
        print("Git clone Repo finalizado. \nLendo arquivos do Repositório e calculando LOC.....")
        tagToClone = "First repo"
    else: #clone repo by tag
        toTag = "--branch " + str(tagToClone)
        reposit = Repo.clone_from(gitURL, repo_path, multi_options=[toTag, '--single-branch']) #clone repo and checkout the tag
        print("Git clone Tag finalizado. \nLendo arquivos do Repositório e calculando LOC.....")
    global totalLoc
    global totalSloc
    global validFiles
    global invalidFiles
    global filesNotRead
    global filesNoMetric
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
    filesNotRead = 0
    filesNoMetric = 0
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
    valEffort = []
    valTimeHas = []
    valBugs = []
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith('.py'):
                fullpath = os.path.join(root, file)
                if os.path.exists(fullpath) and os.path.isfile(fullpath) and os.access(fullpath, os.R_OK):
                    with open(fullpath, encoding="utf8") as f:
                        content = f.read()
                        b = analyze(content) #radon method to get loc and sloc
                        if content:
                            try: #check if radon methos can be run
                                exec(COMPCICLO)
                                exec(MANUINDEX)
                                exec(HASTMETRICS)
                            except SyntaxError:
                                print("-----------")
                                print(file)
                                print("Something went wrong - métricas não podem ser calculadas")
                                # print(b)
                                invalidFiles += 1 #cannot run one of the methods to get the metrics
                            else:
                                x = cc_visit(content) #get cc metric for each function in file
                                y = mi_visit(content, multi=False) #get mi metric not considering multistrings
                                y2 = mi_visit(content, multi=True) #get mi metric  considering multistrings
                                z = h_visit(content) # get halstead metrics
                                valCCintern = []
                                for item in x:
                                    d = GET_COMPLEXITY(item)
                                    valCCintern.append(d) #get cc metric for each function and add in a list
                                valCCintern.sort()
                                # print(valCCintern)
                                if valCCintern and y and z:
                                    validFiles += 1
                                    totalLoc += b[0]
                                    totalSloc += b[2]
                                    valCC.append(ceil(median(valCCintern))) #get cc metric for file and add in a list
                                    valMIfalse.append(y) #add metric in a list
                                    valMItrue.append(y2)
                                    valDiff.append(z[0][8])
                                    valEffort.append(z[0][9])
                                    valTimeHas.append(z[0][10])
                                    valBugs.append(z[0][11])
                                else:
                                    print("-----------")
                                    print(tagToClone + ": Arquivo " + file + " não retornou todos as métricas necessárias")
                                    filesNoMetric += 1 #methods ran but returned no values
                else:
                    print("-----------")
                    print("File " + fullpath + " não pode ser aberto")
                    filesNotRead += 1 # file could not be openned 
    print("\n------------------------------------")
    print("Total loc: " + str(totalLoc) + "\nFiles validos: " + str(validFiles) + "\nFiles invalidos: " + str(invalidFiles) + "\nFiles sem metricas: " + str(filesNoMetric) + "\nFiles não lidos: " + str(filesNotRead))
    if valCC:
        valCC.sort()
        valMIfalse.sort()
        valMItrue.sort()
        valDiff.sort()
        valEffort.sort()
        valTimeHas.sort()
        valBugs.sort()
        cc = ceil(median(valCC)) #get cc metric for the repository
        miMultiFalse = median(valMIfalse)
        miMultiTrue = median(valMItrue)
        difficulty = median(valDiff)
        effort = median(valEffort)
        timeHas = median(valTimeHas)
        bugs = median(valBugs)
    print("tam valCC: " + str(len(valCC)))
    print("-------------------")
    print(" - cc: " + str(cc) + "\n - miMultiFalse: " + str(miMultiFalse) + "\n - difficulty: " + str(difficulty) + "\n - bugs: " + str(bugs))


def main():
    if not os.path.exists("base.csv"):
        # Create base.csv
        print("\n -------------- Iniciando processo pesquisa GraphQl -------------- \n")
        # Query GraphQL to look for first 1000 repositories in Python over 100 stars
        global query
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

        json = {"query": finalQuery, "variables": {}}
        total_pages = 1
        print("Executando Query\n[", end='')
        result = run_query(json, headers)  # Run Query
        print(result)
        # split string to show only the nodes
        nodes = result["data"]["search"]["nodes"]
        next_page = result["data"]["search"]["pageInfo"]["hasNextPage"]

        #page = 0
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
                             str(node['stargazers']['totalCount']), str(
                                 node['releases']['totalCount']),
                             node['primaryLanguage']['name'], node['createdAt'], node['updatedAt']))
            num = num + 1
            if (num % 10) == 0:
                print(".", end='')
        print("]\nProcesso concluido")
        file.close()
    print("\n ------------------- Começo leitura repositorios ------------------- \n")
    
    contNode = 0
    lastLine = where_stop()

    print("lastLine: " + str(lastLine) + "\n")

    # Insert table header in final.csv
    if not os.path.exists("final.csv"):
        fileFinal = open("final.csv", 'w', newline='')
        final = csv.writer(fileFinal)
        final.writerow(('nameWithOwner', 'tag', 'totalLoc', 'totalSloc', 'validFiles', 'invalidFiles', 'filesNotRead', 'filesNoMetric', 'cc', 'ccRank',
                    'miMultiFalse', 'miMultiFalseRank', 'miMultiTrue', 'miMultiTrueRank', 'difficulty', 'effort', 'timeHas', 'bugs'))
        fileFinal.close()

    fileBase = open("base.csv", 'r')
    base = csv.reader(fileBase)

    for node in base:
        global totalLoc
        global totalSloc
        global validFiles
        global invalidFiles
        global filesNotRead
        global cc
        global miMultiFalse
        global miMultiTrue
        global difficulty
        global effort
        global timeHas
        global bugs
        global tags
        if ((contNode >= lastLine) and contNode != 0):
            gitURL = node[1] + ".git"
            print("Começa o git clone")
            print(gitURL)
            t = threadTemp.thread_with_trace(target=cloneAndReadFileAndGetLoc, args=(gitURL, None)) 
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
                print("miMultiFalse: " + str(miMultiFalse))
                print("bugs: " + str(bugs))
                writeInFinalFile(node, "-1", -1, -1, -1, -1, -1, -1, cc, "Z",miMultiFalse, "Z", miMultiTrue, "Z", difficulty, effort, timeHas, bugs)
            else:
                if cc != -1:
                    ccRank = cc_rank(cc)
                    miMultiFalseRank = mi_rank(miMultiFalse)
                    miMultiTrueRank = mi_rank(miMultiTrue)
                tagSize = str(len(tags)) #original repo has the number of tags in "tag" column
                writeInFinalFile(node, tagSize, totalLoc, totalSloc, validFiles, invalidFiles, filesNotRead, filesNoMetric, cc, ccRank, miMultiFalse, miMultiFalseRank, miMultiTrue, miMultiTrueRank, difficulty, effort, timeHas, bugs)
                if tags:
                    for tag in reversed(tags):
                            print("\n--------------- Próxima Tag ---------------------")
                            print("Analisando tag: " + tag.name)
                            time.sleep(3)
                            t1 = threadTemp.thread_with_trace(target=cloneAndReadFileAndGetLoc, args=(gitURL, tag.name)) 
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
                                print("miMultiFalse: " + str(miMultiFalse))
                                print("bugs: " + str(bugs))
                                writeInFinalFile(node, tag.name, -1, -1, -1, -1, -1, -1, cc, "Z", miMultiFalse,"Z", miMultiTrue, "Z", difficulty, effort, timeHas, bugs)
                            else:
                                if cc != -1:
                                    ccRank = cc_rank(cc)
                                    miMultiFalseRank = mi_rank(miMultiFalse)
                                    miMultiTrueRank = mi_rank(miMultiTrue)
                                writeInFinalFile(node, tag.name, totalLoc, totalSloc, validFiles, invalidFiles, filesNotRead, filesNoMetric, cc, ccRank, miMultiFalse, miMultiFalseRank, miMultiTrue, miMultiTrueRank, difficulty, effort, timeHas, bugs)
            print("\n ------ Fim ------- \n")
        else:
            contNode += 1

    fileBase.close()

    print("\n ---------------------- Fim da execução ---------------------- \n")

if __name__ == "__main__":
    main()
