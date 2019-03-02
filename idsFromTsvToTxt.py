import csv

imdbIds = list()

fileRW = open('imdbIDs.txt', "a+")

with open('data.tsv', encoding="utf8") as tsvfile:
    reader = csv.reader(tsvfile, delimiter='\t')
    for row in reader:
        fileRW.write(row[0][2:] + "\n")
