# KURWA POKI CO NIE ZWRACAC UWAGI NA TO O 3.6. ZAINSTALUJCIE '''''GENSIM''''' I POWINNO DZIALAC
# -----Dziala na pythonie 3.6, tensorflow nie dziala jeszcze na 3.7; pobrac z neta, zainstalowac 3.6
# -----Plik -> Opcje -> wyszukac 'interpreter', wyswietlic wszystkie, dodac swoj i wybrac 3.6
# -----zainstalowac ponizsze pakiety w w/w miejscu

import numpy as np
import pandas as pd
# import tensorflow as tf
# from tensorflow import keras
# import os
from gensim.models import word2vec

# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # usuwa warning z tensorflow [wystepuje na Ryzenach]
corpus = list()

df = pd.read_csv("dataSet.csv", sep=";", index_col=0)  # baza danych
dfKey = pd.read_csv("dataKeywords.csv", sep=";", index_col=0)  # keywords

for row in df.values:  # wyciagnij typ i recenzje [poki co tylko tyle, na potrzeby testow]
    corpus.append(row[4] + " " + row[5])  # jeden wpis to jeden film
    # corpus.append(row[5])

tokenized_sentences = [sentence.split() for sentence in corpus]  # wyrazy z sentencji
model = word2vec.Word2Vec(tokenized_sentences, min_count=1, hs=1, negative=0, workers=4)  # pracownicy to wątki CPU
model.train(tokenized_sentences, total_examples=len(tokenized_sentences), epochs=20)  # trenuj
print(model.most_similar(positive=['white']))  # pokaz najbardziej podobne
print(model.most_similar(negative=['white']))  # pokaz najmniej podobne

# print(model.wv.vocab)

# for word in dfKey.values:
#     print(word, " =>", model.wv[word])
