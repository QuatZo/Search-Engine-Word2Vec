# -------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                      #
# TODO - Zabawa parametrami modelu, sprawdzanie najlepszego (najbardziej dokladnego) rozwiazania                       #
#                                                                                                                      #
# Jesli cos  zrobicie to usuncie. Jak zrobicie wszystko z listy zostawcie naglowek i te wiadomosc                      #
# ------------------------------------------ ELO MORDY --------------------------------------------------------------- #

from gensim.models import word2vec
import time


# region Functions


# ------------------------------------ FUNKCJA SPRAWDZAJACA CZY MODEL JUZ ISTNIEJE ----------------------------------- #
def exists(arg_path_to_model):
    try:
        word2vec.Word2Vec.load(arg_path_to_model)
        return True
    except FileNotFoundError:
        return False


# ------------------------------------------------------ KONIEC ------------------------------------------------------ #


# --------------------------------------------- FUNKCJA TRENUJACA MODEL ---------------------------------------------- #
def train(arg_dataset, arg_path_to_model, arg_epochs=20, arg_size=1000, arg_sample=1e-3,
          arg_min_count=5, arg_workers=12, arg_iter=5):
    print("Training...")
    try:
        start = time.time()
        model = word2vec.Word2Vec(arg_dataset, size=arg_size, sample=arg_sample, min_count=arg_min_count,
                                  workers=arg_workers, iter=arg_iter, window=5)
        model.train(arg_dataset, total_examples=len(arg_dataset), epochs=arg_epochs)  # trenowanie
        model.save(arg_path_to_model)  # zapis słownika/modelu do pliku (binarnie)
        print("Training completed, time:", time.time() - start, "secs")
        return True
    except:
        return False
# ------------------------------------------------------ KONIEC ------------------------------------------------------ #
# endregion
