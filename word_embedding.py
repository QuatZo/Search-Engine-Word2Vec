# -------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                      #
# TODO - Testowanie modelu w oparciu o logiczne myslenie                                                               #
# TODO - Usunac most-common english words z corpusu (nie linkingWords) - Wojtek Zimoch                                 #
#                                                                                                                      #
# Jesli cos  zrobicie to usuncie. Jak zrobicie wszystko z listy zostawcie naglowek i te wiadomosc                      #
# ------------------------------------------ ELO MORDY --------------------------------------------------------------- #

import numpy as np
import pandas as pd
from gensim.models import word2vec

# region Variables
# --------------------------------------------- INICJALIZACJA ZMIENNYCH ---------------------------------------------- #
path_to_model = "vocab.model"
path_to_dataset = "dataset.csv"
top_n = 3
corpus = list()  # kręgosłup - wszystkie dane
# ------------------------------------------------------ KONIEC ------------------------------------------------------ #
# endregion

df_set = pd.read_csv(path_to_dataset, sep=";", index_col=0)  # baza danych (czytamy pliki)

for row in df_set.values:  # wyciągnij informacje
    temp_str = ""
    # TODO - Ziojtek tutaj
    for i in range(len(row)):
        if i == 1 or i == 3:
            continue
        if str(row[i]).casefold() != 'nan':
            temp_str += str(row[i]).replace('.', ',').casefold() + '.'

    corpus.append(temp_str)  # jeden wpis to jeden film

corpus = "".join(corpus)  # tworzy dokument
corpus = corpus.replace('?', '.').replace('!', '.').split('.')  # zamiana znaków '?' i '!' na kropki
tokenized_sentences = [sentence.replace('.', '').split() for sentence in corpus]  # wyrazy z sentencji

try:
    model = word2vec.Word2Vec.load(path_to_model)
except FileNotFoundError:
    print("Slownik", path_to_model, "nie istnieje. Zaczynamy trening od poczatku.")
    model = word2vec.Word2Vec(tokenized_sentences, seed=1, sample=1e-3, min_count=3, workers=12)
model.train(tokenized_sentences, total_examples=len(tokenized_sentences), epochs=20)  # trenowanie, epochs - l. iteracji
model.save(path_to_model)  # zapis słownika/modelu do pliku (binarnie)

probability_positive = dict()
probability_negative = dict()
for element in ['david', 'love', 'draw']:
    try:
        print("Word:", element)
        prob_pos_el = probability_positive[element] = model.wv.most_similar(positive=[element], topn=top_n)
        prob_neg_el = probability_negative[element] = model.wv.most_similar(negative=[element], topn=top_n)

        print("\tPositive:")
        for i in range(top_n):
            print("\t\t", prob_pos_el[i][0], ":", prob_pos_el[i][1])
        print("\tNegative:")
        for i in range(top_n):
            print("\t\t", prob_neg_el[i][0], ":", prob_neg_el[i][1])
        print()
    except KeyError as e:
        print("\t", str(e)[1:-1])  # usuwamy "" z początku
