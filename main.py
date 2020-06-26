import csv
import os
import stat
import requests

headers = {"Authorization": "Bearer YOUR KEY HERE "}


def run_query(json, headers):  # Função que executa uma request pela api graphql
    request = requests.post('https://api.github.com/graphql', json=json, headers=headers)
    while request.status_code == 502:
        request = requests.post('https://api.github.com/graphql', json=json, headers=headers)
    if request.status_code == 200:
        return request.json()  # json que retorna da requisição
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


def on_rm_error(func, path, exc_info):
    # path contains the path of the file that couldn't be removed
    # let's just assume that it's read-only and unlink it.
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)


def writeFirstLine(file):
    file.writerow(('nameWithOwner', 'url', 'stargazers/totalCount', 'releases/totalCount', 'primaryLanguage/name',
                   'createdAt', 'updatedAt'))


def writeNodeLine(file, node):
    file.writerow((node['nameWithOwner'], node['url'], str(node['stargazers']['totalCount']),
                   str(node['releases']['totalCount']), node['primaryLanguage']['name'], node['createdAt'],
                   node['updatedAt']))


print("Iniciando processo")
query = """
query example{
    search (query:"stars:100..{STARS} language:Python", type: REPOSITORY, first:50{AFTER}) {
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
    rateLimit{
        remaining
        resetAt
    }
}
"""

first_query = query.replace("{STARS}", "*")
final_query = first_query.replace("{AFTER}", "")

json = {
    "query": final_query, "variables": {}
}

total_pages = 1
print("Executando Query\n[", end='')
result = run_query(json, headers)  # Executar a Query
nodes = result["data"]["search"]["nodes"]  # separar a string para exibir apenas os nodes
next_page = result["data"]["search"]["pageInfo"]["hasNextPage"]

while next_page and total_pages < 200:
    if result['data']['rateLimit']['remaining'] == 0:
        print("[REPORT]: CHANGING TOKEN")
        headers = {"Authorization": "Bearer YOUR KEY HERE "}  # due to query limits

    total_pages += 1

    print("[REPORT]: QUERYING PAGE:" + str(total_pages))

    cursor = result["data"]["search"]["pageInfo"]["endCursor"]

    next_query = first_query.replace("{AFTER}", ", after: \"%s\"" % cursor)

    json["query"] = next_query
    result = run_query(json, headers)
    nodes += result['data']['search']['nodes']
    next_page = result["data"]["search"]["pageInfo"]["hasNextPage"]

    # for each block of 100 pages, qe have to make a new query (based on the number of stars)
    if total_pages % 10 == 0:
        if total_pages == 200:  # some workaround
            continue

        total_pages += 1
        print("[REPORT]: QUERYING PAGE:" + str(total_pages))

        first_query = query.replace("{STARS}", str(nodes[-1]['stargazers']['totalCount']))
        final_query = first_query.replace("{AFTER}", "")
        json["query"] = final_query

        result = run_query(json, headers)
        nodes += result['data']['search']['nodes']
        next_page = result["data"]["search"]["pageInfo"]["hasNextPage"]

fileFinal1000 = open("final1000.csv", 'w', newline='')
final1000 = csv.writer(fileFinal1000)
writeFirstLine(final1000)

fileFinal5000 = open("final5000.csv", 'w', newline='')
final5000 = csv.writer(fileFinal5000)
writeFirstLine(final5000)

fileFinal10000 = open("final10000.csv", 'w', newline='')
final10000 = csv.writer(fileFinal10000)
writeFirstLine(final10000)

numRepo = 0
for node in nodes:
    if numRepo < 1000:
        writeNodeLine(final1000, node)
        writeNodeLine(final5000, node)
        writeNodeLine(final10000, node)
    elif numRepo < 5000:
        writeNodeLine(final5000, node)
        writeNodeLine(final10000, node)
    else:
        writeNodeLine(final10000, node)
    numRepo += 1
print("Total repositórios " + str(numRepo))
fileFinal1000.close()
fileFinal5000.close()
fileFinal10000.close()
print("\n ------------- Fim da execução ------------- \n")
