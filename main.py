import csv
import os

print("Iniciando processo")

higherNumFail = 0

for fileName in os.listdir("RepoTags"):
    print("Lendo " + fileName)
    file = open("RepoTags/" + fileName, encoding='utf-8')
    repo = csv.reader(file)
    numLine = 0
    numFail = 0
    for line in repo:
        if numLine > 2:
            if line[10] == "-1":
                numFail += 1
        numLine += 1
    file.close()
    print("Fim\nfails =  ", numFail, "\ttotal = ", numLine - 2)
    if 0.5 < numFail / (numLine - 2):
        os.rename("RepoTags/" + fileName, "RepoTagsIncorrect/" + fileName)
    if higherNumFail < numFail:
        higherNumFail = numFail
    print("\n ------ Fim de um repositorio ------ \n")
print("Maior numero de erros em um arquivo = ", higherNumFail)
print("\n ------------- Fim da execução ------------- \n")
