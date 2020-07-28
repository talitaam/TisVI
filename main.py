import csv
import os
from statistics import median

print("Iniciando processo")

higherNumFail = 0
filePercent = open("RepoPercent.csv", 'w', newline='', encoding='utf-8')
repoPercent = csv.writer(filePercent)
repoPercent.writerow(("nameWithOwner", "validFiles", "invalidFiles", "filesNotRead", "filesNoMetrics"))

for fileName in os.listdir("RepoTags"):
    print("Lendo " + fileName)
    file = open("RepoTags/" + fileName, encoding='utf-8')
    repo = csv.reader(file)
    validFiles = []
    invalidFiles = []
    filesNotRead = []
    filesNoMetrics = []
    nameWithOwner = ""
    numLine = 0
    numFail = 0
    for line in repo:
        if numLine == 1:
            nameWithOwner = line[0]
        if numLine > 1:
            if line[12] == "-1" or line[12] == "-2" or line[12] == "-3":
                numFail += 1
            if line[6] != -1 and line[7] != -1 and line[8] != -1 and line[9] != -1:
                total = int(line[6]) + int(line[7]) + int(line[8]) + int(line[9])
                if total == 0:
                    validFiles.append(int(0))
                    invalidFiles.append(int(0))
                    filesNotRead.append(int(0))
                    filesNoMetrics.append(int(0))
                else:
                    validFiles.append((int(line[6])/total)*100)
                    invalidFiles.append((int(line[7])/total)*100)
                    filesNotRead.append((int(line[8])/total)*100)
                    filesNoMetrics.append((int(line[9])/total)*100)
        numLine += 1
    repoPercent.writerow((nameWithOwner, median(validFiles), median(invalidFiles), median(filesNotRead), median(filesNoMetrics)))
    file.close()
    print("Fim\nfails =  ", numFail, "\ttotal = ", numLine - 2)
    if 0.5 < numFail / (numLine - 2):
        os.rename("RepoTags/" + fileName, "RepoTagsIncorrect/" + fileName)
    if higherNumFail < numFail:
        higherNumFail = numFail
    print("\n ------ Fim de um repositorio ------ \n")
filePercent.close()
print("Maior numero de erros em um arquivo = ", higherNumFail)
print("\n ------------- Fim da execução ------------- \n")
