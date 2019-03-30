# -------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                      #
# TODO - Zmienne lepiej odzwierciedlajace przechowywane dane (jak bedziemy pewni, ze wszystko zrobione)                #
#                                                                                                                      #
# Jesli cos zrobicie to usuncie. Jak zrobicie wszystko z listy zostawcie naglowek i te wiadomosc                       #
# ------------------------------------------ ELO MORDY --------------------------------------------------------------- #


import numpy as np
import pandas as pd
from imdb import IMDb, IMDbError

# region Variables
# --------------------------------------------- INICJALIZACJA ZMIENNYCH ---------------------------------------------- #
path_to_dataset_ids = "dataset_ids.txt"
path_to_imdb_ids = "imdb_ids.txt"
path_to_dataset = "dataset.csv"
path_to_datakeywords = "datakeywords.csv"
ia = IMDb()  # polaczenie z baza IMDb
i = 0  # reshape <-> rows
stop_term = 0  # warunek stopu (zapisu) [warunek pauzy jest IMO lepszym okresleniem - przyp. Dawida]
row_info = list()  # tworzymy listy
ids_to_save = list()
keywords = list()
marks = {',', '<', '>', '/', ';', ':', '\'', '\'s', '\"', '[', '{', ']', '}', '@', '#', '$', '%', '^',
         '&', '&', '*', '(', ')', '-', '_', '=', '+'}  # lista znakow specjalnych do usunięcia
# ------------------------------------------------------ KONIEC ------------------------------------------------------ #
# endregion

# region Functions


# ----------------------------------- FUNKCJA POBIERAJACA INFO NT FILMU O DANYM ID ----------------------------------- #
def get_info(movie, arg_i, arg_row, arg_keywords, arg_row_info_len=7, bool_title=True, bool_year=True,
             bool_director=True, bool_rating=True, bool_genre=True, bool_plotmark=True, bool_actor=True):
    try:
        list_of_infos = list()  # Lista, w ktorej bedziemy przechowywac informacje nt. pojedycznego filmu

        # zmienne typu Bool obsluguja blad pustej wartosci (w ich miejsce bedzie wpisywany NULL)
        if bool_title:
            list_of_infos.append(movie['title'])  # na początek tytułu
        else:
            list_of_infos.append("NULL")

        if bool_year:
            list_of_infos.append(movie['year'])  # potem rok produkcji
        else:
            list_of_infos.append("NULL")

        if bool_director:
            list_of_directors = list()  # tworzenie listy rezyserow, poniewaz moze byc ich wiecej niz 1
            for director in movie['directors']:  # dla kazdego rezysera
                temp_directors = director['name'].replace(' ', '_')  # usunięcie spacji i zamiana na _
                list_of_directors.append(temp_directors)
            list_of_infos.append(" ".join(list_of_directors))
        else:
            list_of_infos.append("NULL")

        if bool_rating:
            list_of_infos.append(movie['rating'])  # ocena filmu
        else:
            list_of_infos.append("NULL")

        if bool_genre:
            list_of_infos.append(" ".join(movie['genres']))  # kategoria
        else:
            list_of_infos.append("NULL")

        # usuwamy .::, autora tekstu i znaki specjalne -- START
        if bool_plotmark:
            plotsmarks = list()
            for plot in movie['plot']:
                index = plot.find(".::")  # szukamy ".::" i od tego miejsca ucinamy tekst
                plot = plot.replace(".::", ".")
                plot = plot[:index + 1]
                for mark in marks:  # wyszukaj znaku specjalnego (lista marks) i go usun/zamien
                    plot = plot.replace(mark, '')
                plotsmarks.append(plot)
            list_of_infos.append(" ".join(plotsmarks))
        else:
            list_of_infos.append("NULL")
        # usuwamy .::, autora tekstu i znaki specjalne  -- KONIEC

        if bool_actor:
            list_of_actors = list()  # tworzenie listy aktorow (obsady), moze byc wiecej niz jeden
            for actor in movie['cast']:  # dla kazdego actora
                temp_actors = actor['name'].replace(' ', '_')  # usunięcie spacji i zamiana na _
                list_of_actors.append(temp_actors)
            list_of_infos.append(" ".join(list_of_actors))
        else:
            list_of_infos.append("NULL")

        # dopisywanie (w przypadku pierwszego ID tworzenie) wiersza (tablicy) z informacjami nt. aktualnego filmu
        if arg_i == 0:
            arg_row = np.array(list_of_infos)  # tablica numpy (ma więcej metod, latwiej sie na niej operuje)
            arg_i += 1  # powiększamy "i" czyli liczbę wierszy
        else:
            arg_i += 1  # powiększamy "i" czyli liczbę wierszy
            arg_row = np.append(arg_row, list_of_infos)
        arg_row = arg_row.reshape((arg_i, arg_row_info_len))  # zmien tablice numpy 1D na 2D

        # keywords -- START
        temp_keywords = pd.read_csv(path_to_datakeywords, sep=";", index_col=0).to_numpy()

        for el in range(len(list_of_infos)):
            if type(list_of_infos[el]) is int or type(list_of_infos[el]) is float:
                continue
            for word in list_of_infos[el].split():  # pętla która zapisuje wszystkie keywords (category)
                word = word.casefold()
                if word in temp_keywords or word in arg_keywords:  # jesli keywords juz istnieje
                    continue  # pomin
                arg_keywords.append(word)  # jesli nie to dopisz do bazy
        # keywords -- END

        return arg_row, arg_keywords, arg_i  # zwracamy dane, ktore sa potrzebne do kolejnego filmu
    # blad danych (pusta informacja), w takim przypadku oznaczamy tam NULLa i wywolujemy funkcje jeszcze raz
    except KeyError as e:
        e = str(e)
        if "title" in e:
            bool_title = False
        elif "year" in e:
            bool_year = False
        elif "director" in e:
            bool_director = False
        elif "rating" in e:
            bool_rating = False
        elif "genre" in e:
            bool_genre = False
        elif "plot" in e:
            bool_plotmark = False
        elif "cast" in e:
            bool_actor = False
        else:
            print(e)
            exit(-1)
        return get_info(movie, arg_i, arg_row, arg_keywords, arg_row_info_len, bool_title, bool_year, bool_director,
                        bool_rating, bool_genre, bool_plotmark, bool_actor)
