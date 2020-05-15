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

NUMPAGESREPO = 50

class searchAttributes():

    headers = {"Authorization": "Bearer YOUR KEY HERE"}

    query = ""

    # Run an api graphql request
    def run_query(self, json, headers):
        request = requests.post(
            'https://api.github.com/graphql', json=json, headers=headers)
        while (request.status_code == 502):
            time.sleep(3)
            request = requests.post('https://api.github.com/graphql', json=json, headers=headers)
        if request.status_code == 200:
            return request.json()  # json returned by request
        else:
            raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, self.query))


    def createBaseOrTagFile(self, typeSearch, path, owner, name, nodeFinal):
        if typeSearch == "base":#create base.cvs with repositories with all its releases/tags
            print("\n -------------- Iniciando processo pesquisa base.csv GraphQl -------------- \n")
            # Query GraphQL to look for first 1000 repositories in Python over 100 stars
            self.query = """
            query example{
                search (query:"stars:>100 and language:Python and created:>2014-01-01", type: REPOSITORY, first:30{AFTER}) {
                    pageInfo{
                        hasNextPage
                        endCursor
                    }
                    nodes {
                        ... on Repository {
                            nameWithOwner
                            url
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
        elif typeSearch == "tag": #create .cvs files for each repository with all its releases/tags
            print("\n -------------- Iniciando processo pesquisa tags GraphQl -------------- \n")
            self.query = "query example { repository(owner:"+ '"' + owner + '"' + ", name:" + '"' + name + '"' + "){releases(first:50 {AFTER} ){pageInfo{hasNextPage endCursor} nodes{tagName publishedAt}}}}"
        else:
            print("erro em typeSearch -> precisa ser base ou tag: " + typeSearch)
            exit()

        finalQuery = self.query.replace("{AFTER}", "")
        json = {"query": finalQuery, "variables": {}}
        result = self.run_query(json, self.headers)  # Run Query

        print("Executando Query\n[", end='')
        
        # split string to show only the nodes
        if typeSearch == "base":
            nodes = result["data"]["search"]["nodes"]
            next_page = result["data"]["search"]["pageInfo"]["hasNextPage"]
        elif typeSearch == "tag":
            nodes = result["data"]["repository"]["releases"]["nodes"]
            next_page = result["data"]["repository"]["releases"]["pageInfo"]["hasNextPage"]

        if typeSearch == "base":
            numPages = NUMPAGESREPO #define number of pages to search for repositories for base.csv
        elif typeSearch == "tag":            
            releases = int(nodeFinal[2])
            print("\nnum releases: " + str(releases))
            numPages = ceil(releases/30) #define numger of pages to search for releases/tags (specific repositoy)
            print("num pages: " + str(numPages))
        
        total_pages = 1
        while next_page and total_pages < numPages:
            if typeSearch == "base":
                cursor = result["data"]["search"]["pageInfo"]["endCursor"]
            elif typeSearch == "tag":
                cursor = result["data"]["repository"]["releases"]["pageInfo"]["endCursor"]
            next_query = self.query.replace("{AFTER}", ", after: \"%s\"" % cursor)
            json["query"] = next_query
            result = self.run_query(json, self.headers)
            if typeSearch == "base":
                nodes += result['data']['search']['nodes']
                next_page = result["data"]["search"]["pageInfo"]["hasNextPage"]
            elif typeSearch == "tag":
                nodes += result['data']["repository"]["releases"]['nodes']
                next_page = result["data"]["repository"]["releases"]["pageInfo"]["hasNextPage"]
            print(".", end='')
            total_pages += 1
        print("]")
    
        if typeSearch == "base":
            print("Criando arquivo base CSV")
            file = open("base.csv", 'w', newline='')
            repository = csv.writer(file)
            print("Salvando Repositorios:\n[", end='')
            repository.writerow(('nameWithOwner', 'url', 'stars', 'releases', 'primaryLanguage', 'createdAt', 'updatedAt'))
            num = 0
            for node in nodes:
                splitCreatedAt = node['createdAt'].split('T')
                createdAt = splitCreatedAt[0]
                splitUpdatedAt = node['updatedAt'].split('T')
                updatedAt = splitUpdatedAt[0]
                repository.writerow((node['nameWithOwner'], str(node['url']),
                             str(node['stargazers']['totalCount']), str(
                                 node['releases']['totalCount']),
                             node['primaryLanguage']['name'], str(createdAt), str(updatedAt)))
                num = num + 1
                if (num % 10) == 0:
                    print(".", end='')
            print("]\nProcesso concluido")
            file.close()

        if typeSearch == "tag":
            nameWithOwner = nodeFinal[0]
            url = nodeFinal[1]
            newFilePath = owner + "-" + name + ".csv"
            fullFilePath = path + "/" + newFilePath
            print("Criando arquivo tag CSV")
            fileTag = open(fullFilePath, 'w')
            fileTag.close()
            fileTag = open(fullFilePath, 'a', newline='')
            repoTag = csv.writer(fileTag)
            print("Salvando Tags:\n[", end='')
            repoTag.writerow(('nameWithOwner', 'url', 'tagName', 'publishedAt', 'totalLoc', 'totalSloc', 'validFiles', 'invalidFiles', 'filesNotRead', 'filesNoMetric', 'cc', 'ccRank',
                    'miMultiFalse', 'miMultiFalseRank', 'miMultiTrue', 'miMultiTrueRank', 'difficulty', 'effort', 'timeHas', 'bugs'))
            repoTag.writerow(nodeFinal)
            num = 0
            for node in nodes:
                publishedAtSplit = node['publishedAt'].split('T')
                publishedAt = publishedAtSplit[0]
                repoTag.writerow((nameWithOwner, url, node['tagName'], str(publishedAt)))
                num = num + 1
                if (num % 10) == 0:
                    print(".", end='')
            print("]\nProcesso concluido")
            fileTag.close()
        


