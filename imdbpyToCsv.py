# -------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                      #
# TODO - Dodać aktorów                                                                                                 #
# TODO - Sprawdzic warunki try-except                                                                                  #
# TODO - Plik dataKeywords.csv bez powtorzen (teoretycznie warunek jest dobry, ale czasem wartosci sie powtarzaja)     #
# TODO - Komentarze                                                                                                    #
# TODO - Zmienne lepiej odzwierciedlajace przechowywane dane                                                           #
# TODO - Usuniecie cudzyslowia z opisow (mozliwe, ze brakuje \ w tablicy znakow specjalnych)                           #
#                                                                                                                      #
# Jesli cos zrobicie to usuncie. Jak zrobicie wszystko z listy zostawcie naglowek i te wiadomosc                       #
# ------------------------------------------ ELO MORDY --------------------------------------------------------------- #

import numpy as np
import pandas as pd
from imdb import IMDb, IMDbError


def saveIDs(stepIDList):  # funkcja do zapiswania już wykorzystanych ID do pliku
    fileSaveIDs = open("dataSetIds.txt", "a+")  # otwieranie pliku dataSetIds
    for imdbID in stepIDList:
        if imdbID not in fileSaveIDs:
            fileSaveIDs.write(imdbID + "\n")  # wypisywanie każdego elementu w nowej lini
    fileSaveIDs.close()  # zamykanie pliku


def saveToFile(argRowInfo, argKeywords, argDataSet, argDataKeywords):  # zapisywanie pobranych danych do pliku
    try:
        #  tworzenie dataFrame - taka tabelka która ma jasno określone nagłówki i indeksy
        dataSetTemp = pd.DataFrame(argRowInfo, columns=['title', 'year', 'directors', 'rating', 'genres', 'plotmarks'])
        dataKeywordsTemp = pd.DataFrame(argKeywords, columns=['keyword'])

        argDataSet = pd.concat([argDataSet, dataSetTemp])  # konkatenacja - łączenie tego co mamy w pliku i co pobrane
        argDataKeywords = pd.concat([argDataKeywords, dataKeywordsTemp])  # to samo co wyżej

        argDataSet = argDataSet.reset_index(drop=True)  # reset indeksu
        argDataKeywords = argDataKeywords.reset_index(drop=True)  # to samo co wyżej

        argDataSet.to_csv("dataSet.csv", sep=";")  # zmiana na plik .csv
        argDataKeywords.to_csv("dataKeywords.csv", sep=";")  # zmiana na plik .csv

        return True  # zwracamy prawde
    except ValueError as err:  # error
        print("Blad: ", err)
        return False


ia = IMDb()

try:  # spróbuj otworzyć plik
    fileR = open('imdbIDs.txt', "r").read()  # read file
    fileR = fileR.split()  # list from string
except FileNotFoundError as e:
    print("Blad: ", e)
    exit(-1)

# listOfInfos = ['genres', 'countries', 'rating', 'title', 'year', 'directors', 'plot', 'producers']
# temporary deleted: 'reviews', 'synapsis', 'awards', 'keywords', 'writers', 'editors'
# unnecessary: 'cast', 'production companies',
# print(ia.get_movie_infoset())  # args

marks = {'.', ',', '<', '>', '/', '?', ';', ':', '\'', '\'s', '"', '[', '{', ']', '}', '!', '@', '#', '$', '%', '^',
         '&', '&', '*', '(', ')', '-', '_', '=', '+'}  # lista znakow specjalnych do usunięcia

lastId = str(0).zfill(7) + '\n'  # ustawione jako 0000001
try:
    with open('dataSetIds.txt') as Ids:
        try:
            lastId = list(Ids)[-1]  # pobranie ostatniego id żeby nie powtarzać pobierania danych do pliku od początku
            fileR = fileR[fileR.index(lastId[:-1]) + 1:]
        except IndexError:
            print("Plik ID jest pusty, zaczynamy od 0000001!")
except FileNotFoundError as e:
    open("dataSetIds.txt", "w+").write("")

stopTerm = 0
i = 0  # reshape <-> rows
rowInfo = list()  # tworzymy listy
keywords = list()
idsToSave = list()

try:
    dataSet = pd.read_csv("dataSet.csv", sep=";", index_col=0)  # czytaj plik .csv