# ------------------------------------------------------ KONIEC ------------------------------------------------------ #


# ---------------------------- FUNKCJA ZAPISUJACA ID FILMOW, KTORYCH DANE JUZ POBRALISMY ----------------------------- #
def save_ids(id_list):  # funkcja do zapiswania już wykorzystanych ID do pliku
    filesave_ids = open(path_to_dataset_ids, "a+")  # otwieranie pliku dataSetids
    for imdb_id in id_list:
        if imdb_id not in filesave_ids:
            filesave_ids.write(imdb_id + "\n")  # wypisywanie każdego elementu w nowej lini
    filesave_ids.close()  # zamykanie pliku
# ------------------------------------------------------ KONIEC ------------------------------------------------------ #


# ------------------------------------- FUNKCJA ZAPISUJACA DANE FILMOW DO PLIKU -------------------------------------- #
def save_to_file(argrow_info, arg_keywords, arg_dataset, arg_datakeywords):  # zapisywanie pobranych danych do pliku
    try:
        #  tworzenie dataFrame - taka tabelka która ma jasno określone nagłówki i indeksy
        temp_dataset = pd.DataFrame(argrow_info, columns=['title', 'year', 'directors', 'rating', 'genres', 'plotmarks',
                                                          'actors'])
        temp_datakeywords = pd.DataFrame(arg_keywords, columns=['keyword'])

        arg_dataset = pd.concat(
            [arg_dataset, temp_dataset])  # konkatenacja - łączenie tego co mamy w pliku i co pobrane
        arg_datakeywords = pd.concat([arg_datakeywords, temp_datakeywords])  # to samo co wyżej

        arg_dataset = arg_dataset.reset_index(drop=True)  # reset indeksu
        arg_datakeywords = arg_datakeywords.reset_index(drop=True)  # to samo co wyżej

        arg_dataset.to_csv(path_to_dataset, sep=";")  # zmiana na plik .csv
        arg_datakeywords.to_csv(path_to_datakeywords, sep=";")  # zmiana na plik .csv
        return True  # zwracamy prawde, dzieki czemu ID tych filmow mozemy zapisac jako 'zrobione'
    except ValueError as err:  # error
        print("Blad: ", err)
        return False  # cos poszlo nie tak i nic nie zostalo zapisane (ID nie sa oznaczone jako 'zrobione')
# ------------------------------------------------------ KONIEC ------------------------------------------------------ #
# endregion

