# -------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                      #
#                                                                                                                      #
# Jesli cos  zrobicie to usuncie. Jak zrobicie wszystko z listy zostawcie naglowek i te wiadomosc                      #
# ------------------------------------------ ELO MORDY --------------------------------------------------------------- #

from gensim.models import word2vec
import time

# region Functions


# --------------------------------------- FUNKCJA WYZNACZAJACA WYRAZY PODOBNE ---------------------------------------- #
def correlations(arg_input, arg_path_to_model, top_n, arg_ai_rows):
    model = word2vec.Word2Vec.load(arg_path_to_model)
    probability = dict()

    for element in arg_input:
        try:
            most_similar = model.wv.most_similar_cosmul(positive=[element], topn=top_n)
            for i in range(top_n):
                probability[most_similar[i][0]] = most_similar[i][1]
        except KeyError:
            continue

    for el in probability.keys():
        probability[el] = int(probability[el] / len(probability) * arg_ai_rows)

    return probability
# ------------------------------------------------------ KONIEC ------------------------------------------------------ #


# ------------------------------------------- PODFUNKCJA POBIERAJACA DANE -------------------------------------------- #
def fetch_data(arg_data, arg_result, arg_arg_dataset, arg_total_words, similar=False):
    validate_set = [0, 1]  # title, year
    data_search_order = [0, 5, 2, 6]  # title, plot, directors, actors
    for word in arg_data.keys():
        rows = 0
        if similar:
            arg_data[word] = arg_total_words
        for row in arg_arg_dataset.values:
            if rows == arg_data[word]:
                break
            suma = 0
            for el_result in arg_result:
                for i in validate_set:
                    if el_result[i] == row[i]:
                        suma += 1
            if suma == len(validate_set):
                continue

            for el_row in data_search_order:
                try:
                    if word.casefold() in row[el_row].casefold():
                        arg_result.append(row)
                        rows += 1
                        break
                except TypeError:
                    continue
                except AttributeError:
                    continue
        if not similar:
            arg_total_words += rows
    return arg_result
# ------------------------------------------------------ KONIEC ------------------------------------------------------ #


# -------------------------------------------- FUNKCJA POBIERAJACA DANE ---------------------------------------------- #
def return_data(arg_input, arg_match, arg_dataset, arg_total_rows):  # funkcja zwracająca/sortująca wynik wyszukiwania
    input_rows = arg_total_rows - sum(arg_match.values())
    rows_per_input = int(input_rows / len(arg_input))
    total_words = 0
    arg_dataset = arg_dataset.sort_values(by='rating', ascending=False)

    result = list()
    inp = dict()

    for word in arg_input:
        inp[word] = rows_per_input
    del arg_input

    start = time.time()
    result = fetch_data(inp, result, arg_dataset, total_words)

    try:
        total_words = int((arg_total_rows - total_words) / len(arg_match))
    except ZeroDivisionError:
        return result

    result = fetch_data(arg_match, result, arg_dataset, total_words, )

    print(f"Search time: {time.time() - start} secs")
    return result
# ------------------------------------------------------ KONIEC ------------------------------------------------------ #
# endregion