except FileNotFoundError as e:
    open("dataSet.csv", "w+").write(";title;year;directors;rating;genres;plotmarks")  # jeśli go nie ma, to utwórz
    dataSet = pd.read_csv("dataSet.csv", sep=";", index_col=0)  # a potem czytaj

try:
    dataKeywords = pd.read_csv("dataKeywords.csv", sep=";", index_col=0)  # czytaj plik .csv
except FileNotFoundError as e:
    open("dataKeywords.csv", "w+").write(";keyword")  # jeśli go nie ma, to uwtórz
    dataKeywords = pd.read_csv("dataKeywords.csv", sep=";", index_col=0)  # a potem czytaj


for row in fileR:  # kazdy imdbID z bazy
    if row > lastId:
        try:
            stopTerm += 1  # warunek stopu zapisu - kiedy ma zapisać
            if stopTerm == 6:
                print("Zapis do plikow")  # wyświetla że zapisuje
                stopTerm = 0  # zerowanie warunku stopu
                if saveToFile(rowInfo, keywords, dataSet, dataKeywords):  # wywołuje funkcje zapisu do pliku
                    saveIDs(idsToSave)  # zapisuje
                    idsToSave.clear()  # czyści - dupe na przykład
                else:
                    print("Niepowodzenie w zapisie!")  # błąd, wyświetla komunikat błedu
                    exit(-1)  # kod błędu - kończenie programu
            idsToSave.append(row)  # dopisue aktualne ID do listy ID przeznaczonych do zapisu

            movie = ia.get_movie(row)  # pobieramy info nt filmow o danym ID. Jak wywali Error -> wyświetla błąd ID

            listOfInfos = list()  # Lista informacji, które będziemy przechowywać inforamcje na temat jednego filmu
            listOfInfos.append(movie['title'])  # na początek tytułu
            listOfInfos.append(movie['year'])  # potem rok produkcji

            listOfDirectors = list()  # tworzenie listy
            listOfDirectorsSpace = list()  # tworzenie listy
            for director in movie['directors']:  # lista reżyserów, może być więcej niż jeden więc jest pętla
                tempDirectors = director['name'].replace(' ', '_')  # usunięcie spacji i zamiana na _
                listOfDirectors.append(tempDirectors)
            listOfInfos.append(" ".join(listOfDirectors))

            listOfInfos.append(movie['rating'])  # ocena filmu
            listOfInfos.append(" ".join(movie['genres']))  # kategoria

            # usuwamy .::, autora tekstu i znaki specjalne -- START
            plots = list()
            plotsmarks = list()
            for plot in movie['plot']:
                index = plot.find(".::")  # szukamy ".::" i od tego miejsca ucinamy recenzje
                plot = plot[:index]
                plots.append(plot)
                for mark in marks:  # wyszukaj znaku interpunkcyjnego (lista marks) i go usun/zamien
                    plot = plot.replace(mark, '')
                plotsmarks.append(plot)
            listOfInfos.append(" ".join(plotsmarks))
            # usuwamy .::, autora tekstu i znaki specjalne  -- KONIEC

            if i == 0:
                keywords = list()  # tworzymy liste słów kluczowych do danego ID
                rowInfo = np.array(listOfInfos)  # tablica numpy (ma więcej metod)
                rowInfoLen = len(rowInfo)  # ilosc info jaką pobraliśmy z filmu
                i += 1  # powiększamy "i" czyli liczbę wierszy
            else:
                i += 1  # powiększamy "i" czyli liczbę wierszy
                rowInfo = np.append(rowInfo, listOfInfos).reshape((i, rowInfoLen))  # zmien tablice numpy na numpy 2D

            # keywords -- START
            keywordsTemp = pd.read_csv("dataKeywords.csv", sep=";", index_col=0).values.transpose()
            for word in listOfInfos[4].split():  # pętla która zapisuje wszystkie keywords
                if word.casefold() not in keywordsTemp and word not in keywords:
                    keywords.append(word.casefold())
            for word in listOfInfos[5].split():  # taka sama pętla, ale inne info
                if word.casefold() not in keywordsTemp and word not in keywords:
                    keywords.append(word.casefold())
            # keywords -- END

        except IMDbError as e:
            print(row, e)
        except KeyError as e:
            print("Brak pelnych danych filmu o ID: ", row, "; brakujace dane: ", e)

if saveToFile(rowInfo, keywords, dataSet, dataKeywords):
    saveIDs(idsToSave)