# region Files


# ------------------------------------------------------- IMDB ------------------------------------------------------- #
try:  # spróbuj otworzyć plik ze wszystkimi ID IMDb
    file_read = open(path_to_imdb_ids, "r").read()  # czytaj plik
    file_read = file_read.split()[::-1]  # lista ze string, najnowszy jako pierwszy
except FileNotFoundError as e:  # jesli nie ma pliku wejsciowego to nie ma co robic
    print("Blad: ", e)
    exit(-1)  # zamknij program
# ------------------------------------------------------ KONIEC ------------------------------------------------------ #


# ----------------------------------- CZYTAMY JAKIE ID MAMY ZAPISANE JAKO OSTATNIE ----------------------------------- #
last_id = file_read[0]  # ustawione jako najnowszy
try:  # obsluga bledu 'brak pliku'
    with open(path_to_dataset_ids) as ids:  # rownie dobrze mogloby byc cos w stylu:
        try:
            last_id = list(ids)[-1]  # pobranie ostatniego id żeby nie powtarzać pobierania danych do pliku od początku
            file_read = file_read[file_read.index(
                last_id[:-1]) + 1:]  # ucinamy wszystkie ID z IMDb od ostatniego najnowszego ID - 1
        except IndexError:  # jesli plik jest pusty
            print("Plik ID jest pusty, zaczynamy od ", last_id, "!")
except FileNotFoundError as e:
    open(path_to_dataset_ids, "w+").write("")
# ------------------------------------------------------ KONIEC ------------------------------------------------------ #


# ----------------------- SPRAWDZAMY CZY PLIKI Z DANYMI ISTNIEJA I (JESLI TRZEBA) TWORZYMY JE ------------------------ #
try:
    dataset = pd.read_csv(path_to_dataset, sep=";", index_col=0)  # czytaj plik .csv
except FileNotFoundError as e:
    open(path_to_dataset, "w+").write(";title;year;directors;rating;genres;plotmarks;actors")  # jeśli nie ma, to utwórz
    dataset = pd.read_csv(path_to_dataset, sep=";", index_col=0)  # a potem czytaj

try:
    datakeywords = pd.read_csv(path_to_datakeywords, sep=";", index_col=0)  # czytaj plik .csv
except FileNotFoundError as e:
    open(path_to_datakeywords, "w+").write(";keyword")  # jeśli go nie ma, to uwtórz
    datakeywords = pd.read_csv(path_to_datakeywords, sep=";", index_col=0)  # a potem czytaj
# ------------------------------------------------------ KONIEC ------------------------------------------------------ #
# endregion

# region Main
# ------------------------- PETLA WYWOLUJACA WARUNEK STOPU [PAUZY] I FUNKCJE CZYTANIA/ZAPISU ------------------------- #
for row in file_read:  # kazdy imdb_id z bazy
    stop_term += 1  # warunek stopu zapisu - kiedy ma zapisać
    if stop_term == 6:  # co 5
        print("Zapis do plikow")  # wyświetla że zapisuje
        stop_term = 1  # zerowanie warunku stopu [pauzy]
        if save_to_file(row_info, keywords, dataset, datakeywords):  # wywołuje funkcje zapisu do pliku
            save_ids(ids_to_save)  # zapisuje
            ids_to_save.clear()  # czyści - dupe na przykład
        else:
            print("Niepowodzenie w zapisie!")  # błąd, wyświetla komunikat błedu
            exit(-1)  # kod błędu - kończenie programu

    ids_to_save.append(row)  # dopisue aktualne ID do listy ID przeznaczonych do zapisu

    try:
        movie_info = ia.get_movie(row)  # pobieramy info nt filmow o danym ID
        print(row)
        row_info, keywords, i = get_info(movie_info, i, row_info, keywords)
    except IMDbError as e:  # blad z polaczeniem do bazy IMDb lub inny blad zwiazany z biblioteka IMDb
        print(row, e)
# ------------------------------------------------------ KONIEC ------------------------------------------------------ #
# endregion

# region End
# --------------------------------------- ZAMKNIECIE PROGRAMU (OSTATNI ZAPIS) ---------------------------------------- #
if save_to_file(row_info, keywords, dataset, datakeywords):
    save_ids(ids_to_save)
# ------------------------------------------- TO BY BYLO NA TYLE KURWIBĄKI ------------------------------------------- #
# endregion
