# -------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                      #
# TODO - Wyeliminowac potwarzajace sie elementy w wyniku koncowym *wykorzystac liste 'result'*                         #
# TODO - Z dwoch petli wybierajacych dane zrobic jedna funkcje                                                         #
#                                                                                                                      #
# Jesli cos  zrobicie to usuncie. Jak zrobicie wszystko z listy zostawcie naglowek i te wiadomosc                      #
# ------------------------------------------ ELO MORDY --------------------------------------------------------------- #

from gensim.models import word2vec


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


def return_data(arg_input, arg_match, arg_dataset, arg_total_rows):  # funkcja zwracająca/sortująca wynik wyszukiwania
    input_rows = arg_total_rows - sum(arg_match.values())
    rows_per_input = int(input_rows / len(arg_input))
    total_words = 0
    arg_dataset = arg_dataset.sort_values(by='rating', ascending=False)

    result = list()
    for word in arg_input:
        print(word)
        rows = 0
        for row in arg_dataset.values:
            if rows == rows_per_input:
                break
            for el in range(len(row)):
                try:
                    if word.casefold() in row[el].casefold():
                        result.append(row)
                        rows += 1
                        print(f"{rows}/{rows_per_input}")
                        break
                except TypeError:
                    continue
                except AttributeError:
                    continue
        total_words += rows

    total_words = int((arg_total_rows - total_words) / len(arg_match))

    for word in arg_match.keys():
        print(word)
        arg_match[word] = total_words
        rows = 0
        for row in arg_dataset.values:
            if rows == arg_match[word]:
                break
            for el in range(len(row)):
                try:
                    if word.casefold() in row[el].casefold():
                        result.append(row)
                        rows += 1
                        print(f"{rows}/{arg_match[word]}")
                        break
                except TypeError:
                    continue
                except AttributeError:
                    continue
    return result

