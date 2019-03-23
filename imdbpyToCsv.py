# -------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                      #
# TODO - Zmienne lepiej odzwierciedlajace przechowywane dane (jak bedziemy pewni, ze wszystko zrobione)                #
#                                                                                                                      #
# Jesli cos zrobicie to usuncie. Jak zrobicie wszystko z listy zostawcie naglowek i te wiadomosc                       #
# ------------------------------------------ ELO MORDY --------------------------------------------------------------- #

import numpy as np
import pandas as pd
from imdb import IMDb, IMDbError

# --------------------------------------------- INICJALIZACJA ZMIENNYCH ---------------------------------------------- #
ia = IMDb()  # polaczenie z baza IMDb
i = 0  # reshape <-> rows
lastId = str(0).zfill(7) + '\n'  # ustawione jako 0000001
stopTerm = 0  # warunek stopu (zapisu) [warunek pauzy jest IMO lepszym okresleniem - przyp. Dawida]
rowInfo = list()  # tworzymy listy
idsToSave = list()
keywords = list()
marks = {',', '<', '>', '/', ';', ':', '\'', '\'s', '\"', '[', '{', ']', '}', '@', '#', '$', '%', '^',
         '&', '&', '*', '(', ')', '-', '_', '=', '+'}  # lista znakow specjalnych do usunięcia
# ------------------------------------------------------ KONIEC ------------------------------------------------------ #


# ----------------------------------- FUNKCJA POBIERAJACA INFO NT FILMU O DANYM ID ----------------------------------- #
def getInfo(simpleMovie, iTemp, rowTemp, keywordsArg, rowInfoLen=7, boolTitle=True, boolYear=True, boolDirector=True,
            boolRating=True, boolGenre=True, boolPlotmark=True, boolActor=True):
    print(simpleMovie)
    try:
        movie = ia.get_movie(simpleMovie)  # pobieramy info nt filmow o danym ID
        listOfInfos = list()  # Lista, w ktorej bedziemy przechowywac informacje nt. pojedycznego filmu

        # zmienne typu Bool obsluguja blad pustej wartosci (w ich miejsce bedzie wpisywany NULL)
        if boolTitle:
            listOfInfos.append(movie['title'])  # na początek tytułu
        else:
            listOfInfos.append("NULL")

        if boolYear:
            listOfInfos.append(movie['year'])  # potem rok produkcji
        else:
            listOfInfos.append("NULL")

        if boolDirector:
            listOfDirectors = list()  # tworzenie listy rezyserow, poniewaz moze byc ich wiecej niz 1
            for director in movie['directors']:  # dla kazdego rezysera
                tempDirectors = director['name'].replace(' ', '_')  # usunięcie spacji i zamiana na _
                listOfDirectors.append(tempDirectors)
            listOfInfos.append(" ".join(listOfDirectors))
        else:
            listOfInfos.append("NULL")

        if boolRating:
            listOfInfos.append(movie['rating'])  # ocena filmu
        else:
            listOfInfos.append("NULL")

        if boolGenre:
            listOfInfos.append(" ".join(movie['genres']))  # kategoria
        else:
            listOfInfos.append("NULL")

        # usuwamy .::, autora tekstu i znaki specjalne -- START
        if boolPlotmark:
            plotsmarks = list()
            for plot in movie['plot']:
                index = plot.find(".::")  # szukamy ".::" i od tego miejsca ucinamy tekst
                plot = plot.replace(".::", ".")
                plot = plot[:index + 1]
                for mark in marks:  # wyszukaj znaku specjalnego (lista marks) i go usun/zamien
                    plot = plot.replace(mark, '')
                plotsmarks.append(plot)
            listOfInfos.append(" ".join(plotsmarks))
        else:
            listOfInfos.append("NULL")
        # usuwamy .::, autora tekstu i znaki specjalne  -- KONIEC

        if boolActor:
            listOfActors = list()  # tworzenie listy aktorow (obsady), moze byc wiecej niz jeden
            for actor in movie['cast']:  # dla kazdego actora
                tempActors = actor['name'].replace(' ', '_')  # usunięcie spacji i zamiana na _
                listOfActors.append(tempActors)
            listOfInfos.append(" ".join(listOfActors))
        else:
            listOfInfos.append("NULL")

        # dopisywanie (w przypadku pierwszego ID tworzenie) wiersza (tablicy) z informacjami nt. aktualnego filmu
        if iTemp == 0:
            rowTemp = np.array(listOfInfos)  # tablica numpy (ma więcej metod, latwiej sie na niej operuje)
            iTemp += 1  # powiększamy "i" czyli liczbę wierszy
        else:
            iTemp += 1  # powiększamy "i" czyli liczbę wierszy
            rowTemp = np.append(rowTemp, listOfInfos)
        rowTemp = rowTemp.reshape((iTemp, rowInfoLen))  # zmien tablice numpy 1D na 2D

        # keywords -- START
        keywordsTemp = pd.read_csv("dataKeywords.csv", sep=";", index_col=0).to_numpy()

        for el in range(len(listOfInfos)):
            if type(listOfInfos[el]) is int or type(listOfInfos[el]) is float:
                continue
            for word in listOfInfos[el].split():  # pętla która zapisuje wszystkie keywords (category)
                word = word.casefold()
                if word in keywordsTemp or word in keywordsArg:  # jesli keywords juz istnieje
                    continue  # pomin
                keywordsArg.append(word)  # jesli nie to dopisz do bazy
        # keywords -- END

        return rowTemp, keywordsArg, iTemp  # zwracamy dane, ktore sa potrzebne do kolejnego filmu
    except IMDbError as e:  # blad z polaczeniem do bazy IMDb lub inny blad zwiazany z biblioteka IMDb
        print(row, e)
    # blad danych (pusta informacja), w takim przypadku oznaczamy tam NULLa i wywolujemy funkcje jeszcze raz
    except KeyError as e:
        e = str(e)
        if "title" in e:
            boolTitle = False
        elif "year" in e:
            boolYear = False
        elif "director" in e:
            boolDirector = False
        elif "rating" in e:
            boolRating = False
        elif "genre" in e:
            boolGenre = False
        elif "plot" in e:
            boolPlotmark = False
        elif "cast" in e:
            boolActor = False
        else:
            print(e)
            exit(-1)
        return getInfo(simpleMovie, iTemp, rowTemp, keywordsArg, rowInfoLen, boolTitle, boolYear, boolDirector,
                       boolRating, boolGenre, boolPlotmark, boolActor)
