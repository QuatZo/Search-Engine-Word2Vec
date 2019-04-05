# -------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                      #
# TODO - Zabawa parametrami modelu, sprawdzanie najlepszego (najbardziej dokladnego) rozwiazania                       #
# TODO - Sposob sortowania wynikow (myslalem nad sortowaniem wg ratingu, ale wtedy trzeba to [nawet losowo] uzupelnic) #
# TODO - Usunac wszelkie liczby z corpusu (aktualny sposob nie do konca dziala)                                        #
#                                                                                                                      #
# Jesli cos  zrobicie to usuncie. Jak zrobicie wszystko z listy zostawcie naglowek i te wiadomosc                      #
# ------------------------------------------ ELO MORDY --------------------------------------------------------------- #

import numpy as np
import pandas as pd
from gensim.models import word2vec
import time

# region Variables
# --------------------------------------------- INICJALIZACJA ZMIENNYCH ---------------------------------------------- #
path_to_model = "vocab.model"
path_to_dataset = "dataset.csv"
path_to_stop_words = "stop_words.txt"
# ------------------------------------------------------ KONIEC ------------------------------------------------------ #
# endregion

# region Functions


# ------------------------------------ FUNKCJA SPRAWDZAJACA CZY MODEL JUZ ISTNIEJE ----------------------------------- #
def model_exists(arg_path_to_model):
    try:
        word2vec.Word2Vec.load(arg_path_to_model)
        print("Slownik juz istnieje")
        return True
    except FileNotFoundError:
        print("Slownik", arg_path_to_model, "nie istnieje. Zaczynamy trening od poczatku.")
        return False
# ------------------------------------------------------ KONIEC ------------------------------------------------------ #


# ------------------------------------------- FUNKCJA PRZYGOTOWUJACA DANE -------------------------------------------- #
def prepare_data(arg_path_to_dataset, arg_path_to_stop_words):
    print("-" * 10)
    print("Trwa przygotowywanie danych.")
    corpus = list()
    start = time.time()
    try:
        stop_words = open(arg_path_to_stop_words, encoding='utf8').read().split()
    except FileNotFoundError:
        stop_words = list()

    df_set = pd.read_csv(arg_path_to_dataset, sep=";", index_col=0)  # baza danych (czytamy pliki)

    for row in df_set.values:  # wyciągnij informacje
        temp_str = ""
        for i in range(len(row)):
            if i == 1 or i == 3:  # pomijamy rok i rating
                continue
            if str(row[i]).casefold() != 'nan':  # przepisujemy tylko niepuste dane
                temp_str += str(row[i]).replace('.', ',').casefold() + '.'

        corpus.append(temp_str)  # jeden wpis to jeden film

    corpus = "".join(corpus)  # tworzy dokument
    # zamieniamy znaki interpunkcyjne na jeden ('.'), usuwamy '\s' i ',' jesli jeszcze jakies istnieja
    # zamieniamy autorow na {imie} i {nazwisko} zamiast na {imie_nazwisko}
    corpus = corpus.replace('?', '.').replace('!', '.').replace('\'s', '').replace(',', '').replace('_', ' ').split('.')
    tokenized_sentences = [sentence.replace('.', '').split() for sentence in corpus]  # wyrazy z sentencji

    # usuwanie stop-words z corpusu
    print("-" * 10)
    print("Trwa usuwanie niepotrzebnych wyrazow (np. 'a', 'the')")
    for sentence in range(len(tokenized_sentences)):
        for word in tokenized_sentences[sentence]:  # usuwanie liczb
            try:
                int(word)
                tokenized_sentences[sentence].remove(word)

            except ValueError:
                continue
        for stop_word in stop_words:  # usuwanie stop_words
            while True:
                try:
                    tokenized_sentences[sentence].remove(stop_word)
                except ValueError:
                    break

    print("Czyszczenie danych zakonczone. Czas trwania:", time.time() - start, "secs")
    return tokenized_sentences
# ------------------------------------------------------ KONIEC ------------------------------------------------------ #


# --------------------------------------------- FUNKCJA TRENUJACA MODEL ---------------------------------------------- #
def train_model(arg_dataset, arg_path_to_model, arg_epochs=20, arg_size=300, arg_sample=1e-3,
                arg_min_count=5, arg_workers=12, arg_iter=5):
    print("-" * 10)
    print("Rozpoczynamy trening")
    try:
        start = time.time()
        model = word2vec.Word2Vec(arg_dataset, size=arg_size, sample=arg_sample, min_count=arg_min_count,
                                  workers=arg_workers, iter=arg_iter)
        model.train(arg_dataset, total_examples=len(arg_dataset), epochs=arg_epochs)  # trenowanie
        model.save(arg_path_to_model)  # zapis słownika/modelu do pliku (binarnie)
        print("Trening zakonczony. Czas trwania:", time.time() - start, "secs")
        return True
    except:
        return False
# ------------------------------------------------------ KONIEC ------------------------------------------------------ #
# endregion

# region Main


if not model_exists(path_to_model):
    processed_data = prepare_data(path_to_dataset, path_to_stop_words)
    if not train_model(processed_data, path_to_model, arg_epochs=20, arg_iter=10):  # arg_iter=50 - nie polecam
        print("Ups! Cos poszlo nie tak!")
# endregion
