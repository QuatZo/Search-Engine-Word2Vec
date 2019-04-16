# -------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                      #
#                                                                                                                      #
# Jesli cos  zrobicie to usuncie. Jak zrobicie wszystko z listy zostawcie naglowek i te wiadomosc                      #
# ------------------------------------------ ELO MORDY --------------------------------------------------------------- #


import time
import re
import random as rm

# region Functions


# ------------------------------------------- FUNKCJA PRZYGOTOWUJACA DANE -------------------------------------------- #
def prepare(arg_dataset, arg_path_to_stop_words, arg_rating_values):
    print("Preparing/Cleaning data, please wait...")
    corpus = list()
    start = time.time()
    try:
        stop_words = open(arg_path_to_stop_words, encoding='utf8').read().split()
    except FileNotFoundError:
        stop_words = list()

    for row in arg_dataset:  # wyciągnij informacje
        temp_str = ""
        for i in range(len(row)):
            if i == 1:  # pomijamy rok
                continue
            if i == 3 and str(row[i]).casefold() == 'nan':  # losowy wypelniamy rating
                row[i] = rm.choice(arg_rating_values)
            if str(row[i]).casefold() != 'nan':  # przepisujemy tylko niepuste dane
                temp_str += str(row[i]).replace('.', ',').casefold() + '.'

        corpus.append(temp_str)  # jeden wpis to jeden film

    print(f"Info downloaded in: {time.time() - start} secs")

    start = time.time()
    corpus = "".join(corpus)  # tworzy dokument
    # zamieniamy znaki '?' i '!' na jeden ('.'), usuwamy '\s' i ',' jesli jeszcze jakies istnieja
    # zamieniamy autorow na {imie} i {nazwisko} zamiast na {imie_nazwisko}
    corpus = corpus.replace('?', '.').replace('!', '.').replace('\'s', '').replace(',', '').replace('_', ' ').split('.')
    tokenized_sentences = [sentence.replace('.', '').split() for sentence in corpus]  # wyrazy z sentencji
    print(f"Sentences tokenization was done within: {time.time() - start} secs")

    # usuwanie stop-words z corpusu
    print("Removing unnecessary characters (f.e. 'a', 'the')")
    start = time.time()
    for sentence in range(len(tokenized_sentences)):
        for word in range(len(tokenized_sentences[sentence])):  # usuwanie liczb
            tokenized_sentences[sentence][word] = re.sub(r'[0-9\.]+', '', tokenized_sentences[sentence][word])

        try:
            tokenized_sentences[sentence].remove('')
        except ValueError:
            pass

        # list comprehensions instead of typical loop, almost 10x faster (from 290secs to 33secs)
        tokenized_sentences[sentence] = [x for x in tokenized_sentences[sentence]
                                         if x.casefold() not in stop_words]

    print("Preparation/Cleaning completed, time:", time.time() - start, "secs")
    return tokenized_sentences
# ------------------------------------------------------ KONIEC ------------------------------------------------------ #
# endregion
