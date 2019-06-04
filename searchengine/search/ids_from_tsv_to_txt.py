import csv

file_rw = open('imdb_ids.txt', "a+")

with open('data.tsv', encoding="utf8") as tsvfile:
    reader = csv.reader(tsvfile, delimiter='\t')
    for row in reader:
        file_rw.write(row[0][2:] + "\n")
