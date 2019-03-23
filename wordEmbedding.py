# -------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                      #
# TODO - Zmienne lepiej odzwierciedlajace przechowywane dane jak bedziemy pewni, ze wszystko zrobione)                 #
# TODO - Testowanie modelu w oparciu o logiczne myslenie                                                               #
# TODO - Uznac wyrazy typu 'a', 'the' etc za nieważne (czyt. z wagą 0), NULL tez!                                      #
# [OSOBNY BRANCH] THEORY CRAFTING - TODO - Opisy podzielic na zdania, wszystkie zdania rozwalic na wyrazy              #
# TODO - Dodanie reszty info do Corpusu (jak wszystko wyzej zostanie zrobione/przetestowane)                           #
#                                                                                                                      #
# Jesli cos  zrobicie to usuncie. Jak zrobicie wszystko z listy zostawcie naglowek i te wiadomosc                      #
# ------------------------------------------ ELO MORDY --------------------------------------------------------------- #

import numpy as np
import pandas as pd
from gensim.models import word2vec

try:
    linkingWords = open("linkingWords.txt").read().split()
except FileNotFoundError as e:
    linkingWords = open("linkingWords.txt", "w+").write("")
    print(e)

for row in range(len(linkingWords)):
    linkingWords[row] = linkingWords[row].casefold()

corpus = list()  # kręgosłup - wszystkie dane

df = pd.read_csv("dataSet.csv", sem=";", index_col=0)  # baza danych (czytamy pliki)
dfKey = pd.read_csv("dataKeywords.csv", sem=";", index_col=0)  # keywords (czytamy pliki)

for row in df.values:  # wyciagnij typ i recenzje [poki co tylko tyle, na potrzeby testow]
    for element in range(len(row)):
        if type(row[element]) is not str:
            continue
        for word in linkingWords:
            if word in row[element]:
                row[element] = row[element].replace(" " + word + " ", " ")
    corpus.append(str(row[4]).casefold() + " " + str(row[5]).casefold())  # jeden wpis to jeden film

tokenized_sentences = [sentence.split() for sentence in corpus]  # wyrazy z sentencji (dzielimy zdania na wyrazy)
model = word2vec.Word2Vec(tokenized_sentences, min_count=1, hs=1, negative=0, workers=4)  # 'workers' to wątki CPU
model.train(tokenized_sentences, total_examples=len(tokenized_sentences), epochs=20)  # trenowanie, epochs - l. iteracji
model.save("vocab.model")  # zapis słownika/modelu do pliku (binarnie)


# jeden wyraz
# print(model.wv.most_similar(positive=['girl'], topn=3))  # pokaz najbardziej podobne
# print(model.wv.most_similar(negative=['girl'], topn=3))  # pokaz najmniej podobne

# wszystkie keywordsy
# j = 1  # iterator - wiersze
# for row in dfKey.values:  # for ewery (~R.W.) keyword
#     tempPositivities = list()  # tymczasowa lista, przechowuje info o jednym wierszu
#     score = model.wv.most_similar(positive=row, topn=3)  # 3 najbardziej podobne wyniki do keyworda
#     tempPositivities.append(row[0])  # dodaj keyworda
#     for i in range(3):
#         tempPositivities.append(score[i][0])  # utnij prawdopodobienstwo, dodaj tylko nazwe

#     if j == 1:
#        positivities = np.array(tempPositivities)  # pierwszy wpis
#     else:
#        positivities = np.append(positivities, tempPositivities).reshape((j, len(tempPositivities)))  # konwersja na 2d

#     j += 1  # kolejny wiersz

# print(positivities)

# print(model.wv.vocab)

# for word in dfKey.values:
#    print(word, " =>", model.wv[word])

print(model.wv.most_similar(positive=['girl'], topn=3))
print(model.wv.most_similar(negative=['girl'], topn=3))
print(model.wv.most_similar(positive=['documentary'], topn=3))
print(model.wv.most_similar(negative=['documentary'], topn=3))
