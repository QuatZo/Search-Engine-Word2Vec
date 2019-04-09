# -------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                      #
# TODO - Dodac algorytm wyswietlajacy najlepsze wyniki wedlug zadanego kryterium                                       #
#        Ustalone z Bartkiem, ze pierw po tytule, potem opisie, na koncu autorzy i rezyserzy                           #
#                                                                                                                      #
# Jesli cos  zrobicie to usuncie. Jak zrobicie wszystko z listy zostawcie naglowek i te wiadomosc                      #
# ------------------------------------------ ELO MORDY --------------------------------------------------------------- #

from gensim.models import word2vec


def correlations(arg_input, arg_path_to_model, top_n, amount_of_rows):
    model = word2vec.Word2Vec.load(arg_path_to_model)
    probability_positive = dict()
    rows_per_element = dict()

    for element in arg_input:
        try:
            prob_pos_el = probability_positive[element] = model.wv.most_similar_cosmul(positive=[element], topn=top_n)
            probability_ratio = list()
            for i in range(top_n):
                probability_ratio.append(prob_pos_el[i][1] / prob_pos_el[0][1])

            temp_alg = amount_of_rows / sum(probability_ratio)  # ilosc wyrazow na pierwszy wyraz
            rows_per_element[element] = [int(temp_alg), int(probability_ratio[1] * temp_alg),
                                         int(probability_ratio[2] * temp_alg)]  # obliczanie ilosci wierszy na wyraz
        except KeyError:
            probability_positive[element] = "Word " + element + " not in vocabulary."

    return probability_positive, rows_per_element


def return_data(arg_total_rows, arg_match, arg_dataset):  # funkcja zwracająca/sortująca wynik wyszukiwania
    arg_dataset = arg_dataset.sort_values(by='rating', ascending=False)
    result = list()
    print(arg_dataset[['rating']])
    for row in arg_dataset.values:
        for el in range(len(row)):
            try:
                for match in arg_match.keys():
                    if match in row[el]:
                        result.append(row)
            except TypeError:
                continue
    return result

