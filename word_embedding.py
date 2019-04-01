# -------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                      #
# TODO - Testowanie modelu w oparciu o logiczne myslenie                                                               #
# TODO - Stworzenie search engine (osobny plik)                                                                        #
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
path_to_most_common_words = "most_common_english_words.txt"
top_n = 3
corpus = list()  # kręgosłup - wszystkie dane
probability_positive = dict()
rows_per_element = dict()
amount_of_rows = 30
# ------------------------------------------------------ KONIEC ------------------------------------------------------ #
# endregion

try:
    most_common_words = open(path_to_most_common_words).read().split()
except FileNotFoundError as e:
    most_common_words = list()

df_set = pd.read_csv(path_to_dataset, sep=";", index_col=0)  # baza danych (czytamy pliki)

for row in df_set.values:  # wyciągnij informacje
    temp_str = ""
    for i in range(len(row)):
        if i == 1 or i == 3:
            continue
        if str(row[i]).casefold() != 'nan':
            temp_str += str(row[i]).replace('.', ',').casefold() + '.'

    corpus.append(temp_str)  # jeden wpis to jeden film

corpus = "".join(corpus)  # tworzy dokument
corpus = corpus.replace('?', '.').replace('!', '.').replace('\'s', '').replace(',', '').replace('_', ' ').split('.')
tokenized_sentences = [sentence.replace('.', '').split() for sentence in corpus]  # wyrazy z sentencji

# usuwanie most-common english words z corpusu
for sentence in range(len(tokenized_sentences)):
    for most_common_word in most_common_words:
        while True:
            try:
                tokenized_sentences[sentence].remove(most_common_word)
            except ValueError:
                break

try:
    model = word2vec.Word2Vec.load(path_to_model)
except FileNotFoundError:
    print("Slownik", path_to_model, "nie istnieje. Zaczynamy trening od poczatku.")
    model = word2vec.Word2Vec(tokenized_sentences, seed=1, sample=1e-3, min_count=3, workers=12)
    model.train(tokenized_sentences, total_examples=len(tokenized_sentences), epochs=20)  # trenowanie
    model.save(path_to_model)  # zapis słownika/modelu do pliku (binarnie)

for element in ['marvel', 'hate', 'everyone']:
    try:
        print("Word:", element)
        prob_pos_el = probability_positive[element] = model.wv.most_similar(positive=[element], topn=top_n)
        prob_pos_el = model.wv.most_similar_cosmul(positive=[element], topn=top_n)

        print("\tPositive:")
        for i in range(top_n):
            print("\t\t", prob_pos_el[i][0], ":", prob_pos_el[i][1])
        print()
        rows_per_element[element] = [1, prob_pos_el[1][1] / prob_pos_el[0][1], prob_pos_el[2][1] / prob_pos_el[0][1]]
        # Dodanie algorytmu wyznaczajacego ilosc wierszy z danymi wyrazami (mozliwe, ze osobny plik)
        # suma elementow rows_per_element[element] to wspolczynnik x (np. 2.73x), y to liczba wynikow (np. 25)
        # Trzeba wyznaczyc x, dzieki czemu poznamy ilosc wynikow dla poszczegolnego wyrazu podobnego
        temp_alg = amount_of_rows / sum(rows_per_element[element])
        rows_per_element[element] = [int(temp_alg), int((prob_pos_el[1][1] / prob_pos_el[0][1]) * temp_alg),
                                     int((prob_pos_el[2][1] / prob_pos_el[0][1]) * temp_alg)]
        print(rows_per_element)
    except KeyError as e:
        print("\t", str(e)[1:-1])  # usuwamy "" z początku
