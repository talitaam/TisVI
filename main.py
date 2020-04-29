import git
import csv
import os
import shutil
import stat
import time
import requests
from radon.raw import analyze
import threading

global totalLoc

TIME_LIMIT_TO_FIND_LOC = 600 #seconds
TIMESLEEP = 60 #seconds

headers = {"Authorization": "Bearer 8ae75f646ea8969a39bffb77fe3bcc0c1c72d084 "}


def run_query(json, headers):  # Função que executa uma request pela api graphql
    request = requests.post('https://api.github.com/graphql', json=json, headers=headers)
    while (request.status_code == 502):
        time.sleep(2)
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

def cloneAndReadFileAndGetLoc(repo_path, tag, x):
    g.checkout(tag['node']['tagName'])
    print("Lendo arquivos do Repositório e calculando LOC.....")
    global totalLoc
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith('.py'):
                fullpath = os.path.join(root, file)
                with open(fullpath, encoding="utf8") as f:
                    content = f.read()
                    b = analyze(content)
                    i = 0
                    for item in b:
                        if i == 0:
                            totalLoc[x] += item
                            i += 1

if not os.path.exists("base.csv"):
    print("Iniciando processo")

    # Query do GraphQL que procura os primeiros 1000 repositorios com mais de 100 estrelas.
    query = """
    query example{
  search (query:"stars:>100 and language: Python",type: REPOSITORY, first:2) {
      pageInfo{
       hasNextPage
        endCursor
      }
    edges {
      node {
        ... on  Repository{
          name
          updatedAt
          url
          primaryLanguage{
            name
          }
          releases(first: 3){
            totalCount
            edges {
              node {
                tagName
                name
              }
            }
          }
        }
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
    result = run_query(json, headers)  # Executar a Query
    nodes = result["data"]["search"]["edges"]  # separar a string para exibir apenas os nodes
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

    fileFinal = open("final.csv", 'w', newline='')
    final = csv.writer(fileFinal)
    final.writerow(('nameWithOwner', 'updateAt', 'url', 'primary language/name', 'release 1',
                    'release 2', 'release 3'))

    for node in nodes:
        print("\n ------ Começo leitura repositorios ------ \n")

        numRepo = 0
        time.sleep(1)
        totalLoc = 0
        name = node['node']['name']
        repo_path = "path/to/" + name
        gitURL = node['node']['url']

        if not os.path.exists(repo_path):
            print("\n" + "Começa o git clone")
            print(gitURL)
            repo = git.Repo.clone_from(gitURL, repo_path)
            repo.close()
            print("Termina o git clone \n")

        g = git.Git(repo_path)
        x = 0
        totalLoc = [0,0,0]
        for tag in node['node']['releases']['edges']:
            clrd = threading.Thread(target=cloneAndReadFileAndGetLoc, args=(repo_path, tag, x))
            clrd.daemon = True
            clrd.start()
            clrd.join(TIME_LIMIT_TO_FIND_LOC)  # Wait for x seconds or until process finishes
            if clrd.is_alive():  # If thread is still active
                print("\n--> Excedeu limite de tempo. Interrompendo análise do repositório.....")
                th = threading.currentThread()
                th._stop
                time.sleep(TIMESLEEP)
                totalLoc[x] = -1  # Define a negative value for LOC
            print("Total loc final é " + str(totalLoc[x]))
            x += 1
        print("\n ------ Fim de um repositorio ------ \n")
        final.writerow((name, node['node']['updatedAt'], gitURL, node['node']['primaryLanguage']['name'], totalLoc[0],
                        totalLoc[1], totalLoc[2]))
        clean_repository(repo_path)
        numRepo = numRepo + 1
        print("Total repositórios " + str(numRepo))
    fileFinal.close()
    print("\n ------------- Fim da execução ------------- \n")

