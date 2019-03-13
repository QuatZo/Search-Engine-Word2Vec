# -------------------------------------------------------------------------------------------------------------------- #
#                                                                                                                      #
# TODO - Dodać aktorów                                                                                                 #
# TODO - Dokończyc warunki try-catch                                                                                   #
# TODO - Plik dataKeywords.csv nie ma zawierac jednego wyrazu kilka razy                                               #
# TODO - Komentarze                                                                                                    #
# TODO - Zmienne lepiej odzwierciedlajace przechowywane dane                                                           #
#                                                                                                                      #
# Jesli cos zrobicie to usuncie. Jak zrobicie wszystko z listy zostawcie naglowek i te wiadomosc                       #
# ------------------------------------------ ELO MORDY --------------------------------------------------------------- #

import numpy as np
import pandas as pd
from imdb import IMDb, IMDbError


def saveIDs(stepIDList):
    fileSaveIDs = open("dataSetIds.txt", "a+")
    for imdbID in stepIDList:
        if imdbID not in fileSaveIDs:
            fileSaveIDs.write(imdbID + "\n")
    fileSaveIDs.close()


def saveToFile(argRowInfo, argKeywords, argDataSet, argDataKeywords):
    try:
        dataSetTemp = pd.DataFrame(argRowInfo, columns=['title', 'year', 'directors', 'rating', 'genres', 'plotmarks'])
        dataKeywordsTemp = pd.DataFrame(argKeywords, columns=['keyword'])

        argDataSet = pd.concat([argDataSet, dataSetTemp])
        argDataKeywords = pd.concat([argDataKeywords, dataKeywordsTemp])

        argDataSet = argDataSet.reset_index(drop=True)
        argDataKeywords = argDataKeywords.reset_index(drop=True)

        argDataSet.to_csv("dataSet.csv", sep=";")
        argDataKeywords.to_csv("dataKeywords.csv", sep=";")

        return True
    except ValueError:
        return False


ia = IMDb()

fileR = open('imdbIDs.txt', "r").read()  # read file
fileR = fileR.split()  # list from string

# listOfInfos = ['genres', 'countries', 'rating', 'title', 'year', 'directors', 'plot', 'producers']
# temporary deleted: 'reviews', 'synapsis', 'awards', 'keywords', 'writers', 'editors'
# unnecessary: 'cast', 'production companies',
# print(ia.get_movie_infoset())  # args

marks = {'.', ',', '<', '>', '/', '?', ';', ':', '\'', '\'s', '"', '[', '{', ']', '}', '!', '@', '#', '$', '%', '^',
         '&', '&', '*', '(', ')', '-', '_', '=', '+'}  # lista znakow specjalnych do usunięcia

lastId = str(0).zfill(7) + '\n'  # ustawione jako 0000001
with open('dataSetIds.txt') as Ids:
    try:
        lastId = list(Ids)[-1]  # pobranie ostatniego id żeby nie powtarzać pobierania danych do pliku od początku
        fileR = fileR[fileR.index(lastId[:-1]) + 1:]
    except IndexError:
        print("Plik ID jest pusty, zaczynamy od 0000001!")

stopTerm = 0
i = 0  # reshape <-> rows
rowInfo = list()
keywords = list()
idsToSave = list()

dataSet = pd.read_csv("dataSet.csv", sep=";", index_col=0)
dataKeywords = pd.read_csv("dataKeywords.csv", sep=";", index_col=0)

for row in fileR:  # kazdy imdbID z bazy
    if row > lastId:
        try:
            stopTerm += 1
            if stopTerm == 6:
                print("Zapis do plikow")
                stopTerm = 0
                if saveToFile(rowInfo, keywords, dataSet, dataKeywords):
                    saveIDs(idsToSave)
                    idsToSave.clear()  # list
                else:
                    print("Niepowodzenie w zapisie!")
                    exit(-1)
            idsToSave.append(row)

            movie = ia.get_movie(row)  # pobieramy info nt filmow o danym ID. Jak wywali Error -> wyświetla błąd ID

            listOfInfos = list()  # Lista informacji, które będziemy przechowywać inforamcje na temat jednego filmu
            listOfInfos.append(movie['title'])  # na początek tytuł
            listOfInfos.append(movie['year'])  # potem rok produkcji

            listOfDirectors = list()
            listOfDirectorsSpace = list()
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
            for word in listOfInfos[4].split():  # pętla która zapisuje wszystkie keywords
                if word not in pd.read_csv("dataKeywords.csv", sep=";", index_col=0).values:
                    keywords.append(word)
            for word in listOfInfos[5].split():  # taka sama pętla, ale inne info
                if word not in pd.read_csv("dataKeywords.csv", sep=";", index_col=0).values:
                    keywords.append(word)
            # keywords -- END

        except IMDbError as e:
            print(row, e)
        except KeyError as e:
            print("Brak pelnych danych filmu o ID: ", row, "; brakujace dane: ", e)

if saveToFile(rowInfo, keywords, dataSet, dataKeywords):
    saveIDs(idsToSave)