# ------------------------------------------------------ KONIEC ------------------------------------------------------ #


# ---------------------------- FUNKCJA ZAPISUJACA ID FILMOW, KTORYCH DANE JUZ POBRALISMY ----------------------------- #
def saveIDs(stepIDList):  # funkcja do zapiswania już wykorzystanych ID do pliku
    fileSaveIDs = open("dataSetIds.txt", "a+")  # otwieranie pliku dataSetIds
    for imdbID in stepIDList:
        if imdbID not in fileSaveIDs:
            fileSaveIDs.write(imdbID + "\n")  # wypisywanie każdego elementu w nowej lini
    fileSaveIDs.close()  # zamykanie pliku
# ------------------------------------------------------ KONIEC ------------------------------------------------------ #


# ------------------------------------- FUNKCJA ZAPISUJACA DANE FILMOW DO PLIKU -------------------------------------- #
def saveToFile(argRowInfo, argKeywords, argDataSet, argDataKeywords):  # zapisywanie pobranych danych do pliku
    try:
        #  tworzenie dataFrame - taka tabelka która ma jasno określone nagłówki i indeksy
        dataSetTemp = pd.DataFrame(argRowInfo, columns=['title', 'year', 'directors', 'rating', 'genres', 'plotmarks',
                                                        'actors'])
        dataKeywordsTemp = pd.DataFrame(argKeywords, columns=['keyword'])

        argDataSet = pd.concat([argDataSet, dataSetTemp])  # konkatenacja - łączenie tego co mamy w pliku i co pobrane
        argDataKeywords = pd.concat([argDataKeywords, dataKeywordsTemp])  # to samo co wyżej

        argDataSet = argDataSet.reset_index(drop=True)  # reset indeksu
        argDataKeywords = argDataKeywords.reset_index(drop=True)  # to samo co wyżej

        argDataSet.to_csv("dataSet.csv", sep=";")  # zmiana na plik .csv
        argDataKeywords.to_csv("dataKeywords.csv", sep=";")  # zmiana na plik .csv
        return True  # zwracamy prawde, dzieki czemu ID tych filmow mozemy zapisac jako 'zrobione'
    except ValueError as err:  # error
        print("Blad: ", err)
        return False  # cos poszlo nie tak i nic nie zostalo zapisane (ID nie sa oznaczone jako 'zrobione')
