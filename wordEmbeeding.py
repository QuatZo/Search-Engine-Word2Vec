# Dziala na pythonie 3.6, tensorflow nie dziala jeszcze na 3.7; pobrac z neta, zainstalowac 3.6
# Plik -> Opcje -> wyszukac 'interpreter', wyswietlic wszystkie, dodac swoj i wybrac 3.6
# zainstalowac ponizsze pakiety w w/w miejscu

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
import os
from gensim.models import word2vec

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # usuwa warning z tensorflow [wystepuje na Ryzenach]
corpus = list()

df = pd.read_csv("dataSet.csv", sep=";", index_col=0)
dfKey = pd.read_csv("dataKeywords.csv", sep=";", index_col=0)

for row in df.values:
    corpus.append(row[4])
    corpus.append(row[5])

tokenized_sentences = [sentence.split() for sentence in corpus]
model = word2vec.Word2Vec(tokenized_sentences, min_count=1, hs=1, negative=0)

# print(model.wv.vocab)

for word in dfKey.values:
    print(word, " =>", model.wv[word])
