# -------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                      #
#                                                                                                                      #
# Jesli cos  zrobicie to usuncie. Jak zrobicie wszystko z listy zostawcie naglowek i te wiadomosc                      #
# ------------------------------------------ ELO MORDY --------------------------------------------------------------- #

from gensim.models import word2vec
import time
import pandas as pd

# region Functions


# --------------------------------------- FUNKCJA WYZNACZAJACA WYRAZY PODOBNE ---------------------------------------- #
def correlations(arg_input, arg_path_to_model, top_n, arg_ai_rows):
    model = word2vec.Word2Vec.load(arg_path_to_model)
    probability = dict()

    for element in arg_input:
        try:
            most_similar = model.wv.most_similar_cosmul(positive=[element], topn=top_n)  # wyrazy podobne lokalne
            for i in range(top_n):
                probability[most_similar[i][0]] = most_similar[i][1]  # wyrazy podobne globalne
        except KeyError:
            continue

    print(probability)

    for el in probability.keys():
        probability[el] = int(probability[el] / len(probability) * arg_ai_rows)  # ilosc wierszy na wyraz

    return probability
# ------------------------------------------------------ KONIEC ------------------------------------------------------ #


# ------------------------------------------- PODFUNKCJA POBIERAJACA DANE -------------------------------------------- #
def fetch_data(arg_data, arg_result, arg_arg_dataset, arg_total_words, similar=False):
    df_columns = ['title', 'plotmarks', 'directors', 'actors']  # kolejnosc wyszukiwania
    arg_arg_dataset = arg_arg_dataset.fillna(" ")  # zamien 'nan' na spacje
    rows_len = 0

    for word in arg_data.keys():
        if similar:
            arg_data[word] = arg_total_words  # jesli jest to wyraz podobny, podmien ilosc wierszy dla tego wyrazu

        for col in df_columns:
            if rows_len == arg_data[word]:  # jesli osiagnelismy oczekiwana ilosc wierszy dla danego wyrazu
                break  # przejdz do kolejnego
            # pobierz wszystkie wiersze zawierajace dany wyraz w danej kolumnie
            rows = arg_arg_dataset[(arg_arg_dataset[col].str.lower()).str.contains(word.lower())].values
            for row in rows:
                if rows_len == arg_data[word]:  # jesli osiagnelismy oczekiwana ilosc wierszy dla danego wyrazu
                    break  # przejdz do kolejnej kolumny, ktora przejdzie do kolejnego wyrazu
                arg_result.append(row)  # kazdy wynik dopisz do listy wynikow
                rows_len += 1
        if not similar:
            arg_total_words += rows_len  # dodaj ilosc wierszy danego wyrazu do ilosci wszystkich wierszy

    return arg_result  # zwroc wynik
# ------------------------------------------------------ KONIEC ------------------------------------------------------ #


# -------------------------------------------- FUNKCJA POBIERAJACA DANE ---------------------------------------------- #
def return_data(arg_input, arg_match, arg_dataset, arg_total_rows):  # funkcja zwracająca/sortująca wynik wyszukiwania
    input_rows = arg_total_rows - sum(arg_match.values())  # ilosc wierszy przeznaczonych dla wyrazow z wejscia to ilosc
    # wszystkich wierszy minus ilosc wierszy zarezerwowanych dla wyrazow podobnych
    rows_per_input = int(input_rows / len(arg_input))  # ilosc wierszy na wyraz z wejscia
    total_words = 0
    arg_dataset = arg_dataset.sort_values(by='rating', ascending=False)  # sortuj po ratingu

    result = list()
    inp = dict()

    for word in arg_input:
        inp[word] = rows_per_input  # slownik z listy, unifikacja zmiennej dla funkcji fetch_data
    del arg_input

    start = time.time()
    result = fetch_data(inp, result, arg_dataset, total_words)  # wyrazy wejsciowe

    try:
        total_words = int((arg_total_rows - total_words) / len(arg_match))  # aktualna ilosc wierszy na wyraz podobny
    except ZeroDivisionError:
        return result  # brak wyrazow podobnych, zwroc wynik tylko dla wejscia

    result = fetch_data(arg_match, result, arg_dataset, total_words, similar=True)  # wyrazy podobne

    print(f"Search time: {time.time() - start} secs")
    return result
# ------------------------------------------------------ KONIEC ------------------------------------------------------ #
# endregion
