# -------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                      #
# TODO - Usunac wszelkie liczby z corpusu (aktualny sposob nie do konca dziala)                                        #
#                                                                                                                      #
# Jesli cos  zrobicie to usuncie. Jak zrobicie wszystko z listy zostawcie naglowek i te wiadomosc                      #
# ------------------------------------------ ELO MORDY --------------------------------------------------------------- #


import time


# ------------------------------------------- FUNKCJA PRZYGOTOWUJACA DANE -------------------------------------------- #
def prepare(arg_dataset, arg_path_to_stop_words):
    print("-" * 10)
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
    print("Removing unnecessary characters (f.e. 'a', 'the')")
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

    print("-" * 10)
    print("Preparation/Cleaning completed, time:", time.time() - start, "secs")
    return tokenized_sentences
# ------------------------------------------------------ KONIEC ------------------------------------------------------ #
