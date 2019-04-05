# -------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                      #
# TODO - W miejsce tablicy 'which film was the...' wstawic wynik inputa                                                #
# TODO - Dodac algorytm wyswietlajacy najlepsze wyniki wedlug zadanego kryterium (np rating -> trzeba uzupelnic dane)  #
# TODO - Okreslic ilosc wyswietlanych wynikow oraz forme ich reprezentacji                                             #
# TODO - [OSTATNIE Z OSTATNICH] - Stworzyc jeden plik, ktory bedzie wszystko obslugiwal (pewnie moje zadanie ~Dawid)   #
#                                                                                                                      #
# Jesli cos  zrobicie to usuncie. Jak zrobicie wszystko z listy zostawcie naglowek i te wiadomosc                      #
# ------------------------------------------ ELO MORDY --------------------------------------------------------------- #

import numpy as np
import pandas as pd
from gensim.models import word2vec

# region Variables
# --------------------------------------------- INICJALIZACJA ZMIENNYCH ---------------------------------------------- #
path_to_model = "vocab.model"
top_n = 3
probability_positive = dict()
rows_per_element = dict()
amount_of_rows = 30
# ------------------------------------------------------ KONIEC ------------------------------------------------------ #
# endregion

try:
    model = word2vec.Word2Vec.load(path_to_model)
except FileNotFoundError:
    print("Brak modelu")
    exit(-1)

# Przed tym musi byc input z tekstem, ktory zostanie wprowadzony
# Trzeba tez przygotowac w/w tekst do ponizszej postaci (pomoze w tym tokenizacja z word_embedding)
# Tokenizacja tak czy siak musi zostac przeniesiona do innego pliku, bo beda z niej korzystac (teraz) 3 pliki
for element in ['which', 'film', 'was', 'the', 'best', 'in', '2019', 'dc', 'universe', 'or', 'marvel', 'or', 'disney']:
    try:
        print("Word:", element)
        prob_pos_el = probability_positive[element] = model.wv.most_similar_cosmul(positive=[element], topn=top_n)

        probability_ratio = list()
        for i in range(top_n):
            probability_ratio.append(prob_pos_el[i][1] / prob_pos_el[0][1])
            print("\t", prob_pos_el[i][0], ":", prob_pos_el[i][1])  # wyraz : pewnosc

        temp_alg = amount_of_rows / sum(probability_ratio)  # ilosc wyrazow na pierwszy wyraz
        rows_per_element[element] = [int(temp_alg), int(probability_ratio[1] * temp_alg),
                                     int(probability_ratio[2] * temp_alg)]  # obliczanie 2 i 3 wyrazu (ilosc wyrazow)
    except KeyError as e:
        print("\t", str(e)[1:-1])  # usuwamy "" z początku

for key, val in rows_per_element.items():
    print(key, "=>", val)
