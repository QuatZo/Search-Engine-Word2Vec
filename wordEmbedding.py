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
topN = 3
corpus = list()  # kręgosłup - wszystkie dane

df = pd.read_csv("dataSet.csv", sep=";", index_col=0)  # baza danych (czytamy pliki)
dfKey = pd.read_csv("dataKeywords.csv", sep=";", index_col=0)  # keywords (czytamy pliki)

for row in df.values:  # wyciagnij typ i recenzje [poki co tylko tyle, na potrzeby testow]
    corpus.append(str(row[4]).casefold() + " " + str(row[5]).casefold())  # jeden wpis to jeden film

tokenized_sentences = [sentence.split() for sentence in corpus]  # wyrazy z sentencji (dzielimy zdania na wyrazy)

try:
    model = word2vec.Word2Vec.load(pathToModel)
except FileNotFoundError:
    print("Slownik ", pathToModel, " nie istnieje. Zaczynamy trening od poczatku.")
    model = word2vec.Word2Vec(tokenized_sentences, min_count=1, hs=1, negative=0, workers=12)  # 'workers' to wątki CPU
model.train(tokenized_sentences, total_examples=len(tokenized_sentences), epochs=20)  # trenowanie, epochs - l. iteracji
model.save(pathToModel)  # zapis słownika/modelu do pliku (binarnie)

positiveProbability = dict()
negativeProbability = dict()
for element in ['mystery', 'documentary', 'where']:
    try:
        print("Word:", element)
        posProbEl = positiveProbability[element] = model.wv.most_similar(positive=[element], topn=topN)
        negProbEl = negativeProbability[element] = model.wv.most_similar(negative=[element], topn=topN)

        print("\tPositive:")
        for i in range(topN):
            print("\t\t", posProbEl[i][0], ":", posProbEl[i][1])
        print("\tNegative:")
        for i in range(topN):
            print("\t\t", negProbEl[i][0], ":", negProbEl[i][1])
        print()
    except KeyError as e:
        print("\t", str(e)[1:-1])  # usuwamy "" z początku