# ------------------------------------------------------ KONIEC ------------------------------------------------------ #


# ------------------------------------------------------- IMDB ------------------------------------------------------- #
try:  # spróbuj otworzyć plik ze wszystkimi ID IMDb
    fileR = open('imdbIDs.txt', "r").read()  # czytaj plik
    fileR = fileR.split()  # lista ze string
except FileNotFoundError as e:  # jesli nie ma pliku wejsciowego to nie ma co robic
    print("Blad: ", e)
    exit(-1)  # zamknij program
# ------------------------------------------------------ KONIEC ------------------------------------------------------ #


# ----------------------------------- CZYTAMY JAKIE ID MAMY ZAPISANE JAKO OSTATNIE ----------------------------------- #
try:  # obsluga bledu 'brak pliku'
    with open('dataSetIds.txt') as Ids:  # rownie dobrze mogloby byc cos w stylu:
        # file = open('dataSetIds.txt').read()
        try:
            lastId = list(Ids)[-1]  # pobranie ostatniego id żeby nie powtarzać pobierania danych do pliku od początku
            fileR = fileR[fileR.index(lastId[:-1]) + 1:]  # ucinamy wszystkie ID z IMDb od ostatniego ID + 1
        except IndexError:  # jesli plik jest pusty
            print("Plik ID jest pusty, zaczynamy od 0000001!")
except FileNotFoundError as e:
    open("dataSetIds.txt", "w+").write("")
# ------------------------------------------------------ KONIEC ------------------------------------------------------ #


# ----------------------- SPRAWDZAMY CZY PLIKI Z DANYMI ISTNIEJA I (JESLI TRZEBA) TWORZYMY JE ------------------------ #
try:
    dataSet = pd.read_csv("dataSet.csv", sep=";", index_col=0)  # czytaj plik .csv
except FileNotFoundError as e:
    open("dataSet.csv", "w+").write(";title;year;directors;rating;genres;plotmarks;actors")  # jeśli nie ma, to utwórz
    dataSet = pd.read_csv("dataSet.csv", sep=";", index_col=0)  # a potem czytaj

try:
    dataKeywords = pd.read_csv("dataKeywords.csv", sep=";", index_col=0)  # czytaj plik .csv
except FileNotFoundError as e:
    open("dataKeywords.csv", "w+").write(";keyword")  # jeśli go nie ma, to uwtórz
    dataKeywords = pd.read_csv("dataKeywords.csv", sep=";", index_col=0)  # a potem czytaj
# ------------------------------------------------------ KONIEC ------------------------------------------------------ #


# ------------------------- PETLA WYWOLUJACA WARUNEK STOPU [PAUZY] I FUNKCJE CZYTANIA/ZAPISU ------------------------- #
for row in fileR:  # kazdy imdbID z bazy
    if row > lastId:  # na wszelki wypadek sprawdzamy jeszcze raz czy pobralismy poprawne ID (nie-duplikat)
        # prawdopodobnie ta instrukcja warunkowa (up) jest niepotrzebna
        stopTerm += 1  # warunek stopu zapisu - kiedy ma zapisać
        if stopTerm == 6:  # co 5
            print("Zapis do plikow")  # wyświetla że zapisuje
            stopTerm = 0  # zerowanie warunku stopu [pauzy]
            if saveToFile(rowInfo, keywords, dataSet, dataKeywords):  # wywołuje funkcje zapisu do pliku
                saveIDs(idsToSave)  # zapisuje
                idsToSave.clear()  # czyści - dupe na przykład
            else:
                print("Niepowodzenie w zapisie!")  # błąd, wyświetla komunikat błedu
                exit(-1)  # kod błędu - kończenie programu

        idsToSave.append(row)  # dopisue aktualne ID do listy ID przeznaczonych do zapisu

        rowInfo, keywords, i = getInfo(row, i, rowInfo, keywords)
# ------------------------------------------------------ KONIEC ------------------------------------------------------ #


# --------------------------------------- ZAMKNIECIE PROGRAMU (OSTATNI ZAPIS) ---------------------------------------- #
if saveToFile(rowInfo, keywords, dataSet, dataKeywords):
    saveIDs(idsToSave)
# ------------------------------------------- TO BY BYLO NA TYLE KURWIBĄKI ------------------------------------------- #
