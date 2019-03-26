# -------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                      #
#                     OD TRZECIEGO TODO JEST NAJWAŻNIEJSZE, DWA PIERWSZE ZOSTAWCIE NA KONIEC!                          #
#                                                                                                                      #
# TODO - Zmienne lepiej odzwierciedlajace przechowywane dane jak bedziemy pewni, ze wszystko zrobione)                 #
# TODO - Testowanie modelu w oparciu o logiczne myslenie                                                               #
# TODO - Usunac most-common english words z corpusu (nie linkingWords) - Wojtek Zimoch                                 #
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
for row in df.values:  # wyciągnij informacje
    tempStr = ""
    # TODO - Ziojtek tutaj
    if str(row[0]).casefold() != 'nan':
        tempStr += str(row[0]).replace('.', ',').casefold() + '.'
    if str(row[2]).casefold() != 'nan':
        tempStr += str(row[2]).replace('.', ',').casefold() + '.'
    if str(row[4]).casefold() != 'nan':
        tempStr += str(row[4]).replace('.', ',').casefold() + '.'
    if str(row[5]).casefold() != 'nan':
        tempStr += str(row[5]).replace('.', ',').casefold() + '.'
    if str(row[6]).casefold() != 'nan':
        tempStr += str(row[6]).replace('.', ',').casefold() + '.'

    corpus.append(tempStr)  # jeden wpis to jeden film
corpus = "".join(corpus)  # tworzy dokument
corpus = corpus.replace('?', '.').replace('!', '.').split('.')  # zamiana znaków '?' i '!' na kropki
tokenized_sentences = [sentence.replace('.', '').split() for sentence in corpus]  # wyrazy z sentencji

try:
    model = word2vec.Word2Vec.load(pathToModel)
except FileNotFoundError:
    print("Slownik", pathToModel, "nie istnieje. Zaczynamy trening od poczatku.")
    model = word2vec.Word2Vec(tokenized_sentences, min_count=1, hs=1, negative=0, workers=12)  # 'workers' to wątki CPU
model.train(tokenized_sentences, total_examples=len(tokenized_sentences), epochs=20)  # trenowanie, epochs - l. iteracji
model.save(pathToModel)  # zapis słownika/modelu do pliku (binarnie)

positiveProbability = dict()
negativeProbability = dict()
for element in ['mystery', 'documentary', 'episode']:
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
