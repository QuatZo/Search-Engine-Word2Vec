# -------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                      #
#                     OD TRZECIEGO TODO JEST NAJWAŻNIEJSZE, DWA PIERWSZE ZOSTAWCIE NA KONIEC!                          #
#                                                                                                                      #
# TODO - Zmienne lepiej odzwierciedlajace przechowywane dane jak bedziemy pewni, ze wszystko zrobione)                 #
# TODO - Testowanie modelu w oparciu o logiczne myslenie                                                               #
# TODO - Dodanie reszty info do Corpusu (procz ratingu i [możliwe] dat)                                                #
# TODO - Z corpusu stworzyc 'dokument' podzielony na zdania tablica jednowymiarowa, podzielone na zdania wg . ! ?      #
# TODO - Usunac most-common english words z corpusu (nie linkingWords)                                                 #
# TODO - Corpus podzielic na wyrazy (tokenized_sentences, zrobione, ale zostawiam dla informacji)                      #
#                                                                                                                      #
# Jesli cos  zrobicie to usuncie. Jak zrobicie wszystko z listy zostawcie naglowek i te wiadomosc                      #
# ------------------------------------------ ELO MORDY --------------------------------------------------------------- #

import numpy as np
import pandas as pd
from gensim.models import word2vec

pathToModel = "vocab.model"

try:
    linkingWords = open("linkingWords.txt").read().split()
except FileNotFoundError as e:
    linkingWords = open("linkingWords.txt", "w+").write("")
    print(e)

for row in range(len(linkingWords)):
    linkingWords[row] = linkingWords[row].casefold()

corpus = list()  # kręgosłup - wszystkie dane

df = pd.read_csv("dataSet.csv", sep=";", index_col=0)  # baza danych (czytamy pliki)
dfKey = pd.read_csv("dataKeywords.csv", sep=";", index_col=0)  # keywords (czytamy pliki)

for row in df.values:  # wyciagnij typ i recenzje [poki co tylko tyle, na potrzeby testow]
    for element in range(len(row)):
        if type(row[element]) is not str:
            continue
        for word in linkingWords:
            if word in row[element]:
                row[element] = row[element].replace(" " + word + " ", " ")
    corpus.append(str(row[4]).casefold() + " " + str(row[5]).casefold())  # jeden wpis to jeden film

tokenized_sentences = [sentence.split() for sentence in corpus]  # wyrazy z sentencji (dzielimy zdania na wyrazy)

try:
    model = word2vec.Word2Vec.load(pathToModel)
except FileNotFoundError:
    print("Slownik ", pathToModel, " nie istnieje. Zaczynamy trening od poczatku.")
    model = word2vec.Word2Vec(tokenized_sentences, min_count=1, hs=1, negative=0, workers=4)  # 'workers' to wątki CPU
model.train(tokenized_sentences, total_examples=len(tokenized_sentences), epochs=20)  # trenowanie, epochs - l. iteracji
model.save(pathToModel)  # zapis słownika/modelu do pliku (binarnie)

for element in ['mystery', 'documentary']:
    try:
        print("Word: ", element)
        print("\tPositive: ", model.wv.most_similar(positive=[element], topn=3))
        print("\tNegative: ", model.wv.most_similar(negative=[element], topn=3))
    except KeyError as e:
        print("\t", str(e)[1:-1])  # usuwamy "" z początku
